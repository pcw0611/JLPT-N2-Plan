# -*- coding: utf-8 -*-
"""
Apply Kanji Mnemonics to Anki JLPT Vocabulary Decks.
Anki 로컬 MCP 서버(포트 3141)와 통신하여 JLPT 한끝 Voca 덱의 단어들에
부수 파자 연상 기억 힌트를 안전하게 주입합니다.
"""

import urllib.request
import json
import sys
import time
from pathlib import Path

# Fix Windows stdout encoding
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Import our mnemonic dictionary
sys.path.insert(0, str(Path(__file__).resolve().parent))
from kanji_mnemonic_data import generate_mnemonic_html, KANJI_MNEMONICS

ENDPOINT = "http://127.0.0.1:3141/"

def mcp_call(method: str, params: dict, req_id: int = 1) -> dict:
    data = json.dumps({"jsonrpc": "2.0", "id": req_id, "method": method, "params": params}, ensure_ascii=False).encode()
    req = urllib.request.Request(
        ENDPOINT,
        data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json, text/event-stream"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode("utf-8")
    for line in body.splitlines():
        if line.startswith("data: "):
            payload = json.loads(line[6:])
            if "error" in payload:
                raise RuntimeError(payload["error"])
            return payload.get("result", {})
    return {}

def call_tool(name: str, args: dict, req_id: int = 1) -> dict:
    res = mcp_call("tools/call", {"name": name, "arguments": args}, req_id)
    if "structuredContent" in res:
        return res["structuredContent"]
    if "content" in res:
        for c in res["content"]:
            if c.get("type") == "text":
                try:
                    return json.loads(c["text"])
                except:
                    return c["text"]
    return res

def fetch_all_note_ids(query: str, start_req_id: int = 10) -> (list, int):
    """Fetch all note IDs matching query using pagination (limit <= 500)."""
    all_ids = []
    offset = 0
    limit = 500
    req_id = start_req_id

    while True:
        res = call_tool("find_notes", {"query": query, "offset": offset, "limit": limit}, req_id)
        req_id += 1
        if isinstance(res, dict):
            ids = res.get("noteIds", [])
            all_ids.extend(ids)
            if not res.get("hasMore", False) or len(ids) == 0:
                break
            offset += len(ids)
        else:
            break

    return all_ids, req_id

def main():
    print("=== Anki 한자 연상 기억 힌트 적용 시작 ===")
    mcp_call("initialize", {"protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "apply_mnemonics", "version": "1.0"}}, 1)

    deck_queries = [
        ("JLPT 한끝 Voca 4-N2", 'deck:*4-N2*'),
        ("JLPT 한끝 Voca 3-N3", 'deck:*3-N3*'),
        ("JLPT 한끝 Voca 2-N4", 'deck:*2-N4*'),
        ("JLPT 한끝 Voca 1-N5", 'deck:*1-N5*')
    ]

    total_matched = 0
    total_updated = 0
    deck_stats = {}
    req_id = 10

    for deck_label, query in deck_queries:
        print(f"\nScanning {deck_label} ({query})...")
        note_ids, req_id = fetch_all_note_ids(query, req_id)
        print(f"  총 {len(note_ids)}개 노트 검색 완료.")

        if not note_ids:
            continue

        # Fetch notes info in batches of 100
        matched_notes = []
        batch_size = 100
        for i in range(0, len(note_ids), batch_size):
            chunk = note_ids[i:i + batch_size]
            info_res = call_tool("notes_info", {"notes": chunk}, req_id)
            req_id += 1

            notes_data = info_res.get("notes", []) if isinstance(info_res, dict) else []
            for n in notes_data:
                fields = n.get("fields", {})
                kanji_field = fields.get("kanji", {}).get("value", "")
                existing_mnemonic = fields.get("hanja_mnemonic", {}).get("value", "")

                html = generate_mnemonic_html(kanji_field)
                if html:
                    if html != existing_mnemonic:
                        matched_notes.append({
                            "id": n["noteId"],
                            "kanji": kanji_field,
                            "meaning": fields.get("meaning", {}).get("value", ""),
                            "html": html
                        })

        deck_stats[deck_label] = len(matched_notes)
        total_matched += len(matched_notes)
        print(f"  연상 힌트 대상 단어: {len(matched_notes)}개")

        # Update notes in batches of 50
        update_chunk_size = 50
        for i in range(0, len(matched_notes), update_chunk_size):
            chunk = matched_notes[i:i + update_chunk_size]
            update_payload = [
                {
                    "id": item["id"],
                    "fields": {
                        "hanja_mnemonic": item["html"]
                    }
                }
                for item in chunk
            ]
            call_tool("update_notes", {"notes": update_payload}, req_id)
            req_id += 1
            total_updated += len(chunk)
            time.sleep(0.05)

    print("\n==========================================")
    print("=== 적용 결과 요약 ===")
    print("==========================================")
    for deck, cnt in deck_stats.items():
        print(f" - {deck}: {cnt}개 단어에 한자 연상 기억 힌트 적용")
    print(f"\n총 업데이트 카드 수: {total_updated}장")

    # Sample verification on key notes
    print("\n--- 대표 단어 힌트 적용 검증 ---")
    verify_res = call_tool("find_notes", {"query": 'deck:*4-N2* 解決 OR 解散 OR 見解 OR 警察 OR 複雑', "limit": 10}, req_id)
    req_id += 1
    sample_ids = verify_res.get("noteIds", [])[:5] if isinstance(verify_res, dict) else []
    if sample_ids:
        sample_info = call_tool("notes_info", {"notes": sample_ids}, req_id)
        for sn in sample_info.get("notes", []):
            k = sn["fields"]["kanji"]["value"]
            m = sn["fields"]["meaning"]["value"]
            mn = sn["fields"]["hanja_mnemonic"]["value"]
            print(f"\n[단어: {k} ({m})]")
            print(mn)

if __name__ == "__main__":
    main()
