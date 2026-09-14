# -*- coding: utf-8 -*-
import sys
import json
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ENDPOINT = "http://127.0.0.1:3141/"

def mcp(method, params, req_id):
    data = json.dumps({"jsonrpc": "2.0", "id": req_id, "method": method, "params": params}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(ENDPOINT, data=data, headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}, method="POST")
    with urllib.request.urlopen(req) as resp:
        body = resp.read().decode("utf-8")
    payload = json.loads(next(line[6:] for line in body.splitlines() if line.startswith("data: ")))
    return payload["result"]

def main():
    mcp("initialize", {"protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "verify-all", "version": "1.0"}}, 1)
    res = mcp("tools/call", {"name": "list_decks", "arguments": {}}, 2)
    decks_data = res.get("structuredContent") or json.loads(next(x["text"] for x in res["content"] if x["type"] == "text"))
    n2_decks = sorted([d for d in decks_data["decks"] if "JLPT N2::" in d["name"]], key=lambda x: x["name"])

    total_cards = 0
    print(f"=== JLPT N2 12개 전체 덱 현황 (총 {len(n2_decks)}개) ===")
    for idx, d in enumerate(n2_decks, 1):
        q_res = mcp("tools/call", {"name": "find_notes", "arguments": {"query": f'deck:"{d["name"]}"', "limit": 300}}, 10 + idx)
        found = q_res.get("structuredContent") or json.loads(next(x["text"] for x in q_res["content"] if x["type"] == "text"))
        cnt = found.get("count", 0)
        total_cards += cnt
        print(f"{idx:02d}. {d['name']} ➔ {cnt}장")

    print(f"\n[총합] JLPT N2 산하 전체 카드 수: {total_cards}장")

if __name__ == "__main__":
    main()
