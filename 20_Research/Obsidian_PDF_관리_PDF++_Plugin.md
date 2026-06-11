# Obsidian PDF 관리: PDF++ Plugin과 전체 텍스트 검색

> 출처: The Effortless Academic Blog
> 원문: Working with PDFs in Obsidian: PDF++ Plugin and Full-Text Search
> 작성자: Ilya Shabanov
> 게시일: 2025-01-12
> 저장일: 2026-05-08
> 태그: #pdf #obsidian #note-taking #research

---

## 핵심 요약

**목표:** PDF 주해 + 코멘트/결론 + 일반 노트 3가지 연결

```
PDF annotation ↔ 코멘트/결론 노트 ↔ 일반 노트
```

**Deep link 예시:**
- 노트에서 "Ehrlen 2015의 주장을 보면" → PDF 특정 부분으로 이동
- 노트에서 "이 주장이 나온 논문" → 원본 PDF로 이동

---

## 주요 도구

### 1. PDF++ Plugin (권장)

| 기능 | 설명 |
|------|------|
| **주해 저장** | PDF 내부에 직접 저장 (visually preserved) |
| **Deep link** | 특정 주해로 직접 연결 가능 |
| **포맷 커스터마이징** | 링크 색상, 형식 설정 가능 |
| **이미지 주해** | 텍스트뿐만 아니라 이미지 주해도 가능 |

**복사 포맷 3가지:**
- Colour: 주해 색상
- Copy format: 복사될 링크 형식
- Text format: 노트에 표시될 텍스트 형식

### 2. Obsidian Annotator (대안)

| 장점 | 단점 |
|------|------|
| 가벼움, 빠름 | 텍스트만 미리보기, 위치 이동이 부정확할 수 있음 |

### 3. 전체 텍스트 검색

| 도구 | 특징 |
|------|------|
| OmniSearch + Text Extractor | Obsidian 내에서 검색, 텍스트만 |
| Zotero 7 | Advanced Search → Attachment Content |
| PDF Search App (Mac only) | 시각적 미리보기, 관련도 순위 정렬 |

---

## PDF 관리 규칙

### 저장 위치
```
__Papers/ 폴더에 모든 PDF 보관
```
- Plugin 호환성 향상
- Attachment Management Plugin으로 자동 이동 가능

### 파일 명명 규칙
```
"Smith 2020" (저자 + 연도)
```
- 짧게 유지 (노트에서 링크 가독성 향상)

### Zotero 활용
1. Zotero로 메타데이터만 캡처
2. PDF를 Obsidian으로 이동
3. Obsidian에서 주해 작업
4. 원고 작성 시 (MS Word/Google Docs) Zotero 재사용

---

## PDF++ 설정 최적화 (저자 권장)

### In-link 포맷 설정

노트에 다음 형식으로 저장:

```
주해 내용 (인용문)
  ↓
[[Source Note]] ← 해당 논문의 일반 노트
  ↓
[[PDF파일.pdf#page=5]] ← PDF 본문
```

### 링크 색상 커스터마이징

- PDF 링크: 노란색 ( Yellow)
- Source Note: 파란색 (Blue)
- Style Settings + Supercharged Links Plugin 사용

---

## Decision Tree

```
PDF 주해를 PDF 내부에 저장할까?
├── Yes → PDF++에서 "Enable PDF editing" 체크
└── No → Annotator 사용 (Markdown 파일에 저장)
```

---

## 설치 필요 Plugin

| Plugin | 용도 |
|--------|------|
| PDF++ | PDF 주해 및 deep link |
| OmniSearch | 전체 텍스트 검색 |
| Text Extractor | PDF 텍스트 추출 |
| Supercharged Links | 링크 색상 커스터마이징 |
| Style Settings | Obsidian 디자인 설정 |

---

## Quick Start

1. Obsidian → Community Plugins → PDF++ 설치
2. `__Papers/` 폴더 생성
3. PDF++ Settings에서 "Enable PDF editing" 활성화 (선택)
4. PDF 열기 → 텍스트 선택 → 주해 추가
5. 복사 포맷 설정 후 노트에 붙여넣기

---

## 요약

| 항목 | 내용 |
|------|------|
| **최고 PDF Plugin** | PDF++ (학습 곡선 있지만 강력한 기능) |
| **주해 저장 방식** | PDF 내부 vs Markdown 파일 (선택 가능) |
| **핵심 이점** | 노트 ↔ PDF ↔ 주해 간 연결로 리뷰 효율화 |
| **Deep link** | 특정 주해로 직접 이동 가능 |

---

## 관련 리소스

- 원문: The Effortless Academic Blog
- Course: Effortless Note Taking Course (유료)
- 무료.course: "Does your research work for you?" (8일 과정)

---
*최종 업데이트: 2026-06-03 19:02 (일괄 타임스탬프 복구)*
