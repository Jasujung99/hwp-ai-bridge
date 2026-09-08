# 구현 기준과 실험 경계

2026-09-08 정리. 이 허브는 편집 엔진을 복제하거나 새 작성 엔진을 연결하지 않는다.

## 기준 구현

폴더 조사 후속 변경은 [hwpctl PR #24](https://github.com/Jasujung99/hwpctl/pull/24)의
**제안 상태**이며, 병합 전에는 main 제공 기능으로 세지 않는다.
[PR 브랜치의 작성·분석 안내](https://github.com/Jasujung99/hwpctl/blob/integration/promote-reference-candidates/docs/HWPX_AUTHORING.md)와
[후속 후보의 승격/보류 결과](https://github.com/Jasujung99/hwpctl/blob/integration/promote-reference-candidates/docs/INTEGRATION_CANDIDATES.md)를
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

`hwp-live-safe`의 검증 기준은 계속 `384f84e`다. 자동화 소유 새 문서,
preview → revision 확인 → 승인된 apply, stale 거부, 제한 Undo 계약을 유지한다.
이번 정리는 safe에 작성 드라이버를 연결하거나 저장·열기·닫기 도구를 추가하지 않는다.
두 엔진의 환경·대상 문서·Undo·잠금은 자동 공유하지 않는다.

[safe PR #17](https://github.com/Jasujung99/hwp-live-safe/pull/17)은 native 수동 검증
하네스만 제안한다. 개인 프로필/foreground 선택은 제외하고 명시적 YES 확인을 요구한다.
자동 회귀 45개·fake stdio 15 tools·공개 파일/패키지 검사를 통과했지만, 실제 화면을
확인하는 수동 실기는 이번 작업에서 실행하지 않았다. 해당 PR은 저장/닫기/작성 엔진
연결을 추가하지 않는다. 이 hub PR은 두 엔진 PR과 독립적으로 경계를 문서화한다.

## 후속 후보 PR의 계층 연결

| 계층/범위 | hwpctl PR 제안 | hub / safe의 책임 |
| --- | --- | --- |
| 패키지·입출력 | HWPX 런·문단·실제 표·쪽 설정 / 참조 HWPML·PDF·포함 그림 번들 | hub는 진입점만 안내. 참조 내보내기를 작성 경로로 추천하지 않음 |
| 문서 모델 | 정적 참조 분석, 미지원 제어·누락 서식·다중 구역/표 차단 | 전체 FAQ importer와 구별. 기존 작성 명세 preflight는 별도 |
| 구성·조판 | HU/mm/pt 변환, 기존 layout.py 유지 | 문서별 여백 1/2·좌표 보정·기본값을 전역화하지 않음 |
| 검증 | 격자 정확/정보 부족/모순 구분, 표/페이지/내보내기 회귀 | safe는 자기 계약의 별도 수동 게이트만 승격 |
| 실행 관리 | 기존 Engine/HangulCanvas 및 격리 COM 소유권 | 세션·창·잠금·Undo·revision 공유 없음 |

hwpctl 로컬 자동 회귀는 339 passed, 15 skipped다. 한/글 opt-in은 12 passed이나
참조 export 종료에서 COM RPC `0x800706ba` 진단이 반복되어 깨끗한 종료 검증으로
표시하지 않는다. PR의 검증 기록과 CI 결과를 확인하고, 구조 검사 성공을 시각 동일성으로
해석하지 않는다. 이 hub PR은 엔진 설치 버전이나 MCP 설정을 자동으로 바꾸지 않는다.

FAQ 전체 작성 명세 변환, 복잡 병합·페이지 자동 조판, 형식별 생략/기본값 변환,
HAEON/포스터 전용 어댑터와 구형 복제본 추가 중복 감사는 후속으로 남는다.
