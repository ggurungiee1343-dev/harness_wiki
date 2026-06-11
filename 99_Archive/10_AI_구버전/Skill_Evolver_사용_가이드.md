# 🛠️ Skill Evolver 사용 가이드

`skill_evolver.py`는 헤르메스 봇이 `/exec` 명령어로 Bash를 실행하다가 **에러 복구에 성공**할 때마다 자동으로 해결 패턴을 `SKILL.md` 파일로 학습·저장하는 자기진화 모듈입니다.

---

## 🔄 전체 자동화 흐름

```
/exec [명령어]
      │
      ▼
executor.py 실행
      │
      ├─ ✅ 성공 → 결과 바로 반환
      │
      └─ ❌ 에러 발생
            │
            ▼
        hybrid_router(Gemma4)에게 대체 명령어 요청
            │
            ├─ 최대 3회 재시도
            │
            ├─ 🔁 복구 성공 → 결과 반환
            │       │
            │       ▼
            │   skill_evolver.record_exec_recovery()
            │       │
            │       ├─ ~/.hermes/skills/learned/에 SKILL.md 생성
            │       └─ Mjobsidian/wiki/10_AI_Automation/skills/에 동기화
            │
            └─ ❌ 3회 모두 실패 → 실패 메시지 반환
```

---

## 📂 파일 저장 위치

| 경로 | 내용 |
|------|------|
| `~/.hermes/skills/learned/<slug>/SKILL.md` | 학습된 에러 복구 패턴 |
| `Mjobsidian/wiki/10_AI_Automation/skills/` | 옵시디언 위키 동기화 사본 |
| `~/.hermes/session_events.jsonl` | 전체 이벤트 로그 (JSONL) |

---

## 📖 SKILL.md 예시

```markdown
# SKILL: permission_denied_chmod_a1b2c3d4

## 메타데이터
- **생성일**: 2026-05-20T07:30:00
- **트리거**: error_recovery
- **원본 명령어**: `rm /usr/local/bin/myfile`
- **실패 원인**: Permission denied
- **복구 명령어**: `sudo rm /usr/local/bin/myfile`
- **재시도 횟수**: 1회

## 문제 설명
에러: Permission denied (원본 명령: rm /usr/local/bin/myfile)

## 해결 방법
복구 명령어: sudo rm /usr/local/bin/myfile

## 재사용 가이드
1. 에러 키워드 매칭: `rm /usr/local/bin/myfile`
2. 복구 명령어 패턴 적용
3. 결과 검증 후 완료
```

---

## 💬 텔레그램에서 사용하기

```
/exec rm /usr/local/bin/myfile
```

에러 발생 시 자동으로 복구를 시도하며, 성공하면 다음과 같은 메시지를 받습니다:

> ✅ **에러 자율 복구 성공** (1회 수정)
> 🔧 복구 명령어: `sudo rm /usr/local/bin/myfile`
> STDOUT: (결과)
> 💡 SKILL.md가 학습 DB에 자동 저장되었습니다.

---

## 🔍 학습된 스킬 확인

텔레그램에서:
```
/exec ls ~/.hermes/skills/learned/
```

또는 옵시디언 위키에서 `10_AI_Automation/skills/` 폴더를 확인하세요.

---

## ⚙️ 직접 호출 (개발자용)

```python
from skill_evolver import record_exec_recovery

skill_path = record_exec_recovery(
    original_cmd="rm /protected/file",
    error_msg="Permission denied",
    fixed_cmd="sudo rm /protected/file",
    retries=1,
)
print(f"생성된 스킬: {skill_path}")
```

---
*최종 업데이트: 2026-05-20*
*작성자: Antigravity AI*
