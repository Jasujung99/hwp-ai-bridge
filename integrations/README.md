# MCP 설정 예제

각 폴더에는 세 가지 방식의 설정이 있습니다.

| 파일 이름 | 등록하는 서버 |
| --- | --- |
| `direct.*` | `hwpctl`만 등록 |
| `safe.*` | `hwp-live-safe`만 등록 |
| `hybrid.*` | 둘 다 등록 |

모든 파일은 예제입니다. 기존 설정 전체를 덮어쓰지 말고, `mcpServers` 또는
`mcp_servers` 안의 해당 항목만 병합하세요.

공통 원칙:

- 명령은 PATH에 설치된 `hwpctl`과 `hwp-live-safe`를 사용합니다.
- 예제에는 사용자 폴더, 토큰, HTTP 주소, 프로필 값이 없습니다.
- 동일한 한글 문서에는 한 번에 한 엔진만 쓰세요.
- 직접 모드에서는 `HWPCTL_CLIENT` 값이 잠금 관련 진단에만 쓰입니다.

연결 절차는 [클라이언트 연결 문서](../docs/client-setup.md)를 참고하세요.

엔진 저장소:

- 직접 모드: [`Jasujung99/hwpctl`](https://github.com/Jasujung99/hwpctl)
- 안전 모드: [`Jasujung99/hwp-live-safe`](https://github.com/Jasujung99/hwp-live-safe)
