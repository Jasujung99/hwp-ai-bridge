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
py -m pip install -e ".[windows]"
hwpctl status
```

`status`가 한글을 찾지 못하면 한글 2022 설치, Windows 환경, 보안 모듈 안내를 먼저
확인하세요. MCP 설정은 [클라이언트 연결](client-setup.md)을 따릅니다.

공개 패키지 릴리스 전에는 `pipx install`이나 `uv tool install` 명령을 배포용 설치법으로
안내하지 않습니다. 태그된 릴리스와 설치 경로가 준비된 뒤에만 추가합니다.

## 안전 모드 태그된 소스 설치

`hwp-live-safe`는 [GitHub pre-release `v0.3.0-rc.1`](https://github.com/Jasujung99/hwp-live-safe/releases/tag/v0.3.0-rc.1)의
태그된 소스를 독립 환경에 설치합니다.

```powershell
git clone --branch v0.3.0-rc.1 --depth 1 https://github.com/Jasujung99/hwp-live-safe.git
Set-Location hwp-live-safe
uv tool install .
hwp-live-safe
```

개발·테스트에만 `uv sync --extra dev`를 사용합니다. 초기 배포 단계에서는 PyPI
배포를 하지 않으므로 `uv tool install hwp-live-safe`나 `pip install hwp-live-safe`처럼
패키지 이름만으로 설치하지 않습니다.

## 둘 다 설치하기

직접 모드와 안전 모드의 설치를 각각 마친 뒤, 같은 AI 클라이언트에 `hybrid` 예제를
병합합니다. 두 엔진을 같은 Python 가상환경에 억지로 넣지 마세요. 현재는 MCP SDK의
주 버전이 달라 의존성이 충돌할 수 있습니다.

## 제거

엔진별 설치 방법에 맞춰 제거합니다. 허브는 설정 예제와 문서만 포함하므로, AI 클라이언트
설정에서 해당 MCP 서버 항목을 제거하면 연결이 중단됩니다. 프로필·토큰·문서 사본은
사용자가 저장한 위치에서 별도로 관리하세요.
