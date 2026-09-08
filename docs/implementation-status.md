# 구현 기준과 실험 경계

2026-09-08 정리. 이 허브는 편집 엔진을 복제하거나 새 작성 엔진을 연결하지 않는다.

## 기준 구현

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
