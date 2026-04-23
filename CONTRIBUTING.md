# Contributing

> 한성대 SW공학과 강의 실습 저장소. 학생이 PR을 보내며 SDLC 전 과정을 체험합니다.

## 기본 규칙

1. **Main 직접 push 금지** — 항상 feature 브랜치 + PR 흐름.
2. **브랜치 네이밍** — `feature/issue-<N>-<kebab-slug>` (예: `feature/issue-11-us-01-search-slice`).
3. **커밋 메시지** — [Conventional Commits](https://www.conventionalcommits.org) (`feat`, `fix`, `ci`, `docs`, `test`, `refactor`, `chore`). 본문 끝에 `Refs #N` 또는 `Closes #N`.
4. **PR 본문** — 반드시 `Closes #<N>` 포함. 리뷰어 체크리스트는 템플릿을 사용.
5. **머지 정책** — Squash merge, 머지 후 브랜치 삭제.

## 머지 전 체크리스트 (PR 본문에 포함)

- [ ] 이슈 본문의 **수락 기준(AC)** 을 모두 충족했는가?
- [ ] 로컬 `pnpm --dir frontend lint test typecheck` / `cd backend && ruff check . && pytest` 통과?
- [ ] `lint` · `test` 워크플로가 초록불인가?
- [ ] 민감 정보(`.env`, API key) 가 포함되지 않았는가?
- [ ] README / CLAUDE.md 업데이트가 필요하면 반영했는가?

## Branch Protection (main)

본 저장소의 `main` 브랜치는 다음 규칙으로 보호됩니다:

- Pull request 경유 머지만 허용 (직접 push 금지)
- 필수 상태 체크: `Frontend · Biome`, `Backend · Ruff`, `Frontend · Vitest + typecheck`, `Backend · pytest` — 모두 초록불이어야 머지 가능
- Stale 리뷰 자동 해제 (브랜치에 새 커밋이 들어오면 기존 승인 무효화)
- 관리자(교수) 는 비상시 우회 가능 (`enforce_admins: false`)

## 로컬 개발 셋업

```bash
git clone https://github.com/ischung/techreport-from-utube.git
cd techreport-from-utube
cp .env.example .env
pnpm --dir frontend install
uv --directory backend sync --extra dev
```

상세한 실행 방법은 [README.md](./README.md) 를 참조하세요.

## Pre-commit 설치 (선택, 강력 권장)

```bash
pipx install pre-commit
pre-commit install
pre-commit run --all-files     # 최초 검증
```

매 커밋마다 `ruff` (backend), `biome` (frontend), 파일 위생 hook 이 자동 실행됩니다.

## 질문

- Issue: https://github.com/ischung/techreport-from-utube/issues
- Email: insang@hansung.ac.kr
