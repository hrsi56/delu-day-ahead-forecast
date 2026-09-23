#!/bin/sh
# Samples every 20 s: UTC time, number of admission Python processes, summed %CPU and RSS (KiB).
OUT="$1"
while true; do
  ps -A -o pid=,pcpu=,rss=,command= | grep "weather-admission/venv/bin/python" | grep -v grep | \
    awk -v t="$(date -u +%Y-%m-%dT%H:%M:%SZ)" '{n++; c+=$2; r+=$3} END {printf "%s %d %.1f %d\n", t, n, c, r}' >> "$OUT"
  sleep 20
done
