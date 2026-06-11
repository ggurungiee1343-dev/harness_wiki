#!/usr/bin/env python3
"""
PostToolUse Hook — Wiki 파일 수정 시 자동 git 스테이징
Write|Edit 툴 사용 후 호출. wiki 경로 파일만 스테이징.
"""
import sys, json, subprocess, os

data = json.load(sys.stdin) if not sys.stdin.isatty() else {}

fp = (data.get("tool_input") or {}).get("file_path", "")
wiki = os.path.expanduser("~/Applications/Mjobsidian/wiki")

if fp and os.path.abspath(fp).startswith(os.path.abspath(wiki)):
    try:
        subprocess.run(
            ["git", "-C", wiki, "add", fp],
            capture_output=True, timeout=5
        )
        fname = os.path.basename(fp)
        print(json.dumps({"systemMessage": f"📝 Wiki 자동 스테이징: {fname}"}))
    except Exception as e:
        print(json.dumps({"systemMessage": f"⚠️ Wiki 스테이징 실패: {e}"}))
else:
    print("{}")
