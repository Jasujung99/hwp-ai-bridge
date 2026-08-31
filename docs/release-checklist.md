# 공개 순서와 체크리스트

## 1. `hwpctl` 직접 모드 공개

- [ ] README에서 개인 PC 이름, 절대 경로, 사용자명을 제거
- [ ] 실제 한글 2022에서 기존 창 연결과 기본 편집을 검증
- [ ] 저장·덮어쓰기·닫기 보호 장치를 문서화
- [ ] Undo와 다중 창의 제한을 `KNOWN_LIMITATIONS.md`에 명시
- [ ] 개인정보 없는 샘플과 테스트를 제공
- [ ] 라이선스·보안 신고 경로·비제휴 고지를 점검

## 2. `hwp-live-safe` 안전 모드 공개

- [ ] 공개 패키지 이름과 `hwp-live-safe` CLI를 확정
- [ ] 개인 로컬 프로필과 예제 파일을 분리
- [ ] 미리보기·승인·문서 변경 감지의 행동을 테스트
- [ ] 열기·저장·닫기·임의 액션을 제공하지 않는 기본값을 재확인
- [ ] 32비트 한글 2022 연결을 실제 PC에서 검증

## 3. 이 허브 공개

- [x] 두 엔진의 공개 URL과 버전 호환표 형식을 추가
- [ ] Codex·Claude Code·Cursor·Grok Build 예제를 각각 확인
- [ ] 예제에서 토큰·모든 드라이브 절대 경로·UNC 경로·프로필·사용자 이름이 없는지 검사
- [ ] 직접·안전·혼합 모드의 실제 범위를 명확히 표시
- [ ] validator 단위 테스트, `python scripts/validate_repository.py`, `scripts/Test-IntegrationExamples.ps1`, `git diff --check` 통과
- [ ] GitHub Discussions와 private vulnerability reporting 활성화
- [ ] `main` 브랜치 규칙과 필수 `Public baseline / validate` 검사 적용

## 4. 공용 라우터·설치기 (후속)

- [ ] 두 엔진의 명령 모델과 버전 호환성 확정
- [ ] 문서 대상 식별·잠금·변경 감지 설계
- [ ] 승인된 변경 계획만 전달하는 정책 구현
- [ ] 설치기의 설정 백업·병합·되돌리기 설계
- [ ] 복수 AI 클라이언트 동시 사용 시나리오 검증

상세 종료 조건은 [ROADMAP](../ROADMAP.md)과 [마일스톤](milestones.md)을 따릅니다.
