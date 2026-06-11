# 📋 MarineOS-XR 스크립트 완성 피드백 체크리스트

**사용처:** Claude이 당신의 완성된 스크립트들을 검토할 때 사용  
**제출 시점:** 모든 스크립트 완성 후  
**피드백 대상:** 총 10개 스크립트

---

## 🔍 각 스크립트별 확인 항목

### **1️⃣ ais_simulator.py** (Week 1-2)

#### 기본 기능
- [ ] VirtualShip 클래스가 MMSI, 이름, 길이, 폭, 흘수를 저장하는가?
- [ ] update_position() 메서드가 SOG/COG에 기반해 위치를 업데이트하는가?
- [ ] build_type_1_payload() & build_type_5_payload()가 NMEA 형식을 정확히 생성하는가?
- [ ] 체크섬 계산이 정확한가?

#### 네트워크 기능
- [ ] AISSignalInjector가 UDP 5631로 데이터를 전송하는가?
- [ ] 동시에 여러 선박을 생성할 수 있는가?
- [ ] 실시간 제어 콘솔이 작동하는가?
- [ ] Ctrl+C로 안전하게 종료되는가?

#### 에러 처리
- [ ] 잘못된 입력값 처리가 있는가?
- [ ] 네트워크 오류 시 재시도 로직이 있는가?
- [ ] 로깅이 충분한가?

#### 통합성
- [ ] ais_nmea_parser.py와 호환되는가? (같은 NMEA 형식)
- [ ] JSON 출력 옵션이 있는가?
- [ ] 웹 대시보드와 연동 가능한가?

**제출 명령어:**
```bash
# 테스트
python3 ais_simulator.py

# 실제 사용
python3 ais_simulator.py --ships 10 --duration 300
```

---

### **2️⃣ web_dashboard.py** (Week 1-2)

#### 기본 기능
- [ ] Flask 서버가 localhost:5000에서 실행되는가?
- [ ] ais_simulator.py의 UDP 신호를 수신하는가?
- [ ] WebSocket으로 실시간 업데이트가 가능한가?
- [ ] 브라우저에서 선박 위치를 시각화하는가?

#### UI/UX
- [ ] 극좌표 레이더 표시가 있는가?
- [ ] 거리/방위각 실시간 표시가 있는가?
- [ ] 야간 모드 토글이 있는가?
- [ ] 선박 정보(MMSI, 이름, SOG, 흘수)가 표시되는가?

#### 성능
- [ ] 10척 동시 렌더링 시 FPS가 60 이상인가?
- [ ] 웹소켓 지연이 <100ms인가?
- [ ] 메모리 누수가 없는가?

#### 호환성
- [ ] 크롬/Safari/Firefox 모두 작동하는가?
- [ ] iPhone/iPad 모바일에서도 보이는가?
- [ ] Three.js 최신 버전과 호환되는가?

**제출 명령어:**
```bash
# 웹 서버 + AIS 시뮬레이터 동시 실행
python3 ais_simulator.py &
python3 web_dashboard.py

# 브라우저: http://localhost:5000
```

---

### **3️⃣ ship_mesh_generator_unity.cs** (Week 3-4) ⭐ 신규

#### 기본 기능 (C# Unity)
- [ ] ShipMesh 클래스가 Mesh 컴포넌트를 생성하는가?
- [ ] LOD 시스템이 작동하는가?
- [ ] 선박 유형별 메쉬 형태가 다른가?

#### 성능
- [ ] 메쉬 생성 시간이 <10ms인가?
- [ ] GPU Instancing이 활성화되어 있는가?
- [ ] 100척 동시 렌더링 시 60 FPS 유지되는가?

#### 렌더링
- [ ] 색상이 선박 유형별로 다른가?
- [ ] 법선 벡터가 제대로 계산되는가?
- [ ] 그림자가 정상적으로 렌더링되는가?

**제출 형식:** Unity 프로젝트 폴더

---

### **4️⃣ kalman_filter_realtime.py** (Week 3-4)

#### 기본 기능
- [ ] 칼만 필터 상태 업데이트가 정상인가?
- [ ] 예측 step이 정확한가?
- [ ] 신뢰도 계산이 올바른가?

#### 정확도
- [ ] 예측 오차가 <200m인가?
- [ ] AIS 신호 두절 후 5초 예측이 가능한가?
- [ ] 다중 선박 동시 추적이 가능한가?

#### 성능
- [ ] 100척 동시 추적 시 <50ms인가?
- [ ] 메모리 누수가 없는가?

**제출 명령어:**
```bash
python3 kalman_filter_realtime.py --ships 100
```

---

### **5️⃣ smcp_voice_parser.py** (Week 5+)

#### 기능
- [ ] Whisper-Base가 정상 작동하는가?
- [ ] SMCP 명령어 인식률이 90% 이상인가?
- [ ] 한국어 + 영어 혼합 인식이 가능한가?

#### 명령어 맵핑
- [ ] "Full ahead" → RPM 100%
- [ ] "Right rudder 15" → δ = +15°
- [ ] "Stop" → RPM 0
- [ ] "Hard port" → δ = -35°

**체크할 명령어 목록:**
- Full/Half/Slow ahead
- Astern full
- Right/Left rudder 10/20/30/35
- Hard-a-port/starboard
- Midships
- Stop

---

### **6️⃣ unity_xr_renderer.cs** (Week 5+) ⭐ 신규

#### XR 기능 (Meta Quest 3)
- [ ] WebSocket으로 AIS 데이터를 수신하는가?
- [ ] 실시간 선박 위치가 XR 공간에 표시되는가?
- [ ] 손동작 제어가 작동하는가?
- [ ] Eye tracking 포커스가 작동하는가?

#### 성능
- [ ] 50척 렌더링 시 72 FPS (Quest 3 표준)가 유지되는가?
- [ ] 지연 <20ms가 유지되는가?
- [ ] 배터리 소모가 시간당 10% 이하인가?

#### UI
- [ ] 극좌표 레이더가 표시되는가?
- [ ] 거리/방위각 숫자가 보이는가?
- [ ] 선박 이름이 표시되는가?
- [ ] 야간 모드가 자동 전환되는가?

**제출 형식:** Unity XR 프로젝트

---

### **7️⃣ omniverse_usd_exporter.py** (Week 8+)

#### 기능
- [ ] AIS JSON → USD 형식 변환이 정상인가?
- [ ] NVIDIA Omniverse에서 열리는가?
- [ ] 메쉬 지오메트리가 정확한가?
- [ ] 메타데이터(MMSI, 선박명)가 포함되는가?

**제출 명령어:**
```bash
python3 omniverse_usd_exporter.py --input ships.json --output ulsan_port.usd
```

---

### **8️⃣ performance_benchmark.py** (Week 10+)

#### 벤치마크 항목
- [ ] AIS 파싱 성능: >1000 msg/sec?
- [ ] 좌표 변환: <5ms/100척?
- [ ] 메쉬 생성: <10ms/척?
- [ ] 렌더링: 72 FPS 유지?

#### 출력 형식
- [ ] CSV 보고서 생성 가능한가?
- [ ] 그래프 생성이 자동인가?
- [ ] 성능 추이 비교가 가능한가?

---

### **9️⃣ test_integration.py** (전체)

#### 통합 테스트
- [ ] ais_simulator → web_dashboard 연동
- [ ] web_dashboard → kalman_filter 연동
- [ ] kalman_filter → unity_renderer 연동
- [ ] 전체 파이프라인이 오류 없이 실행되는가?

#### 테스트 케이스
- [ ] 단일 선박 추적
- [ ] 100척 동시 추적
- [ ] AIS 신호 두절 시나리오
- [ ] 야간 도선 시나리오

**제출 명령어:**
```bash
python3 test_integration.py --scenarios ulsan_night,multi_ship,ais_dropout
```

---

### **🔟 ci_cd_pipeline.yml** (배포)

#### GitHub Actions 자동화
- [ ] 코드 스타일 검사 (Black, Flake8)
- [ ] 타입 검사 (mypy)
- [ ] 유닛 테스트 (pytest)
- [ ] 통합 테스트 (자동)
- [ ] 성능 벤치마크 (자동)
- [ ] Docker 빌드 (자동)
- [ ] 자동 배포 (staging → production)

**확인 항목:**
- [ ] 모든 커밋 시 자동 테스트 실행되는가?
- [ ] 성능 저하 시 알림이 오는가?
- [ ] 배포 실패 시 롤백되는가?

---

## 📝 피드백 제출 형식

### **방법 1: 직접 터미널에서 보여주기**

```bash
# 각 스크립트 단독 테스트
python3 ais_simulator.py
python3 web_dashboard.py
python3 kalman_filter_realtime.py

# 통합 테스트
python3 test_integration.py --verbose

# 성능 벤치마크
python3 performance_benchmark.py --export report.csv
```

### **방법 2: 파일로 제출하기**

다음 파일들을 `/mnt/user-data/uploads/` 에 올려주세요:

1. **완성 스크립트들** (10개 .py/.cs 파일)
2. **test_results.log** (테스트 결과)
3. **performance_report.csv** (성능 데이터)
4. **bugs_and_issues.md** (발견된 버그 / 개선사항)

### **방법 3: 요약 문서**

```markdown
# 완성 보고서

## 완성된 스크립트
- [x] ais_simulator.py (1000줄)
- [x] web_dashboard.py (800줄)
- [x] ... (총 10개)

## 테스트 결과
- ais_simulator: ✅ 통과 (10척 동시)
- web_dashboard: ✅ 통과 (60 FPS)
- ...

## 발견된 이슈
1. ship_mesh_generator에서 LOD 전환 시 끊김 (개선 필요)
2. kalman_filter 신뢰도가 초기화 후 0.3 (정상/문제 확인 필요)
3. ...

## 통합 준비도
- 전체 통합: 95% (UI 마무리만 남음)
- 성능: 100 FPS 달성
- 메모리: <500MB 사용

## 다음 단계
- [ ] Meta Quest 3 Unity 어댑터
- [ ] 음성 명령어 통합
- [ ] 도선사협회 테스트 준비
```

---

## ✅ 최종 확인 체크리스트

제출하기 전에 **반드시** 확인하세요:

- [ ] 모든 .py 파일이 `python3 -m py_compile` 통과하는가?
- [ ] 모든 파일에 한글 주석이 UTF-8로 인코딩되었는가?
- [ ] 각 파일의 `if __name__ == '__main__':` 테스트가 에러 없이 실행되는가?
- [ ] requirements.txt가 최신인가?
- [ ] README.md가 모든 스크립트 사용법을 설명하는가?
- [ ] 로깅이 충분한가? (--debug 플래그 지원)
- [ ] 에러 메시지가 명확한가?
- [ ] 성능 최적화가 되었는가? (프로파일링 결과 포함)

---

## 🎬 제출 준비 완료 신호

다음 상태가 되면 제출 준비 완료:

```
✅ 모든 스크립트 완성
✅ 각 스크립트 단독 테스트 통과
✅ 통합 테스트 통과
✅ 성능 벤치마크 달성
✅ 문서 작성 완료
✅ 버그 리스트 정리 완료

→ 이 상태에서 위의 "방법 1, 2, 3" 중 하나로 제출 ✅
```

---

## 📞 Claude에게 피드백 요청할 때

다음과 같이 말해주세요:

> **"Week 1-4 스크립트 완성했습니다. 아래를 확인해주세요:**
> 
> 1. 각 스크립트 기본 기능 동작 확인
> 2. 성능 기준 달성 여부
> 3. 버그/개선 제안
> 4. 다음 주 (Week 5+) 스크립트 우선순위 조정"

이렇게 하면 **정확하고 빠른 피드백**을 받을 수 있습니다!

---

*이 체크리스트는 당신의 완성된 코드 품질을 보증하는 최종 게이트입니다.*
