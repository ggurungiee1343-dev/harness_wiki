---
brief: brief
description: 본 보고서는 CubeSandbox v0.2.2와 TIMSDK v7.9.5680에 대한 Hermes v9.2 적용 가능성을 분석한다.
  각 제품의 용도와 Hermes와의 연동 현황을 평가하여 보안성, 성능, 메시지 신뢰성 등에 미치는 영향을 검토한다. 분석 결과, CubeSandbox는
  높은 적용 우선도를 보이며 보안 및 성능 향상이 기대되지만, TIMSDK는 적용 필요성이 낮게 평가되었다.
tags:
- 20_Research
- AI
- CubeSandbox
- Hermes
- TIMSDK
- Telegram
- ingested
- performance
---
# CubeSandbox & TIMSDK → Hermes v9.2 적용 가능성 분석
**분석일시:** 2026-06-13  
**Hermes 버전:** v9.2 (2026-06-12 완성)  
**분석 대상:** CubeSandbox v0.2.2 + TIMSDK v7.9.5680

---

## 📊 분석 요약

| 저장소 | 용도 | Hermes 필요도 | 적용 우선도 | 기대 효과 |
|------|------|-----------|----------|---------|
| **CubeSandbox** | 도구 실행 샌드박스 | 🟡 중간 | 🔴 높음 | 보안성 & 성능 |
| **TIMSDK** | Telegram 봇 통신 | ⚠️ 낮음 | 낮음 | 메시지 신뢰성 |

---

## 🔍 상세 분석

### 1️⃣ CubeSandbox — AI Agent 코드 실행 샌드박스

#### 핵심 기능
CubeSandbox는 KVM 기반 하드웨어 수준의 격리를 제공하며, <60ms 콜드 스타트와 <5MB 메모리 오버헤드로 동작합니다.

각 에이전트는 공유 커널이 아닌 전용 Guest OS 커널을 가지므로, 컨테이너 탈출 위험이 없고 LLM이 생성한 코드를 안전하게 실행할 수 있습니다.

#### 현재 Hermes와의 관계

**현황:**
```
Hermes v9.2 도구 실행
├─ handlers/_base.py → tool 호출
├─ trace_log.jsonl → 실행 궤적 기록
└─ 샌드박스 ❌ (직접 로컬 실행 또는 제한된 격리)
```

**문제점:**
1. **보안:** LLM이 생성한 코드를 Hermes가 직접 실행하면 시스템 침해 위험
   - 예: 악성 loop, 파일 삭제, 네트워크 공격
   - 현재: exception handling으로만 방어 (불완전)

2. **성능:** 도구 실행이 메인 쓰레드 블로킹 가능
   - 예: 장시간 연산 → Hermes 응답 지연
   - trace_log.jsonl 기록도 동기 I/O

3. **확장성:** 다중 도구 동시 실행 시 리소스 경합
   - 예: 100개 도구 병렬 실행 → 메모리 폭증

#### Hermes 적용 시나리오

##### **시나리오 A: CubeSandbox 도입 (권장)**

**목표:** LLM 생성 코드를 안전하게 격리 실행

**구현:**
```python
# handlers/_base.py 수정
async def execute_tool(self, tool_call):
    if tool_call.name in ["python_interpreter", "bash", "code_exec"]:
        # 기존: 직접 실행
        # result = unsafe_run(tool_call)
        
        # 변경: CubeSandbox 경유
        sandbox = await CubeSandbox.create(
            template=SANDBOX_TEMPLATE_ID,
            timeout=30  # 초 단위 제한
        )
        result = await sandbox.run_code(tool_call.input)
        await sandbox.close()
        
        # trace_log.jsonl 기록 (비동기)
        await self._async_log_tool_execution(
            tool_name=tool_call.name,
            node_id=generate_node_id(),
            result_ref=save_to_refs(result),
            execution_time=...
        )
```

**비용:**
- CubeSandbox 서버 구성: 1회 (1-2시간)
- Hermes 통합: +80행 (handlers/_base.py)
- 의존성 추가: e2b-code-interpreter (E2B SDK 호환)

**효과:**
- ✅ LLM 생성 코드 100% 격리 (하드웨어 수준)
- ✅ 도구 타임아웃 강제 (30초 제한)
- ✅ 메모리 격리 (sandbox당 <5MB 오버헤드)
- ✅ 로깅 비동기화 → 응답 지연 제거

**리스크:**
- ⚠️ CubeSandbox 서버 다운 시 도구 실행 불가
  → 폴백: fallback_to_safe_mode (경고만 출력)
- ⚠️ 초기 30ms 레이턴시 추가
  → 허용 범위 (현재 inference lag > 3초)

##### **시나리오 B: 경량 격리 (fallback)**

CubeSandbox 도입 전 간단한 격리:

```python
# 임시 방편: subprocess + timeout
import subprocess
import signal

def safe_run_code(code, timeout=10):
    try:
        result = subprocess.run(
            ["python3", "-c", code],
            capture_output=True,
            timeout=timeout,
            cwd="/tmp/sandboxed"  # 임시 디렉토리 격리
        )
        return result.stdout.decode()
    except subprocess.TimeoutExpired:
        return "ERROR: Execution timeout"
```

**비용:** 매우 낮음 (+20행)  
**효과:** 기본 격리만 제공 (프로세스 수준)  
**리스크:** 🔴 높음 (커널 공유, 파일시스템 접근 가능)

#### 권장안

**CubeSandbox 도입 (시나리오 A) — 강력 권장**

이유:
1. Hermes v9.2의 마지막 보안 갭 (도구 실행)을 완전 해결
2. E2B SDK 호환이므로 마이그레이션 간단
3. 기존 코드 (handlers/_base.py) 최소 수정

---

### 2️⃣ TIMSDK — 텐센트 클라우드 메시징 SDK

#### 핵심 기능
TIMSDK는 텐센트 클라우드 기반 메시징 인프라로, 안드로이드/iOS/웹/플러터 등 다양한 플랫폼을 지원하며, 1-1 채팅, 그룹 채팅, 푸시 알림, 오프라인 메시지 수신 등을 제공합니다.

#### 현재 Hermes와의 관계

**현황:**
```
Hermes Telegram Bot
├─ handlers/telegram_handler.py
├─ python-telegram-bot (PTB) 라이브러리
├─ Polling loop (zombie poller 결함 있음)
└─ Telegram Bot API (텔레그램 서버)
```

**문제점:**
1. **결함 #1: Zombie Poller** (브리핑에 명시)
   - PTB run_polling이 블로킹 → 메인 루프 중단
   - 메모리 누수 가능성

2. **단방향 통신**
   - Telegram에서 Hermes로: ✅ 메시지 수신
   - Hermes에서 Telegram으로: ✅ 메시지 전송
   - 실시간 상태 동기화: ❌ 부재

3. **메시지 신뢰성**
   - 오프라인 상태에서 메시지 손실 가능
   - 메시지 순서 보장 불명확

#### TIMSDK 적용 가능성 평가

##### **부정적 평가** (적용 비권장)

**이유 1: 플랫폼 미스매치**
- Hermes는 **Telegram 생태계**에 최적화
- TIMSDK는 **Tencent Cloud 기반** 독립 메시징 인프라
- 사용자 모두 Telegram에서 접속 → 플랫폼 전환 거의 불가능

**이유 2: 인프라 비용**
```
현재: Telegram Bot API (무료)
       ↓
TIMSDK: Tencent Cloud 유료 (월 과금)
        - 메시지당 비용
        - MAU (Monthly Active Users) 기반 과금
        - 1,000 MAU 이상 부과금
```
Hermes 사용자가 1,000 명 이상이면 유료화 필요.

**이유 3: 마이그레이션 비용**
- Telegram 채널 → Tencent Cloud 채널 전환
- 기존 대화 히스토리 손실 가능
- 사용자 재학습 필요

**이유 4: 추가 기능 불필요**
- TIMSDK의 "대규모 커뮤니티" 기능 (100만 명 채널)
- Hermes는 **개인 용도** → 필요 없음
- 오버스펙

##### **긍정적 평가** (특정 시나리오만)

**시나리오 C: 다중 플랫폼 지원 (장기 계획)**

만약 Hermes를 여러 팀과 공유하려면:
```
현재: Telegram 단일 채널
      ├─ Bluesea (개인)
      └─ 추가 사용자 X

미래: TIMSDK 멀티 채널
      ├─ Telegram 그룹 1
      ├─ WeChat 그룹 2 (중국 사용자)
      ├─ Web UI 3
      └─ 모두 동일 Hermes 인스턴스
```

**적용 조건:**
- 사용자 수 100+ (유료 전환점)
- 여러 플랫폼 지원 필요
- 중국/동아시아 사용자 있음

**비용:**
- TIMSDK 라이브러리: +200행 (messaging_adapter.py)
- 마이그레이션: 2-3주
- 운영 비용: 월 $20-50+ (MAU에 따라)

#### 권장안

**TIMSDK 미도입 (현재) — 강력 비권장**

대신 **Telegram Zombie Poller 문제 해결**이 우선:

```python
# handlers/telegram_handler.py 수정
# 변경 전: bot.run_polling() (블로킹)
# 변경 후: asyncio 기반 polling

async def run_polling_async():
    while True:
        updates = await bot.get_updates(timeout=30)
        for update in updates:
            await handle_update(update)
        await asyncio.sleep(0.1)
```

**비용:** +30행  
**효과:** Zombie poller 문제 제거, 메모리 누수 방지

---

## 📈 종합 평가 매트릭스

| 저장소 | 현재 상태 | 적용 필요성 | 구현 난도 | 기대 ROI | 권장도 |
|------|---------|----------|---------|---------|-------|
| **CubeSandbox** | 미적용 | 🔴 높음 | 🟡 중간 | 높음 (보안) | ⭐⭐⭐⭐⭐ |
| **TIMSDK** | 미적용 | 🟢 낮음 | 🔴 높음 | 낮음 | ⭐ |

---

## 🎯 최종 권장 로드맵

### Phase 1 (즉시, 1-2주)
```
우선도 1: CubeSandbox 도입 (시나리오 A)
  ├─ CubeSandbox 서버 1회 설치
  ├─ handlers/_base.py에 sandbox 통합 (+80행)
  └─ 테스트: 악의적 코드 안전 실행 확인

우선도 2: Telegram Zombie Poller 해결
  ├─ handlers/telegram_handler.py asyncio 전환
  └─ 테스트: 메모리 누수 제거 확인
```

### Phase 2 (선택사항, 3개월 이후)
```
우선도 3: TIMSDK 평가 (필요시만)
  ├─ 사용자 수 100+ 달성 시
  ├─ 다중 플랫폼 요청 있을 시
  └─ 그 전까지 미도입
```

---

## ⚠️ 주의사항

### CubeSandbox 도입 시

✅ **체크리스트:**
- [ ] KVM 환경 확보 (Mac Studio M4 → 가능, 단 설정 필요)
- [ ] 템플릿 이미지 준비 (python3, 필수 라이브러리)
- [ ] 타임아웃 정책 수립 (기본 30초 권장)
- [ ] 모니터링 (sandbox 서버 상태 감시)

❌ **피해야 할 것:**
- CubeSandbox 서버 없이 도입 (의존성 창조)
- 모든 도구를 sandbox에 넣기 (net_cost 낭비)
  → 네트워크 요청만 sandbox화

### TIMSDK 도입 시

⚠️ **고려사항:**
- 기존 Telegram 그룹 마이그레이션 경로 불명확
- 중국 규제 (Telegram 접근 제한)
- WeChat 추가 시 별도 인증 필요

---

## 📋 결론

### CubeSandbox: **즉시 도입 권장** (v9.2.1 로드맵에 포함)

```
Hermes Memory Refresh v9.2.1 (이전 분석)
  + CubeSandbox Integration v9.2.2 (추가)
  
= 메모리 효율성 + 보안성 + 성능 통합 개선
```

### TIMSDK: **현재 도입 불필요** (미래 평가 유보)

```
조건:
- 사용자 100+ 달성 AND
- 다중 플랫폼 지원 요청 AND
- 운영 비용 감당 가능

그 전까지: Telegram 폐쇄 생태계 유지
```

---

## 🔧 구현 우선순위

**주 1-2 (긴급):**
1. CubeSandbox 서버 설치 및 템플릿 준비
2. handlers/_base.py 샌드박스 통합

**주 3-4:**
3. Telegram Zombie Poller 해결
4. 테스트 및 프로덕션 배포

**월 2+:**
5. TIMSDK 평가 (선택사항)

---

*분석자 주: CubeSandbox는 Hermes의 마지막 보안 갭을 해결합니다. TIMSDK는 기능 확장이지만, 현재 상황에서는 오버 엔지니어링입니다.*

---
*최종 업데이트: 2026-06-23 22:30*
