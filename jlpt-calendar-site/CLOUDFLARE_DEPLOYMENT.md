# 캘린더 Cloudflare 배포

- 기본 공개 주소: https://jlpt-study-calendar.pcw0611.workers.dev/
- 기존 Sites 주소: https://jlpt-study-calendar.pcwww.chatgpt.site/ (유지)
- 게임: https://slay-the-jlpt.pages.dev/
- 사용자 소유 Cloudflare Worker: `jlpt-study-calendar`
- 사용자 소유 D1: `jlpt-study-calendar-production`, APAC
- 배포 설정: `wrangler.cloudflare.jsonc`
- 기존 `.openai/hosting.json`은 수정하지 않는다. Sites의 DB ID와 사용자 Cloudflare의 DB ID를 혼용하지 않는다.

## 배포

같은 Vinext 소스와 빌드 결과를 그대로 사용한다. 직접 이전이므로 기존 빌드의 compatibility_date `2026-05-15`를 유지한다. UI·집계·시험 결과는 이번 이전에서 변경하지 않는다.

```powershell
pnpm build
if ($LASTEXITCODE -ne 0) { throw 'Build failed' }
$runtime = 'C:\Users\pcw06\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\bin\node.exe'
& $runtime node_modules/wrangler/bin/wrangler.js deploy --config wrangler.cloudflare.jsonc --dry-run
if ($LASTEXITCODE -ne 0) { throw 'Deployment validation failed' }
& $runtime node_modules/wrangler/bin/wrangler.js deploy --config wrangler.cloudflare.jsonc
```

DB 변경이 있는 경우에만 `d1 migrations apply DB --remote --config wrangler.cloudflare.jsonc`로 미적용 마이그레이션을 반영한다. 초기 0000·0001은 이미 적용했다. 비밀키 `JLPT_SYNC_SECRET`은 Wrangler secret으로 등록했으며 설정이나 빌드 결과에 넣지 않는다.

## 학습 데이터 동기화

기존 명령을 그대로 쓰면 기본적으로 Cloudflare와 Sites **양쪽**에 전송한다.

```powershell
python scripts/sync_learning_data.py 2026-08-28
python scripts/sync_learning_data.py --all
python scripts/sync_learning_data.py 2026-08-28 --target cloudflare
python scripts/sync_learning_data.py 2026-08-28 --target legacy
```

`JLPT_SYNC_URL`을 지정한 기존 사용 방식은 그 주소 한 곳에만 전송하는 동작을 유지한다. 각 목적지의 성공 여부를 출력하고 일부 실패도 종료 코드에 반영한다. 실패한 목적지만 `--target`으로 재시도할 수 있다. 로컬 DB는 읽기 전용으로 사용한다.

## 이전 데이터와 검증

- 이전 공개 API의 3일분 JSON을 백업한 후 새 API와 전체 값이 같은지 확인했다.
- Sites DB의 5개 테이블을 이전했다: daily_reports 3, study_days 1, review_schedule 18, skill_snapshots 4, type_metrics 9행.
- JSON 긴 필드는 커넥터가 잘라 반환하므로 daily_reports.payload_json은 기존 공개 API의 완전한 JSON으로 가져왔다.
- 원본 백업과 가져오기 SQL은 git에서 제외되는 `outputs/`에 보관한다. 기존 Sites DB와 로컬 원본 DB는 삭제하지 않았다.
- 새 홈페이지와 기록 API HTTP 200, 게임 링크 포함, 비인증 동기화 HTTP 401을 확인했다.
- 새 동기화 단위 테스트 4개 통과. 전체 기존 Python 테스트 중 2개는 오래된 고정값(32문항/20정답)과 최신 DB(40문항/24정답)가 달라 실패하며, 집계 로직은 이번에 수정하지 않았다.
- 브라우저 화면 비교·전체 상호작용·체감 속도 비교는 수행하지 않았다.

롤백 시 기존 Sites 주소를 사용한다. 새 Cloudflare 리소스를 삭제할 필요는 없다. 기존 Sites 공개 버전 8은 그대로 유지하며, 다음 소스 변경 시 두 호스팅을 함께 갱신해야 한다.
