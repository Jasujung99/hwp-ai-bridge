# 프로젝트 마일스톤

GitHub Milestone 제목은 간결하게 `0.1`, `0.2`, `0.3`으로 관리합니다. 아래 제목의
설명 문구는 각 버전의 주제이며, 종료 조건을 충족한 이슈만 닫습니다.

## `0.1 Public Hub`

- 네 클라이언트의 direct/safe/hybrid 설정 예제가 자동 검사를 통과한다.
- 두 엔진의 실제 공개 URL, 설치법, 책임 경계가 README와 아키텍처 문서에서 일치한다.
- 혼합 모드가 순차 선택 방식이며 자동 전달·공용 잠금·공용 Undo가 없음을 명시한다.
- Discussions, 엔진별 Issues, 비공개 보안 신고의 라우팅이 연결된다.
- 한글 2022 수동 검증 결과를 기록할 호환성 형식이 준비된다.

## `0.2 Windows Installer`

- direct/safe/both 선택 설치와 제거를 지원한다.
- 두 엔진을 별도 환경에 설치하고 각 실행 명령을 독립적으로 검사한다.
- Codex, Claude Code, Cursor, Grok Build의 기존 설정을 백업·병합·복구한다.
- 부분 실패와 재실행이 기존 설정 또는 문서를 손상시키지 않는다.
- 로그와 진단 자료에 토큰·프로필·문서 본문이 남지 않는다.

## `0.3 Local Router`

- 사용자가 대상 창과 작업 모드를 확인할 수 있다.
- 한 번에 한 엔진만 대상 문서에 쓰도록 잠금을 관리한다.
- 승인 이후 대상 문서가 달라지면 적용을 거부한다.
- 각 엔진은 독립 프로세스로 실행되며 의존성을 공유하지 않는다.
- 실패·취소·클라이언트 종료 후 잠금 복구를 실기 검증한다.

## 운영 방식

- 로드맵·설치·조합 질문은 [Discussions](https://github.com/Jasujung99/hwp-ai-bridge/discussions)에서 다룬다.
- 구현 가능한 단일 변경은 해당 Milestone의 Issue로 전환한다.
- 엔진 자체 결함은 [`hwpctl`](https://github.com/Jasujung99/hwpctl/issues) 또는
  [`hwp-live-safe`](https://github.com/Jasujung99/hwp-live-safe/issues)로 이동한다.
- Milestone 종료 전 [릴리스 체크리스트](release-checklist.md)를 다시 실행한다.
