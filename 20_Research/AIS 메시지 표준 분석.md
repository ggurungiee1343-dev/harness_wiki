---
tags: [scanned, 20_Research, AIS, ITU-R M.1371, binary-data, message-structure, maritime-standard, protocol-analysis]
description: "AIS 소프트웨어나 가속 장치 개발 시 핵심 표준인 ITU-R M.1371을 분석한다. AIS는 27가지 메시지 타입을 가진 이진 데이터 구조로 구성되어 있다. 프로그램 설계 단계에서 반드시 구현해야 할 핵심 메시지 구조와 바이너리 레이아웃을 정리한다."
---

AIS 소프트웨어나 가속 장치를 개발할 때, 가장 먼저 이해해야 할 핵심 표준은 국제전기통신연합(ITU)의 [ITU-R M.1371](https://www.itu.int/rec/R-REC-M.1371) 표준입니다. 이 표준에 따르면 AIS는 단순한 텍스트 데이터가 아니라, 이진 데이터(Binary Bits)의 배열로 구성된 총 27가지의 메시지 타입(Message ID)을 가지고 있습니다. [1, 2, 3]

프로그램 설계 단계에서 반드시 구현해야 하는 핵심 메시지 구조, 바이너리 레이아웃(순서), 그리고 필수 타입을 정밀하게 정리해 드립니다.

---

## 1. AIS 메시지의 기본 공통 헤더 구조 (나열 순서)

어떤 종류의 AIS 메시지든(동적, 정적 불문), 원시 비트 스트림(Bit Stream)을 수신하면 가장 앞부분의 38비트는 무조건 다음과 같은 순서로 고정되어 배치됩니다. 이를 파싱하여 어떤 메시지인지, 어떤 배인지 판별합니다.

|비트 위치 (Bit) [1, 4]|데이터 필드명 (Field Name)|타입 / 크기|설명|
|---|---|---|---|
|0 ~ 5 (6 bits)|Message ID|Unsigned Integer|메시지 종류 (1~27) 구분 번호|
|6 ~ 7 (2 bits)|Repeat Indicator|Unsigned Integer|메시지 중계 횟수 (0=최초, 3=중계 중단)|
|8 ~ 37 (30 bits)|MMSI|Unsigned Integer|선박 고유 식별 번호 (9자리 고유 키)|

이 헤더(38비트) 바로 다음부터 각 메시지 ID별로 고유한 데이터들이 약속된 비트 순서대로 정렬됩니다.

---

## 2. 메시지 타입별 상세 필드 구성 (데이터 나열 순서)

개발자가 엑디스(ECDIS) 연동용 파서를 만들 때 반드시 완벽하게 파싱해야 하는 4대 핵심 메시지의 내부 구조와 순서입니다.

## ① 동적 정보 (Dynamic Report) — 메시지 1, 2, 3번

- 대상: Class A 선박이 운항 속도에 따라 2초~3분 주기로 가장 자주 쏘는 메시지입니다.
- 총 크기: 168 Bits 고정 [4, 5, 6]

> [비트 순서대로 배치된 필드 리스트]
> 
> 1. Message ID / Repeat Indicator / MMSI (38 bits) — 공통 헤더
> 2. Navigational Status (4 bits): 항해 상태 코드 (0=밑줄 운항 중, 1=묘박 중, 5=계류 중 등)
> 3. Rate of Turn, ROT (8 bits): 선회율 (좌우 회전 속도)
> 4. Speed Over Ground, SOG (10 bits): 대지속력 (0.1노트 단위, 1023=사용 불가)
> 5. Position Accuracy (1 bit): GPS 정밀도 (1=고정밀, 0=저정밀)
> 6. Longitude (28 bits): 경도 (1/10000 분 단위, 정밀 좌표 변환 필요)
> 7. Latitude (27 bits): 위도 (1/10000 분 단위)
> 8. Course Over Ground, COG (12 bits): 대지침로 (0.1도 단위, 0~3599)
> 9. True Heading (9 bits): 선수방위 (0~359도, 511=사용 불가)
> 10. Time Stamp (6 bits): UTC 초 (0~59초 표시)
> 11. Special Manoeuvre Indicator (2 bits): 특수 조종 구역 표지 (0=제공 안 함)
> 12. Spare (3 bits): 예비 비트 (0으로 채워짐)
> 13. RAIM Flag (1 bit): 위성항법 무결성 감시 여부
> 14. Communication State (19 bits): 무선 통신 동기화 정보 (SOTDMA/ITDMA 구조)
> 
> [7, 8]

## ② 정적 및 항해 정보 (Static & Voyage Report) — 메시지 5번

- 대상: 선박의 제원과 목적지 정보로, 6분 주기 또는 요청 시 송신됩니다.
- 총 크기: 424 Bits 고정 [1, 4]

> [비트 순서대로 배치된 필드 리스트]
> 
> 1. Message ID / Repeat Indicator / MMSI (38 bits) — 공통 헤더
> 2. AIS Version (2 bits): AIS 스테이션 버전
> 3. IMO Number (30 bits): 선박 고유 IMO 번호 (7자리 숫자)
> 4. Call Sign (42 bits): 호출부호 (6-bit ASCII 문자로 인코딩된 7글자)
> 5. Vessel Name (120 bits): 선명 (6-bit ASCII 문자로 인코딩된 20글자)
> 6. Type of Ship and Cargo (8 bits): 선종 및 화물 코드 (상위 자리는 선종, 하위 자리는 화물 성격)
> 7. Dimensions of Ship (30 bits): 선박 크기 및 GPS 위치 (선수 A, 선미 B, 좌현 C, 우현 D 내부 거리 구성)
> 8. Type of Electronic Position Fixing Device (4 bits): GPS 종류 (1=GPS, 2=GLONASS 등)
> 9. ETA (20 bits): 도착 예정 시간 (월 4bit, 일 5bit, 시 5bit, 분 6bit 순서 배치)
> 10. Maximum Present Static Draught (8 bits): 현재 최대 흘수 (0.1미터 단위)
> 11. Destination (120 bits): 목적지 항구명 (6-bit ASCII 문자로 인코딩된 20글자)
> 12. Data Terminal Ready, DTR (1 bit): 데이터 단말 준비 상태
> 13. Spare (3 bits): 예비 비트
> 
> [4]

## ③ Class B 선박용 동적/정적 정보 — 메시지 18, 19, 24번

- 어선이나 소형 요트(Class B)는 장비 출력이 낮고 전송 방식이 다릅니다.
- 메시지 18번: 소형선용 동적 정보 (168 bits) — 메시지 1~3번과 유사하나 데이터 압축 형태.
- 메시지 24번 (A/B 구조): 소형선용 정적 정보. 비트 수를 줄이기 위해 Part A(선명만 포함)와 Part B(선종, 호출부호, 크기 포함)로 쪼개어 번갈아 발송하는 구조이므로 파싱할 때 `MMSI`를 기준으로 두 파트를 결합하는 로직이 프로그램에 들어가야 합니다. [4, 9]

## ④ 안전 메시지 및 특수 바이너리 — 메시지 12, 14, 8번

- 메시지 12 / 14번 (Safety Related Message): 해상 조난, 경보 텍스트를 담은 메시지입니다 (12번은 특정 선박 타겟, 14번은 전체 방송). [1, 2, 4]
- 메시지 8번 (Binary Broadcast / ASM): e-Navigation 환경에서 매우 중요해진 메시지입니다. 기상 정보(풍속, 파고), 조석 정보, 가상 항로 표지(Virtual AtoN) 등을 개발사나 국가 기관이 정의한 레이아웃(Application Specific Message)대로 인코딩하여 전송합니다. [1, 4, 10]

---

## 3. 프로그램 개발 시 주의해야 할 구현 포인트

1. 6비트 ASCII 디코딩 공식 (6-bit ASCII):
    
    - AIS의 선명(Name)이나 목적지(Destination) 필드는 일반 8비트(1바이트) 문자열이 아닙니다.
    - 1문자당 6비트씩 압축되어 있으므로, 비트 스트림을 6비트씩 끊어서 AIS 전용 6비트 ASCII 변환 표(ITU-R M.1371 참조)를 통해 실제 영문과 숫자로 디코딩하는 알고리즘을 최우선으로 구현해야 합니다.
    
2. 좌표 음수 처리 (2의 보수):
    
    - 경도(Longitude)와 위도(Latitude)는 남위(S)나 서경(W)일 경우 음수로 표현됩니다. 비트열을 읽을 때 최상위 비트(MSB)를 확인하여 2의 보수(2's complement) 연산을 적용해야 지도(ECDIS 화면)에 엉뚱한 위치로 튀지 않습니다.
    
3. NMEA 0183 문장 파싱 (`!AIVDM` / `!AIVDO`):
    
    - 선박 내부 장비에서 데이터가 넘어올 때는 대개 `!AIVDM,1,1,,A,13HOIATI00S:` 같은 형태의 ASCII 문자열(NMEA 0183 포맷)로 전달됩니다.
    - 개발하시는 프로그램은 먼저 이 NMEA 문장의 체크섬을 검사한 뒤, 페이로드(Payload) 영역을 추출하여 위에서 설명한 바이너리 비트 스트림으로 변환하는 과정을 거쳐야 합니다.
    

---

현재 개발 중이신 프로그램의 주요 개발 언어(C++, Python, Java 등)나 데이터 수신 방식(이더넷 UDP 통신, 직렬 시리얼 통신 등)을 알려주시면, 프로토타입 파싱 코드 설계나 라이브러리(예: libais, pyais 등) 활용법을 추가로 지원해 드리겠습니다.

  

[1] [https://www.navcen.uscg.gov](https://www.navcen.uscg.gov/ais-messages)

[2] [https://vislab-ccom.unh.edu](https://vislab-ccom.unh.edu/~schwehr/papers/schwehr2007-ushydro-ais.pdf)

[3] [https://www.itu.int](https://www.itu.int/rec/R-REC-M.1371)

[4] [https://blog.naver.com](https://blog.naver.com/ulsan-port/224289077500?viewType=pc)

[5] [https://servicedocs-sm.kpler.com](https://servicedocs-sm.kpler.com/ais-fundamentals/)

[6] [https://www.itu.int](https://www.itu.int/dms_pub/itu-r/opb/rep/R-REP-M.2169-2009-PDF-E.pdf)

[7] [https://law.resource.org](https://law.resource.org/pub/us/cfr/ibr/004/itu-r.M-1371-1.2001.pdf)

[8] [https://m.blog.naver.com](https://m.blog.naver.com/oh_standard/221982515273)

[9] [https://ko.saiyungmarine.com](https://ko.saiyungmarine.com/info/what-is-automatic-identification-system-ais-17272593863353344.html)

[10] [https://www.kci.go.kr](https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART002281558)