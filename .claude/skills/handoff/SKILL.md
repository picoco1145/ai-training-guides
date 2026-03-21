---
name: handoff
description: |
  세션/섹션 종료 시 작업 요약 + 다음 할 일을 정리하여 핸드오프 노트를 생성한다.
  다음 세션에서 이 노트를 보고 바로 흐름을 파악하고 이어서 작업할 수 있게 한다.
  Triggers: /handoff, 핸드오프, 정리해줘, 여기까지, 세션 마무리, 오늘은 여기까지, wrap up, checkpoint
tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Handoff — 세션/섹션 핸드오프 노트

> 작업 구간이 끝날 때 **무엇을 했고, 어디까지 왔고, 다음에 뭘 해야 하는지**를 정리한다.
> 다음 세션의 Claude(또는 사람)가 이 노트만 읽으면 10초 안에 컨텍스트를 파악할 수 있어야 한다.

---

## Workflow

### Step 1: 컨텍스트 수집

현재 프로젝트 상태를 파악한다:

```bash
# git 상태
git status --short 2>/dev/null
git log --oneline -5 2>/dev/null

# 이전 핸드오프 노트 확인
ls -t outputs/handoff/ 2>/dev/null | head -3
```

그리고 다음을 수집:
- 이번 세션에서 변경된 파일 목록
- 현재 대화에서 다룬 주요 주제/태스크
- 완료된 것과 미완료된 것
- 발생한 이슈/블로커

### Step 2: 핸드오프 노트 작성

`references/handoff-template.md` 형식을 따라 작성한다.

**작성 규칙:**
- **완료 항목**: 체크박스 `[x]`로 표시, 커밋 해시가 있으면 포함
- **미완료 항목**: 체크박스 `[ ]`로 표시, 왜 못 했는지 한 줄로 설명
- **다음 할 일**: 우선순위 순으로 번호 매김, 각 항목에 예상 난이도 표시
- **컨텍스트 메모**: 다음 세션에서 알아야 할 비자명한 정보 (결정 사항, 주의점, 디버깅 단서)
- **길이**: 전체 50줄 이내로 간결하게

### Step 3: 저장

```
outputs/handoff/handoff_{YYYY-MM-DD}_{HHmm}.md
```

`outputs/handoff/` 디렉토리가 없으면 생성한다.

저장 후 사용자에게 요약을 보여준다:

```
--- Handoff Note ---
완료: {N}개 | 미완료: {M}개 | 다음 할 일: {K}개
저장: outputs/handoff/handoff_{timestamp}.md

다음 세션 시작 시: "핸드오프 노트 읽어줘" 또는 이 파일을 직접 참조
```

### Step 4: CLAUDE.md 업데이트 제안 (선택)

이번 세션에서 발견한 것 중 CLAUDE.md에 추가할 만한 것이 있으면 제안한다:
- 새로 발견한 gotcha
- 변경된 빌드/테스트 명령어
- 확립된 코딩 패턴

**직접 수정하지 말고 제안만 한다.**

---

## 다음 세션 시작 시 사용법

다음 세션에서 Claude에게:
```
outputs/handoff/ 폴더에서 가장 최근 핸드오프 노트를 읽고 이어서 작업해줘
```

또는 CLAUDE.md에 다음을 추가해두면 자동으로 읽는다:
```markdown
## 이전 세션 핸드오프
@outputs/handoff/handoff_{latest}.md
```

---

## References
- **`references/handoff-template.md`** — 핸드오프 노트 마크다운 템플릿
