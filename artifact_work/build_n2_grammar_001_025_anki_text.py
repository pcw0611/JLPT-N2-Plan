from __future__ import annotations

import ast
import csv
import html
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifact_work" / "build_n2_grammar_001_025_anki.py"
OUTPUT_DIR = ROOT / "outputs" / "anki"
TSV_PATH = OUTPUT_DIR / "jlpt-n2-grammar-001-025-examples.tsv"
IMPORT_PATH = OUTPUT_DIR / "jlpt-n2-grammar-001-025-anki-import.txt"


def load_literal(name: str):
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == name for target in node.targets
        ):
            return ast.literal_eval(node.value)
    raise RuntimeError(f"{name} data was not found")


def esc(value: str) -> str:
    return html.escape(value, quote=False)


def front(number: str, pattern: str) -> str:
    return (
        f'<div style="color:#6b7280;font-size:14px">{esc(number)}</div>'
        f'<div style="font-size:30px;font-weight:700;margin:8px 0 14px">{esc(pattern)}</div>'
        '<div style="color:#6b7280">접속 · 핵심 의미 · 예문을 떠올려 보세요.</div>'
    )


def back(row: tuple[str, ...], gloss: str) -> str:
    number, pattern, connection, meaning, ex1, tr1, ex2, tr2, contrast, signal = row
    sections = [
        ("접속", connection),
        ("핵심 의미", meaning),
        ("예문 1", f"{ex1}<br><span style='color:#6b7280'>{tr1}</span>"),
        ("예문 2", f"{ex2}<br><span style='color:#6b7280'>{tr2}</span>"),
        ("구별 포인트", contrast),
        ("시험 신호", signal),
    ]
    body = [
        f'<div style="font-size:20px;font-weight:700;margin:0 0 14px;color:#52606d">{esc(gloss)}</div>'
    ]
    for label, value in sections:
        safe_value = value if "<br>" in value else esc(value)
        body.append(
            f'<div style="color:#52606d;font-size:13px;font-weight:700;margin-top:14px">{label}</div>'
            f'<div style="line-height:1.55;margin-top:4px">{safe_value}</div>'
        )
    return "".join(body)


def main() -> None:
    cards = load_literal("CARDS")
    glosses = load_literal("GLOSSES")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with TSV_PATH.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow([
            "ID", "문형", "짧은 뜻", "접속", "핵심 의미", "예문 1", "예문 1 해석",
            "예문 2", "예문 2 해석", "구별 포인트", "시험 신호", "Tags",
        ])
        for row in cards:
            number = row[0]
            priority = "priority_high" if number in {
                "009", "010", "011", "012", "013", "014", "015", "016", "017", "019", "022"
            } else "priority_normal"
            tags = f"JLPT_N2 문법_001_025 문법_{number} {priority}"
            writer.writerow([row[0], row[1], glosses[number], *row[2:], tags])

    with IMPORT_PATH.open("w", encoding="utf-8", newline="") as handle:
        handle.write("#separator:Tab\n")
        handle.write("#html:true\n")
        handle.write("#deck:JLPT N2::문법 001-025 예문 복습\n")
        handle.write("#tags column:3\n")
        handle.write("#columns:Front\tBack\tTags\n")
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        for row in cards:
            number, pattern = row[0], row[1]
            priority = "priority_high" if number in {
                "009", "010", "011", "012", "013", "014", "015", "016", "017", "019", "022"
            } else "priority_normal"
            tags = f"JLPT_N2 문법_001_025 문법_{number} {priority}"
            writer.writerow([front(number, pattern), back(row, glosses[number]), tags])

    print(f"Created {IMPORT_PATH}")
    print(f"Created {TSV_PATH}")
    print(f"Notes: {len(cards)}")


if __name__ == "__main__":
    main()
