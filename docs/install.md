# 설치

## 공통 준비

- Windows PC
- 한글 오피스 2022
- Python 3.10 이상 (`hwp-live-safe` 개발 환경은 Python 3.11 이상)
- Git

설치 전 중요한 한글 문서는 복사해 두세요. 이 허브와 엔진은 자동 백업 도구가 아닙니다.

## 직접 모드 설치

```powershell
git clone https://github.com/Jasujung99/hwpctl.git
Set-Location hwpctl
uv tool install ".[windows]"
hwpctl --help
```

2026-09-03 Windows 검증에서는 임시 `UV_TOOL_DIR`/`UV_TOOL_BIN_DIR`에 최신 소스를
설치해 독립 환경과 `hwpctl` 실행 파일 생성을 확인했습니다. 실제 연결 확인은 대상
한글 창을 활성화하고 `hwpctl open`으로 재고정한 뒤 `hwpctl status`를 실행합니다.
`status`가 한글을 찾지 못하면 한글 2022 설치, Windows 환경, 보안 모듈 안내를 먼저
확인하세요. MCP 설정은 [클라이언트 연결](client-setup.md)을 따릅니다.

이 명령은 현재 소스 체크아웃을 uv의 독립 도구 환경에 설치하고 `hwpctl` 실행 파일을
PATH에 연결합니다. 패키지 이름만으로 레지스트리에서 설치하는 명령과는 다릅니다.
전역 Python에 `pip install -e`로 설치하면 다른 MCP SDK와 충돌할 수 있으므로 권장하지
않습니다.

직접 엔진은 아직 허브가 고정할 공개 릴리스 태그가 없어 최신 `main` 소스 설치를
안내합니다. 재현성이 필요한 배포에서는 검증한 hwpctl 커밋을 별도로 고정하세요.
안전 엔진은 혼합 모드 안전 경계가 바뀐 지점을 명확히 하기 위해 아래 커밋을 고정합니다.

## 안전 모드 소스 설치

혼합 모드 공존과 안전 수정 #10–#15가 필요한 현재 권장 기준은 `hwp-live-safe`
커밋 `384f84e`입니다. 새 태그가 나오기 전까지 재현 가능한 커밋을 고정해 독립 환경에
설치합니다.

```powershell
git clone https://github.com/Jasujung99/hwp-live-safe.git
Set-Location hwp-live-safe
git checkout 384f84e
uv tool install .
hwp-live-safe
```

[`v0.3.0-rc.1`](https://github.com/Jasujung99/hwp-live-safe/releases/tag/v0.3.0-rc.1)은
2026-09-02 수동 검증 기록을 보존하는 태그지만, 표 탈출·서식 복원·제한 Undo·워커
타임아웃·혼합 모드 공존 수정 전 버전입니다. 이 태그는 열린 한글 창이 있으면 시작을
거부하므로 혼합 모드에는 사용하지 않습니다. 개발·테스트에만 `uv sync --extra dev`를
사용합니다. PyPI 배포를 하지 않으므로 `uv tool install hwp-live-safe`나
`pip install hwp-live-safe`처럼 패키지 이름만으로 설치하지 않습니다.

## 둘 다 설치하기

직접 모드와 안전 모드의 설치를 각각 마친 뒤, 같은 AI 클라이언트에 `hybrid` 예제를
병합합니다. 두 엔진을 같은 Python 가상환경에 억지로 넣지 마세요. 현재는 MCP SDK의
주 버전이 달라 의존성이 충돌할 수 있습니다.

두 `uv tool install` 명령은 각각 별도 환경을 만들면서도 `hwpctl`과
`hwp-live-safe` 명령을 PATH에 노출하므로, 통합 예제의 경로 없는 `command` 값을 그대로
사용할 수 있습니다.

## 제거

엔진별 설치 방법에 맞춰 제거합니다. 허브는 설정 예제와 문서만 포함하므로, AI 클라이언트
설정에서 해당 MCP 서버 항목을 제거하면 연결이 중단됩니다. 프로필·토큰·문서 사본은
사용자가 저장한 위치에서 별도로 관리하세요.
