# MarineOS-XR 빠른 시작 가이드
## AIS Pilot Plug → Mac Studio → XR 헤드셋

**최종 업데이트:** 2026-06-04  
**개발 환경:** Mac Studio (M4 Ultra, 36GB)

---

## 📋 준비 사항

✅ **보유 장비 확인:**
- [ ] Mac Studio (M3/M4 Ultra, 메모리 ≥36GB)
- [ ] AIS Pilot Plug (도선사가 보유 중)
- [ ] WiFi 네트워크 (선박 AIS와 Mac을 같은 WiFi에 연결)
- [ ] 터미널 기본 지식

---

## 🚀 Phase 1: 테스트 (지금 바로)

### Step 1: Python 설정

```bash
# 1) 프로젝트 폴더 생성
mkdir -p ~/Projects/marineosXR
cd ~/Projects/marineosXR

# 2) Python 가상 환경 설정 (권장)
python3 -m venv venv
source venv/bin/activate

# 3) 필수 패키지 설치
pip install --upgrade pip
# (이 단계에서는 추가 패키지 필요 없음 - 순수 Python)
```

### Step 2: 코드 다운로드

```bash
# 위에서 받은 파일들을 복사
# 1) ais_nmea_parser.py
# 2) test_nmea.txt

# 폴더 구조:
# ~/Projects/marineosXR/
#   ├── ais_nmea_parser.py
#   ├── test_nmea.txt
#   └── venv/
```

### Step 3: 파일 파서 테스트 (즉시 테스트 가능)

```bash
# 터미널에서 실행
python3 ais_nmea_parser.py --file test_nmea.txt --debug

# 출력 예시:
# ================================================================================
# [14:30:25] 선박 수신
#   MMSI: 441000001
#   Name: (Type 5가 아직 수신 안 됨)
#   Position: 35.0523°N, 129.4195°E
#   SOG: 4.2 knots
#   COG: 270.5°
#   Length: N/A × N/A
#   Type: Not available
#   From: file
```

---

## 🌐 Phase 2: 실제 AIS Pilot Plug 연결

### 네트워크 설정

당신의 현재 방식:
```
선박 AIS Plug (선박 내 설치)
  ↓ (AIS 신호 발송)
AIS Pilot Plug (WiFi 릴레이, 도선사 휴대용)
  ↓ (NMEA 0183 over UDP)
iPad의 iSailor 앱
```

변경할 방식:
```
선박 AIS Plug
  ↓
AIS Pilot Plug (WiFi Master 역할)
  ├→ iPad의 iSailor 앱 (기존 방식 유지)
  └→ Mac Studio (새로운 XR 데이터 레이어)
```

### AIS Pilot Plug 설정 확인

**AIS Pilot Plug의 WiFi 네트워크 접속 확인:**

1. **AIS Pilot Plug의 IP 주소 확인**
   ```bash
   # Mac에서 현재 WiFi 네트워크의 모든 장비 목록 표시
   arp -a
   
   # 또는 더 정확하게:
   nmap -sn 192.168.x.0/24  # 당신의 WiFi 네트워크 범위로 변경
   ```

2. **AIS Pilot Plug가 UDP 5631 포트에서 NMEA 송신하는지 확인**
   ```bash
   # 터미널 1: 수신 대기
   nc -lu 0.0.0.0 5631
   
   # 또는 netstat로 포트 모니터링
   netstat -an | grep 5631
   
   # 데이터가 들어오면:
   # $AIVDM,1,1,,A,13P03v0...,0*7B
   # 같은 형식의 문장이 보입니다
   ```

### MarineOS-XR 실시간 수신 모드 시작

```bash
# Mac Studio의 터미널에서
cd ~/Projects/marineosXR
source venv/bin/activate

# AIS Pilot Plug에서 수신 대기
python3 ais_nmea_parser.py --port 5631 --debug

# 출력:
# INFO:__main__:AIS Pilot Plug 수신 대기 중: 0.0.0.0:5631
# (Ctrl+C로 종료)
#
# [14:35:10] 선박 수신
#   MMSI: 441000001
#   Name: ULSAN STAR
#   Position: 35.0523°N, 129.4195°E
#   SOG: 4.2 knots
#   ...
```

---

## 📡 Phase 3: 데이터 검증 (선박 정보 확인)

### 수신된 데이터 형식 확인

**iSailor 호환 GeoJSON 출력 (--debug 플래그 사용 시):**

```json
{
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [129.4195, 35.0523]
  },
  "properties": {
    "mmsi": 441000001,
    "name": "ULSAN STAR",
    "callsign": "D5Z6789",
    "ship_type": 80,
    "ship_type_name": "Tanker",
    "length_m": 320,
    "beam_m": 58,
    "sog": 4.2,
    "cog": 270.5,
    "heading": 271.2,
    "timestamp": 1717425800.123,
    "iso_timestamp": "2026-06-04T08:30:00Z",
    "channel": "A"
  }
}
```

### 데이터 저장 (선택 사항)

```bash
# 수신한 모든 선박 정보를 JSON 파일로 저장
python3 ais_nmea_parser.py --port 5631 > ship_data_$(date +%Y%m%d_%H%M%S).json

# 이 데이터를 나중에 XR 렌더링에 사용합니다
```

---

## 🎯 Phase 4: 좌표 변환 (Mac Studio 로컬 좌표계)

### WGS84 → UTM 변환 (울산항 Zone 52S)

```python
# 별도 테스트 스크립트: test_coordinates.py
import math

def latlon_to_utm(lat, lon):
    """WGS84 → UTM 변환"""
    # UTM Zone 52S (울산항)
    # 표준 자오선: 129°E
    
    k0 = 0.9996
    lon_origin = 129
    
    x = lon - lon_origin
    N = 6356752.3
    T = math.tan(math.radians(lat)) ** 2
    C = 0.081082 * math.cos(math.radians(lat)) ** 2
    A = x * math.cos(math.radians(lat))
    
    M = 6367449.1 * lat - 32045.4 * math.sin(2*math.radians(lat)) + 133.86 * math.sin(4*math.radians(lat))
    
    easting = k0 * N * (A + (A**3/6) * (1 - T + C)) + 500000
    northing = k0 * (M + N * math.tan(math.radians(lat)) * ((A**2/2) + (A**4/24) * (5 - T + 9*C + 4*C**2)))
    
    return easting, northing

# �## 🖥️ Phase 5: Mac Studio에서 웹 기반 대시보드

### 간단한 웹 UI로 실시간 모니터링 (REST API Polling 방식)

현재 구현된 웹 대시보드는 WebSocket + 백그라운드 스레드 간 충돌 문제를 해결하기 위해 **REST API + 브라우저 1초 Polling 방식**을 사용하여 극도의 안정성을 제공합니다.

#### 실행 및 테스트 방법:

```bash
# 1) 터미널 1: 웹 대시보드 서버 기동
cd "/Users/bluesea/Applications/MarineOS-XR Project"
python3 xr_interface/web_dashboard.py

# 2) 터미널 2: 가상 AIS 시뮬레이터 구동 (선박 표시용)
cd "/Users/bluesea/Applications/MarineOS-XR Project"
python3 ais_layer/ais_simulator.py --ships 5 --rate 1.0
```

#### 접속 방법:
- **로컬 브라우저:** [http://localhost:5050](http://localhost:5050)
- **외부 장비(iPad/XR 등):** `http://[Mac_IP_주소]:5050` (같은 WiFi 네트워크)

#### 화면 표시 항목:
- **해도 뷰:** Leaflet.js + OpenSeaMap을 결합하여 지도 위에 선박 방향 지시 삼각형 아이콘(어선=초록, 화물선=파랑, 유조선=빨강 등)을 렌더링합니다.
- **실시간 데이터:** MMSI, 선명, 위경도 좌표(울산항 부근 129°E 정상 표기), 속도(SOG), 침로(COG)가 1초마다 실시간으로 업데이트됩니다.

---print("AIS 수신 대기 중: 0.0.0.0:5631")
    
    while True:
        try:
            data, addr = sock.recvfrom(1024)
            sentence = data.decode('utf-8', errors='ignore').strip()
            
            if sentence:
                ais_data = decoder.parse(sentence)
                
                if ais_data:
                    mmsi = ais_data['mmsi']
                    ship_database[mmsi] = ais_data
                    
                    # 모든 웹 클라이언트에 실시간 전송
                    socketio.emit('ship_update', ais_data, broadcast=True)
                    
                    print(f"✓ {ais_data['mmsi']} - {ais_data.get('name', 'Unknown')} @ {ais_data['lat']:.4f}, {ais_data['lng']:.4f}")
        
        except socket.timeout:
            continue
        except Exception as e:
            print(f"오류: {e}")

# 백그라운드에서 AIS 수신 시작
ais_thread = threading.Thread(target=ais_receiver_thread, daemon=True)
ais_thread.start()

if __name__ == '__main__':
    print("\n🚀 웹 대시보드 시작: http://localhost:5000")
    print("   브라우저에서 접속하면 실시간 선박 정보가 표시됩니다\n")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
```

실행:
```bash
# Flask 설치
pip install flask flask-socketio python-socketio python-engineio

# 대시보드 실행
python3 web_dashboard.py

# 브라우저에서 접속
# http://localhost:5000
# 또는 iPhone/iPad에서:
# http://[Mac_IP]:5000  (같은 WiFi 네트워크)
```

---

## 🔧 문제 해결

### 문제 1: AIS 신호가 수신 안 됨

```bash
# 1) AIS Pilot Plug가 WiFi에 제대로 연결되었는지 확인
ping [AIS_Pilot_Plug_IP]

# 2) 포트가 제대로 열려 있는지 확인
netstat -an | grep 5631

# 3) 방화벽 확인 (Mac)
# System Preferences → Security & Privacy → Firewall
# Python이 인바운드 트래픽 허용되어 있는지 확인
```

### 문제 2: 파서 오류 ("체크섬 오류" 등)

```bash
# --debug 플래그로 상세 로그 확인
python3 ais_nmea_parser.py --port 5631 --debug

# 실제 수신된 원본 문장 확인
nc -lu 0.0.0.0 5631
```

### 문제 3: iSailor와 동시 사용 (신호 충돌)

```
AIS Pilot Plug는 멀티캐스트 또는 브로드캐스트로 데이터를 발송합니다.
따라서 Mac Studio와 iPad가 동시에 같은 신호를 수신할 수 있습니다.
충돌 없음 ✓
```

---

## 📊 다음 단계

### Step 1: ✅ 현재 (완료)
- [x] AIS NMEA 파서 작성
- [x] iSailor 호환 포맷 변환
- [x] Mac Studio에서 실시간 수신

### Step 2: 🔄 다음 (1-2주)
- [ ] UTM 좌표 변환
- [ ] 선박 3D 메쉬 생성 (프로시저럴)
- [ ] Flask 웹 대시보드

### Step 3: 🚀 이후 (3-4주)
- [ ] Meta Quest 3 Unity 어댑터
- [ ] XR 렌더링 (울산항 3D 배경)
- [ ] 실시간 레이더 UI
- [ ] 야간 모드 + 거리 표시

---

## 📞 추가 도움

**실제 문제 발생 시:**
1. 터미널 출력을 스크린샷으로 저장
2. `--debug` 플래그 추가 실행
3. 원본 NMEA 문장 몇 개 확인

---

*Made with ❤️ for Ulsan Port Pilots*
*MarineOS-XR v2.0*
