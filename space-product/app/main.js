// The final-product Space (A9). Everything shown comes from four sources: the dated bundle (verified file by file
// against its manifest before use), the build record (app/space-build.json), the live claims (app/claims.json,
// rendered by cp18.live_claims at build time) and, in a live build, the live record (app/live-record.json: the
// store's issuance record and the running intervals, both computed at build time and listed with their hash).
// Status, badges, fixed wording and limitations are the claims' text; numbers are the records'. The page requests
// nothing from another origin.
(function () {
  'use strict';
  const Charts = window.Charts;
  const S = {usedClaims: new Set(), files: {}, verified: [], redraw: {}, results: {}, pw: null, views: {}};
  window.__space = S;

  // ------------------------------------------------------------------ small helpers
  function h(tag, attrs, ...kids) {
    const e = document.createElement(tag);
    if (attrs) {
      for (const [k, v] of Object.entries(attrs)) {
        if (v === undefined || v === null || v === false) continue;
        if (k === 'class') e.className = v;
        else if (k === 'text') e.textContent = v;
        else if (k.startsWith('on') && typeof v === 'function') e.addEventListener(k.slice(2), v);
        else e.setAttribute(k, v === true ? '' : String(v));
      }
    }
    for (const kid of kids.flat(Infinity)) {
      if (kid === null || kid === undefined || kid === false) continue;
      e.appendChild(typeof kid === 'string' || typeof kid === 'number' ? document.createTextNode(String(kid)) : kid);
    }
    return e;
  }
  const $ = (sel) => document.querySelector(sel);
  function L(key) {
    const v = S.claims.values[key];
    if (v === undefined) throw new Error('the live claims hold no ' + key);
    S.usedClaims.add(key);
    return v;
  }
  function shared(key) {
    const v = S.claims.shared[key];
    if (v === undefined) throw new Error('the shared claims hold no ' + key);
    S.usedClaims.add(key);
    return v;
  }
  function fill(template, values) { return template.replace(/\{(\w+)\}/g, (m, k) => (k in values ? values[k] : m)); }
  function minus(s) { return s.replace(/^-/, '−'); }
  function eur(v, d) {
    if (v === null || v === undefined || !isFinite(v)) return '—';
    const s = Number(v).toFixed(d === undefined ? 1 : d);
    return Number(s) === 0 ? s.replace(/^-/, '') : minus(s);
  }
  function signed(v, d) { const s = eur(v, d); return v > 0 && Number(Math.abs(v).toFixed(d === undefined ? 1 : d)) !== 0 ? '+' + s : s; }
  function pct(share, d) { return (share === null || share === undefined || !isFinite(share)) ? '—' : (share * 100).toFixed(d === undefined ? 1 : d) + '%'; }
  function sci(v) {
    if (v === null || v === undefined) return '—';
    if (v === 0) return '0';
    return Math.abs(v) < 1e-3 ? minus(v.toExponential(2)).replace('e', '×10^') : eur(v, 4);
  }
  function exact(v) {
    if (v === null || v === undefined) return 'none';
    if (typeof v === 'number') return Number.isInteger(v) ? v.toLocaleString('en-US') : minus(String(Number(v.toPrecision(12))));
    return String(v);
  }
  function num(v, text, attrs) { return h('span', Object.assign({class: 'num', 'data-v': v === null || v === undefined ? '' : String(v)}, attrs || {}), text); }
  function mb(bytes) { return (bytes / 1e6).toFixed(1) + ' MB'; }
  function bytesText(bytes) { return `about ${mb(bytes)} (${bytes.toLocaleString('en-US')} bytes)`; }
  function short(sha) { return sha ? sha.slice(0, 12) : '—'; }
  function addDays(day, n) {
    const [y, m, d] = day.split('-').map(Number);
    const t = new Date(Date.UTC(y, m - 1, d + n));
    return t.toISOString().slice(0, 10);
  }
  // Europe/Berlin by the EU rule (summer time from the last Sunday of March to the last Sunday of October, 01:00 UTC)
  function lastSunday(year, month) { const d = new Date(Date.UTC(year, month + 1, 0)); d.setUTCDate(d.getUTCDate() - d.getUTCDay()); return d.getTime(); }
  const DST = {};
  function berlinOffset(ms) {
    const y = new Date(ms).getUTCFullYear();
    const r = DST[y] || (DST[y] = [lastSunday(y, 2) + 3600e3, lastSunday(y, 9) + 3600e3]);
    return ms >= r[0] && ms < r[1] ? 2 : 1;
  }
  function berlin(iso) {
    const ms = Date.parse(iso);
    const off = berlinOffset(ms);
    const t = new Date(ms + off * 3600e3).toISOString();
    return {day: t.slice(0, 10), hour: Number(t.slice(11, 13)), hm: t.slice(11, 16), zone: off === 2 ? 'CEST' : 'CET',
            month: Number(t.slice(5, 7))};
  }
  function when(iso) {
    if (!iso) return 'not recorded';
    const b = berlin(iso);
    return `${b.day} ${b.hm} Europe/Berlin (${b.zone}; ${iso.slice(0, 16).replace('T', ' ')} UTC)`;
  }
  function hourLabels(keys) {
    const parts = keys.map(berlin);
    const seen = {};
    parts.forEach(p => { seen[p.hour] = (seen[p.hour] || 0) + 1; });
    const dup = Object.values(seen).some(c => c > 1) || keys.length !== 24;
    return parts.map(p => String(p.hour).padStart(2, '0') + ':00' + (dup ? ' ' + p.zone : ''));
  }
  async function sha256hex(buffer) {
    const digest = await crypto.subtle.digest('SHA-256', buffer);
    return Array.from(new Uint8Array(digest)).map(b => b.toString(16).padStart(2, '0')).join('');
  }
  const REPORT_URL = (document.querySelector('[data-report]') || document.querySelector('[data-report-foot]')).getAttribute('href');
  function reportURL() { return REPORT_URL; }
  function routeBack() {
    return h('p', {}, h('a', {class: 'ext', href: reportURL(), rel: 'external noopener'}, 'Back to the static report ',
                         h('span', {class: 'ext-mark'}, '(external site)')));
  }
  // states: ready, loading, pending, partial, stale, failed, notissued, unavailable, verification, cancelled
  function state(kind, title, detail, opts) {
    opts = opts || {};
    const box = h('div', {class: `state state-${kind}`, role: opts.alert ? 'alert' : 'status', 'data-state': kind},
                  h('p', {class: 'state-title'}, title));
    for (const d of [].concat(detail || [])) box.appendChild(typeof d === 'string' ? h('p', {}, d) : d);
    if (opts.retry) box.appendChild(h('p', {}, h('button', {type: 'button', class: 'secondary-btn', 'data-retry': '1', onclick: opts.retry}, opts.retryLabel || 'Retry')));
    if (opts.route !== false && ['failed', 'verification', 'unavailable', 'cancelled', 'stale'].includes(kind)) box.appendChild(routeBack());
    return box;
  }
  function badge(text, strong) { return h('span', {class: 'badge' + (strong ? ' strong' : ''), 'data-badge': '1'}, text); }
  function details(summary, ...body) { return h('details', {}, h('summary', {}, summary), ...body); }
  function table(caption, head, rows, attrs) {
    const t = h('table', attrs || {}, h('caption', {}, caption),
                h('thead', {}, h('tr', {}, head.map(c => h('th', {scope: 'col', class: c.n ? 'n' : null}, c.t || c)))),
                rows.length === 1 && rows[0].tagName === 'TBODY' ? rows[0] : h('tbody', {}, rows));
    return h('div', {class: 'table-wrap', role: 'region', 'aria-label': caption, tabindex: '0'}, t);
  }
  function td(content, n, attrs) { return h('td', Object.assign({class: n ? 'n' : null}, attrs || {}), content); }
  // a chart slot that redraws itself at its container's width
  function chart(viewKey, draw) {
    const slot = h('div', {class: 'chart-slot'});
    const run = () => { slot.textContent = ''; draw(slot); slot.dataset.width = String(slot.clientWidth); };
    (S.redraw[viewKey] = S.redraw[viewKey] || []).push({slot, run});
    requestAnimationFrame(run);
    return slot;
  }

  class VerifyError extends Error {
    constructor(file, reason) { super(`${file}: ${reason}`); this.file = file; this.reason = reason; this.kind = 'verification'; }
  }
  class FetchError extends Error {
    constructor(url, status) { super(`${url}: ${status}`); this.url = url; this.status = status; this.kind = 'unavailable'; }
  }
  async function getBytes(url) {
    let response;
    try { response = await fetch(url); } catch (e) { throw new FetchError(url, 'the request failed (' + e.message + ')'); }
    if (!response.ok) throw new FetchError(url, 'HTTP ' + response.status);
    return response.arrayBuffer();
  }
  function decode(bytes) { return JSON.parse(new TextDecoder().decode(bytes)); }

  // a bundle file, verified against the manifest (SHA-256 and bytes) before anything reads it
  async function payload(name) {
    if (S.files[name]) return S.files[name];
    const entry = (S.manifest.files || []).find(f => f.path === name);
    if (!entry) throw new VerifyError(name, 'the manifest does not list this file');
    const buffer = await getBytes('/payloads/' + name);
    if (buffer.byteLength !== entry.bytes) throw new VerifyError(name, `${buffer.byteLength} bytes were served; the manifest lists ${entry.bytes}`);
    const got = await sha256hex(buffer);
    if (got !== entry.sha256) throw new VerifyError(name, `its SHA-256 is ${got}; the manifest lists ${entry.sha256}`);
    const item = {name, bytes: new Uint8Array(buffer), sha256: got};
    S.files[name] = item;
    S.verified.push({name, sha256: got, bytes: buffer.byteLength});
    return item;
  }
  async function payloads(names) { const out = {}; for (const n of names) out[n] = (await payload(n)).bytes; return out; }

  // ------------------------------------------------------------------ the product worker (one, reused)
  function productWorker() {
    if (S.pw) return S.pw;
    const w = new Worker('/app/product-worker.js');
    const pw = {worker: w, seq: 0, waiting: new Map(), booted: false};
    w.onmessage = (event) => {
      const m = event.data;
      const job = pw.waiting.get(m.id);
      if (!job) return;
      if (m.type === 'stage') { if (m.stage === 'package unpacked') pw.booted = true; job.onStage(m.stage, m.ms); return; }
      pw.waiting.delete(m.id);
      if (m.type === 'result') job.resolve(m.result); else job.reject(new Error(m.message));
    };
    w.onerror = (event) => {
      for (const job of pw.waiting.values()) job.reject(new Error('the product worker stopped: ' + (event.message || 'an error')));
      pw.waiting.clear();
      w.terminate();
      if (S.pw === pw) S.pw = null;
    };
    S.pw = pw;
    return pw;
  }
  function runGlue(op, files, onStage, retrained) {
    const pw = productWorker();
    const id = ++pw.seq;
    const expected = {zip_sha256: S.build.zip.sha256, glue_sha256: S.build.glue.sha256, packages: S.build.pyodide.packages};
    return new Promise((resolve, reject) => {
      pw.waiting.set(id, {resolve, reject: (e) => { if (!pw.booted) { pw.worker.terminate(); if (S.pw === pw) S.pw = null; } reject(e); },
                          onStage: onStage || (() => {})});
      pw.worker.postMessage({id, op, files, expected, retrained});
    });
  }
  function runtimeLoaded() { return !!(S.pw && S.pw.booted); }
  function downloadNote(extraBytes, extraWhat) {
    const a = S.build.size.actions.product_runtime;
    if (runtimeLoaded()) return `Downloads ${bytesText(extraBytes)} more (${extraWhat}); the runtime is already loaded in this page.`;
    return `Downloads ${bytesText(a.bytes + extraBytes)} the first time: the pinned runtime ${mb(a.parts.runtime)}, its packages ` +
           `${mb(a.parts.packages)}, the frozen package and the shared glue ${mb(a.parts.code)}, and ${extraWhat} ${mb(extraBytes)}. ` +
           'Everything runs in your browser.';
  }
  // runs one in-browser computation behind a view's primary action, with honest stages, failure and retry
  function glueAction(box, op, fileNames, render, opts) {
    const status = h('div', {class: 'op-status', 'aria-live': 'polite'});
    const button = h('button', {type: 'button', class: 'primary', 'data-action': op}, opts.label);
    const meta = h('p', {class: 'action-meta', 'data-size': op}, '');
    const out = h('div', {class: 'op-result'});
    const refreshMeta = () => { meta.textContent = downloadNote(opts.extraBytes(), opts.extraWhat); };
    refreshMeta();
    S.refreshMeta = (S.refreshMeta || []).concat([refreshMeta]);
    const go = async () => {
      button.hidden = true;
      out.textContent = '';
      const stages = [];
      const started = performance.now();
      const show = () => {
        status.textContent = '';
        status.appendChild(state('loading', 'Running in your browser', [
          h('p', {}, stages.length ? 'Stages reached: ' + stages.join(' · ') : 'Starting: checking the files against the manifest.')]));
      };
      show();
      try {
        const files = await payloads(fileNames());
        const result = await runGlue(op, files, (stage, ms) => { stages.push(stage); show(); });
        S.results[op] = result;
        status.textContent = '';
        status.appendChild(state('ready', 'Done in your browser', `Computed in ${((performance.now() - started) / 1000).toFixed(1)} s on this device; stages: ${stages.join(' · ')}.`));
        render(out, result);
        (S.refreshMeta || []).forEach(f => f());
      } catch (error) {
        status.textContent = '';
        const verification = error.kind === 'verification';
        status.appendChild(state(verification ? 'verification' : 'failed',
          verification ? `Verification failed: ${error.file}` : 'Failed in your browser',
          [verification ? `${error.reason}. Nothing from this file is shown.` : (error.message || String(error)).split('\n').slice(-3).join(' ')],
          {alert: true, retry: () => { button.hidden = false; status.textContent = ''; go(); }}));
        S.results[op + '_error'] = String(error.message || error);
      }
      button.hidden = false;
      button.textContent = opts.againLabel || opts.label;
    };
    button.addEventListener('click', go);
    box.appendChild(h('div', {class: 'action'}, meta, button));
    box.appendChild(status);
    box.appendChild(out);
  }

  // ------------------------------------------------------------------ records
  function windowsOf(policy) { return S.evaluation.windows.filter(w => w.policy === policy); }
  function isRehearsal(w) { return w.evidence_class.startsWith('development rehearsal'); }
  function recomputedWindow(w) { return w.window === '4.7T' || w.window === 'prospective' || isRehearsal(w); }
  function badgeFor(w) {
    if (isRehearsal(w)) return L('live_rehearsal_badge');
    if (w.window === '4.7T') return L('live_fresh_test_badge');
    if (w.window === 'prospective') return L('live_prospective_label');
    return L('live_development_badge');
  }
  const B0_LABEL = 'similar-day naive · reference, not a target';
  function policyName(p) { return p === 'product' ? L('live_product_name') : `B0 · ${B0_LABEL}`; }
  function dayEntry(day) {
    for (const w of windowsOf('product').filter(recomputedWindow)) {
      const e = (w.record.days || []).find(d => d.day === day);
      if (e) return {entry: e, window: w};
    }
    return null;
  }
  function forecastOf(day) { return S.forecasts.days.find(d => d.delivery_day === day) || null; }
  function notIssuedItems() {
    // the manifest's evidence label names each day not issued with its cause, after "; not issued: "
    const label = S.manifest.product.evidence_label || '';
    const i = label.indexOf('; not issued: ');
    const out = new Map();
    if (i < 0) return out;
    const rest = label.slice(i + '; not issued: '.length);
    const re = /(\d{4}-\d{2}-\d{2}), (.*?)(?=; \d{4}-\d{2}-\d{2}, |$)/g;
    let m;
    while ((m = re.exec(rest))) out.set(m[1], m[2]);
    return out;
  }
  // the cause exactly as the bundle states it, or no cause at all: never an invented one
  function notIssuedText(day) {
    const o = outsideOf(day);
    if (o) return `Outside the live record, ${o.first_day} to ${o.last_day}: ${L('live_outside_wording')}.`;
    const t = S.notIssued.get(day);
    return t ? `${t}.` : 'The served record states no cause for this day.';
  }
  function liveNotIssued() {
    const out = new Map();
    for (const d of S.live.record.not_issued) out.set(d.day, d.cause_text);
    for (const d of S.live.record.failed) out.set(d.day, d.cause_text);
    for (const d of S.live.record.open || []) out.set(d.day, `${d.cause_text} (${L('live_open_day_wording')})`);
    return out;
  }
  function cutoffTime() { const m = /(\d{2}:\d{2})/.exec(L('live_cutoff')); return m ? m[1] : ''; }
  function cap(t) { return t ? t.charAt(0).toUpperCase() + t.slice(1) : t; }
  // the last development delivery day, as the claims state the development displays' scope
  function devBoundary() { const m = /(\d{4}-\d{2}-\d{2})/.exec(L('live_development_scope')); return m ? m[1] : null; }
  // the frozen records name the product's policy by its record name; the page names it as the claims do (O30)
  function policyLabel(p) { return p && p === S.manifest.product.designated_policy ? L('live_product_record_name') : (p || 'none'); }
  // O18's N7: each issued day's actual run, from the live record (never the artifact's nominal time)
  function issuanceOf(day) {
    if (!S.live) return null;
    const r = S.live.record;
    return r.issued.find(d => d.day === day) || r.failed.find(d => d.day === day) || null;
  }
  function outsideOf(day) { return S.live ? S.live.record.outside.find(o => o.first_day <= day && day <= o.last_day) || null : null; }
  function clock(iso) { if (!iso) return 'not recorded'; const b = berlin(iso); return `${b.hm} ${b.zone}`; }
  function hostText(it) {
    const base = it.host_kind === 'runner' ? L('live_host_runner') : L('live_host_local');
    const r = it.runner;
    if (!r) return base;
    const parts = [r.image_os, r.image_version ? 'image ' + r.image_version : null, r.github_run_id ? 'run ' + r.github_run_id : null].filter(Boolean);
    return parts.length ? `${base}, ${parts.join(', ')}` : base;
  }
  function runText(it) {
    if (!it) return L('live_run_time_absent');
    const sameDay = it.issuance_started_utc && berlin(it.issuance_started_utc).day === berlin(it.issuance_finished_utc || it.issuance_started_utc).day;
    return `the run started ${when(it.run_started_utc)}; the issuance ran ${sameDay ? `${berlin(it.issuance_started_utc).day} ${clock(it.issuance_started_utc)}` : when(it.issuance_started_utc)} to ` +
           `${clock(it.issuance_finished_utc)}, on ${hostText(it)} (run ${it.run_id})`;
  }
  // the two times of an issued day: the cutoff-based issue time (the artifact's) and the actual run (the record's)
  function issueTimes(day, issueIso, attrs) {
    const it = issuanceOf(day);
    return h('div', Object.assign({class: 'issue-times', 'data-issue-times': day, 'data-cutoff-time': issueIso || '',
                                   'data-run-started': it ? it.run_started_utc : '', 'data-issuance-started': it ? it.issuance_started_utc : '',
                                   'data-issuance-finished': it ? it.issuance_finished_utc : '', 'data-host': it ? it.host_kind : ''}, attrs || {}),
      h('p', {class: 'subtitle', 'data-time-kind': 'cutoff'}, h('strong', {}, cap(L('live_issue_time_label')) + ': '), when(issueIso), ` (${L('live_issue_time_note')})`),
      h('p', {class: 'subtitle', 'data-time-kind': 'run'}, h('strong', {}, cap(L('live_run_time_label')) + ': '), runText(it)));
  }

  // ------------------------------------------------------------------ start-up
  async function start() {
    try {
      if (!(window.crypto && crypto.subtle)) {
        throw new VerifyError('every file', 'this browser context offers no SHA-256 (crypto.subtle), so nothing can be verified');
      }
      const claimsBytes = await getBytes('/app/claims.json');
      S.build = decode(await getBytes('/app/space-build.json'));
      const claimsEntry = S.build.files.find(f => f.path === 'app/claims.json');
      if (!claimsEntry || claimsEntry.sha256 !== await sha256hex(claimsBytes)) throw new VerifyError('app/claims.json', 'it is not the file the build record lists');
      S.claims = decode(claimsBytes);
      if (S.build.live) {
        const liveBytes = await getBytes('/' + S.build.live.path);
        const liveEntry = S.build.files.find(f => f.path === S.build.live.path);
        const got = await sha256hex(liveBytes);
        if (!liveEntry || liveEntry.sha256 !== got || S.build.live.sha256 !== got) throw new VerifyError(S.build.live.path, 'it is not the file the build record lists');
        S.live = decode(liveBytes);
      }
      const manifestBytes = await getBytes('/payloads/manifest.json');
      S.manifestSha = await sha256hex(manifestBytes);
      if (S.manifestSha !== S.build.bundle.manifest_sha256) {
        throw new VerifyError('manifest.json', `its SHA-256 is ${S.manifestSha}; the build record lists ${S.build.bundle.manifest_sha256}`);
      }
      S.manifest = decode(manifestBytes);
      if (S.live && S.live.bundle_manifest_sha256 !== S.manifestSha) {
        throw new VerifyError(S.build.live.path, `it was built for manifest ${S.live.bundle_manifest_sha256}; the served manifest is ${S.manifestSha}`);
      }
      for (const name of S.build.bundle.start_records) await payload(name);
      S.forecasts = decode(S.files['issued-forecasts.json'].bytes);
      S.outcomesRecord = decode(S.files['outcomes.json'].bytes);
      S.evaluation = decode(S.files['evaluation.json'].bytes);
      S.artifact = decode(S.files['artifact.json'].bytes);
      if (S.artifact.artifact_sha256 !== S.manifest.artifact.artifact_sha256) {
        throw new VerifyError('artifact.json', `it is artifact ${S.artifact.artifact_sha256}; the manifest names ${S.manifest.artifact.artifact_sha256}`);
      }
      if (S.live) {
        const ours = S.live.record.issued.map(d => d.day + ' ' + d.artifact_sha256).sort().join(',');
        const theirs = S.forecasts.days.map(d => d.delivery_day + ' ' + d.issuing_artifact_sha256).sort().join(',');
        if (ours !== theirs) throw new VerifyError(S.build.live.path, 'it names other issued days or artifacts than the served bundle');
      }
      const p = S.manifest.policy;
      if (p.policy_identity_sha256 !== L('live_policy_identity_sha256') || p.package_sha256 !== L('live_package_sha256') ||
          p.issuing_host !== L('live_issuing_host')) {
        throw new VerifyError('manifest.json', 'the served policy identity, package or issuing host is not the frozen one the claims name');
      }
    } catch (error) {
      return startFailed(error);
    }
    S.outcomes = new Map(S.outcomesRecord.prices.map(r => [r.timestamp_utc, r]));
    S.issuedDays = S.forecasts.days.map(d => d.delivery_day).sort();
    S.today = S.manifest.freshness.as_of_day;
    S.tomorrow = addDays(S.today, 1);
    S.notIssued = S.live ? liveNotIssued() : notIssuedItems();
    S.yesterday = addDays(S.today, -1);
    $('#boot').remove();
    if (S.build.refused) {
      $('#banner').hidden = false;
      $('#banner').appendChild(state('failed', 'This build is refused',
        [`Its bundle did not pass the publication gate: ${S.build.gate.reason || 'the bundle does not verify'}. It exists for an acceptance check, never for publication.`], {alert: true}));
    }
    renderProduct();
    renderTabs();
    $('#foot').hidden = false;
    S.ready = true;
    window.addEventListener('resize', onResize);
  }

  function startFailed(error) {
    const boot = $('#boot');
    boot.textContent = '';
    boot.className = '';
    const verification = error.kind === 'verification';
    const box = verification
      ? state('verification', `Verification failed: ${error.file}`,
          [`${error.reason}.`, 'No view is shown, because no view shows data from an unverified file.'], {alert: true})
      : state('unavailable', `Unavailable: ${error.url || 'a record'} could not be loaded`,
          [`${error.status || error.message}. Nothing is shown in its place.`], {alert: true, retry: () => location.reload(), retryLabel: 'Reload the page'});
    box.setAttribute('data-failed-file', error.file || error.url || '');
    boot.appendChild(box);
    if (S.manifest && S.manifestSha) boot.appendChild(identityBlock(true));
    S.startError = {kind: error.kind || 'error', file: error.file || error.url || null, message: String(error.message || error)};
  }

  // ------------------------------------------------------------------ the product panel
  function identityBlock(partial) {
    const m = S.manifest;
    const rows = [
      ['Manifest SHA-256', S.manifestSha, 'manifest'],
      ['Policy identity', m.policy.policy_identity_sha256, 'policy'],
      ['Package SHA-256', m.policy.package_sha256, 'package'],
      ['Daily artifact SHA-256', m.artifact.artifact_sha256, 'artifact'],
    ];
    const dl = h('dl', {class: 'kv'});
    for (const [k, v, id] of rows) {
      dl.appendChild(h('dt', {}, k));
      dl.appendChild(h('dd', {}, h('span', {class: 'mono', 'data-identity': id, 'data-full': v}, short(v))));
    }
    dl.appendChild(h('dt', {}, 'Issuing host'));
    dl.appendChild(h('dd', {'data-identity': 'host'}, m.policy.issuing_host));
    const full = h('dl', {class: 'kv'});
    for (const [k, v, id] of rows) { full.appendChild(h('dt', {}, k)); full.appendChild(h('dd', {class: 'mono', 'data-identity-full': id}, v)); }
    return h('div', {class: 'identity', id: 'served-identity'},
      h('h2', {}, 'Served identity'),
      h('p', {class: 'subtitle'}, partial ? 'As the verified manifest states it.'
        : `Checked at start: the manifest against the build record, then ${S.build.bundle.start_records.join(', ')} against the manifest (SHA-256 and bytes).`),
      dl, details('The full SHA-256 values', full));
  }

  function renderProduct() {
    const m = S.manifest, a = m.artifact;
    $('#product').hidden = false;
    $('#product-title').textContent = L('live_product_name');
    document.title = `${L('live_product_name')} · ${L('live_product_status')}`;
    const status = $('#product-status');
    status.appendChild(badge(L('live_product_status'), true));
    status.appendChild(badge(L('live_prospective_label')));
    status.appendChild(document.createTextNode(' ' + L('live_released_product') + '.'));
    $('#product-rule').textContent = L('live_hero_rule');
    $('#product-rule').after(h('p', {class: 'secondary', 'data-evidence-label': '1'}, h('strong', {}, L('live_evidence_prefix')), m.product.evidence_label));
    const id = $('#identity');
    id.replaceWith(identityBlock(false));

    const times = $('#times');
    const f = m.freshness;
    let fresh;
    if (f.state === 'fresh') fresh = h('span', {'data-freshness': 'fresh'}, h('strong', {}, 'fresh'), ` · as of ${f.as_of_day}; the latest issued day is ${f.latest_issued_day}`);
    else if (f.state === 'stale') fresh = h('span', {'data-freshness': 'stale'}, h('strong', {}, `stale since ${when(m.times.issuance_utc)}`), `, the last issuance (for ${f.latest_issued_day}) · as of ${f.as_of_day}`);
    else fresh = h('span', {'data-freshness': f.state}, h('strong', {}, f.state), ` · as of ${f.as_of_day}; the latest issued day is ${f.latest_issued_day}`);
    const items = [...S.notIssued.entries()];
    const trained = S.live ? (S.live.record.issued.concat(S.live.record.failed)).find(d => d.cutoff_utc === m.times.last_training_utc) || null : null;
    const issuedRun = issuanceOf(a.delivery_day);
    const outside = S.live ? S.live.record.outside : [];
    const dl = h('dl', {class: 'kv'},
      h('dt', {}, 'Daily artifact'), h('dd', {}, h('span', {class: 'mono'}, short(a.artifact_sha256)), ` · delivery day ${a.delivery_day} · issued policy ${policyLabel(a.issued_policy)} · ${a.display}`),
      h('dt', {}, 'Last training'), h('dd', {'data-time': 'training', 'data-cutoff-time': m.times.last_training_utc, 'data-run-started': trained ? trained.issuance_started_utc : ''},
        `${cap(L('live_issue_time_label'))}: ${when(m.times.last_training_utc)}. ${cap(L('live_run_time_label'))}: `,
        trained ? `the fit ran inside the issuance of ${trained.day}, ${when(trained.issuance_started_utc)} to ${clock(trained.issuance_finished_utc)}, on ${hostText(trained)}` : L('live_run_time_absent')),
      h('dt', {}, 'Data refresh'), h('dd', {'data-time': 'refresh'}, when(m.times.data_refresh_utc)),
      h('dt', {}, 'Forecast issuance'), h('dd', {'data-time': 'issuance', 'data-cutoff-time': m.times.issuance_utc, 'data-run-started': issuedRun ? issuedRun.run_started_utc : ''},
        `${cap(L('live_issue_time_label'))}: ${when(m.times.issuance_utc)}. ${cap(L('live_run_time_label'))}: ${runText(issuedRun)}`),
      h('dt', {}, 'Information cutoff'), h('dd', {}, L('live_cutoff')),
      h('dt', {}, 'Delivery dates'), h('dd', {}, `today ${S.today} and tomorrow ${S.tomorrow}; the timezone is Europe/Berlin`),
      h('dt', {}, 'Freshness'), h('dd', {}, fresh),
      items.length ? [h('dt', {}, 'Days not issued'), h('dd', {}, h('ul', {class: 'plain'}, items.map(([d, t]) => h('li', {'data-not-issued': d}, `${d}: ${t}.`))))] : null,
      outside.length ? [h('dt', {}, 'Outside the live record'), h('dd', {}, h('ul', {class: 'plain'}, outside.map(o =>
        h('li', {'data-outside': o.first_day + '/' + o.last_day}, `${o.first_day} to ${o.last_day} (${o.days} days): ${L('live_outside_wording')}.`))))] : null);
    times.appendChild(h('h2', {}, 'Times and freshness'));
    times.appendChild(dl);
    if (f.state !== 'fresh') {
      times.appendChild(state(f.state === 'stale' ? 'stale' : 'failed', f.state === 'stale' ? `Stale: no issuance after ${f.latest_issued_day}` : `Failed: as of ${f.as_of_day}`,
        [f.state === 'stale' ? `The forecasts shown are the issuance for ${f.latest_issued_day}; they are not presented as newly issued.`
          : `A delivery day after the latest issued one was decided as not issued${items.length ? ' (the days not issued are listed above, with their causes)' : ''}. The forecasts shown are the issuance for ${f.latest_issued_day}.`]));
    }
    renderToday();
    renderTomorrow();
    renderEarlier();
    renderHowSure();
  }

  function forecastRows(day, keys, q, labels) {
    return keys.map((k, i) => {
      const o = S.outcomes.get(k);
      const price = o && o.price !== null && o.price !== undefined ? o.price : null;
      return h('tr', {'data-key': k},
        td(labels[i]), td(num(q[i][3], eur(q[i][3]), {'data-p50': '1'}), true),
        td(`${eur(q[i][2])} to ${eur(q[i][4])}`, true), td(`${eur(q[i][1])} to ${eur(q[i][5])}`, true), td(`${eur(q[i][0])} to ${eur(q[i][6])}`, true),
        td(price === null ? h('span', {'data-pending': '1'}, 'pending (not published; unscored)') : num(price, eur(price, 2), {'data-price': '1'}), true));
    });
  }
  const FORECAST_HEAD = ['Hour (Europe/Berlin)', {t: 'p50, EUR/MWh', n: 1}, {t: '50% band', n: 1}, {t: '80% band', n: 1}, {t: '95% band', n: 1}, {t: 'Published price, EUR/MWh', n: 1}];
  function forecastFigure(viewKey, f, title) {
    const labels = hourLabels(f.keys);
    const y = f.keys.map(k => { const o = S.outcomes.get(k); return o && o.price !== null && o.price !== undefined ? o.price : null; });
    const box = h('div', {});
    box.appendChild(chart(viewKey, slot => Charts.hourly(slot, {labels, q: f.quantiles, y, title,
      caption: 'Bands are the issued nominal 50%, 80% and 95% intervals; pending hours are shaded and unscored.'})));
    box.appendChild(details('Table: the issued forecast and the published prices',
      table(`${f.delivery_day}: issued quantiles and published prices, EUR/MWh`, FORECAST_HEAD, forecastRows(f.delivery_day, f.keys, f.quantiles, labels))));
    return box;
  }
  function partialNote(f) {
    if (!f.partial) return null;
    return state('partial', `Partial day: ${f.partial.issued_hours} of ${f.partial.canonical_hours} hours issued`,
      `The missing hours: ${f.partial.missing_hours.map(k => hourLabels([k])[0] + ' (' + k + ')').join(', ')}.`);
  }
  function publishedHours(f) { return f.keys.filter(k => { const o = S.outcomes.get(k); return o && o.price !== null && o.price !== undefined; }).length; }
  // the score of one issued day over its published hours, from the committed evaluation record; never 0% or 100% unscored
  function scoreBlock(day) {
    const found = dayEntry(day);
    const scoreBox = h('div', {class: 'score-block', 'data-score': day});
    if (!found || !found.entry.scored || !found.entry.scored_hours) {
      scoreBox.appendChild(state('pending', 'Not yet scored', found
        ? `No published price for ${day} is in the committed evaluation record yet; its hours are pending and unscored.`
        : `The committed evaluation records hold no entry for ${day} yet; its hours are unscored.`));
      scoreBox.dataset.scored = '0';
      return scoreBox;
    }
    const e = found.entry;
    const share = e.within_tau_hours / e.scored_hours;
    scoreBox.dataset.scored = String(e.scored_hours);
    scoreBox.appendChild(h('div', {class: 'score'},
      h('div', {}, h('div', {class: 'big'}, num(share, pct(share), {'data-metric': 'percentage'})), h('div', {class: 'lab'}, L('live_percentage_label'))),
      h('div', {}, h('div', {class: 'big'}, num(e.mae_eur, eur(e.mae_eur) + ' EUR/MWh', {'data-metric': 'mae'})), h('div', {class: 'lab'}, 'MAE of the issued p50 over the same hours')),
      h('div', {}, h('div', {class: 'big'}, num(e.scored_hours, `${e.scored_hours} of ${e.canonical_hours}`, {'data-metric': 'scored-hours'})), h('div', {class: 'lab'}, `scored hours of the day's canonical ${e.canonical_hours}`))));
    scoreBox.appendChild(h('p', {class: 'qual'}, `Scored over ${day}'s published hours (${e.within_tau_hours} of ${e.scored_hours} within ±${found.window.record.tau_eur} EUR/MWh), from the committed evaluation record: `,
      badge(found.window.evidence_class), ' ', badge(badgeFor(found.window))));
    if (e.scored_hours < e.canonical_hours) {
      scoreBox.appendChild(state('partial', `Partial: ${e.scored_hours} of ${e.canonical_hours} hours scored`, 'The other hours have no published price yet; they are pending and unscored.'));
    }
    return scoreBox;
  }
  // a day the record did not issue: its cause, the outside range, or not decided yet
  function dayState(day, pendingDetail) {
    const o = outsideOf(day);
    if (o) return {kind: 'outside', box: state('notissued', `${day}: outside the live record`, notIssuedText(day))};
    if (S.notIssued.has(day)) return {kind: 'not issued', box: state('notissued', `${day}: not issued`, notIssuedText(day))};
    return {kind: 'pending', box: state('pending', `Not issued yet: ${day}`, pendingDetail)};
  }
  // one delivery day of the product panel (A7): the issued forecast, its two times, its score and the published prices
  function dayPanel(box, day, heading, key, pendingDetail, scored) {
    box.textContent = '';
    box.appendChild(h('h2', {}, heading));
    const f = forecastOf(day);
    if (!f) {
      const st = dayState(day, pendingDetail);
      box.appendChild(st.box);
      box.dataset[key] = st.kind;
      return null;
    }
    box.appendChild(h('p', {class: 'subtitle'}, `Issued hourly p50 with its nominal bands, against the published hourly price where published · artifact `,
      h('span', {class: 'mono'}, short(f.issuing_artifact_sha256)), ` · ${policyLabel(f.issued_policy)} · ${f.display}`));
    box.appendChild(issueTimes(day, f.issue_utc));
    const pn = partialNote(f);
    if (pn) box.appendChild(pn);
    if (scored || publishedHours(f)) box.appendChild(scoreBlock(day));
    else box.appendChild(state('pending', 'Not yet scored', `No price for ${day} is published in the served outcomes yet; its hours are pending and unscored.`));
    box.appendChild(forecastFigure('product', f, `${heading.split(':')[0]}: issued p50 and nominal bands against the published price where published, EUR/MWh by hour`));
    box.dataset[key] = 'issued';
    return f;
  }

  function renderToday() {
    const day = S.today;
    dayPanel($('#today'), day, `Today, ${day}: the issued forecast against the published prices`, 'today',
      `No forecast for ${day} is in the served record, and the record names no cause for it.`, true);
  }

  function renderTomorrow() {
    const day = S.tomorrow;
    dayPanel($('#tomorrow'), day, `Tomorrow, ${day}: the issued forecast with its nominal bands`, 'tomorrow',
      `Its cutoff is ${S.today} at ${cutoffTime()} Europe/Berlin (${L('live_cutoff')}). No forecast for ${day} is in the served bundle.`, false);
  }

  // O31: earlier issued forecasts against the published prices (yesterday's when it exists) and the whole issued record
  function renderEarlier() {
    const box = $('#earlier');
    const day = S.yesterday;
    dayPanel(box, day, `Yesterday, ${day}: the issued forecast against the published prices`, 'yesterday',
      `No forecast for ${day} is in the served record, and the record names no cause for it.`, true);
    box.appendChild(h('h3', {}, 'Every issued day against the published prices'));
    box.appendChild(recordTable('product'));
    box.appendChild(h('p', {}, h('a', {class: 'route', href: '#forecast'}, 'Forecast: any issued day, hour by hour')));
  }
  // every issued day: its two times, its scored hours and its scores, newest first (the panel and the Forecast view)
  function recordTable(viewKey) {
    const days = S.issuedDays.slice().reverse();
    const rows = days.map(d => {
      const f = forecastOf(d), it = issuanceOf(d), found = dayEntry(d);
      const e = found && found.entry.scored && found.entry.scored_hours ? found.entry : null;
      return h('tr', {'data-record-day': d},
        td(d), td(when(f.issue_utc)), td(it ? `${when(it.issuance_started_utc)} to ${clock(it.issuance_finished_utc)}` : L('live_run_time_absent')),
        td(it ? hostText(it) : '—'),
        td(e ? num(e.scored_hours, `${e.scored_hours} of ${e.canonical_hours}`, {'data-metric': 'scored-hours'}) : h('span', {'data-not-scored': '1'}, 'not yet scored'), true),
        td(e ? num(e.mae_eur, eur(e.mae_eur, 2), {'data-metric': 'mae'}) : '—', true),
        td(e ? num(e.within_tau_hours / e.scored_hours, pct(e.within_tau_hours / e.scored_hours), {'data-metric': 'percentage'}) : '—', true),
        td(e ? num(e.wis_eur, eur(e.wis_eur, 2), {'data-metric': 'wis'}) : '—', true));
    });
    const tau = (dayEntry(days[0] || '') || {window: {record: {tau_eur: null}}}).window.record.tau_eur;
    return h('div', {'data-issued-record': viewKey},
      table('Every issued day: its cutoff-based issue time, its actual run, and its score over the published hours',
        ['Delivery day', cap(L('live_issue_time_label')), cap(L('live_run_time_label')) + ' (issuance)', 'Where it ran', {t: 'Scored hours', n: 1},
         {t: 'MAE, EUR/MWh', n: 1}, {t: tau === null ? 'Within the tolerance' : `Within ±${tau} EUR/MWh`, n: 1}, {t: 'WIS, EUR/MWh', n: 1}], rows),
      h('p', {class: 'qual'}, `Scores are the committed evaluation record's, `, badge(L('live_prospective_label')),
        '; each row is one issued day, never pooled with development.'));
  }

  function panelWindow(policy) {
    const pol = policy || 'product';
    if (S.live) return S.evaluation.windows.find(w => w.window === 'prospective' && w.policy === pol);
    return rehearsalRecord(pol);
  }
  function rehearsalRecord(policy) { return S.evaluation.windows.find(w => isRehearsal(w) && w.policy === (policy || 'product')); }
  function coverageSentence(level, share, windowText, width) {
    return fill(L('live_coverage_wording'), {level, share: pct(share), window: windowText, width: eur(width)});
  }
  function rollingWindowText(r, days) { return `the last ${r.window_days} scored delivery days (${r.window_first_day} to ${r.day}; the rolling window holds up to ${days || (panelWindow() || {record: {}}).record.rolling_days})`; }

  function renderHowSure() {
    const box = $('#howsure');
    box.appendChild(h('h2', {}, 'How sure: measured coverage, with width, of the nominal bands'));
    const w = panelWindow();
    const last = w && w.record.rolling && w.record.rolling[w.record.rolling.length - 1];
    if (!last) { box.appendChild(state('pending', 'Not yet scored', S.live ? 'The live record holds no scored day yet.' : 'The rehearsal record holds no scored day yet.')); return; }
    box.appendChild(h('p', {class: 'subtitle'}, `Share of scored hours inside each nominal band and the band's mean width, over the named window · the nominal level is a reference, not a target · `, badge(badgeFor(w))));
    box.appendChild(h('ul', {class: 'plain'}, ['50', '80', '95'].map(b =>
      h('li', {'data-band': b, 'data-share': String(last['coverage' + b]), 'data-width': String(last['width' + b + '_eur'])},
        coverageSentence(b, last['coverage' + b], rollingWindowText(last, w.record.rolling_days), last['width' + b + '_eur'])))));
    box.appendChild(h('p', {}, h('a', {class: 'route', href: '#reliability'}, 'Reliability: every level, the rolling series and the quantile-band PIT')));
  }

  // ------------------------------------------------------------------ the tab list
  const VIEWS = [['train', 'Train it yourself'], ['forecast', 'Forecast'], ['validation', 'Validation'], ['reliability', 'Reliability'],
                 ['explainability', 'Explainability'], ['features', 'Features'], ['data', 'Data'], ['limitations', 'Limitations'],
                 ['history', 'History (historical)']];
  const RENDER = {};
  function renderTabs() {
    $('#views').hidden = false;
    const list = $('#tablist');
    const panels = $('#panels');
    VIEWS.forEach(([id, label], i) => {
      const tab = h('button', {type: 'button', role: 'tab', id: 'tab-' + id, 'aria-controls': id, 'aria-selected': 'false', tabindex: '-1', 'data-view': id}, label);
      tab.addEventListener('click', () => select(id, {hash: true}));
      list.appendChild(tab);
      const panel = h('section', {role: 'tabpanel', id, 'aria-labelledby': 'tab-' + id, tabindex: '0', hidden: true, 'data-view-panel': id});
      panels.appendChild(panel);
    });
    list.addEventListener('keydown', (event) => {
      const tabs = [...list.querySelectorAll('[role="tab"]')];
      const i = tabs.indexOf(document.activeElement);
      if (i < 0) return;
      let j = null;
      if (event.key === 'ArrowRight') j = (i + 1) % tabs.length;
      else if (event.key === 'ArrowLeft') j = (i - 1 + tabs.length) % tabs.length;
      else if (event.key === 'Home') j = 0;
      else if (event.key === 'End') j = tabs.length - 1;
      if (j === null) return;
      event.preventDefault();
      tabs.forEach((t, k) => t.setAttribute('tabindex', k === j ? '0' : '-1'));
      tabs[j].focus();
    });
    list.addEventListener('focusout', () => {
      setTimeout(() => {
        if (list.contains(document.activeElement)) return;
        const tabs = [...list.querySelectorAll('[role="tab"]')];
        tabs.forEach(t => t.setAttribute('tabindex', t.getAttribute('aria-selected') === 'true' ? '0' : '-1'));
      }, 0);
    });
    const fromHash = viewOf(location.hash);
    select(fromHash || VIEWS[0][0], {hash: false});
    if (fromHash) requestAnimationFrame(() => $('#views').scrollIntoView({block: 'start'}));
    window.addEventListener('hashchange', () => {
      const v = viewOf(location.hash);
      if (v) { select(v, {hash: false}); $('#views').scrollIntoView({block: 'start'}); }
    });
  }
  function viewOf(hash) { const id = (hash || '').replace(/^#/, ''); return VIEWS.some(v => v[0] === id) ? id : null; }
  function select(id, opts) {
    for (const [v] of VIEWS) {
      const tab = $('#tab-' + v), panel = document.getElementById(v);
      const on = v === id;
      tab.setAttribute('aria-selected', on ? 'true' : 'false');
      tab.setAttribute('tabindex', on ? '0' : '-1');
      panel.hidden = !on;
    }
    const panel = document.getElementById(id);
    if (!S.views[id]) {
      S.views[id] = true;
      try { RENDER[id](panel); } catch (error) {
        panel.appendChild(state('failed', 'This view could not be drawn', String(error.message || error), {alert: true}));
      }
    } else {
      redraw(id);
    }
    if (opts && opts.hash && location.hash !== '#' + id) history.replaceState(null, '', '#' + id);
    S.selected = id;
  }
  let lastWidth = window.innerWidth;
  let timer = null;
  function onResize() {
    clearTimeout(timer);
    timer = setTimeout(() => {
      if (Math.abs(window.innerWidth - lastWidth) < 8) return;
      lastWidth = window.innerWidth;
      redraw('product');
      if (S.selected) redraw(S.selected);
    }, 150);
  }
  function redraw(key) { for (const item of S.redraw[key] || []) if (item.slot.isConnected) item.run(); }
  window.__redrawAll = () => { redraw('product'); if (S.selected) redraw(S.selected); };

  function viewHead(panel, title, subtitle) {
    panel.appendChild(h('h2', {}, title));
    if (subtitle) panel.appendChild(h('p', {class: 'subtitle'}, subtitle));
  }
  function noArtifact(panel, what) {
    panel.appendChild(state('unavailable', `Unavailable: ${what}`, `The served artifact (${S.artifact.delivery_day}) is a failed issuance: there is no fitted model to ${what}.`));
  }

  // ------------------------------------------------------------------ Train it yourself
  RENDER.train = (panel) => {
    const a = S.artifact;
    if (!a.issued_policy) { viewHead(panel, 'Train it yourself'); return noArtifact(panel, 'retrain'); }
    const day = a.delivery_day, stem = `${a.issued_policy}-${day}`;
    const size = S.build.size.actions.train_it_yourself;
    const ref = S.build.reference;
    viewHead(panel, `Train it yourself: retrain ${day}'s model in your browser`,
      `Retrains the issued fit of ${day} by ${policyLabel(a.issued_policy)} (artifact ${short(a.artifact_sha256)}) from its shipped training window, with the frozen package in WebAssembly, and compares ${L('live_retrained_label')} with the issued artifact.`);
    panel.appendChild(issueTimes(day, a.issue_utc, {'data-train-times': '1'}));
    panel.appendChild(h('dl', {class: 'kv', 'data-train-meta': '1'},
      h('dt', {}, 'Extra download'), h('dd', {'data-size': 'train', 'data-v': String(size.bytes)}, `${bytesText(size.bytes)}: the runtime ${mb(size.parts.runtime)}, its packages ${mb(size.parts.packages)}, the frozen code ${mb(size.parts.code)} and this day's training window ${mb(size.parts.training_window)}`),
      h('dt', {}, 'Reference fit time'), h('dd', {}, h('ul', {class: 'plain'}, ref.runs.map(r =>
        h('li', {'data-reference': r.browser}, `${r.browser === 'webkit' ? 'WebKit' : 'Chromium'} ${r.browser_version}: ${r.fit_seconds.toFixed(1)} s to fit (${r.total_in_worker_seconds.toFixed(1)} s in the worker), measured ${ref.measured_date}`))),
        h('p', {class: 'secondary'}, 'Reference runtime: ', L('live_reference_runtime'), '.')),
      h('dt', {}, 'What it means'), h('dd', {}, L('live_retrain_wording'))));
    const status = h('div', {class: 'op-status', 'aria-live': 'polite', 'data-train-status': 'idle'});
    const button = h('button', {type: 'button', class: 'primary', 'data-action': 'train'}, `Retrain ${day}'s model in your browser`);
    const out = h('div', {class: 'op-result', 'data-train-result': '1'});
    panel.appendChild(h('div', {class: 'action'}, button));
    panel.appendChild(status);
    panel.appendChild(out);
    let run = null;
    const setStatus = (kind, box) => { status.textContent = ''; status.dataset.trainStatus = kind; status.appendChild(box); };
    const go = async () => {
      button.hidden = true;
      out.textContent = '';
      const t0 = performance.now();
      run = {cancelled: false};
      const mine = run;
      setStatus('checking', state('loading', 'Checking the training window', `Verifying ${stem}.json and ${stem}.npz against the manifest before the run.`));
      let files;
      try {
        files = await payloads([stem + '.json', stem + '.npz', 'artifact.json']);
      } catch (error) {
        setStatus('failed', state(error.kind === 'verification' ? 'verification' : 'failed', error.kind === 'verification' ? `Verification failed: ${error.file}` : 'Failed',
          [`${error.reason || error.message}. Nothing was run.`], {alert: true, retry: go}));
        button.hidden = false;
        return;
      }
      if (mine.cancelled) return;
      const worker = new Worker('/app/worker.js');
      mine.worker = worker;
      const elapsed = h('span', {class: 'num', 'data-elapsed': '1'}, '0');
      const cancel = h('button', {type: 'button', class: 'secondary-btn', 'data-action': 'cancel'}, 'Cancel');
      setStatus('running', state('loading', 'Running in your browser…', [h('p', {}, elapsed, ' s elapsed. The frozen runner reports only when it is done, so no stage or percentage is shown.'), h('p', {}, cancel)]));
      const tick = setInterval(() => { elapsed.textContent = ((performance.now() - t0) / 1000).toFixed(0); }, 1000);
      cancel.addEventListener('click', () => {
        mine.cancelled = true;
        clearInterval(tick);
        worker.terminate();
        setStatus('cancelled', state('cancelled', 'Cancelled', 'The run was stopped in your browser; nothing was compared.', {retry: go, retryLabel: 'Retry the retrain'}));
        button.hidden = false;
      });
      const finish = async (message) => {
        clearInterval(tick);
        worker.terminate();
        if (mine.cancelled) return;
        S.results.train_raw = message;
        if (message.errors && message.errors.length) {
          setStatus('failed', state('failed', 'Failed in your browser', [`The frozen runner reported: ${String(message.errors[0]).split('\n').filter(Boolean).slice(-2).join(' ')}`], {alert: true, retry: go, retryLabel: 'Retry the retrain'}));
          button.hidden = false;
          return;
        }
        setStatus('comparing', state('loading', 'Comparing with the issued artifact', 'In the product worker, by cp17.retrain\'s rule (the shared glue\'s retrain_report).'));
        try {
          const report = await runGlue('retrain_report', {'artifact.json': files['artifact.json']}, null, JSON.stringify(message.python.result));
          S.results.retrain = report;
          setStatus('done', state('ready', 'Done in your browser', `The whole run took ${(message.total_ms / 1000).toFixed(1)} s in the runner.`));
          renderRetrain(out, report, message);
        } catch (error) {
          setStatus('failed', state('failed', 'The comparison failed', String(error.message || error).split('\n').slice(-2).join(' '), {alert: true, retry: go, retryLabel: 'Retry the retrain'}));
        }
        button.hidden = false;
      };
      worker.onmessage = (event) => finish(event.data);
      worker.onerror = (event) => finish({errors: ['the runner stopped: ' + (event.message || 'an error')], total_ms: performance.now() - t0});
      worker.postMessage({stem, packages: S.build.pyodide.packages.join(','), attribution: '0'});
    };
    button.addEventListener('click', go);
  };

  function renderRetrain(out, r, message) {
    const dev = r.deviation || {};
    out.appendChild(h('h3', {}, `Result: ${L('live_retrained_label')} against the issued artifact`));
    out.appendChild(h('p', {class: 'score'}, h('span', {class: 'big', 'data-retrain-status': r.status}, r.status)));
    if (r.reason) out.appendChild(h('p', {}, `Why: ${r.reason}.`));
    out.appendChild(h('dl', {class: 'kv'},
      h('dt', {}, 'Training window'), h('dd', {'data-binding': String(r.payload_sha256_equal)}, r.payload_sha256_equal
        ? "your run used the issued fit's shipped training window (its payload identity is the artifact's)"
        : "your run's training window is not the issued fit's (its payload identity differs)"),
      h('dt', {}, 'Measured status'), h('dd', {}, `${r.measured_status || r.status} (quantiles and selections alone; τ_eq ${eur(r.tau_eq_eur, 2)} EUR/MWh)`),
      h('dt', {}, 'Every compared selection matched'), h('dd', {'data-selections-match': String(r.selections_match)}, r.selections_match ? 'yes' : 'no'),
      h('dt', {}, 'Largest difference'), h('dd', {}, dev.shape_equal ? num(dev.max_abs_eur, sci(dev.max_abs_eur) + ' EUR/MWh') : 'the shapes differ')));
    if (dev.shape_equal) {
      const levels = Object.keys(dev.max_abs_eur_by_level);
      out.appendChild(table('Largest absolute difference per quantile level, your retrained model against the issued artifact, EUR/MWh',
        levels.map(l => ({t: l, n: 1})), [h('tr', {}, levels.map(l => td(num(dev.max_abs_eur_by_level[l], sci(dev.max_abs_eur_by_level[l]), {'data-level': l}), true)))]));
    }
    out.appendChild(h('h4', {}, 'The selections compared, member by member'));
    out.appendChild(h('p', {class: 'secondary'}, L('live_limitation_retrain_selections')));
    const diag = new Map((r.diagnostics || []).map(d => [d.member, d.differences]));
    out.appendChild(table('Per member: the seed, the compared selections and any difference', ['Member', {t: 'Seed', n: 1}, 'Compared', 'Differences', "Weights' hash"],
      (r.selections || []).map(s => h('tr', {'data-member': s.member},
        td(String(s.member)), td(String(s.seed), true), td(s.compared.join(', ')),
        td(s.differences.length ? h('strong', {}, s.differences.join(', ')) : 'none'),
        td((diag.get(s.member) || []).length ? 'differs' : 'equal')))));
    if (r.search_match === false) out.appendChild(h('p', {}, 'The search record or the ensemble content differs from the issued artifact\'s.'));
    const marks = message.marks || {};
    out.appendChild(h('h4', {}, 'Your runtime'));
    const py = message.python || {};
    out.appendChild(h('dl', {class: 'kv'},
      h('dt', {}, 'Total in the runner'), h('dd', {}, num(message.total_ms, `${(message.total_ms / 1000).toFixed(1)} s`, {'data-total-ms': '1'})),
      h('dt', {}, 'Marks'), h('dd', {}, Object.entries(marks).map(([k, v]) => `${k.replace(/_ms$/, '')} ${(v / 1000).toFixed(1)} s`).join(' · ')),
      h('dt', {}, 'WebAssembly memory'), h('dd', {}, message.wasm_memory_bytes ? mb(message.wasm_memory_bytes) : 'not reported'),
      h('dt', {}, 'Runtime'), h('dd', {}, `Pyodide ${message.pyodide_version || '?'} · Python ${py.python || '?'} · NumPy ${py.numpy || '?'}`)));
  }

  // ------------------------------------------------------------------ Forecast
  RENDER.forecast = (panel) => {
    viewHead(panel, 'Forecast: what the product issued for a day, and what happened',
      'Issued p50 and nominal 50/80/95% bands against the published hourly price, EUR/MWh; only issued days can be picked.');
    const days = S.issuedDays;
    const select_ = h('select', {id: 'forecast-day', 'data-control': 'forecast-day'}, days.slice().reverse().map(d => h('option', {value: d}, d === S.yesterday ? `${d} (yesterday)` : d === S.today ? `${d} (today)` : d === S.tomorrow ? `${d} (tomorrow)` : d)));
    panel.appendChild(h('div', {class: 'field'}, h('label', {for: 'forecast-day'}, 'Issued day'), h('span', {class: 'sel'}, select_)));
    const out = h('div', {class: 'panel', 'data-forecast-panel': '1'});
    panel.appendChild(out);
    const show = (day) => {
      out.textContent = '';
      S.redraw.forecast = [];
      const f = forecastOf(day);
      out.dataset.day = day;
      out.appendChild(h('h3', {}, `${day}: the issued forecast against the published price`));
      out.appendChild(h('p', {class: 'subtitle', 'data-issued-by': f.issuing_artifact_sha256},
        `Issued by artifact `, h('span', {class: 'mono'}, short(f.issuing_artifact_sha256)), ` · ${policyLabel(f.issued_policy)} · ${f.display}`));
      out.appendChild(issueTimes(day, f.issue_utc));
      const pn = partialNote(f);
      if (pn) out.appendChild(pn);
      const pending = f.keys.filter(k => { const o = S.outcomes.get(k); return !o || o.price === null; }).length;
      if (pending) out.appendChild(state('pending', `${pending} of ${f.keys.length} hours pending`, 'Those hours have no published price in the served outcomes; they are unscored.'));
      if (pending < f.keys.length) out.appendChild(scoreBlock(day));
      out.appendChild(forecastFigure('forecast', f, `${day}: issued p50 and nominal bands against the published price, EUR/MWh by hour`));
    };
    select_.addEventListener('change', () => show(select_.value));
    show(days[days.length - 1]);
    // days not issued: the record's items (the label's, without a live record), then any gap the record does not name
    const gaps = new Map(S.notIssued);
    for (let d = days[0]; d && d <= S.today; d = addDays(d, 1)) if (!days.includes(d) && !gaps.has(d) && !outsideOf(d)) gaps.set(d, null);
    if (!days.includes(S.today) && !gaps.has(S.today) && !outsideOf(S.today)) gaps.set(S.today, null);
    const list = [...gaps.entries()].sort((a, b) => a[0] < b[0] ? -1 : 1);
    panel.appendChild(h('h3', {}, 'Every issued day against the published prices'));
    panel.appendChild(recordTable('forecast'));
    panel.appendChild(h('h3', {}, 'Days not issued'));
    panel.appendChild(list.length ? h('ul', {class: 'plain', 'data-not-issued-list': '1'}, list.map(([d, t]) =>
      h('li', {'data-not-issued': d}, h('strong', {}, d), ': ', t ? `${t}.` : 'not issued; the served record states no cause for this day.')))
      : h('p', {}, 'Every day in the served record is issued.'));
    const outside = S.live ? S.live.record.outside : [];
    if (outside.length) {
      panel.appendChild(h('h3', {}, 'Outside the live record'));
      panel.appendChild(h('ul', {class: 'plain'}, outside.map(o => h('li', {'data-outside': o.first_day + '/' + o.last_day},
        h('strong', {}, `${o.first_day} to ${o.last_day}`), ` (${o.days} days): ${L('live_outside_wording')}.`))));
    }
  };

  // ------------------------------------------------------------------ Validation
  function metricCells(rec) {
    const p = rec.pooled;
    if (!p.scored_hours) return [td('Not yet scored', false, {colspan: '6', 'data-not-scored': '1'})];
    return [td(num(p.mae_eur, eur(p.mae_eur, 2), {'data-metric': 'mae'}), true), td(num(p.wis_eur, eur(p.wis_eur, 2), {'data-metric': 'wis'}), true),
            td(num(p.percentage.share, pct(p.percentage.share), {'data-metric': 'percentage'}), true),
            ...['50', '80', '95'].map(b => td([num(p.coverage[b].share, pct(p.coverage[b].share), {'data-metric': 'coverage' + b}), ' · ',
                                               num(p.coverage[b].mean_width_eur, eur(p.coverage[b].mean_width_eur), {'data-metric': 'width' + b})], true))];
  }
  function groups() {
    const out = [];
    S.evaluation.windows.forEach((w, i) => {
      const key = w.window + '|' + w.evidence_class;
      let g = out.find(x => x.key === key);
      if (!g) { g = {key, window: w.window, evidence_class: w.evidence_class, entries: []}; out.push(g); }
      g.entries.push({index: i, w});
    });
    return out;
  }
  // O32: a window's per-day errors beside B0 (a reference, not a target): one window per chart and table, never pooled
  function dayRows(w) { return (w.record.days || []).filter(d => d.scored && d.scored_hours); }
  function bandCells(d) {
    return ['50', '80', '95'].map(b => {
      const share = d.covered[b] / d.scored_hours, width = d.width_sum_eur[b] / d.scored_hours;
      return td([num(share, pct(share), {'data-metric': 'day-coverage' + b}), ' · ', num(width, eur(width), {'data-metric': 'day-width' + b})], true);
    });
  }
  function perDay(sec, g) {
    const prod = g.entries.find(x => x.w.policy === 'product'), ref = g.entries.find(x => x.w.policy === 'B0');
    if (!prod) return null;
    const development = g.window === 'development';
    const limit = devBoundary();
    let days = dayRows(prod.w);
    const beyond = development && limit ? days.filter(d => d.day > limit).map(d => d.day) : [];
    if (beyond.length) {
      sec.appendChild(state('failed', 'Not shown: development days after the boundary', `${beyond.length} day(s) after ${limit} are in a development record (${beyond.slice(0, 3).join(', ')}); a development display stays on days through ${limit}.`, {alert: true}));
      days = days.filter(d => d.day <= limit);
    }
    const holder = h('div', {class: 'per-day', 'data-per-day': String(prod.index)});
    sec.appendChild(holder);
    holder.appendChild(h('h4', {}, `Per day: ${L('live_daily_errors_wording')}`));
    if (!days.length) { holder.appendChild(state('pending', 'Not yet scored', 'This window holds no scored day yet; there is no per-day error to show.')); return {days: [], holder}; }
    const refBy = new Map((ref ? dayRows(ref.w) : []).map(d => [d.day, d]));
    const labels = days.map(d => d.day);
    holder.appendChild(h('p', {class: 'subtitle'}, `${days.length} scored delivery day${days.length === 1 ? '' : 's'}, ${days[0].day} to ${days[days.length - 1].day} · `,
      badge(badgeFor(prod.w)), development ? [' ', badge(L('live_development_scope'))] : null));
    for (const [metric, name] of [['mae_eur', 'MAE'], ['wis_eur', 'WIS (the interval score)']]) {
      const series = [{name: `${L('live_product_name')}: daily ${name}`, short: 'product', values: days.map(d => d[metric]), color: Charts.colours.issued, marker: 'circle', dash: null, id: 'product-' + metric}];
      if (ref) series.push({name: `B0 · ${B0_LABEL}: daily ${name}`, short: 'B0 (reference)', values: days.map(d => refBy.has(d.day) ? refBy.get(d.day)[metric] : NaN),
                            color: Charts.colours.ref, dash: '6 3', marker: 'ring', id: 'b0-' + metric});
      holder.appendChild(chart('validation', slot => Charts.lines(slot, {labels, series, unit: 'EUR/MWh', xTitle: 'delivery day (Europe/Berlin)',
        title: `${g.evidence_class}: daily ${name} of ${L('live_product_name')}, with the similar-day naive (B0) as a reference, not a target, EUR/MWh by delivery day`})));
    }
    const tau = prod.w.record.tau_eur;
    const body = h('tbody', {}, days.map(d => {
      const r = refBy.get(d.day);
      return h('tr', {'data-day-row': d.day, 'data-window-index': String(prod.index)},
        td(d.day), td(num(d.scored_hours, `${d.scored_hours} of ${d.canonical_hours}`, {'data-metric': 'day-hours'}), true),
        td(num(d.mae_eur, eur(d.mae_eur, 2), {'data-metric': 'day-mae'}), true), td(r ? num(r.mae_eur, eur(r.mae_eur, 2), {'data-metric': 'day-b0-mae'}) : '—', true),
        td(num(d.wis_eur, eur(d.wis_eur, 2), {'data-metric': 'day-wis'}), true), td(r ? num(r.wis_eur, eur(r.wis_eur, 2), {'data-metric': 'day-b0-wis'}) : '—', true),
        td(num(d.within_tau_hours, `${d.within_tau_hours} of ${d.scored_hours}`, {'data-metric': 'day-within'}), true), ...bandCells(d));
    }));
    let finalDay = null;
    if (recomputedWindow(prod.w)) {
      finalDay = td('Not recomputed yet: use “Recompute in your browser” above.', false, {colspan: '10'});
      body.appendChild(h('tr', {class: 'final-day', 'data-final-day': String(prod.index)}, td('Matches the stored value · per day'), finalDay));
    }
    holder.appendChild(details(`Table: the per-day errors, with coverage and width per band (${days.length} day${days.length === 1 ? '' : 's'})`,
      table(`${g.evidence_class}: per-day errors of ${L('live_product_name')} and B0 (a reference), EUR/MWh; coverage · mean width per nominal band`,
        ['Delivery day', {t: 'Scored hours', n: 1}, {t: 'MAE', n: 1}, {t: 'B0 MAE', n: 1}, {t: 'WIS', n: 1}, {t: 'B0 WIS', n: 1}, {t: `Within ±${tau} EUR/MWh`, n: 1},
         {t: '50%: coverage · width', n: 1}, {t: '80%: coverage · width', n: 1}, {t: '95%: coverage · width', n: 1}], [body])));
    return {days, holder, finalDay, index: prod.index, refIndex: ref ? ref.index : null};
  }
  // the per-day row after the in-browser recomputation: every day's entries are among the compared items
  function fillPerDay(pd, result) {
    if (!pd || !pd.finalDay) return;
    const cell = pd.finalDay;
    cell.textContent = '';
    const rows = [pd.index, pd.refIndex].filter(i => i !== null).map(i => result.rows.find(x => x.index === i)).filter(Boolean);
    if (!rows.length || rows.some(r => !r.recomputed)) { cell.textContent = 'not recomputed'; return; }
    const bad = rows.flatMap(r => r.mismatches.filter(mm => /^days\[\d+\]/.test(mm.path)).map(mm => Object.assign({policy: r.policy}, mm)));
    const ok = rows.every(r => r.match);
    cell.parentElement.dataset.match = String(ok);
    if (ok) {
      cell.appendChild(h('p', {}, h('span', {class: 'match-ok', 'data-mark-match-day': 'ok'}, '✓ matches'),
        ` · every day's entry (its MAE, WIS, counts, coverage and width) recomputed in your browser equals the committed record, for the product and B0, among the ${rows.reduce((a, r) => a + r.compared, 0).toLocaleString('en-US')} compared items, over ${pd.days.map(d => d.day).join(', ')}`));
    } else {
      cell.appendChild(h('p', {}, h('span', {class: 'match-fail', 'data-mark-match-day': 'fail'}, '✗ does not match'),
        ` · ${bad.length} per-day item${bad.length === 1 ? '' : 's'} listed differ (the first 20 mismatches per window are listed). This blocks that day's publication.`));
      cell.appendChild(h('ul', {class: 'plain'}, bad.map(mm => h('li', {'data-mismatch-day': mm.path}, `${mm.policy} ${mm.path}: recomputed ${exact(mm.recomputed)} · committed ${exact(mm.committed)}`))));
    }
  }
  // O33: the live record's running means with their 95% intervals, computed at build time (cp18.running); drawn only
  function runningSection(sec) {
    const r = S.live && S.live.running;
    if (!r) return;
    const box = h('div', {class: 'running', 'data-running': '1'});
    sec.appendChild(box);
    box.appendChild(h('h4', {}, 'Cumulative: the running mean daily error of the issued days, and its interval'));
    const mae = r.series.mae, wis = r.series.wis, dm = r.series.mae_vs_B0, dw = r.series.wis_vs_B0;
    if (!mae.length) { box.appendChild(state('pending', 'Not yet scored', 'The live record holds no scored day yet; there is no running mean.')); return; }
    const last = mae[mae.length - 1];
    const words = (p) => p.lower !== null && p.upper !== null ? fill(L('live_running_wording'), {n: p.n}) : L('live_running_before_minimum');
    box.appendChild(h('p', {class: 'subtitle'}, `After each scored day: the running mean of the daily MAE and of the daily WIS, EUR/MWh; the band is the ${fill(L('live_running_wording'), {n: 'n'})}, drawn from ${r.minimum_days} scored days (before that, the running mean alone: ${L('live_running_before_minimum')}) · `,
      badge(L('live_prospective_label'), true)));
    const labels = mae.map(p => p.last_day);
    const bandName = `${fill(L('live_running_wording'), {n: 'n'})} (${L('live_running_before_minimum')})`;
    box.appendChild(chart('validation', slot => Charts.running(slot, {labels, unit: 'EUR/MWh', bandLabel: bandName,
      title: `Running mean daily MAE and WIS of ${L('live_product_name')} over the live record's scored days, each with the ${fill(L('live_running_wording'), {n: 'n'})} as a band, EUR/MWh`,
      series: [{name: 'running mean daily MAE', short: 'MAE', points: mae, color: Charts.colours.issued, marker: 'circle', dash: null, id: 'running-mae'},
               {name: 'running mean daily WIS', short: 'WIS', points: wis, color: Charts.colours.accent, marker: 'square', dash: '6 3', id: 'running-wis'}]})));
    box.appendChild(h('p', {class: 'finding', 'data-running-latest': String(last.n)}, `Over ${last.n} scored day${last.n === 1 ? '' : 's'} to ${last.last_day}: mean daily MAE ${eur(last.mean, 2)} EUR/MWh` +
      (last.lower !== null ? ` (${words(last)}: ${eur(last.lower, 2)} to ${eur(last.upper, 2)})` : ` (${words(last)})`) +
      `; mean daily WIS ${eur(wis[wis.length - 1].mean, 2)} EUR/MWh` + (wis[wis.length - 1].lower !== null ? ` (${eur(wis[wis.length - 1].lower, 2)} to ${eur(wis[wis.length - 1].upper, 2)})` : '') + '.'));
    if (dm.length) {
      const dl = dm[dm.length - 1];
      box.appendChild(chart('validation', slot => Charts.running(slot, {labels: dm.map(p => p.last_day), unit: 'EUR/MWh', bandLabel: bandName,
        zero: 'zero: no difference from the similar-day naive (B0), a reference',
        title: `Running mean paired difference, ${L('live_product_name')} minus the similar-day naive (B0), daily MAE and WIS, each with the ${fill(L('live_running_wording'), {n: 'n'})} as a band, EUR/MWh; zero is a reference`,
        series: [{name: 'running mean difference in daily MAE', short: 'MAE − B0', points: dm, color: Charts.colours.issued, marker: 'circle', dash: null, id: 'running-mae-b0'},
                 {name: 'running mean difference in daily WIS', short: 'WIS − B0', points: dw, color: Charts.colours.accent, marker: 'square', dash: '6 3', id: 'running-wis-b0'}]})));
      box.appendChild(h('p', {class: 'finding', 'data-running-difference': String(dl.n)}, `Over ${dl.n} paired day${dl.n === 1 ? '' : 's'}: mean difference in daily MAE ${signed(dl.mean, 2)} EUR/MWh` +
        (dl.lower !== null ? ` (${words(dl)}: ${signed(dl.lower, 2)} to ${signed(dl.upper, 2)})` : ` (${words(dl)})`) + ` · ${L('live_running_difference')}.`));
    }
    const cell = (p) => p ? [num(p.mean, eur(p.mean, 2), {'data-mean': '1', 'data-lower': p.lower === null ? '' : String(p.lower), 'data-upper': p.upper === null ? '' : String(p.upper)}),
                             p.lower !== null ? ` [${eur(p.lower, 2)}, ${eur(p.upper, 2)}]` : ''] : '—';
    const byN = (list, n) => list.find(p => p.n === n);
    box.appendChild(details('Table: the running means and their intervals',
      table(`Running means after each scored day, EUR/MWh: the mean [the ${fill(L('live_running_wording'), {n: 'n'})}]`,
        [{t: 'Scored days', n: 1}, 'Last day', {t: 'MAE', n: 1}, {t: 'WIS', n: 1}, {t: 'MAE − B0', n: 1}, {t: 'WIS − B0', n: 1}, 'Interval'],
        mae.map((p, i) => h('tr', {'data-running-n': String(p.n)}, td(String(p.n), true), td(p.last_day), td(cell(p), true), td(cell(wis[i]), true),
          td(cell(byN(dm, p.n)), true), td(cell(byN(dw, p.n)), true), td(words(p)))))));
    box.appendChild(h('p', {class: 'qual', 'data-running-method': '1'}, `Interval method: ${r.method}. Only the method is shared; the record is the live product's own, ${L('live_prospective_label')}: not 4.7T's issuance or score and not a test result, and never pooled with development.`));
  }

  RENDER.validation = (panel) => {
    viewHead(panel, 'Validation: how the product scores, window by window, never pooled',
      `MAE and WIS (the interval score) in EUR/MWh, lower is better; ${L('live_percentage_label')}; coverage · mean width per nominal band. ` +
      `B0 is the ${B0_LABEL}.`);
    const box = h('div', {});
    const b0 = () => S.manifest.files.filter(f => f.path.startsWith('B0-')).map(f => f.path);
    const sections = [];
    glueAction(box, 'recompute', () => ['issued-forecasts.json', 'outcomes.json', 'evaluation.json', ...b0()], (out, result) => {
      for (const s of sections) s.fill(result);
    }, {label: 'Recompute in your browser', againLabel: 'Recompute again', extraWhat: "B0's served training windows",
        extraBytes: () => S.build.size.actions.recompute_data.bytes});
    panel.appendChild(h('p', {}, 'The development folds are static, from evidence. The development rehearsal, the one-shot fresh-data test (4.7T) and the prospective record are recomputed in your browser from the served issued forecasts and outcomes with the frozen scoring code, and compared with the committed records.'));
    panel.appendChild(box);
    for (const g of groups()) {
      const first = g.entries[0].w;
      const recomputed = recomputedWindow(first);
      const sec = h('div', {class: 'panel', 'data-window': g.window, 'data-evidence': g.evidence_class});
      sec.appendChild(h('h3', {}, g.evidence_class));
      sec.appendChild(h('p', {}, badge(badgeFor(first), true), ' ', h('span', {class: 'secondary'}, recomputed ? 'recomputed in your browser on request' : 'static, from evidence (not recomputed in the browser)')));
      const body = h('tbody', {});
      for (const {index, w} of g.entries) {
        const p = w.record.pooled;
        body.appendChild(h('tr', {'data-index': index, 'data-policy': w.policy},
          td(policyName(w.policy)), td(num(p.scored_days, String(p.scored_days)), true), td(num(p.scored_hours, p.scored_hours.toLocaleString('en-US')), true),
          td(num(p.partial_days, String(p.partial_days)), true), td(num(p.pending_or_unscored_days, String(p.pending_or_unscored_days)), true), ...metricCells(w.record)));
      }
      const finals = [];
      if (recomputed) {
        for (const {index, w} of g.entries) {
          const cell = td('Not recomputed yet: use “Recompute in your browser” above.', false, {colspan: '10'});
          const row = h('tr', {class: 'final', 'data-final': index, 'data-policy': w.policy}, td(`Matches the stored value · ${w.policy === 'product' ? 'the product' : 'B0'}`), cell);
          body.appendChild(row);
          finals.push({index, cell, row});
        }
      }
      sec.appendChild(table(`${g.evidence_class}: pooled over the window's scored days`,
        ['Policy', {t: 'Days scored', n: 1}, {t: 'Scored hours', n: 1}, {t: 'Partial days', n: 1}, {t: 'Pending or unscored days', n: 1},
         {t: 'MAE, EUR/MWh', n: 1}, {t: 'WIS, EUR/MWh', n: 1}, {t: `Within ±${g.entries[0].w.record.tau_eur} EUR/MWh`, n: 1},
         {t: '50%: coverage · width', n: 1}, {t: '80%: coverage · width', n: 1}, {t: '95%: coverage · width', n: 1}], [body]));
      panel.appendChild(sec);
      const pd = perDay(sec, g);
      if (g.window === 'prospective') runningSection(sec);
      sections.push({fill: (result) => {
        fillPerDay(pd, result);
        for (const f of finals) {
          const r = result.rows.find(x => x.index === f.index);
          f.cell.textContent = '';
          if (!r || !r.recomputed) { f.cell.textContent = 'not recomputed'; continue; }
          f.row.dataset.match = String(r.match);
          const shown = h('ul', {class: 'plain'}, r.shown.map(s => h('li', {'data-path': s.path, 'data-recomputed': JSON.stringify(s.recomputed), 'data-committed': JSON.stringify(s.committed)},
            `${s.path.replace('pooled/', '').replace('/share', ' share')}: recomputed ${exact(s.recomputed)} · committed ${exact(s.committed)}`)));
          if (r.match) {
            f.cell.appendChild(h('p', {}, h('span', {class: 'match-ok', 'data-mark-match': 'ok'}, '✓ matches'), ` · ${r.compared.toLocaleString('en-US')} items compared (${r.rule})` +
              (r.days.length ? ` over ${r.days.join(', ')}` : '; no scored day in this window yet')));
          } else {
            f.cell.appendChild(h('p', {}, h('span', {class: 'match-fail', 'data-mark-match': 'fail'}, '✗ does not match'),
              ` · ${r.mismatches.length} of ${r.compared.toLocaleString('en-US')} compared items differ (${r.rule}). This blocks that day's publication.`));
            f.cell.appendChild(h('ul', {class: 'plain'}, r.mismatches.map(mm => h('li', {'data-mismatch': mm.path}, `${mm.path}: recomputed ${exact(mm.recomputed)} · committed ${exact(mm.committed)}`))));
          }
          f.cell.appendChild(shown);
        }
      }});
    }
  };

  // ------------------------------------------------------------------ Reliability
  const PIT_NAMES = ['p025', 'p10', 'p25', 'p50', 'p75', 'p90', 'p975'];
  function pitInterval(k) { return k === 0 ? `(−∞, ${PIT_NAMES[0]}]` : k === 7 ? `(${PIT_NAMES[6]}, ∞)` : `(${PIT_NAMES[k - 1]}, ${PIT_NAMES[k]}]`; }
  RENDER.reliability = (panel) => {
    viewHead(panel, 'Reliability: how often the intervals hold, and how wide they are',
      'From the committed evaluation records (verified at start), one panel per record, never pooled. The nominal level is drawn as a reference, not a target.');
    const live = S.live ? windowsOf('product').filter(w => w.window === 'prospective') : [];
    const records = live.concat(windowsOf('product').filter(w => isRehearsal(w)), windowsOf('product').filter(w => w.window === 'development' && !isRehearsal(w)));
    for (const w of records) {
      const rec = w.record, p = rec.pooled;
      const sec = h('div', {class: 'panel', 'data-reliability': w.evidence_class});
      sec.appendChild(h('h3', {}, w.evidence_class));
      sec.appendChild(h('p', {}, badge(badgeFor(w), true), ' ', h('span', {class: 'secondary'}, `${L('live_product_name')} · ${p.scored_hours.toLocaleString('en-US')} scored hours over ${p.scored_days} days`)));
      if (!p.scored_hours) { sec.appendChild(state('pending', 'Not yet scored', 'This record has no scored hour.')); panel.appendChild(sec); continue; }
      // 1. reliability diagram
      const worst = p.reliability.reduce((a, b) => Math.abs(b.share - b.level) > Math.abs(a.share - a.level) ? b : a);
      sec.appendChild(h('h4', {}, 'Does the observed share at or below each quantile match its level?'));
      sec.appendChild(h('p', {class: 'subtitle'}, `Observed share of scored hours at or below each emitted quantile, against the level · counts beside each point · ${w.evidence_class}`));
      sec.appendChild(chart('reliability', slot => Charts.reliability(slot, {points: p.reliability,
        title: `Reliability diagram, ${w.evidence_class}: observed share at or below each quantile against its level, with counts; the diagonal is the nominal level, a reference not a target`})));
      sec.appendChild(h('p', {class: 'finding'}, `The largest gap is at ${worst.name}: ${pct(worst.share)} of hours fell at or below it, against its level ${pct(worst.level)}.`));
      sec.appendChild(h('p', {class: 'qual'}, `${p.scored_hours.toLocaleString('en-US')} scored hours over ${p.scored_days} delivery days; hours within a day are not independent.`));
      sec.appendChild(details('Table: the reliability diagram', table(`Reliability, ${w.evidence_class}`, ['Level', 'Quantile', {t: 'At or below', n: 1}, {t: 'Scored hours', n: 1}, {t: 'Observed share', n: 1}],
        p.reliability.map(r => h('tr', {}, td(pct(r.level)), td(r.name), td(String(r.at_or_below), true), td(String(r.scored_hours), true), td(num(r.share, pct(r.share)), true))))));
      // 2. rolling coverage with width
      const last = rec.rolling[rec.rolling.length - 1];
      sec.appendChild(h('h4', {}, 'How often did each band hold over the rolling window, and how wide was it?'));
      sec.appendChild(h('p', {class: 'subtitle'}, `Coverage and mean width per nominal band over the last up to ${rec.rolling_days} scored delivery days ending at each day · ${w.evidence_class}`));
      sec.appendChild(h('ul', {class: 'plain'}, ['50', '80', '95'].map(b => h('li', {}, coverageSentence(b, last['coverage' + b], rollingWindowText(last, rec.rolling_days), last['width' + b + '_eur'])))));
      sec.appendChild(chart('reliability', slot => Charts.rolling(slot, {series: rec.rolling,
        title: `Rolling coverage per nominal band, ${w.evidence_class}; the nominal levels are references, not targets`,
        widthTitle: `Rolling mean width per nominal band, ${w.evidence_class}, EUR/MWh`,
        caption: 'Coverage: share of the window\'s scored hours inside each band.', widthCaption: 'Width: mean upper minus lower bound over the same hours, EUR/MWh.'})));
      sec.appendChild(h('p', {class: 'qual'}, 'Higher coverage is not better on its own when the bands widen; read the two charts together.'));
      sec.appendChild(details('Table: the rolling coverage and width', table(`Rolling coverage and width, ${w.evidence_class}`,
        ['Day', 'Window from', {t: 'Days', n: 1}, {t: 'Hours', n: 1}, {t: '50% cov.', n: 1}, {t: '50% width', n: 1}, {t: '80% cov.', n: 1}, {t: '80% width', n: 1}, {t: '95% cov.', n: 1}, {t: '95% width', n: 1}],
        rec.rolling.map(r => h('tr', {}, td(r.day), td(r.window_first_day), td(String(r.window_days), true), td(String(r.scored_hours), true),
          ...['50', '80', '95'].flatMap(b => [td(pct(r['coverage' + b]), true), td(eur(r['width' + b + '_eur']), true)]))))));
      // 3. the quantile-band PIT
      sec.appendChild(h('h4', {}, 'Where do the outcomes fall between the emitted quantiles?'));
      sec.appendChild(h('p', {class: 'subtitle'}, `Quantile-band PIT: the share of scored hours in each of the eight bands the seven levels define, against each band's nominal share (blue tick, a reference) · ${w.evidence_class}`));
      sec.appendChild(chart('reliability', slot => Charts.bars(slot, p.pit.map(b => ({label: pitInterval(b.band), value: b.share, nominal: b.nominal_share, text: `${pct(b.share)} (${b.count})`})),
        {title: `Quantile-band PIT, ${w.evidence_class}: observed share per band with counts, against the nominal share`, pct: true, unit: 'share of hours', valueLabels: true,
         refLabel: "the band's nominal share (a reference, not a target)", horizontal: true})));
      const maxGap = p.pit.reduce((a, b) => Math.abs(b.share - b.nominal_share) > Math.abs(a.share - a.nominal_share) ? b : a);
      sec.appendChild(h('p', {class: 'finding'}, `The largest gap is band ${pitInterval(maxGap.band)}: ${pct(maxGap.share)} of hours against a nominal ${pct(maxGap.nominal_share)}.`));
      sec.appendChild(h('p', {class: 'qual'}, 'A quantile-band PIT of seven emitted levels, with counts; no continuous PIT is claimed.'));
      sec.appendChild(details('Table: the quantile-band PIT', table(`Quantile-band PIT, ${w.evidence_class}`, ['Band', {t: 'Count', n: 1}, {t: 'Share', n: 1}, {t: 'Nominal share', n: 1}],
        p.pit.map(b => h('tr', {}, td(pitInterval(b.band)), td(String(b.count), true), td(pct(b.share), true), td(pct(b.nominal_share), true))))));
      panel.appendChild(sec);
    }
    const unscored = windowsOf('product').filter(w => w.window !== 'development' && !live.includes(w));
    panel.appendChild(h('div', {class: 'panel'}, h('h3', {}, 'The windows not yet scored'), h('ul', {class: 'plain'}, unscored.map(w =>
      h('li', {}, badge(badgeFor(w)), ' ', w.record.pooled.scored_hours ? `${w.record.pooled.scored_hours} scored hours` : 'not yet scored')))));
  };

  // ------------------------------------------------------------------ Explainability
  function explainFiles() {
    const a = S.artifact;
    return ['artifact.json', 'artifact-arrays.npz', `${a.issued_policy}-${a.delivery_day}.json`, `${a.issued_policy}-${a.delivery_day}.npz`];
  }
  RENDER.explainability = (panel) => {
    const a = S.artifact;
    viewHead(panel, "Explainability: what this fitted model's p50 rests on, by input group",
      `The issued p50 of ${a.delivery_day} decomposed into input-group contributions in EUR/MWh, against the model's stated baseline · artifact ${short(a.artifact_sha256)} · ${L('live_attribution_wording')}`);
    if (!a.issued_policy) return noArtifact(panel, 'explain');
    const members = (a.lineage.training.members || []).length;
    panel.appendChild(h('p', {}, `${policyLabel(a.issued_policy)} has no blend: it is one model, so there is no component decomposition. Its intervals are its own Johnson SU quantiles, the median of its ${members} members' quantiles at each level; they are not attributed to inputs, and the decomposition below is of the p50 only.`));
    const box = h('div', {});
    glueAction(box, 'explain', explainFiles, (out, r) => renderExplain(out, r),
      {label: 'Explain in your browser', againLabel: 'Explain again', extraWhat: 'the fitted arrays and the training window',
       extraBytes: () => S.build.size.actions.explain_data.bytes});
    panel.appendChild(box);
  };
  function renderExplain(out, r) {
    S.redraw.explainability = [];
    const labels = hourLabels(r.keys);
    const n = r.keys.length;
    const sum = (i) => r.phi_eur.reduce((s, phi) => s + phi[i], 0);
    out.appendChild(h('dl', {class: 'kv', 'data-explain-summary': '1'},
      h('dt', {}, 'Method'), h('dd', {}, `${r.method}; ${r.coalitions.toLocaleString('en-US')} coalitions of ${r.players.length} input groups`),
      h('dt', {}, 'Reproduced'), h('dd', {'data-reproduced': r.reproduced}, `the served arrays reproduced the issued quantiles ${r.reproduced}`),
      h('dt', {}, 'Efficiency'), h('dd', {}, 'the contributions sum to the full p50 minus the baseline within ', num(r.efficiency_max_abs, sci(r.efficiency_max_abs) + ' EUR/MWh', {'data-efficiency': '1'}), ' (the largest gap over the day\'s hours)'),
      h('dt', {}, 'Wording'), h('dd', {}, L('live_attribution_wording'))));
    const sel = h('select', {id: 'explain-hour', 'data-control': 'explain-hour'}, labels.map((lab, i) => h('option', {value: String(i)}, lab)));
    out.appendChild(h('div', {class: 'field'}, h('label', {for: 'explain-hour'}, 'Delivery hour'), h('span', {class: 'sel'}, sel)));
    const hourBox = h('div', {class: 'panel', 'data-explain-hour': '0'});
    out.appendChild(hourBox);
    const showHour = (i) => {
      hourBox.textContent = '';
      hourBox.dataset.explainHour = String(i);
      S.redraw.explainability = (S.redraw.explainability || []).filter(x => !hourBox.contains(x.slot) && x.slot.isConnected);
      const items = r.players.map((g, k) => ({label: g, value: r.phi_eur[k][i]})).sort((x, y) => Math.abs(y.value) - Math.abs(x.value));
      hourBox.appendChild(h('h3', {}, `${labels[i]}: p50 ${eur(r.issued_p50[i])} EUR/MWh`));
      hourBox.appendChild(h('p', {class: 'subtitle'}, `Contribution of each input group, EUR/MWh, relative to the baseline p50 ${eur(r.baseline_p50[i])} EUR/MWh (every group at its training mean) · ${r.delivery_day} · artifact ${short(r.artifact_sha256)}`));
      hourBox.appendChild(chart('explainability', slot => Charts.bars(slot, items.map(it => ({label: it.label, value: it.value, text: signed(it.value) })),
        {title: `Input-group contributions to the p50 at ${labels[i]}, EUR/MWh, relative to the model's baseline`, unit: 'EUR/MWh', horizontal: true, tickDigits: 0})));
      hourBox.appendChild(h('ul', {class: 'plain'}, items.slice(0, 3).map(it => h('li', {}, h('code', {}, it.label), ' ', fill(L('live_explain_wording'), {value: signed(it.value)}), '.'))));
      hourBox.appendChild(h('p', {class: 'qual'}, `Baseline ${eur(r.baseline_p50[i], 2)} + contributions ${signed(sum(i), 2)} = ${eur(r.baseline_p50[i] + sum(i), 2)} EUR/MWh; the full p50 is ${eur(r.full_p50[i], 2)} and the issued p50 ${eur(r.issued_p50[i], 2)}. ${L('live_attribution_wording')}.`));
      hourBox.appendChild(details('Table: the contributions at this hour', table(`Contributions at ${labels[i]}, EUR/MWh`, ['Input group', {t: 'Contribution', n: 1}],
        items.map(it => h('tr', {'data-group': it.label}, td(h('code', {}, it.label)), td(num(it.value, signed(it.value, 2)), true))))));
    };
    sel.addEventListener('change', () => showHour(Number(sel.value)));
    showHour(0);
    out.appendChild(details('Table: every hour and group, EUR/MWh', table(`Contributions by hour, ${r.delivery_day}, EUR/MWh`,
      ['Hour', {t: 'Baseline', n: 1}, ...r.players.map(g => ({t: g, n: 1})), {t: 'Full p50', n: 1}, {t: 'Issued p50', n: 1}],
      labels.map((lab, i) => h('tr', {}, td(lab), td(eur(r.baseline_p50[i], 2), true), ...r.players.map((g, k) => td(signed(r.phi_eur[k][i], 2), true)),
        td(eur(r.full_p50[i], 2), true), td(num(r.issued_p50[i], eur(r.issued_p50[i], 2)), true))))));
    // the what-if control: one input group removed, by its attribution
    const cf = h('div', {class: 'cf-panel', 'data-counterfactual': '1'});
    cf.appendChild(h('h3', {}, h('span', {class: 'cf-label', 'data-cf-label': '1'}, L('live_counterfactual_label'))));
    cf.appendChild(h('p', {}, "What if one input group were removed, set to its baseline? The approximate effect shown is the attribution's p50 with every group minus that group's contribution. The model is not run again: with interactions between groups, its own output with the group at its baseline would differ by an amount not shown here."));
    const gsel = h('select', {id: 'cf-group', 'data-control': 'cf-group'}, r.players.map((g, k) => h('option', {value: String(k)}, g)));
    cf.appendChild(h('div', {class: 'field'}, h('label', {for: 'cf-group'}, 'Remove the input group'), h('span', {class: 'sel'}, gsel)));
    const cfOut = h('div', {'data-cf-output': '1'});
    cf.appendChild(cfOut);
    const showCf = (k) => {
      cfOut.textContent = '';
      S.redraw.explainability = (S.redraw.explainability || []).filter(x => !cfOut.contains(x.slot) && x.slot.isConnected);
      const g = r.players[k];
      // the attribution's own numbers: its full-coalition p50 (every group present) minus the group's contribution
      const values = r.full_p50.map((v, i) => v - r.phi_eur[k][i]);
      cfOut.dataset.group = g;
      cfOut.appendChild(chart('explainability', slot => Charts.lines(slot, {labels, unit: 'EUR/MWh', xTitle: 'delivery hour, Europe/Berlin',
        title: `${L('live_counterfactual_label')}: the p50 without the ${g} contribution, beside the attribution's p50 with every group (a reference), EUR/MWh by hour`,
        series: [{name: "the attribution's p50 with every group (a reference)", short: 'every group (reference)', values: r.full_p50, color: Charts.colours.ref, dash: '2 3', marker: 'ring', id: 'reference-p50'},
                 {name: `${L('live_counterfactual_label')}: without ${g} (approximate)`, short: 'counterfactual', values, color: Charts.colours.cf, dash: '6 4', marker: 'diamond', id: 'counterfactual', cls: 'counterfactual'}]})));
      cfOut.appendChild(details(`Table: the counterfactual without ${g}`, table(`${L('live_counterfactual_label')}: without ${g}, EUR/MWh`,
        ['Hour', {t: 'p50 with every group', n: 1}, {t: `${g} contribution`, n: 1}, {t: 'Counterfactual (approximate)', n: 1}],
        labels.map((lab, i) => h('tr', {}, td(lab), td(eur(r.full_p50[i], 2), true), td(signed(r.phi_eur[k][i], 2), true), td(h('span', {class: 'cf-value', 'data-cf-value': String(values[i])}, eur(values[i], 2)), true))))));
    };
    gsel.addEventListener('change', () => showCf(Number(gsel.value)));
    showCf(0);
    out.appendChild(cf);
  }

  // ------------------------------------------------------------------ Features
  RENDER.features = (panel) => {
    const a = S.artifact;
    viewHead(panel, "Features: how unusual are this day's inputs, and how much does the fitted model rely on each group?",
      `${a.delivery_day}'s inputs in their source units against the fit's training window · artifact ${short(a.artifact_sha256)} of ${a.delivery_day}`);
    if (!a.issued_policy) return noArtifact(panel, 'describe');
    const box = h('div', {});
    glueAction(box, 'features', explainFiles, (out, r) => renderFeatures(out, r),
      {label: 'Show the inputs in your browser', againLabel: 'Show again', extraWhat: 'the fitted arrays and the training window',
       extraBytes: () => S.results.explain ? 0 : S.build.size.actions.explain_data.bytes});
    panel.appendChild(box);
  };
  function renderFeatures(out, r) {
    S.redraw.features = [];
    const sha = short(r.artifact_sha256);
    out.appendChild(h('h3', {}, `${L('live_features_wording')}: ${r.delivery_day}, artifact ${sha}`));
    out.appendChild(h('p', {class: 'subtitle'}, `Mean absolute contribution of each input group over the day's hours, EUR/MWh · ${L('live_attribution_wording')} · a property of this one fitted artifact, which changes with each daily refit`));
    out.appendChild(chart('features', slot => Charts.bars(slot, r.reliance.map(x => ({label: x.group, value: x.mean_abs_eur, text: eur(x.mean_abs_eur, 2)})),
      {title: `${L('live_features_wording')}: mean absolute contribution per input group, ${r.delivery_day}, artifact ${sha}, EUR/MWh`, unit: 'EUR/MWh', horizontal: true})));
    out.appendChild(details('Table: the reliance per group', table(`${L('live_features_wording')}, ${r.delivery_day}, artifact ${sha}`, ['Input group', {t: 'Mean |contribution|, EUR/MWh', n: 1}, {t: 'Largest |contribution|, EUR/MWh', n: 1}],
      r.reliance.map(x => h('tr', {'data-group': x.group}, td(h('code', {}, x.group)), td(num(x.mean_abs_eur, eur(x.mean_abs_eur, 2)), true), td(eur(x.max_abs_eur, 2), true))))));
    out.appendChild(details(`The fit's ${r.members.length} members`, table('Members: configuration, input groups and transform', ['Member', 'Configuration', 'Input groups', 'Transform'],
      r.members.map(m => h('tr', {}, td(String(m.member)), td(String(m.config)), td(m.groups.join(', ')), td(String(m.transform)))))));
    out.appendChild(h('h3', {}, `The inputs against the training window (${r.window_days} days from ${r.window_first_day})`));
    out.appendChild(h('p', {class: 'subtitle'}, 'Each input\'s value on the day in its source unit, its percentile within the training window, and the window\'s minimum, median and maximum; a missing value is flagged.'));
    const byGroup = new Map();
    for (const row of r.inputs) { if (!byGroup.has(row.group)) byGroup.set(row.group, []); byGroup.get(row.group).push(row); }
    for (const [group, rows] of byGroup) {
      const missing = rows.filter(x => x.missing).length;
      const d = h('details', {'data-feature-group': group}, h('summary', {}, `${group} · ${rows.length} inputs${missing ? ` · ${missing} missing` : ''}${rows.some(x => x.used_by_members) ? '' : ' · not used by the members'}`));
      if (group === 'gfs') d.appendChild(h('p', {class: 'secondary'}, shared('gfs_attribution')));
      d.appendChild(table(`${group}: the day's inputs against the training window`, ['Input', {t: 'Value', n: 1}, 'Unit', {t: 'Percentile', n: 1}, {t: 'Min', n: 1}, {t: 'Median', n: 1}, {t: 'Max', n: 1}, 'Missing'],
        rows.map(x => h('tr', {}, td(h('code', {}, x.name)), td(x.value === null ? '—' : num(x.value, eur(x.value, 2)), true), td(x.unit),
          td(x.percentile === null ? '—' : pct(x.percentile, 0), true), td(eur(x.window_min, 2), true), td(eur(x.window_median, 2), true), td(eur(x.window_max, 2), true),
          td(x.missing ? 'missing' : 'no')))));
      out.appendChild(d);
    }
  }

  // ------------------------------------------------------------------ Data
  RENDER.data = (panel) => {
    viewHead(panel, 'Data: what the price series looks like', 'Hourly DE-LU day-ahead prices from the served series, EUR/MWh, computed in your browser.');
    const bytes = S.build.size.actions.data_view.bytes;
    const status = h('div', {class: 'op-status', 'aria-live': 'polite'});
    const out = h('div', {});
    const button = h('button', {type: 'button', class: 'primary', 'data-action': 'data'}, 'Load the price series');
    panel.appendChild(h('div', {class: 'action'}, h('p', {class: 'action-meta', 'data-size': 'data'}, `Downloads ${bytesText(bytes)}: the hourly series (series.json).`), button));
    panel.appendChild(status);
    panel.appendChild(out);
    const go = async () => {
      button.hidden = true;
      status.textContent = '';
      status.appendChild(state('loading', 'Loading and checking the series', 'Verifying series.json against the manifest.'));
      try {
        const series = decode((await payload('series.json')).bytes);
        status.textContent = '';
        renderData(out, series);
      } catch (error) {
        status.textContent = '';
        status.appendChild(state(error.kind === 'verification' ? 'verification' : 'failed', error.kind === 'verification' ? `Verification failed: ${error.file}` : 'Failed',
          `${error.reason || error.message}. Nothing from it is shown.`, {alert: true, retry: () => { status.textContent = ''; go(); }}));
        button.hidden = false;
      }
    };
    button.addEventListener('click', go);
  };
  function renderData(out, s) {
    S.redraw.data = [];
    const range = `${s.first_day} to ${s.last_day}`;
    S.results.data = {first_day: s.first_day, last_day: s.last_day, hours: s.price.filter(v => v !== null).length};
    out.appendChild(h('p', {'data-series-range': range}, h('strong', {}, `The series runs from ${s.first_day} to ${s.last_day}`), ` (last date ${s.last_day}): ${S.results.data.hours.toLocaleString('en-US')} hourly prices, ${s.unit}.`));
    out.appendChild(h('dl', {class: 'kv'}, h('dt', {}, 'Quarter-hour averaging'), h('dd', {}, shared('limitation_mtu_averaging')),
                                        h('dt', {}, 'The price floor'), h('dd', {}, L('live_data_floor'))));
    const floorMatch = /([−-]\d+(?:\.\d+)?) EUR\/MWh/.exec(L('live_data_floor'));
    const floor = floorMatch ? -Math.abs(Number(floorMatch[1].replace('−', ''))) : null;
    const vals = s.price.filter(v => v !== null && isFinite(v));
    let lo = Math.min(...vals), hi = Math.max(...vals);
    if (floor !== null) lo = Math.min(lo, floor);
    const raw = (hi - lo) / 45, p10 = Math.pow(10, Math.floor(Math.log10(raw))), m = raw / p10;
    const step = (m <= 1 ? 1 : m <= 2 ? 2 : m <= 5 ? 5 : 10) * p10;
    const start = Math.floor(lo / step) * step;
    const nb = Math.ceil((hi - start) / step) + 1;
    const counts = new Array(nb).fill(0);
    for (const v of vals) counts[Math.min(nb - 1, Math.floor((v - start) / step))] += 1;
    const negative = vals.filter(v => v < 0).length;
    const items = counts.map((c, i) => ({label: eur(start + i * step, 0), value: c, color: start + i * step < 0 ? Charts.colours.pending : Charts.colours.text}));
    const at = (v) => (v - start) / step;
    out.appendChild(h('div', {class: 'panel'},
      h('h3', {}, 'How are the hourly prices distributed?'),
      h('p', {class: 'subtitle'}, `Hours per ${eur(step, 0)} EUR/MWh bin, ${range} · negative-price bins are marked in a second colour and named below · `, num(negative, `${negative.toLocaleString('en-US')} negative hours`, {'data-negative': '1'})),
      chart('data', slot => Charts.bars(slot, items, {title: `Distribution of hourly prices, ${range}: hours per ${eur(step, 0)} EUR/MWh bin, with zero and the price floor marked as references`, unit: 'hours',
        xTitle: 'price, EUR/MWh (bin start)', refs: [{at: at(0), name: 'zero', label: '0 EUR/MWh', dy: 0}].concat(floor !== null ? [{at: at(floor), name: 'floor', label: `floor ${eur(floor, 0)}`, dy: 16}] : [])})),
      h('p', {class: 'qual'}, `Bins below zero hold the ${negative.toLocaleString('en-US')} negative hours; the dashed lines mark 0 EUR/MWh and the price floor (${L('live_data_floor')})`),
      details('Table: the distribution', table(`Hours per bin, ${range}`, [{t: 'Bin from, EUR/MWh', n: 1}, {t: 'Bin to, EUR/MWh', n: 1}, {t: 'Hours', n: 1}],
        counts.map((c, i) => h('tr', {}, td(eur(start + i * step, 0), true), td(eur(start + (i + 1) * step, 0), true), td(String(c), true)))))));
    // negative hours by quarter (Berlin delivery date)
    const quarters = new Map();
    const season = {winter: new Array(24).fill(0), spring: new Array(24).fill(0), summer: new Array(24).fill(0), autumn: new Array(24).fill(0)};
    const seasonN = {winter: new Array(24).fill(0), spring: new Array(24).fill(0), summer: new Array(24).fill(0), autumn: new Array(24).fill(0)};
    const SEASON = ['winter', 'winter', 'spring', 'spring', 'spring', 'summer', 'summer', 'summer', 'autumn', 'autumn', 'autumn', 'winter'];
    s.timestamp_utc.forEach((k, i) => {
      const v = s.price[i];
      if (v === null || !isFinite(v)) return;
      const b = berlin(k);
      const q = `${b.day.slice(0, 4)} Q${Math.floor((b.month - 1) / 3) + 1}`;
      if (!quarters.has(q)) quarters.set(q, [0, 0]);
      const e = quarters.get(q);
      e[1] += 1;
      if (v < 0) e[0] += 1;
      const sn = SEASON[b.month - 1];
      season[sn][b.hour] += v;
      seasonN[sn][b.hour] += 1;
    });
    const qs = [...quarters.entries()];
    out.appendChild(h('div', {class: 'panel'},
      h('h3', {}, 'How many hours had a negative price, quarter by quarter?'),
      h('p', {class: 'subtitle'}, `Hours with a price below 0 EUR/MWh per calendar quarter (Europe/Berlin delivery dates), ${range}`),
      chart('data', slot => Charts.bars(slot, qs.map(([q, e]) => ({label: q, value: e[0], text: String(e[0])})),
        {title: `Negative-price hours per quarter, ${range}`, unit: 'hours', valueLabels: true, horizontal: Charts.isMobile(Charts.widthOf(slot)) || qs.length > 40, digits: 0})),
      h('p', {class: 'qual'}, `${shared('limitation_mtu_averaging')}`),
      details('Table: negative hours by quarter', table(`Negative-price hours per quarter, ${range}`, ['Quarter', {t: 'Negative hours', n: 1}, {t: 'Hours', n: 1}],
        qs.map(([q, e]) => h('tr', {}, td(q), td(String(e[0]), true), td(String(e[1]), true)))))));
    const names = Object.keys(season);
    const profile = names.map(n => ({name: `${n} (mean)`, short: n, values: season[n].map((t, hh) => seasonN[n][hh] ? t / seasonN[n][hh] : NaN)}));
    const hours = Array.from({length: 24}, (_, i) => String(i).padStart(2, '0'));
    out.appendChild(h('div', {class: 'panel'},
      h('h3', {}, 'What does the average day look like in each season?'),
      h('p', {class: 'subtitle'}, `Mean price by delivery hour (Europe/Berlin), per meteorological season, ${range}, EUR/MWh`),
      chart('data', slot => Charts.lines(slot, {labels: hours, series: profile, unit: 'EUR/MWh', xTitle: 'delivery hour, Europe/Berlin',
        title: `Hourly profile by season, mean price by hour, ${range}, EUR/MWh`})),
      h('p', {class: 'qual'}, `Means over every year of the series pool very different price regimes; ${range}.`),
      details('Table: the hourly profile by season', table(`Mean price by hour and season, ${range}, EUR/MWh`, ['Hour', ...names.map(n => ({t: n, n: 1}))],
        hours.map((lab, hh) => h('tr', {}, td(lab), ...profile.map(p => td(eur(p.values[hh], 1), true))))))));
  }

  // ------------------------------------------------------------------ Limitations and History
  RENDER.limitations = (panel) => {
    viewHead(panel, 'Limitations', null);
    panel.appendChild(h('dl', {class: 'lim', 'data-limitations': '1'}, S.claims.limitations.map(item => [
      h('dt', {'data-key': item.key}, item.label), h('dd', {'data-key': item.key}, item.text)])));
  };
  RENDER.history = (panel) => {
    viewHead(panel, 'History', null);
    panel.appendChild(h('p', {'data-history-wording': '1'}, badge('Historical', true), ' ', L('live_history_wording')));
    panel.appendChild(h('p', {}, L('live_history_network')));
    const hist = S.build.history || {};
    if (hist.present) {
      panel.appendChild(h('p', {}, h('a', {class: 'route', href: 'history/index.html', 'data-history-link': '1'}, "Open v1's frozen demo (historical)")));
      if (hist.note) panel.appendChild(h('p', {class: 'secondary', 'data-history-note': '1'}, `Note: ${hist.note}.`));
    } else {
      panel.appendChild(state('unavailable', "v1's demo is not in this build", 'This local build has no /history/ route.', {route: true}));
    }
  };

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
