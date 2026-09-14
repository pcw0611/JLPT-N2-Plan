#!/usr/bin/env python3
"""
JLPT N2 Plan - 원클릭 동기화 스크립트 (Windows & macOS 지원)
사용법:
    python sync.py          # 최신 내용 당겨오기(Pull) + 로컬 변경점 올리기(Push) + 캘린더 웹 동기화
    python sync.py pull     # 원격 변경점만 당겨오기
    python sync.py push     # 로컬 변경점만 원격에 올리기
"""

import sys
import subprocess
import platform
import socket
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent

def run_cmd(cmd, check=True):
    result = subprocess.run(
        cmd,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        shell=True,
        encoding="utf-8",
        errors="replace"
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"명령 실패: {cmd}\n[에러 출력]: {result.stderr.strip() or result.stdout.strip()}")
    return result

def has_uncommitted_changes():
    res = run_cmd("git status --porcelain", check=False)
    return bool(res.stdout.strip())

def is_ahead_of_remote():
    res = run_cmd("git status -sb", check=False)
    return "ahead" in res.stdout

def commit_local():
    if not has_uncommitted_changes():
        return True
    print("[로컬] 변경된 파일들을 커밋합니다...")
    run_cmd("git add .")
    hostname = socket.gethostname()
    os_name = "macOS" if platform.system() == "Darwin" else "Windows"
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"동기화: {now_str} ({os_name} / {hostname})"
    res = run_cmd(f'git commit -m "{commit_msg}"', check=False)
    if res.returncode == 0:
        print(f"  -> 커밋 완료: {commit_msg}")
        return True
    else:
        print(f"  [에러] 커밋 실패:\n{res.stderr or res.stdout}")
        return False

def sync_pull():
    print("[1/3] 원격 저장소(GitHub)로부터 최신 변경사항 확인 중...")
    run_cmd("git fetch origin main")
    pull_res = run_cmd("git pull --rebase origin main", check=False)
    if pull_res.returncode == 0:
        print("  -> 원격 최신 기록을 성공적으로 가져왔습니다.")
        return True
    else:
        print(f"  [주의] Rebase 실패 (충돌 가능성):\n{pull_res.stderr or pull_res.stdout}")
        return False

def sync_push():
    print("[2/3] GitHub 원격 저장소 푸시 확인 중...")
    if not is_ahead_of_remote():
        print("  -> 원격에 올릴 새 커밋이 없습니다. (이미 최신 상태)")
        return True

    push_res = run_cmd("git push origin main", check=False)
    if push_res.returncode == 0:
        print("  -> GitHub 푸시 성공 (https://github.com/pcw0611/JLPT-N2-Plan)")
        return True
    else:
        print(f"  [에러] GitHub 푸시 실패:\n{push_res.stderr or push_res.stdout}")
        return False

def sync_calendar():
    print("[3/3] 웹 캘린더 사이트 동기화 확인 중...")
    secret_file = ROOT / "jlpt-calendar-site" / ".sync-secret"
    sync_script = ROOT / "jlpt-calendar-site" / "scripts" / "sync_learning_data.py"
    
    if not secret_file.exists():
        print("  [알림] 'jlpt-calendar-site/.sync-secret' 파일이 없어 웹 캘린더 동기화는 건너뜁니다.")
        print("        (동기화가 필요하시면 Windows PC의 해당 파일을 복사해 넣어주세요.)")
        return

    if sync_script.exists():
        py_cmd = "python3" if platform.system() == "Darwin" else "python"
        res = run_cmd(f"{py_cmd} {sync_script}", check=False)
        if res.returncode == 0:
            print("  -> 캘린더 사이트(Cloudflare & Legacy) 동기화 완료!")
        else:
            print(f"  [주의] 캘린더 사이트 동기화 중 에러 발생:\n{res.stderr.strip() or res.stdout.strip()}")

def main():
    mode = sys.argv[1].lower() if len(sys.argv) > 1 else "all"
    print("=" * 60)
    print("   JLPT N2 Plan 프로젝트 원클릭 동기화 (GitHub & Web)")
    print("=" * 60)
    
    success = True
    if mode in ("all", "push"):
        if not commit_local():
            success = False

    if mode in ("all", "pull") and success:
        if not sync_pull():
            success = False
            
    if mode in ("all", "push") and success:
        if not sync_push():
            success = False

    if mode in ("all", "calendar") and success:
        sync_calendar()

    print("-" * 60)
    if success:
        print("[완료] 프로젝트 및 데이터베이스 동기화가 완료되었습니다!")
        print("[안내] Anki 앱에서도 '동기화(단축키: y)' 버튼을 꼭 눌러주세요!")
    else:
        print("[주의] 일부 동기화 작업 중 확인이 필요한 항목이 있습니다.")
    print("=" * 60)

if __name__ == "__main__":
    main()
