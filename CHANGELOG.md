# Changelog

[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) + [SemVer](https://semver.org/).

## [Unreleased]

## [0.1.0] — 2026-04-24

프로젝트 초도 릴리즈. SDLC 한 바퀴 전 과정을 강의 자료로 남길 수 있는 **9/20 → 19/20 이슈 완료** 상태의 스냅샷. 프로덕션 배포(#18)는 보안 정책상 수동 작업으로 유보.

### Added — Phase 0 (기반 · CI/CD · Walking Skeleton)

- Monorepo 스캐폴딩: `/frontend` (Vite + React + TS + Tailwind) · `/backend` (FastAPI + uv + Pydantic) — #1
- GitHub Actions 기본 워크플로 (`lint.yml`, `test.yml`) — #2
- README 상태 배지 + `CONTRIBUTING.md` + branch-protection 정책 문서 — #3
- `Dockerfile × 2` + `docker-compose.yml` + nginx SPA 프록시 — #4
- 스테이징 자동 배포 (`deploy-staging.yml` — runner 내 compose up) — #5
- Smoke test 스크립트 `scripts/smoke.sh` + emergency teardown — #6
- `GET /api/health` + React 다크 대시보드 AppShell — #7
- `Config` + `LLMProvider` Port + Claude/OpenAI/Ollama Adapter 스텁 — #8
- Playwright E2E smoke 1건 — #9
- Security 워크플로 (bandit + pip-audit + biome + pnpm audit) — #10

### Added — Phase 1 (Core MVP)

- **US-01**: `POST /api/search` · YouTubeDataAdapter · SearchService + LRU 5분 캐시 · `KeywordInputView` · `VideoCard` · `VideoListView` — #11
- **US-02**: `POST /api/analyze` · YouTubeTranscriptAdapter · ClaudeAdapter (prompt caching) · `AnalysisPipeline` · `MarkdownRenderer` · `FileRepository` · `ReportResultView` (마크다운 미리보기 + 파일 경로 복사) — #12
- AnalyzingView 폴리시: `LogStream` (JetBrains Mono, 3색, auto-scroll) + `ProgressBar` (단계별 %) — #13

### Added — Phase 2 (엣지 케이스)

- 검색 0건 → `EmptyState` (200 + 빈 배열 정규화) · 네트워크 오류 → 502 + 재시도 — #14
- 자막 없음 → ErrorBanner warning 변형 + "다른 영상 선택" CTA · LLM 30s timeout + 자동 1회 재시도 — #15

### Added — Phase 3 (운영화)

- Playwright E2E 3건 확장 (success / no-results / no-transcript, `page.route` mock 기반) — #16
- WCAG AA 대비율 튜닝 · "/" 전역 단축키 · `@axe-core/playwright` E2E 가드 — #17
- Claude 토큰 누적 카운터 + `/api/health` 비용 노출 + Sidebar 스펜드 배지 — #19
- README · CHANGELOG · `docs/education-notes.md` · Provider 교체 실습 가이드 — #20

### Deferred

- **#3 branch protection API** — 보안 정책상 AI 수동 실행 불가. 이슈 #3 에 남긴 1회성 `gh api` 명령을 교수님이 직접 실행하시면 활성화됩니다.
- **#18 프로덕션 배포** (Fly.io + Vercel + 수동 승인 게이트) — 외부 서비스 유료 계정 + 시크릿 등록이 필요하므로 의도적으로 유보. 스테이징(#5) 레시피를 그대로 옮겨 확장하면 됩니다.

### Stack

| 계층 | 구성 |
|------|------|
| Frontend | React 18 · TypeScript 5 · Vite 5 · Tailwind 3 · Biome 1.8 · Zustand · lucide-react |
| Backend | FastAPI 0.111 · Uvicorn · Pydantic 2.7 · httpx · uv 0.4 · ruff |
| LLM | `LLMProvider` Port → ClaudeAdapter (기본, Sonnet 4.6) · OpenAI/Ollama 학생 실습 스텁 |
| External | YouTube Data API v3 · youtube-transcript-api · anthropic SDK |
| Storage | 로컬 FS (`./reports/*.md`) — DB 없음 |
| CI/CD | GitHub Actions × 5 (lint · test · e2e · security · deploy-staging) |
| Test | Vitest + Testing Library · Playwright + axe-core · pytest + respx |

### SDLC 산출물

- [`prd.md`](./prd.md), [`techspec.md`](./techspec.md), [`issues-vertical.md`](./issues-vertical.md)
- GitHub Issues #1~#20 · Project #20 "TechReport Sprint 1"

[0.1.0]: https://github.com/ischung/techreport-from-utube/releases/tag/v0.1.0
[Unreleased]: https://github.com/ischung/techreport-from-utube/compare/v0.1.0...HEAD
