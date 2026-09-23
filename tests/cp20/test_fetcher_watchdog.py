"""Fetcher hardening against a local server: watchdog deadline independent of chunk size,
per-attempt buffers (a late trickle never reaches the retry), fresh-connection retry,
keep-alive reuse, bounded jittered backoff, stop during backoff. No external network."""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import threading
import time

import pytest

from cp20 import net
from cp20.budget import Budget

SIZE = 4000


class Handler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'
    plan = []            # per request: 'trickle' or 'fast'
    connections = set()
    served = []

    def log_message(self, *a):
        pass

    def do_GET(self):
        Handler.connections.add(self.client_address)
        mode = Handler.plan.pop(0) if Handler.plan else 'fast'
        Handler.served.append(mode)
        a, b = map(int, self.headers['Range'].split('=')[1].split('-'))
        n = b - a + 1
        self.send_response(206)
        self.send_header('Content-Length', str(n))
        self.send_header('Content-Range', f'bytes {a}-{b}/100000')
        self.end_headers()
        if mode == 'trickle':
            try:
                for _ in range(n):
                    self.wfile.write(b'A')
                    self.wfile.flush()
                    time.sleep(0.05)
            except (BrokenPipeError, ConnectionResetError):
                pass
        else:
            self.wfile.write(b'B' * n)


@pytest.fixture
def server():
    srv = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    Handler.plan, Handler.connections, Handler.served = [], set(), []
    yield f'127.0.0.1:{srv.server_address[1]}'
    srv.shutdown()


def fetcher(tmp_path, host, **kw):
    b = Budget(tmp_path / 'ledger.json')
    b.initialise({})
    return net.Fetcher(b, tmp_path / 'requests.jsonl', 10 ** 9, allowed_hosts={host: 'aws'},
                       deadline=(1.0, 0.0), sleep=kw.pop('sleep', lambda s: False), **kw), b


def test_trickle_is_cut_at_the_deadline_and_never_feeds_the_retry(tmp_path, server):
    Handler.plan = ['trickle', 'fast']
    f, b = fetcher(tmp_path, server)
    began = time.time()
    status, _, body = f.get(f'http://{server}/x', 'probe', byte_range=(0, SIZE - 1))
    assert time.time() - began < 4.0                   # 1 s deadline + backoff, not the 200 s trickle
    assert status == 206 and body == b'B' * SIZE        # only the retry's own buffer
    assert f.stats['deadline_expiries'] == 1 and f.stats['network_retries'] == 1
    assert Handler.served == ['trickle', 'fast'] and len(Handler.connections) == 2   # fresh connection
    assert b.read()['counts']['transfer_bytes'] >= 2 * (SIZE + net.ALLOWANCE)       # both tries charged


def test_healthy_connections_are_kept_alive(tmp_path, server):
    f, _ = fetcher(tmp_path, server)
    for _ in range(3):
        assert f.get(f'http://{server}/x', 'probe', byte_range=(0, 99))[2] == b'B' * 100
    assert len(Handler.connections) == 1


def test_stop_during_backoff_ends_retrying(tmp_path, server):
    Handler.plan = ['trickle'] * 5
    stop = threading.Event()
    f, _ = fetcher(tmp_path, server, stop_event=stop, sleep=lambda s: (stop.set(), True)[1])
    with pytest.raises(net.NetworkError):
        f.get(f'http://{server}/x', 'probe', byte_range=(0, SIZE - 1))


def test_backoff_is_exponential_jittered_and_capped_at_ten_minutes():
    import random
    rng = random.Random(1)
    delays = [net.backoff_delay(k, rng) for k in range(1, 20)]
    assert all(0 < d <= 600 for d in delays) and max(delays) == 600
    assert 2.5 <= net.backoff_delay(1, random.Random(0)) <= 7.5


def test_unauthorised_host_and_unbounded_request_refused(tmp_path, server):
    f, _ = fetcher(tmp_path, server)
    with pytest.raises(ValueError):
        f.get('https://example.com/x', 'probe', byte_range=(0, 1))
    with pytest.raises(ValueError):
        f.get(f'http://{server}/x', 'probe')
