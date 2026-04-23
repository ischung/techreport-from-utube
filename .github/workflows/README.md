# GitHub Actions Workflows

이 디렉토리의 워크플로는 프로젝트의 **품질 게이트**를 담당합니다.

## 워크플로 목록

| 파일 | 트리거 | 역할 | 필요 시크릿 | Phase |
|------|--------|------|-------------|-------|
| [`lint.yml`](./lint.yml) | PR, push to main, manual | Biome(frontend) + Ruff(backend) 린트·포맷 검증 | 없음 | 0-A (#2) |
| [`test.yml`](./test.yml) | PR, push to main, manual | Vitest(frontend) + pytest(backend) 단위 테스트 | 없음 | 0-A (#2) |

향후 추가될 워크플로 (계획):
- `security.yml` — SAST + 의존성 취약점 스캔 (#10 / CI-16)
- `deploy-staging.yml` — main 머지 시 스테이징 자동 배포 (#5 / CI-5)
- `e2e.yml` — Playwright E2E (#9 / CI-9)
- `kanban.yml` — 이슈/PR ↔ 칸반 동기화 (`KANBAN_TOKEN` runtime-guard 적용)

## 설계 원칙

1. **최소 권한**: 모든 워크플로는 `permissions: contents: read` 로 시작. 쓰기 권한은 필요할 때만 개별 job에 추가.
2. **3분 이내**: `timeout-minutes: 5` 로 상한을 두고, 의존성 캐시(pnpm cache + uv cache)로 실제 2~3분 내 종료 목표.
3. **Fork-safe**: 이 두 워크플로는 **외부 시크릿 불필요**하므로 fork PR에서도 그대로 실행 가능. 보안 민감 워크플로(배포·칸반 동기화)는 별도 파일로 분리하고 `if: secrets.KANBAN_TOKEN != ''` 같은 **runtime-guard** 로 가드.
4. **동시성 제어**: `concurrency` 그룹으로 같은 PR 의 이전 실행을 자동 취소 → 비용·시간 절감.

## KANBAN_TOKEN runtime-guard 패턴

교수님 SDLC 표준 정책에 따라, **`KANBAN_TOKEN` 시크릿이 저장소에 없는 환경에서도 워크플로가 빨간 X 없이 graceful skip** 되도록 설계합니다. 예시 (향후 `kanban.yml` 에서):

```yaml
jobs:
  sync-kanban:
    if: ${{ secrets.KANBAN_TOKEN != '' }}
    runs-on: ubuntu-latest
    env:
      GH_TOKEN: ${{ secrets.KANBAN_TOKEN }}
    steps:
      - run: echo "Token present, syncing..."
```

이 패턴은 교수님 강의의 다른 프로젝트(예: ship-test-v1, SmartGrader)와 일관성을 유지합니다.

## 로컬 재현

로컬에서 CI와 동일한 체인을 돌려보려면:

```bash
# Frontend
cd frontend && pnpm install && pnpm lint && pnpm typecheck && pnpm test

# Backend
cd backend && uv sync --extra dev && uv run ruff check . && uv run pytest -q
```

`act` (로컬 GitHub Actions 러너) 설치 시 `act -n` 으로 drying-run 플랜을 확인할 수도 있습니다.
