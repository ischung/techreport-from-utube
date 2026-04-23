# 강의용 교육 노트

이 저장소는 한성대 소프트웨어공학 강의의 **SDLC 전 과정 교재**로 만들어졌습니다. 학생들이 실물 코드를 짚으면서 이론과 연결할 수 있도록 핵심 개념별 "어디를 보라"를 정리합니다.

---

## 1. 의존성 역전 원칙 (DIP)

> "고수준 모듈은 저수준 모듈에 의존해서는 안 된다. 둘 다 추상(abstraction)에 의존해야 한다." — Robert C. Martin

### 어디서 관찰하나

| 추상 (Port) | 구현 (Adapter) | 소비자 |
|---|---|---|
| [`app/ports/llm_provider.py`](../backend/app/ports/llm_provider.py) | [`claude_adapter.py`](../backend/app/adapters/claude_adapter.py), [`openai_adapter.py`](../backend/app/adapters/openai_adapter.py), [`ollama_adapter.py`](../backend/app/adapters/ollama_adapter.py) | [`app/pipeline/analysis_pipeline.py`](../backend/app/pipeline/analysis_pipeline.py) |
| [`app/ports/youtube_search_port.py`](../backend/app/ports/youtube_search_port.py) | [`youtube_data_adapter.py`](../backend/app/adapters/youtube_data_adapter.py) | [`app/services/search_service.py`](../backend/app/services/search_service.py) |
| [`app/ports/transcript_port.py`](../backend/app/ports/transcript_port.py) | [`youtube_transcript_adapter.py`](../backend/app/adapters/youtube_transcript_adapter.py) | `analysis_pipeline.py` |

### 실험

1. `grep -r "import anthropic" backend/app/pipeline/` — **0건**
2. `grep -r "import anthropic" backend/app/services/` — **0건**
3. `grep -r "import anthropic" backend/app/adapters/` — **1건** (claude_adapter만)

→ Pipeline 과 Services 는 Claude SDK 의 존재를 모릅니다. `LLMProvider` 계약만 보면 충분합니다. 이것이 **의존성 역전**입니다.

---

## 2. Hexagonal (Ports & Adapters) 아키텍처

### 두 경계선

```
                      ┌─────────────────────────────────┐
  Driving side        │         Application             │     Driven side
  (Primary actors)    │         (pure business)         │    (secondary actors)
  ────────────►       │                                 │    ◄────────────
                      │     Services · Pipelines        │
  HTTP request        │                                 │     YouTube API
  (FastAPI routes) ──►│  depends only on Ports          │───► Anthropic API
                      │                                 │     File system
                      └─────────────────────────────────┘
                              ↑                 ↑
                              │                 │
                         Ports (추상)       Ports (추상)
                              │                 │
                              ↓                 ↓
                         Routes            Adapters
                       (Driving)         (Driven — 실제 I/O)
```

### 이 저장소에서

- **Driving side (HTTP 입구)**: `app/api/*.py` — `/api/search`, `/api/analyze`, `/api/health`
- **Application core**: `app/services/`, `app/pipeline/` — 외부 I/O 에 대해 무지(無知)한 비즈니스 흐름
- **Driven side (I/O 출구)**: `app/adapters/` — 실제 네트워크 / 파일 I/O 를 수행하는 구현체
- **계약선(Ports)**: `app/ports/` — 어느 쪽도 서로를 직접 부르지 않고 이 인터페이스만 참조

### 교체 실험

README의 "Provider 교체 실습" 섹션을 따라 `LLM_PROVIDER=openai` 로 바꾸면 **Adapter 한 파일만** 교체되고 Application core 는 재컴파일조차 하지 않습니다.

---

## 3. Walking Skeleton (Alistair Cockburn)

> "End-to-End 로 최소 동작하는 최초의 베이스라인. 여기 위에 기능을 덧붙인다."

### 이 저장소의 Walking Skeleton

**PR #22 + #28** = 초도 Walking Skeleton:
- 브라우저 열기 (`http://localhost`)
- React 대시보드가 렌더된다
- `/api/health` 응답을 받아 사이드바의 상태 도트가 **emerald 로 바뀐다**
- 위 흐름이 **CI 워크플로 (lint + test + e2e) 모두 초록불** 위에서 반복 가능하다

### 교육 포인트

1. **뼈대 먼저**: #7 에서 "Hello Dashboard" + `/api/health` 만 구현. 이때는 키워드 검색도, LLM 도 없습니다.
2. **파이프라인 위에 올라타기**: #11 (search) · #12 (analyze) · #13 (logstream) 세 슬라이스가 이 뼈대에 하나씩 얹혀 들어가며 매번 `pnpm test:e2e` 가 초록불로 남습니다.
3. **Regressions 감지**: #11 에서 `App.tsx` 를 wizard 로 교체했을 때 기존 `App.test.tsx` 가 즉시 실패 → 문제 **수정 전에 발견**. 이것이 Walking Skeleton 의 가치입니다.

---

## 4. CI/CD First (이 프로젝트의 특이점)

보통 "기능 먼저, CI 는 나중에" 순서지만 이 저장소는 `issues-vertical.md` 의 전략에 따라 **반대**로 움직였습니다.

### 실행 순서 (머지 순)

1. `#1` Monorepo 스캐폴딩
2. `#2` lint + test 워크플로 → **이 시점부터 모든 PR 은 CI green 이어야 머지 가능**
3. `#3` 보호 규칙 + 배지
4. `#4~#6` Docker + 스테이징 + smoke
5. `#7~#9` Walking Skeleton (위 절)
6. `#10` Security 스캔
7. `#11~#20` 기능 슬라이스들

### 교육 포인트

- 기능 슬라이스 PR 모두가 **이미 작동하는 CI/CD 고속도로 위에 올라탑니다**. "CI 가 빨간색이라 머지 못 함" 같은 블로커가 발생하면 **코드가 아니라 파이프라인 을 먼저 고친다**는 엔지니어 습관이 자연스럽게 형성됩니다.
- 실제로 본 저장소의 초창기 CI 실패들은 대부분 **설정 실수** (lockfile 경로 · biome 1.9 vs 1.8 · ruff 포맷 차이) 였습니다. 기능 버그가 아님. 이 경험이 학생에게 "CI 는 약속의 장부"라는 감각을 남깁니다.

---

## 5. Vertical Slice + YAGNI

각 `[Slice]` 이슈는 **UI + API + Adapter + Test** 를 모두 포함합니다. 예) #11 PR 의 diff:

- `frontend/src/components/KeywordInputView.tsx` (UI)
- `frontend/src/store/useAppStore.ts` (상태)
- `backend/app/api/search.py` (API)
- `backend/app/services/search_service.py` (비즈니스)
- `backend/app/adapters/youtube_data_adapter.py` (I/O)
- `backend/tests/test_search_route.py`, `test_youtube_adapter.py` (Test)

### YAGNI 의 증거

- DB 가 없습니다. 모든 저장은 `./reports/*.md` 파일. 왜? PRD §7 이 "단일 사용자 로컬 도구" 라고 못박았기 때문.
- 인증 시스템이 없습니다. 왜? Out-of-Scope.
- Redis 캐시가 없습니다. 5분 LRU 는 `OrderedDict` 로 충분합니다.

학기 말에 "이제 DB가 필요하다" 는 순간이 오면 그때 붙입니다. **지금 필요 없으면 만들지 않는 것이 YAGNI** 입니다.

---

## 6. 추천 강의 진행 순서

| 주차 | 이론 | 실물 PR |
|:---:|------|--------|
| 1 | SDLC 개요 + PRD 작성법 | [`prd.md`](../prd.md) |
| 2 | TechSpec · 아키텍처 패턴 | [`techspec.md`](../techspec.md) |
| 3 | 이슈 분할 전략 (Vertical vs Layered) | [`issues-vertical.md`](../issues-vertical.md) |
| 4 | GitHub Flow + CI 부트스트랩 | PR #22, #23, #24 |
| 5 | 컨테이너 + 배포 기초 | PR #25, #26, #27 |
| 6 | Walking Skeleton 철학 | PR #28, #29, #30 |
| 7 | Security 스캔 + SAST | PR #31 |
| 8 | Port-Adapter 실습 (US-01) | PR #32 |
| 9 | 파이프라인 + Prompt Caching | PR #33 |
| 10 | UX 폴리시 (LogStream) | PR #34 |
| 11 | 엣지 케이스 + 에러 모델링 | PR #35, #36 |
| 12 | 자동화 테스트 확장 (E2E mock) | PR #37 |
| 13 | 접근성 (WCAG AA) | PR #38 |
| 14 | 관측성 (토큰 · 비용) | PR #39 |
| 15 | 문서화 + 릴리즈 | PR #40 (this) |

---

## 7. 다음 학기 과제 아이디어 (Out-of-Scope 이슈들)

PRD §1.3 의 Out-of-Scope 리스트는 **학기말 과제 포트폴리오** 로 직결됩니다:

- 썸네일 표시 (`#next-1`)
- 검색 히스토리 SQLite 영속화 (`#next-2`, `TokenCounter` 도 함께 지속)
- 여러 영상 비교 보고서 (`#next-3`)
- 영문 보고서 모드 (`#next-4`)
- Firebase 등 외부 저장 (`#next-5`)

각 과제는 이미 Hexagonal 경계가 잡혀 있어서 **Adapter 한 개 교체 / Repository 한 개 추가** 로 완성할 수 있습니다.
