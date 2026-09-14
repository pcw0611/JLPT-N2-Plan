# 호스팅 검토

## 2026-08-28 — N2 단어 게임 공개 및 캘린더 연결

사용자가 Cloudflare 사용 및 기존 CLI 로그인으로 진행하는 것을 승인했다. 게임 로직과 저장 형식은 변경하지 않는다. 캘린더의 Sites 설정, 기존 주소와 DB는 유지한다.

| 후보 | 비용·조건 | 호환성·위험 | 결정 |
| --- | --- | --- | --- |
| [Cloudflare Pages Direct Upload](https://developers.cloudflare.com/pages/get-started/direct-upload/) | 정적 요청은 [무료·무제한](https://developers.cloudflare.com/pages/functions/pricing/). 서비스 약관 적용, 소스 라이선스 변경 없음 | 기존 Vite dist 직접 배포 가능. 같은 프로젝트를 Git 자동 배포 방식으로 전환할 수 없어 필요 시 새 프로젝트 필요. 브라우저 저장은 주소가 달라지면 자동 이전되지 않음 | 채택: 정적 게임에 필요한 기능만 사용, 신규 패키지·유료 서비스 없음 |
| [Cloudflare Workers Static Assets](https://developers.cloudflare.com/workers/static-assets/) | [정적 요청 무료](https://developers.cloudflare.com/workers/static-assets/billing-and-limitations/), 동적 Worker는 별도 제한·과금. 서비스 약관 적용 | API 확장에 적합하나 현재 게임은 서버 코드가 없어 필요 없음 | 보류 |

## 같은 날 정정 — 캘린더도 Cloudflare로 이전

사용자가 캘린더까지 이전하는 것이 원래 요청이었음을 확인했다. 게임만 옮기는 해석을 정정한다.

- Workers + D1: 캘린더에 채택. 기존 Vinext의 Workers 빌드와 Drizzle D1을 재사용해 새 프레임워크·패키지 도입 없이 사용자 계정에 직접 배포한다.
- Pages 정적 호스팅만 사용: 캘린더에서는 제외. 기존 DB·동기화 API를 유지해야 하기 때문.
- [Workers 요금](https://developers.cloudflare.com/workers/platform/pricing/)과 [D1 요금](https://developers.cloudflare.com/d1/platform/pricing/)의 무료 제공량을 확인했다. 새 유료 플랜 가입이나 업그레이드는 하지 않았다. 계정 플랜·사용량에 따른 제한은 적용된다. 서비스 약관 적용, 기존 소스 라이선스 변경 없음.
- 기존 Sites 주소·설정·DB는 유지하고 동기화는 두 곳에 반영한다. 사용자 Cloudflare D1은 APAC 위치로 생성했다. 호스팅 변경에 따른 실제 체감 속도 개선은 측정 전이며 보장하지 않는다.

## 2026-08-31 — N2 문법 001~025 Anki 덱 생성

| 후보 | 비용·라이선스 | 호환성·위험 | 결정 |
| --- | --- | --- | --- |
| [Anki 기본 텍스트 가져오기](https://docs.ankiweb.net/importing/text-files.html) | 무료, Anki 공식 기능 | TSV를 직접 가져올 수 있지만 필드 매핑과 카드 템플릿을 사용자가 설정해야 함 | 보조 산출물로 채택: 편집 가능한 TSV 제공 |
| [genanki 0.13.1](https://pypi.org/project/genanki/) | 무료, MIT | 커뮤니티 Python 패키지이며 Anki 공식 SDK는 아님. 생성 시에만 필요하고 완성된 APKG에는 런타임 의존성이 없음 | 채택: 프로젝트 의존성에 추가하지 않고 격리된 임시 설치로 APKG 생성 |

- Anki 공식 설명에서 `.apkg`는 덱 패키지 형식임을 확인했다. 고정 덱·모델 ID와 문형별 안정적인 GUID를 사용해 같은 파일의 재생성·재가져오기 시 중복 위험을 낮춘다.

### 같은 날 정정 — 현재 환경의 APKG 생성 제한과 Anki MCP 후보

- `genanki` 다운로드가 로컬 실행 환경에서 두 차례 멈춰 설치하지 않았다. 프로젝트 의존성이나 기존 Anki 프로필은 변경하지 않았다.
- 공식 Anki UTF-8 텍스트 가져오기 형식의 파일 헤더(`separator`, `html`, `deck`, `tags column`, `columns`)를 사용한 25장짜리 가져오기 파일과 편집용 TSV를 대신 생성했다.

| 후보 | 비용·라이선스 | 호환성·권한 위험 | 상태 |
| --- | --- | --- | --- |
| [AnkiMCP Server 애드온](https://ankiweb.net/shared/info/124672614) | 무료, AGPL-3.0-or-later | Anki 25.x 이상. Anki 내부에서 로컬 MCP 서버를 열고 노트·덱·미디어 생성·수정·삭제 도구를 노출하므로 연결 권한을 제한해야 함. 첫 실행 시 플랫폼 바이너리를 내려받음 | 채택: v0.27.1 설치, 로컬 `127.0.0.1:3141`만 사용, 외부 터널 미사용 |
| [CamdenClark/anki-mcp-server](https://github.com/CamdenClark/anki-mcp-server) | 무료, MIT | AnkiConnect 애드온과 Node 빌드가 별도로 필요. 덱·모델 조회 및 노트 추가 중심이며 저장소 활동·호환성을 설치 전 재확인해야 함 | 보류: 구성 요소가 더 많고 현재 작업에는 공식 텍스트 가져오기로 충분 |

- 공식 GitHub 릴리스 `anki_mcp_server.ankiaddon`의 SHA-256 `e705d30f368340a4718240a9a967d539e3040477ea2682629609e0dfec892d22`를 검증 후 설치했다.
- 첫 실행의 `pydantic_core 2.46.4` 자동 다운로드가 Anki를 응답 불가로 만들어 프로세스를 종료했다. PyPI JSON의 Windows CPython 3.13 wheel을 직접 내려받아 SHA-256 `6b3ace8194b0e5204818c92802dcdca7fc6d88aabbb799d7c795540d9cd6d292`를 검증하고 애드온 전용 캐시에 배치했다.
- Codex 전역 MCP 서버 `anki`를 `http://127.0.0.1:3141/`로 등록했다. 현재 작업의 도구 목록은 세션 시작 시 고정되므로 새 작업에서 정식 MCP 도구로 노출된다.
- 기본 설정의 삭제 계열 도구는 비활성화 상태이며 외부 터널 로그인·공개 주소는 설정하지 않았다.
- MCP를 통해 `JLPT N2::문법 001-025 예문 복습` 덱과 Basic 노트 25장을 생성했다. `deck:"JLPT N2::문법 001-025 예문 복습" tag:문법_001_025` 재조회에서 25장을 확인했다.

## 2026-09-01 — 한끝 Voca 전체 카드의 N2 수준 예문·후리가나 보강

대상은 `日本語::JLPT 한끝 Voca`의 N5~N2 하위 덱 2,734장이다. 기존 카드 1장만 `sentences`가 채워져 있고 나머지는 비어 있음을 Anki MCP로 확인했다. 기존 단어·뜻·스케줄은 유지하고 `sentences` 필드와 해당 노트 유형의 예문 표시만 변경하는 방안을 검토했다.

| 후보 | 비용·라이선스 | 호환성·위험 | 상태 |
| --- | --- | --- | --- |
| [Tatoeba 일본어 CC0 문장](https://tatoeba.org/en/downloads) + [공식 읽기 전용 API](https://api.tatoeba.org/) | 무료, CC0 1.0 문장만 사용하면 카드별 저작자 표기 의무 없음 | 확인 결과 일본어 CC0 내보내기는 문장 2개뿐이라 전체 2,734개 표제어를 덮을 수 없음 | 제외 |
| [Tatoeba 전체 일본어 문장](https://tatoeba.org/en/downloads) | 무료, 기본 CC BY 2.0 FR; 재배포 시 저작자·라이선스 표기 필요 | 범위는 넓지만 Anki 카드에 출처 메타데이터와 변경 표시를 보존해야 하며 비원어민 문장의 품질 편차가 있음 | 보류: 카드가 복잡해지고 검수 비용이 큼 |
| [Sudachi / SudachiPy](https://github.com/WorksApplications/sudachi.rs) + core 사전 | 무료, Apache-2.0 계열 구성요소; 생성 시에만 사용하는 임시 도구 | 표면형·활용형 읽기 생성에 적합하나 core 사전이 약 70MB이며 고유명사·문맥 의존 읽기는 표본 검수가 필요함 | 채택: 사용자 승인 후 `tmp/voca-example-work/pydeps`에 격리 설치, Anki 런타임 의존성 없음 |
| [Tanaka Corpus 마지막 Public Domain 판](http://ftp.edrdg.org/pub/Nihongo/examples_pd-2008-10-10-tabbed-ck.zip) | 무료, Public Domain | 2008년 판이라 최신 수정은 포함하지 않으며 일부 문장에 품질 편차가 있음. 표제어·활용형 인덱스와 N2 문형·길이 점수로 선별하고 부족분은 자체 작성해야 함 | 채택: 150,341개 문장 사용, SHA-256 `e5d4fb34e8e146307c03246e08cccaf7d34ea606d80541adcea9480daba30055` |

- 외부 문장을 그대로 복제하지 않는 대안은 2,734개를 자체 작성하는 것이지만, 자동 템플릿은 자연스러움과 의미 적합성이 떨어져 채택하지 않는다.
- 사용자 승인 후 Public Domain 용례 2,667장과 자체 작성·의미 보정 67장으로 전 카드 2,734장의 예문을 구성했다.
- Sudachi가 표제어 원형을 잘못 읽을 수 있는 경우에는 카드의 기존 `kana` 값을 우선하도록 보정했다. 자동 생성된 문장 내 일반 한자의 후리가나는 문맥에 따라 추가 수동 교정이 필요할 수 있다.
- Anki MCP 사전 검증 2,734 성공 예정·0 실패, 실제 업데이트 2,734 성공·0 실패, 재조회 `sentences:_*` 2,734장을 확인했다.

## 2026-09-01 — 한끝 Voca 예문 한국어 해석 생성

기존 2,734개 일본어 예문에 한국어 해석을 추가하기 위한 오프라인 번역 후보를 검토했다. 현재 Python 환경에는 `torch`, `transformers`, `sentencepiece`가 설치되어 있지 않다.

| 후보 | 비용·라이선스 | 크기·품질 위험 | 상태 |
| --- | --- | --- | --- |
| [sappho192/gemma3-multilingual-translator-270m](https://huggingface.co/sappho192/gemma3-multilingual-translator-270m) | 무료, Apache-2.0 | 일본어·한국어를 직접 지원하고 가중치 약 536MB. 비교적 새 모델이라 대량 적용 전 표본 검수가 필요하며 실행 라이브러리까지 포함하면 임시 용량이 더 큼 | 추천 후보, 사용자 승인 대기 |
| [facebook/nllb-200-distilled-600M](https://huggingface.co/facebook/nllb-200-distilled-600M) | 무료, CC BY-NC 4.0 | 약 2.5GB, 연구·비상업 조건이며 모델 카드상 프로덕션 배포 용도가 아님 | 제외: 현재 개인 학습 카드에는 쓸 수 있으나 용량·조건이 불필요하게 큼 |
| [Argos Translate](https://github.com/argosopentech/argos-translate) | 실행 코드는 MIT/CC0 | 일본어·한국어를 지원하지만 개별 언어 모델 패키지의 라이선스가 명시되지 않았다는 공개 이슈가 남아 있고 품질 손실을 공식 README가 경고함 | 제외 |

- 번역 모델을 채택하더라도 생성 과정의 임시 도구로만 사용하며 Anki 런타임 의존성으로 남기지 않는다.
- 전체 반영 전 일본어 원문과 생성된 한국어 해석의 표본을 검사하고, Anki MCP `dry_run`을 통과한 경우에만 쓰기 작업을 한다.
