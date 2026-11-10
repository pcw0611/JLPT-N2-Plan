"""Read-only structural preflight. Passing does NOT certify source or answer quality.

Usage: python scripts/audit_exam_data.py database/past_exams/2021_12.json
Exit 1 means the data must not be presented as a ready exam.
"""
import argparse
from collections import defaultdict
from html import unescape
import json
from pathlib import Path
import re
import unicodedata


def plain(value):
    text = re.sub(r"<rt\b[^>]*>.*?</rt>", "", str(value), flags=re.S)
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", unescape(text)))


def audit(data):
    errors = []
    questions = data.get("questions", data.get("sampleQuestions", []))
    if not isinstance(questions, list):
        return {"ready": False, "errors": ["Question collection must be an array"]}
    if "sampleQuestions" in data and "questions" not in data:
        errors.append("Only sampleQuestions exist; this is not a complete exam")
    expected = data.get("totalItems", len(questions))
    if expected != len(questions):
        errors.append(f"Declared count {expected} differs from actual count {len(questions)}")
    if not questions:
        errors.append("No questions")
    ids, prompts = defaultdict(list), defaultdict(list)
    for pos, q in enumerate(questions, 1):
        prefix = f"Q{q.get('id', pos)}"
        ids[str(q.get("id"))].append(pos)
        choices = q.get("choices", [])
        if not isinstance(choices, list):
            errors.append(f"{prefix}: choices must be an array")
            choices = []
        if len(choices) not in (3, 4):
            errors.append(f"{prefix}: expected 3 or 4 choices, got {len(choices)}")
        seen = defaultdict(list)
        for i, choice in enumerate(choices, 1):
            normalized = plain(choice)
            seen[normalized].append(i)
            if not normalized:
                errors.append(f"{prefix}: empty choice {i}")
        for value, positions in seen.items():
            if len(positions) > 1:
                errors.append(f"{prefix}: duplicate choices {positions}: {value}")
        answer = q.get("answer")
        if type(answer) is not int or not 0 <= answer < len(choices):
            errors.append(f"{prefix}: answer is not a valid zero-based choice index")
        for field in ("instruction", "prompt", "section"):
            if not q.get(field):
                errors.append(f"{prefix}: missing {field}")
        prompt = plain(q.get("prompt", ""))
        if prompt:
            prompts[prompt].append(q.get("id", pos))
        display = [q.get("instruction", ""), q.get("prompt", ""), q.get("passage", ""), *choices]
        # audio is spoken before submission too; inspect legacy TTS arrays.
        display.extend(a.get("text", "") for a in q.get("audio", []) if isinstance(a, dict))
        if re.search("[가-힣]", " ".join(map(str, display))):
            errors.append(f"{prefix}: Korean in pre-submission text or TTS")
        if re.search(r"こうほ\d|実践例文|実戦活用例文", json.dumps(q, ensure_ascii=False)):
            errors.append(f"{prefix}: placeholder content")
        if not q.get("sourcePages"):
            errors.append(f"{prefix}: no source page mapping")
        if q.get("order") is not None:
            order, slot = q["order"], q.get("starSlot", 3)
            if sorted(order) != [1, 2, 3, 4] or type(slot) is not int or not 1 <= slot <= 4:
                errors.append(f"{prefix}: invalid sentence order or star position")
            elif order[slot - 1] - 1 != answer:
                errors.append(f"{prefix}: star answer does not match completed order")
        if q.get("section") == "listening" and not q.get("transcript"):
            errors.append(f"{prefix}: no transcript for post-submission verification")
    for value, positions in ids.items():
        if value == "None" or len(positions) > 1:
            errors.append(f"Missing/duplicate ID {value}: rows {positions}")
    for value, question_ids in prompts.items():
        if len(question_ids) > 1:
            errors.append(f"Repeated prompt in questions {question_ids}: {value}")
    return {
        "ready": False,  # Human/source/audio review cannot be replaced by this script.
        "structuralCheckPassed": not errors,
        "declaredQuestions": expected,
        "actualQuestions": len(questions),
        "errors": errors,
        "requiredManualChecks": [
            "Source pages, figures, layout and answer key correspondence",
            "Solve every question; reject every distractor; check unique answers",
            "Complete recording and question-number correspondence",
            "Browser flow, grading/export consistency and no test learning writes",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    result = audit(json.loads(args.source.read_text(encoding="utf-8")))
    result["source"] = args.source.as_posix()
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.report:
        args.report.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    raise SystemExit(0 if result.get("structuralCheckPassed") else 1)


if __name__ == "__main__":
    main()
