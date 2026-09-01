# 호환성

| 항목 | 직접 모드 (`hwpctl`) | 안전 모드 (`hwp-live-safe`) |
| --- | --- | --- |
| 운영체제 | Windows | Windows |
| 대상 앱 | 한글 오피스 2022 | 한글 오피스 2022 |
| 주요 연결 방식 | `pyhwpx` / COM | 허용 목록 기반 COM 작업자 |
| 문서 대상 | 사용자가 열어 둔 문서 | 엔진이 새로 연 문서 |
| 기본 저장 정책 | 자동저장 없음, 새 이름 저장 권장 | 열기·저장·닫기 도구 미제공 |
| AI 연결 방식 | stdio MCP | stdio MCP |

## 검증 조합 기록

릴리스 판단에 사용한 실기 결과만 아래 표에 추가합니다. “계획”, “모의 객체 테스트”와
“한글 2022 실기 통과”를 구분하고, 실제 문서명이나 PC명은 기록하지 않습니다.

| 날짜 | Windows | 한글 빌드 | Python | `pyhwpx` | AI 클라이언트 | 엔진 버전 | 결과 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-09-02 | Windows 10 Home 22H2 `22621.4317` | Hancom Office 2022 `12.0.0.850` | `3.12.13` | 해당 없음 — native COM worker | Codex CLI `0.147.0` / MCP Python SDK `2.1.1` | [`hwp-live-safe v0.3.0-rc.1`](https://github.com/Jasujung99/hwp-live-safe/releases/tag/v0.3.0-rc.1); tagged source checkout + `uv tool install .` | native safe-mode manual gate 기록: 새 문서, text/table preview·apply·read-back, 더미 프로필, stale 거부, 안전 Undo, 짧은 foreground 입력; 금지된 파일 작업 도구 없음 |

위 기록은 `hwp-live-safe`의 native safe mode와 별도로 범위를 제한한 foreground
입력에만 적용됩니다. 기존 열린 문서를 다루는 `hwpctl` 직접 모드와 두 엔진을 함께
쓰는 혼합 모드의 일반 호환성을 뜻하지 않습니다.

## 추가 실기 검증이 필요한 항목

한글의 설치 방식과 열린 창 상태는 PC마다 다를 수 있습니다. 다음은 배포 전에 실제
한글 2022 환경에서 확인해야 합니다.

- 기존 한글 창 연결
- 여러 한글 창 중 정확한 문서 선택
- Undo 단위와 사용자의 수동 편집 간 상호작용
- 표·셀 이동 및 표 서식
- 차트 삽입과 대화상자 억제
- 설치된 글꼴의 한글·영문·한자 혼합 적용

검증되지 않은 항목은 “지원”이라고 단정하지 않고, 버전·환경·재현 절차와 함께
제한 사항으로 남깁니다.
