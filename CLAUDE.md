# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Training Guide Team

팀원 교육 실습 가이드를 협업으로 기획 → 작성 → 검수 → 배포하는 프로젝트.
최종 산출물은 Notion 페이지 (텍스트 블록 + 이미지 블록 번갈아 배치).

## Commands

| Command | Description |
|---------|-------------|
| `/new-guide` | 새 교육 가이드 생성 (기획→점검→작성→검수→배포) |
| `/batch` | 여러 가이드 일괄 생성 |
| `/review-guide` | 가이드 초보자 관점 검수 |
| `/dashboard` | 전체 가이드 현황 대시보드 |
| `/handoff` | 세션 마무리 핸드오프 노트 |
| `/resume` | 이전 세션 이어받기 |
| `/status` | 프로젝트 현황 확인 |

## Architecture

```
templates/     # 기획서·체크리스트 양식
outputs/       # 모든 산출물 (가이드MD, 이미지, 검수리포트)
registry/      # guide-registry.json (가이드 등록대장, 단일 진실 소스)
scripts/       # Python 유틸리티 (이미지 생성, 캡처, Notion 업로드)
```

## Key Files

- `registry/guide-registry.json` — 모든 가이드의 상태/담당자/URL 추적
- `outputs/spec.md` — planner가 관리하는 현재 작업 명세
- `templates/guide-brief.md` — 가이드 기획서 표준 양식
- `templates/review-checklist.md` — 초보자 관점 검수 체크리스트
- `scripts/generate_image.py` — Gemini Imagen API (개념도/흐름도용)
- `scripts/capture_screen.py` — /browse 캡처 + PIL 어노테이션 (UI 스크린샷용)
- `scripts/upload_to_notion.py` — Notion File Upload API 래퍼

## Agents

- **planner** (Opus) — 링크/내용 분석 → 과제 도출 → 기획서 → 사용자 점검
- **content-writer** (Sonnet) — 콘텐츠 작성 + 이미지 지시서 (위치, 유형, 프롬프트)
- **image-producer** (Sonnet) — 이미지 소스 판단(캡처 vs 생성) → 제작 → 어노테이션
- **image-reviewer** (Sonnet) — 이미지 품질 검수 전담: 내용 정합성·어노테이션 정확성·캡처 품질 3항목 점검. 문제 발견 시 image-producer에게 재작업 요청
- **reviewer** (Sonnet) — 초보자가 그대로 따라할 수 있는지 검수
- **publisher** (Sonnet) — Notion File Upload API로 이미지 직접 업로드 + 블록 구성
- **debugger** (Sonnet) — API 에러, 이미지 생성 실패 분석

## Skills

- **guide-create** — 단일 가이드 전체 파이프라인
- **guide-batch** — 여러 가이드 일괄 생성
- **guide-review** — 초보자 관점 검수
- **guide-status** — 현황 대시보드
- **handoff** — 세션 핸드오프

## Workflow

```
사용자: 링크/내용 제공
  ↓
planner → 과제 도출 + 기획서
  ↓
★ 사용자 점검 ★ (반드시 승인 후 진행)
  ↓
content-writer → 콘텐츠 + 이미지 지시서
  ↓
image-producer → 이미지 제작 (Track A: 캡처 / Track B: Gemini)
  ↓
★ image-reviewer → 이미지 품질 검수 ★ (반드시 통과 후 진행)
  - 내용 정합성: 이미지가 해당 단계 텍스트와 일치하는가
  - 어노테이션 정확성: 레이블 한국어·화살표 위치 정확한가
  - 캡처 품질: 로딩 중·빈 응답·플레이스홀더 없는가
  ↓ Pass (Fail 시 image-producer 재작업 → 재검수)
reviewer → 초보자 관점 검수
  ↓ Pass
publisher → Notion 페이지 (이미지 직접 업로드)
  ↓
registry 업데이트
```

## 이미지 2-Track 전략

| 이미지 유형 | Track | 방법 |
|------------|-------|------|
| 소프트웨어 UI 화면 | A (캡처) | /browse 캡처 → PIL 어노테이션 |
| 클릭 경로/설정 화면 | A (캡처) | /browse 캡처 → 화살표/하이라이트 합성 |
| 워크플로우/흐름도 | B (생성) | Gemini Imagen API |
| 개념 설명/비유 | B (생성) | Gemini Imagen API |

## 배포 인프라

- **Notion DB**: AI 실습 가이드 DB (`04ac85213c6b492ea4dd2fd97f846bbb`)
- **Notion API**: `~/.zshrc`의 `NOTION_API_KEY`
- **Notion 이미지**: File Upload API 직접 업로드 (외부 호스팅 불필요)
- **notion-save-guide CLI**: DB 항목 생성에만 사용 (블록 구성은 publisher가 직접)
- **Gemini API**: `~/vocab_cards/config.json`의 API 키 참조

## Gotchas

- **사용자 점검 필수**: 과제 기획 후 반드시 사용자 승인 → 승인 없이 작성 진행 금지
- **이미지 Track 선택**: UI 화면은 반드시 Track A(캡처). Gemini로 UI 스크린샷 생성 시도 금지
- **Notion 파일 업로드 시한**: 업로드 후 1시간 내 블록 첨부 필수
- **Notion API 90블록 청크 제한**: 한 번에 90블록까지만 append 가능
- **Registry 무결성**: guide-registry.json은 읽기 후 쓰기 (동시 수정 금지)
- **notion-save-guide 한계**: DB 항목만 생성 가능, 블록/이미지 처리 불가
- **Gemini 한국어**: 긴 문장 불안정 → 이미지 내 텍스트는 최소화
