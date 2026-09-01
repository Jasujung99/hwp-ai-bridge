# 클라이언트 연결

모든 예제는 stdio MCP 서버를 사용합니다. 즉, AI 클라이언트가 같은 PC에서
`hwpctl` 또는 `hwp-live-safe` 명령을 실행합니다. 토큰이나 외부 터널은 필요하지 않습니다.

## 공통 규칙

1. 먼저 선택한 엔진의 명령이 터미널에서 실행되는지 확인합니다.
2. 아래 예제를 기존 설정에 **병합**합니다. 기존 MCP 서버를 지우지 마세요.
3. 직접·안전·혼합 중 하나의 예제를 선택합니다.
4. AI 클라이언트를 완전히 재시작합니다.
5. 새 문서 또는 복사본에서 한 번 검증합니다.

예제에는 절대 경로가 없습니다. 명령을 PATH에 설치하지 않은 개발 환경에서는 해당
클라이언트의 설정 파일에 경로를 직접 넣기보다, 엔진의 개발용 실행 안내를 따르거나
배포용 설치를 완료한 뒤 연결하는 편이 안전합니다.

안전 모드 예제는 `hwp-live-safe v0.3.0-rc.1`의 태그된 소스 체크아웃을 `uv tool install .`
으로 설치해 `hwp-live-safe` 명령이 PATH에 있는 상태를 전제로 합니다. PyPI 패키지 설치를
전제로 하지 않습니다.

## Codex

[`integrations/codex`](../integrations/codex)의 선택한 `.toml` 내용을 기존
`~/.codex/config.toml`에 병합합니다. Codex의 테이블 이름은 중복될 수 없으므로 같은
서버 항목이 있으면 하나만 유지하세요.

## Claude Code

[`integrations/claude-code`](../integrations/claude-code)의 선택한 JSON을 프로젝트
`.mcp.json` 또는 Claude Code가 사용하는 MCP 설정에 병합합니다. JSON은 주석을
지원하지 않으므로 쉼표와 중괄호를 주의하세요.

## Cursor

[`integrations/cursor`](../integrations/cursor)의 선택한 JSON을 프로젝트
`.cursor/mcp.json` 또는 Cursor 사용자 MCP 설정에 병합합니다.

## Grok Build / 로컬 CLI

[`integrations/grok-build`](../integrations/grok-build)의 선택한 TOML을 Grok Build가
읽는 프로젝트 `.grok/config.toml` 또는 사용자 `~/.grok/config.toml`에 병합합니다.
Grok Build는 `.mcp.json`도 호환 형식으로 읽을 수 있지만, 이 허브는 Grok의 자체 TOML
형식을 기본 예제로 사용합니다. 로컬에서 실행되는 Grok Build/CLI는 stdio 명령과
`localhost`에 직접 접근할 수 있으므로, 이 구성에는 터널이 필요 없습니다.

웹에서만 작동하는 원격 AI에 한글을 연결하려는 경우는 별도 보안 설계가 필요합니다.
기본 예제는 외부 네트워크 노출을 만들지 않습니다.

## 실행 전 확인

- 직접 모드: 한글을 열고 `hwpctl status`를 먼저 실행합니다.
- 안전 모드: `hwp-live-safe`가 보이는 새 문서를 열 수 있는지 확인합니다.
- 혼합 모드: 한 번에 한 엔진만 한글을 수정하도록 AI에게 명시합니다.
- 중요한 변경: AI가 적용 전에 범위와 변경 내용을 보여 주도록 요청합니다.
