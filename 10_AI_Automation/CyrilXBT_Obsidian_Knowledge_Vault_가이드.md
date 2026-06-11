# How to Build an Obsidian Knowledge Vault That Gets Smarter Every Day Without You Doing Anything

**작성자:** CyrilXBT (@cyrilXBT)
**게시일:** 2026년 5월 7일
**원문:** Twitter/X Thread
**태그:** #obsidian #knowledge-vault #automation #claude #second-brain

---

## 핵심 메시지

모든 기사, 트위터 저장, 음성 메모가 자동으로 유입된다. Claude가 연결고리를 발견한다. 당신은 인사이트만 수집한다.

대부분의 사람들은 Obsidian 볼트를 서랍처럼 사용한다. 넣기만 하고 빼지 않는다. 6개월 후, 완전히 잊어버린 정보의 아름답게 정리된 아카이브를 갖게 된다.

**이 가이드는 다르게 만든다. 당신이 추가하는 볼트가 아니라, 당신에게 추가하는 볼트.**

---

## 왜 대부분의 시스템이 실패하는가?

| 문제 | 이유 |
|------|------|
| **수집 마찰** | 10초 이상 걸리면 포기함 |
| **연결 부재** | 각 노트가 고립되어 있음 |
| **복귀 이유 없음** | 시스템이 인사이트를 건네주지 않음 |

**결론:** 정보가 들어갔지만 나오지 않으면, 이것은 지식 시스템이 아니라 묘지다.

---

## 4단계 아키텍처

```
Layer 1: 수집 (Capture)
  → Readwise (기사/하이라이트)
  → Airr (팟캐스트 클립)
  → Whisper (음성 노트)
  → Telegram Bot (빠른 저장)

Layer 2: 파이프라인 (N8N)
  → 각 소스에서 콘텐츠를 Obsidian으로 자동 라우팅

Layer 3: Obsidian 볼트
  → 마크다운 파일 저장소 (ground truth)

Layer 4: Claude
  → 연결 발견, 패턴 표면화, 일일 브리프 작성
```

---

## 5개 폴더 구조

```
Inbox    → 모든 것이 먼저 도착하는 곳
Notes    → 처리된 하이라이트, 기사
Ideas    → 나만의 생각
Projects → 진행 중인 작업
CLAUDE.md → Claude에게 주는 지시사항
```

**원칙:** 5개 폴더. 단순하게 유지. 어느 폴더에 넣을지 모르겠으면 inbox에 넣어라.

---

## Layer 1: 자동 수집 설정

### 기사/하이라이트
- **Readwise**가 중추
- 브라우저 확장 설치
- 하이라이트만 하면 자동 저장
- Kindle, Twitter, Instapaper, Pocket과 연동

### 팟캐스트/오디오
- **Airr**: 휴대전화 흔들어서 팟캐스트 클립
- **Whisper**: 음성 녹음 → 전사

### 빠른 캡처
- **Telegram Bot**으로 어디서든 저장
- 차 안에서, 대화 중, 문득 떠오른 아이디어
- 30분 만에 Claude Code + N8N으로 구축 가능

### N8N 워크플로우 — Telegram → Obsidian

```
Node 1: Telegram Trigger
Node 2: Code (format note)
        → filename: inbox/{{date}}-quick-capture.md
        → content: # Quick Capture / {{message}} / Source: Telegram / Date: {{date}}
Node 3: Write File to Obsidian vault
        → path: /your-vault/inbox/
```

---

## Layer 3: CLAUDE.md 파일

가장 중요한 파일. 없으면 Claude는 매 세션마다"context 없이" 시작한다.

**템플릿:**

```markdown
# Who I Am
Name: [이름]
Work: [직업]
Focus: [지금 무엇을 잘하고 싶은지]
Goals 2026: [3가지 구체적 결과]

# Current Projects
Active: [지금 무엇을 만들고 있는지]
Stuck on: [가장 많은 사고 도움이 필요한 곳]
Next milestone: [완료된 모습이 어떤지]

# How This Vault Works
Inbox: /inbox — 미처리 캡처
Notes: /notes — 처리된 기사, 하이라이트, 연구
Ideas: /ideas — 나만의 생각과 관찰
Projects: /projects — 진행 중인 작업 폴더

# What I Want From You
- 보지 못한 연결 고리를 찾아줘
- 동의하기 전에 내 가정을 도전시켜줘
- 어디에 집중할지 물으면vault 컨텍스트에서 답해줘
- 내가 earlier 저장한 것과 모순될 때 경고해줘
```

**주간 업데이트:** 매주 월요일 아침 5분. 이것이 Claude의 컨텍스트를 정확하게 유지하는 비결이다.

---

## Layer 4: 일일 브리프 (매일 아침 6시 자동 실행)

N8N Cronjob으로 자동화. 내가 요청하지 않아도 inbox에 도착.

**브리프 프롬프트:**

```
"You are reading my Obsidian knowledge vault.
Read everything in /inbox from the last 24 hours
and everything in /notes from the last 7 days.

Then do three things:

CONNECTIONS — 최근 캡처와 older notes 사이의
              3가지 흥미로운 연결을 찾아줘.
              구체적으로. 관련 구문을 인용해줘.

PATTERN — 이번 주 읽은 것 중 나타나는 패턴을 파악해줘.
           내 뇌가 명시적으로 말하지 않았더라도
           어떤 것에서 작동하고 있는지.

QUESTION — 패턴을 기반으로 오늘 앉아서 생각할
            한 가지 질문을 줘. 작업이 아니라 질문.

이것을 Obsidian용 마크다운 파일로 작성해.
/inbox/brief-{{date}}.md로 저장해줘."
```

**시간:** 평일 아침 6시

---

## 주간 종합 (매주 15분)

**프롬프트:**

```
"Read my entire Obsidian vault.
Focus on everything added in the last 7 days.

I want four things:

EMERGING THESIS — 명시하지 않았지만 형성 중인 아이디어.
                  어떤 입장이 내 사고에서 формируется.

CONTRADICTIONS — 최근 저장한 것과 모순되는 과거 믿음.
                 내 own 노트에서 양쪽을 보여줘.

KNOWLEDGE GAPS — 내가 읽고 있는 것과 생각하고 있는 것을 기반으로,
                 내가 분명히 읽지 않고 있을 것은?
                 어떤 관점이 빠져 있는지?

ONE ACTION — 이 볼트의 모든 것을 고려할 때,
             이번 주 내가 하거나 생각할 수 있는
             가장 영향력 있는 한 가지는?"
```

---

## 6개월 후의 효과

| 기간 | 효과 |
|------|------|
| **1개월** | 유용한 도구. 좋은 아이디어를 덜 잃음 |
| **3개월** | Claude가 1개월 전 노트를 현재问题和 연결 |
| **6개월** | 당신의信仰 변화 기록, 모든 가정과 변경사항 보유 |

> **"6개월 후의 AI는 시작한 때와 다르다. 당신의 삶을 살면서 당신의 마음을 읽고 있었다."**

---

## 6단계 시작 가이드

1. **Obsidian 설치** + 5개 폴더 생성
2. **Readwise Obsidian 연동** 설정
3. **N8N으로 Telegram 캡처 봇** 구축 (30분)
4. **CLAUDE.md 작성** (템플릿 사용)
5. **N8N으로 일일 브리프** 자동화 (매일 6시)
6. **매주 월요일 15분** 주간 종합 시간 확보

---

## 핵심 원칙

> **"5개 노트로 시작하라. 오늘 밤. Claude가 그 사이의 연결을 발견할 것이다. 언제나 그렇다."**

---

## 우리 시스템과의 비교

| CyrilXBT 시스템 | 우리 현재 시스템 |
|-----------------|-----------------|
| N8N (파이프라인) | Harness + Clipping 자동 분류 |
| Readwise (수집) | Reader (수동 처리 예정) |
| Telegram Bot (빠른 캡처) | Catcher (이미 구현) |
| CLAUDE.md | hot.md + MEMORY.md |
| 일일 브리프 (N8N Cron) | Dreaming (Harness Cronjob) |
| 주간 종합 | 미구현 (나중에 추가 예정) |

---

**원문 출처:** CyrilXBT (@cyrilXBT) - 2026년 5월 7일
**가져온 곳:** Clippings

---
*최종 업데이트: 2026-06-03 19:02 (일괄 타임스탬프 복구)*
