# CLAUDE.md — TechReport from YouTube

이 파일은 Claude Code가 이 저장소에서 작업할 때 참고하는 프로젝트 규칙입니다.

## 프로젝트 개요
- **목적**: 키워드로 최근 1개월 YouTube 영상을 찾아 한국어 기술보고서(md)를 생성하는 로컬 웹 대시보드
- **도메인**: 교육·강의 데모
- **규모**: 단일 사용자 로컬 도구, 8일 마일스톤

## 기획 산출물
모든 구현은 다음 세 문서를 기준으로 한다.
- `prd.md` — What/Why (기능 요구 · 유저 스토리 · KPI)
- `techspec.md` — How (아키텍처 · API · 데이터 모델 · 마일스톤)
- `issues-vertical.md` — 실행 단위 (CI-1 ~ CI-20, GitHub #1~#20)

## 아키텍처 원칙
- **3-Tier + Pipeline + Port-Adapter(LLM)**
- Frontend: React 18 + TS + Vite + Tailwind + shadcn/ui + Zustand
- Backend: FastAPI + uv + Pydantic + httpx + anthropic
- Pipeline: Retrieval → Selection → Analysis → Rendering
- LLM 교체: `.env` 의 `LLM_PROVIDER` (기본 `claude`, 대안 `openai` / `ollama`)
- 스토리지: 로컬 파일시스템 (`./reports/*.md`), DB 없음

## 코드 규칙
- **Frontend**: Biome (lint + format), 2-space indent, double quotes, 세미콜론 필수
- **Backend**: Ruff (lint + format), 4-space indent, line-length 100
- **커밋**: Conventional Commits (`feat`, `fix`, `ci`, `docs`, `test`, `refactor`, `chore`)
- **브랜치**: `feature/issue-<N>-<kebab-slug>`, main 직접 푸시 금지 (항상 PR)
- **PR**: 본문에 `Closes #<N>` 명시

## 테스트 정책
- Frontend 단위: Vitest + Testing Library
- Frontend E2E: Playwright (반드시 추가)
- Backend 단위: pytest (async 지원)
- 외부 API 모킹: `respx` (httpx 기반)
- 모든 슬라이스(CI-10~CI-14)는 단위 + 통합 + (UI 변경 시) E2E 최소 1건 포함

## CI/CD 규약
- GitHub Actions: `lint.yml`, `test.yml`, `e2e.yml`, `security.yml`, `deploy-staging.yml`
- 교수님 표준 시크릿명: **`KANBAN_TOKEN`** (칸반 자동화 전용)
- 모든 KANBAN_TOKEN 의존 워크플로는 **runtime-guard 패턴** 사용
  ```yaml
  if: secrets.KANBAN_TOKEN != ''
  ```
- main 브랜치 보호: `lint` + `test` 초록불 + 1인 리뷰 승인 필수

## 교육적 원칙 (교수님 선호)
- **설계 우선**: 코드 전에 구조 논의 → SDD
- **관심사 분리**: 레이어별·포트별 책임 명확히
- **YAGNI**: TechSpec 에 없으면 구현하지 않는다
- **문서화**: PRD / TechSpec / Issues 의 변경은 README 에도 반영
- **시각화**: Mermaid 차트 적극 활용

## 금지 사항
- main 브랜치 직접 푸시
- `git add -A` (명시적 경로 기반 staging 사용)
- `.env` / `*.pem` / `*.key` 커밋
- TechSpec 에 없는 임의 기능·리팩터 추가
- 최신 기술 스택을 "멋져 보인다"는 이유로 교체 (교과서적 안정성 우선)

## 외부 서비스 의존성
- YouTube Data API v3 (search, transcript via youtube-transcript-api)
- Anthropic Claude API (`claude-sonnet-4-6`, prompt caching 활용)

## 진행 상황
- GitHub Issues: https://github.com/ischung/techreport-from-utube/issues
- Project #20 (TechReport Sprint 1): https://github.com/users/ischung/projects/20
