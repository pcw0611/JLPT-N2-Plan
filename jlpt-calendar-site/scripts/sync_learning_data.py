import json
import os
import sqlite3
import argparse
from report_builder import make_report
import urllib.request
from urllib.parse import urlsplit
from pathlib import Path
import socket
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Force IPv4 socket resolution to prevent hanging on broken IPv6 networks
_orig_getaddrinfo = socket.getaddrinfo
def _getaddrinfo_ipv4(host, port, family=0, type=0, proto=0, flags=0):
    return _orig_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
socket.getaddrinfo = _getaddrinfo_ipv4

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT.parent / "database" / "jlpt_learning.db"
SYNC_ENDPOINTS = {
    "cloudflare": "https://jlpt-study-calendar.pcw0611.workers.dev/api/sync",
    "legacy": "https://jlpt-study-calendar.pcwww.chatgpt.site/api/sync",
}

def sync_endpoints(target, override=None):
    if override:
        return [("custom", override)]
    return list(SYNC_ENDPOINTS.items()) if target == "both" else [(target, SYNC_ENDPOINTS[target])]

def sync_report(report, endpoint, secret):
    url = urlsplit(endpoint)
    request = urllib.request.Request(endpoint, data=json.dumps(report, ensure_ascii=False).encode("utf-8"), headers={
        "Authorization": f"Bearer {secret}", "Content-Type": "application/json",
        "Origin": f"{url.scheme}://{url.netloc}",
        "User-Agent": "Mozilla/5.0 JLPT-Study-Sync/1.0",
    }, method="POST")
    with urllib.request.urlopen(request, timeout=90) as response:
        result = json.load(response)
    if result.get('ok') is not True or result.get('date') != report['date']:
        raise RuntimeError('Site did not confirm synchronization for the requested date')
def scalar(conn, sql, params=()):
    row = conn.execute(sql, params).fetchone()
    return row[0] if row else None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('date', nargs='?')
    parser.add_argument('--all', action='store_true')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--target', choices=['cloudflare', 'legacy', 'both'], default='both')
    args = parser.parse_args()
    if args.date and args.all:
        parser.error('Use a date or --all, not both')
    db_path = Path(os.environ.get("JLPT_LOCAL_DB", DEFAULT_DB))
    with sqlite3.connect(f'{db_path.resolve().as_uri()}?mode=ro', uri=True) as conn:
        dates = [r[0] for r in conn.execute('SELECT session_date FROM study_sessions ORDER BY session_date')] if args.all else [args.date or scalar(conn, 'SELECT MAX(session_date) FROM study_sessions')]
        reports = [make_report(conn, date) for date in dates]
    if args.dry_run:
        print(json.dumps(reports, ensure_ascii=False, indent=2))
        return
    endpoints = sync_endpoints(args.target, os.environ.get("JLPT_SYNC_URL"))
    secret = os.environ.get("JLPT_SYNC_SECRET")
    if not secret:
        secret_path = ROOT / ".sync-secret"
        secret = secret_path.read_text(encoding="utf-8").strip() if secret_path.exists() else None
    if not secret:
        raise SystemExit("JLPT_SYNC_SECRET is not configured")
    failures = []
    for target, endpoint in endpoints:
        for report in reports:
            try:
                sync_report(report, endpoint, secret)
                print(json.dumps({"ok": True, "target": target, "date": report['date'], "studyMinutes": report["studyMinutes"], "questions": report["tests"]["total"], "schemaVersion": 2}, ensure_ascii=False), flush=True)
            except Exception as error:
                failures.append(f"{target}: {report['date']} ({type(error).__name__})")
    if failures:
        raise SystemExit("Synchronization failed for " + "; ".join(failures))

if __name__ == "__main__":
    main()
