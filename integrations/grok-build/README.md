# Grok Build / 로컬 CLI

로컬에서 실행되는 Grok Build/CLI는 이 PC의 명령줄과 localhost에 접근할 수 있습니다.
따라서 `hwpctl`과 `hwp-live-safe`에는 다른 데스크톱 클라이언트와 같은 stdio MCP
설정을 사용합니다.

1. `direct.config.toml.example`, `safe.config.toml.example`, `hybrid.config.toml.example` 중 하나를 고릅니다.
2. 그 내용을 Grok Build가 읽는 프로젝트 `.grok/config.toml` 또는 사용자 `~/.grok/config.toml`에 병합합니다.
3. Grok Build를 재시작하고, 먼저 복사본 문서에서 한 도구만 검증합니다.

파일 이름은 `direct.config.toml.example`, `safe.config.toml.example`,
`hybrid.config.toml.example`입니다. `.mcp.json`은 Grok Build가 호환 형식으로 읽을 수
있지만, 이 예제는 Grok의 자체 TOML 형식을 우선합니다.

이 설정은 원격 웹 서비스에 로컬 한글을 공개하지 않습니다. 원격 접근을 별도로
구성하려면 인증·localhost 바인딩·사용자 승인 정책을 먼저 설계해야 합니다.
