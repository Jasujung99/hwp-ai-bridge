# 구현 기준과 실험 경계

2026-09-26 통합 기준. 이 허브는 편집 엔진을 복제하거나 safe에 작성 엔진을 연결하지 않는다.

## 기준 구현

폴더 조사 후속 변경과 실험적 작성·변환 기반은
[hwpctl PR #24](https://github.com/Jasujung99/hwpctl/pull/24)로 main에 병합됐다.
기준 커밋은 [`4f8fe55`](https://github.com/Jasujung99/hwpctl/commit/4f8fe55714a723f26466cb75ba77cfb64ec38968)다.
[main 작성·분석 안내](https://github.com/Jasujung99/hwpctl/blob/main/docs/HWPX_AUTHORING.md)와
[후속 후보의 승격/보류 결과](https://github.com/Jasujung99/hwpctl/blob/main/docs/INTEGRATION_CANDIDATES.md)를
기준으로 한다. 기존 대장은 모든 작업창의 개발을 포괄한다는 뜻이 아니다.

`hwpctl`의 [통합 대장](https://github.com/Jasujung99/hwpctl/blob/main/docs/INTEGRATION_STATUS.md)이
기능별 원본 커밋·기준 코드·공식 진입점·테스트·제한의 단일 기준이다.
[검증 기록](https://github.com/Jasujung99/hwpctl/blob/main/docs/INTEGRATION_VERIFICATION.md)은
자동 회귀와 한/글 실기, 시각 비교를 구분한다.

| 범위 | 제공 상태 | 진입점·제한 |
| --- | --- | --- |
| 네이티브 문단·런·실제 표·셀 | hwpctl main | 기존 Engine/CLI/MCP. 본문을 렌더링 그림으로 대체하지 않음 |
| 표 격자·전역 안 여백·셀 탐색·부모 표 탈출 | 참조 브랜치 구현을 main에 통합 | `set_table_grid`, `set_table_inside_margin`, `move_to_cell`, `exit_table`; 병합 전 격자 및 문맥 검증 |
| 문자권 글꼴·문단 흐름 | main | `font_slots`, `insert_paragraph(terminate=False)`; 환경별 글꼴 설치 필요 |
| 조판부호·서식 정의 정리 | main 유지 | `set_edit_marks`; 서식 정리는 내부 순수 함수, 무차별 빈 문단 삭제 도구 아님 |
| HWPX 새 문서·문단·실제 표 래퍼 | main 라이브러리 | `hwpctl.hwpx`; 일반 작성 CLI를 신설한 것은 아님 |
| 참조 정규화·구조 비교 | main의 실험 라이브러리 API | `hwpctl.reference`; 미지원 개체는 inconclusive, 구조 성공 ≠ 시각 동일 |
| FAQ 공개 명령 작성 드라이버 | 공식 합성 예제 | [사용 안내](https://github.com/Jasujung99/hwpctl/blob/main/examples/FAQ_002_NORMALIZED_SPEC.md), [합성 명세](https://github.com/Jasujung99/hwpctl/blob/main/examples/specs/faq.synthetic.json); 범용 importer·자동 조판 엔진 아님 |
| 순서 있는 v1/v2 작성·참조 변환 | main 실험 기능 | `build_document`, `reference_to_spec`; 손실 시 실행 명세 미게시. 새 작성기의 네이티브 실기·ChartML 보존은 미완료 |
| HAEON·공고문 전용 보정·포스터 좌표 우회 | 실험 보관 | 개인 템플릿·내부 API·문서별 보정의 검증 전 기본 동작 승격 금지 |

HAEON 글상자·사각형 조합 표를 네이티브 표로 분류하지 않는다. 로고·낙관·삽화는
허용된 별도 그림일 수 있으므로 `그림 0개`를 공통 성공 기준으로 쓰지 않는다.

## 4계층은 저장소 4개가 아니다

1. 패키지·입출력: HWPX 파트·참조·저장과 작성 어댑터.
2. 문서 모델: 문단·런·표·셀·도형 의미와 입력 변환.
3. 구성·조판: 스타일·단위·배치·표 크기·문서 흐름.
4. 검증: 내용·실제 개체·서식·범위·참조 비교.

기존 import/API를 유지하며 책임을 명확히 한 것이다. 참조 관찰 모델과 FAQ 작성
명세는 다른 목적이며 강제 통합하지 않았다. 창 생성·저장·닫기·고정·잠금·Undo는
4계층 바깥의 기존 Engine/HangulCanvas 실행 관리에 남는다.

## 안전 엔진 계약 유지

`hwp-live-safe`의 현재 main 기준은
[`db59417`](https://github.com/Jasujung99/hwp-live-safe/commit/db594178f3e8e625b71451bb555891d2727beca4)이다. 자동화 소유 새 문서,
preview → revision 확인 → 승인된 apply, stale 거부, 제한 Undo 계약을 유지한다.
이번 정리는 safe에 작성 드라이버를 연결하거나 저장·열기·닫기 도구를 추가하지 않는다.
두 엔진의 환경·대상 문서·Undo·잠금은 자동 공유하지 않는다.

[safe PR #17](https://github.com/Jasujung99/hwp-live-safe/pull/17)은 main에 병합돼 소유 문서의
preview·revision·apply·Undo 계약을 위한 합성 검증과 native 검증 게이트를 보강한다.
fake 테스트, 실제 한/글 COM 검증, 화면을 확인하는 수동 검증은 서로 다른 증거로
기록한다. Windows 3.11/3.12 CI와 main CI가 통과했고, 수동 화면 검증은 수행하지
않았다. 개인 프로필이나 기존 foreground 문서는 검증 대상으로 사용하지 않는다.
해당 PR은 hwpctl 작성 엔진을 연결하거나 저장·닫기 명령을 추가하지 않는다.

## 통합된 기준의 계층 연결

| 계층/범위 | hwpctl main의 기준 구현 | hub / safe의 책임 |
| --- | --- | --- |
| 패키지·입출력 | HWPML/HWPX/캡처 번들 변환, 포함 자산과 HWP/HWPX 저장 어댑터 | hub는 확인된 진입점만 안내. 입력이나 출력을 보관하지 않음 |
| 문서 모델 | 순서 있는 v2 작성 명세, v1 호환, 다중 구역·셀 내부·중첩 개체와 손실 보고 | 참조 관찰 모델과 작성 명세를 같은 스키마로 오인하지 않음 |
| 구성·조판 | 병합 격자, 생략·명시·상속 구분, 쪽 흐름과 floating 개체 | 문서별 좌표·여백 보정을 전역 기본값으로 만들지 않음 |
| 검증 | 독립 합성 원본·기대값, 원시 단위와 실패 경로; 새 작성기의 저장·재열기 실기는 미완 | safe는 자기 preview·revision·Undo 계약을 별도로 검증 |
| 실행 관리 | 새 소유 COM 세션, 전체 사전 검증, 실패 위치와 정리 결과 | 세션·창·잠금·Undo·revision을 safe와 공유하지 않음 |

hwpctl의 `reference_to_spec`과 `build_document`는 Engine·CLI·MCP에서 호출할 수 있는
실험 기능이다. [v2 합성 명세](https://github.com/Jasujung99/hwpctl/blob/main/examples/specs/authoring-v2.synthetic.json)로
`hwpctl build_document examples/specs/authoring-v2.synthetic.json output/synthetic.hwpx --dry-run`을
실행하면 COM 없이 명령 계획을 확인할 수 있다. 일반 회귀 439개와 Windows/Linux CI가
통과했지만, 개발 환경의 COM 활성화 멈춤으로 새 작성기의 저장·재열기·편집·Undo는
미검증이다. 원본 ChartML·일부 쪽 번호/탭/문자 배경/특수 공백 변환도 미완료이며
[hwpctl #25](https://github.com/Jasujung99/hwpctl/issues/25)에서 이어간다.
구조 검사 성공을 시각 동일성으로 해석하지 않는다.
이 hub PR은 엔진 설치나 MCP 설정을 자동으로 바꾸지 않는다.

허브의 설치 안내는 병합된 엔진 커밋과 main의 실제 진입점을 기준으로 한다.
검증되지 않은 HAEON·포스터 전용 보정이나 범용 오프라인 자동 조판 엔진을
제공한다고 주장하지 않는다.
