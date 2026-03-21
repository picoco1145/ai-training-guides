---
description: 팀 워크플로우 규칙. 모든 가이드 생성/수정 작업에 적용.
---

# 워크플로우 규칙

## 필수 순서
1. 과제 기획 후 **반드시 사용자 점검** — 승인 없이 콘텐츠 작성 금지
2. 콘텐츠 완성 후 **반드시 reviewer 검수** — Pass 없이 Notion 배포 금지
3. 가이드 생성/수정 시 **반드시 registry 업데이트**

## 이미지 규칙
- UI 화면 → Track A (캡처) 필수. Gemini로 UI 스크린샷 생성 시도 금지
- 개념도/흐름도만 Track B (Gemini) 허용

## 에이전트 활용
- 새 기능/가이드 시작 → planner로 기획 분해
- 콘텐츠 작성 → content-writer
- 이미지 제작 → image-producer
- 구현 완료 → reviewer로 검수
- Notion 배포 → publisher
- 에러 발생 → debugger로 분석

## 파일 소유권
- 하나의 가이드를 여러 에이전트가 동시 수정 금지
- 에이전트별 출력 디렉토리 준수:
  - planner: outputs/guides/{번호}_brief.md
  - content-writer: outputs/guides/{번호}_{제목}.md
  - image-producer: outputs/images/{번호}/
  - reviewer: outputs/reviews/{번호}_review.md
  - publisher: registry/guide-registry.json

## 세션 관리
- 세션/섹션 종료 시 `/handoff`로 핸드오프 노트 작성
- 다음 세션 시작 시 `/resume`으로 이전 세션 이어받기
