---
tags: [meta, pdf, ingest, pipeline, reference]
title: "PDF→MD 파이프라인"
created: 2026-06-01 09:00
updated: 2026-06-01 19:00
---

# PDF→MD 파이프라인

## 개요

Obsidian 볼트로 PDF 문서를 수집하여 FTS5 검색(`/reduce wiki`) 가능한 Markdown으로 자동 변환하는 파이프라인. `IngestEngine`에 통합되어 `/ingest` 명령어 하나로 PDF도 .md와 동일하게 처리된다.

## 구현 위치

| 항목 | 경로 |
|------|------|
| 메인 엔진 | `~/Applications/Mjauto/Scripts/modules/ingest_engine.py` |
| PDF 추출기 | `IngestEngine._read_file_content()` (정적 메서드, line 97-112) |
| Clippings 수집 루프 | `_process_clippings()` — `_read_file_content()` 호출 (line 276) |
| 루트 파일 수집 루프 | `_process_root_files()` — `_read_file_content()` 호출 (line 366) |
| 파일 필터 | `.md`, `.pdf` 모두 허용 (line 357) |

## 처리 흐름

```mermaid
flowchart LR
    A[PDF 파일] --> B{PyMuPDF<br/>(fitz)}
    B -->|텍스트 추출 성공| C[raw_text]
    B -->|추출 실패/빈 텍스트| D[⚠️ skip]
    C --> E[LLM 분류<br/>category/title/description/keywords]
    E --> F[frontmatter 병합]
    F --> G[.md 저장 → category/]
    G --> H[원본 PDF → Archive/]
    H --> I[FTS5 인덱싱<br/>→ /reduce wiki 검색 가능]
```

## 상세 구현

### `_read_file_content()` (정적 메서드)

```python
@staticmethod
def _read_file_content(file_path: Path) -> str:
    suffix = file_path.suffix.lower()
    if suffix == ".pdf":
        import fitz
        doc = fitz.open(str(file_path))
        text = "".join(page.get_text() for page in doc)
        doc.close()
        return text.strip()
    return file_path.read_text(encoding="utf-8", errors="replace")
```

- `.pdf` → `fitz` (PyMuPDF)로 텍스트 추출
- `.md` / 기타 → 일반 텍스트 읽기 (`read_text`)
- 추출 실패 시 `""` 반환, 상위 루프에서 `if not raw_text: continue`로 skip

### 파일 필터 변경

```python
# Before: .md만 수집
f.suffix.lower() == ".md"

# After: .md + .pdf 수집
f.suffix.lower() in (".md", ".pdf")
```

### Clippings 루프 (line 276)

```python
raw_text = self._read_file_content(f)   # ← 통합 진입점
if not raw_text:
    continue
```

이후 LLM 분류 → frontmatter 생성/병합 → `.md` 저장 → 소스 PDF는 `Archive/`로 이동 → FTS5 인덱싱 → `/reduce wiki` 검색 가능.

### 루트 파일 루프 (line 366)

```python
raw_text = self._read_file_content(f)   # ← 동일 진입점
if not raw_text:
    continue
```

이후 동일한 LLM 분류 + 정리 파이프라인 실행.

## 사용법

### `/ingest` (자동 통합)

```bash
# Clippings/ 내 모든 .md + .pdf 처리
/ingest

# PDF만 따로 → Clippings/에 넣고 /ingest
# (별도 명령어 불필요)
```

### CLI에서 단독 추출 (디버깅용)

```bash
cd ~/Applications/Mjauto/Scripts
python3 -c "
import fitz
doc = fitz.open('path/to/file.pdf')
text = ''.join(page.get_text() for page in doc)
doc.close()
print(text[:2000])
"
```

### `/reduce wiki` 검색

변환된 `.md` 파일의 내용은 FTS5 인덱스에 포함되므로:

```bash
/reduce wiki 검색어
```

으로 PDF 내용 검색 가능 (원본 PDF 자체 검색은 불가, 변환된 .md만 검색됨).

## 의존성

| 패키지 | 용도 | 버전 |
|--------|------|------|
| `pymupdf` | PDF 텍스트 추출 (fitz) | 1.27.2.3 |

```bash
# 설치 (필요시)
python3 -m pip install pymupdf
```

## 제약 사항

⚠️ **다음은 현재 처리 불가 / 주의 필요:**

| 항목 | 설명 |
|------|------|
| 이미지/표/차트 | PyMuPDF `get_text()`는 텍스트만 추출, 시각적 요소는 소실 |
| 2단/다단 레이아웃 | 읽기 순서가 깨질 수 있음 (좌→우 컬럼 순서 불명확) |
| 스캔 PDF (OCR 없음) | 텍스트 레이어가 없어 빈 문자열 반환 → 자동 skip |
| 암호 PDF | `fitz.open()` 단계에서 실패 → skip |
| 대용량 PDF | 메모리 전체 로드, 매우 큰 문서는 OOM 가능성 |

## 변경 이력

| 날짜 | 변경 내용 |
|------|-----------|
| 2026-06-01 | 최초 구현 — `IngestEngine`에 PDF 지원 추가 |

---
*최종 업데이트: 2026-06-03 19:02 (일괄 타임스탬프 복구)*
