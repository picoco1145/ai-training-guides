---
name: guide-create
description: |
  교육 실습 가이드 생성 전체 파이프라인.
  사용자가 링크/내용을 제공하면: 과제 기획 → 사용자 점검 → 콘텐츠+이미지 작성 → 초보자 검수 → Notion 배포.
  Triggers: /new-guide, 가이드 만들어줘, 교육 가이드 생성, 실습 과제 만들어줘, 새 가이드
---

# 교육 실습 가이드 생성

사용자가 교육 내용(링크, 영상, 텍스트)을 제공하면 실습 가이드를 기획 → 작성 → 검수 → 배포한다.

---

## Step 1: 입력 수집

사용자가 링크/내용을 제공하면 바로 Step 2로 진행.
내용이 없으면 아래 안내:

```
📋 교육 내용을 제공해주세요.

가능한 형식:
- URL (블로그, 영상, 문서)
- 텍스트 복사/붙여넣기
- 주제 키워드 + 대상 설명

예시:
"코덱스 사용법을 초보자 대상으로 만들어줘"
"이 영상 기반으로 실습 과제 뽑아줘: [URL]"
```

---

## Step 2: 과제 기획 (planner 에이전트)

planner 에이전트를 사용하여:
1. 입력 내용 분석 (링크면 /browse로 내용 확인)
2. 실습 가능한 과제 도출
3. `templates/guide-brief.md` 양식으로 기획서 작성
4. `outputs/guides/{번호}_brief.md`에 저장
5. `registry/guide-registry.json`에 항목 등록 (상태: "기획중")

번호는 registry의 최대값 + 1.

---

## Step 3: ★ 사용자 점검 ★ (필수)

**이 단계를 절대 건너뛰지 않는다.**

기획서를 사용자에게 보여주고 점검을 받는다:

```
📋 아래 과제를 실습 가이드로 작성하려고 합니다. 확인해주세요!

━━━━━━━━━━━━━━━━━━
📌 과제: {제목}
👥 대상: {대상}
🛠 도구: {도구}
⏱ 예상 소요: {시간}
━━━━━━━━━━━━━━━━━━

📚 실습 단계:
  1️⃣  {단계 1}
  2️⃣  {단계 2}
  3️⃣  {단계 3}
  ...

수정할 부분이 있으면 말씀해주세요.
"진행해" / "OK" / "좋아" 라고 하시면 콘텐츠 작성을 시작할게요.
```

사용자가 수정 요청 → 기획서 수정 → 다시 제시 (루프)
사용자가 승인 → Step 4로 진행

---

## Step 4: 콘텐츠 작성 (content-writer 에이전트)

content-writer 에이전트를 사용하여:
1. 기획서 기반으로 상세 콘텐츠 작성
2. 각 단계에 이미지 지시서 삽입 (CAPTURE 또는 GENERATE)
3. `outputs/guides/{번호}_{제목}.md`에 저장

### 이미지 지시서 규칙
- UI 화면 → `<!-- CAPTURE: url=... annotate=... -->`
- 개념도/흐름도 → `<!-- GENERATE: prompt="..." style=... -->`
- **UI 화면에 GENERATE 사용 금지**

---

## Step 5: 이미지 제작 (image-producer 에이전트)

image-producer 에이전트를 사용하여:
1. 콘텐츠 MD의 이미지 지시서 파싱
2. Track A (CAPTURE): /browse로 캡처 → `scripts/capture_screen.py`로 어노테이션
3. Track B (GENERATE): `scripts/generate_image.py`로 Gemini 생성
4. `outputs/images/{번호}/step_{N}.png`에 저장
5. 콘텐츠 MD의 이미지 경로 업데이트

---

## Step 6: 검수 (reviewer 에이전트)

reviewer 에이전트를 사용하여:
1. `templates/review-checklist.md` 기반 초보자 관점 검수
2. 결과를 `outputs/reviews/{번호}_{제목}_review.md`에 저장
3. **Pass** → Step 7로 진행
4. **Fail** → 이슈 목록을 content-writer에게 전달 → 수정 → 재검수

---

## Step 7: Notion 배포 (publisher 에이전트)

publisher 에이전트를 사용하여:
1. `notion-save-guide` CLI로 DB 항목 생성
2. `scripts/upload_to_notion.py`로 이미지 Notion 직접 업로드
3. 콘텐츠를 Notion 블록으로 변환 (텍스트 ↔ 이미지 번갈아 배치)
4. Notion API로 블록 append (90개 청크 분할)
5. DB 속성 업데이트

---

## Step 8: 완료

```
✅ 가이드 배포 완료!

📌 과제: {제목}
📝 Notion 페이지: {URL}
📋 DB 항목: {URL} (번호: {N}, 도구: [...], 주제: [...])
🖼 이미지: {N}장
```

registry 업데이트 (상태: "배포완료")

---

## 에러 처리

| 상황 | 처리 |
|------|------|
| 입력이 너무 짧음 | "내용이 부족해요. 구체적인 주제/링크를 제공해주세요." |
| /browse 접근 실패 | 로그인 필요 여부 확인 → 사용자에게 안내 |
| Gemini 이미지 생성 실패 | 3회 재시도 → 실패 시 프롬프트 수정 후 재시도 |
| Notion 업로드 실패 | NOTION_API_KEY 확인 → debugger 에이전트 투입 |
| reviewer Fail | 이슈 목록 → content-writer 수정 → 재검수 |
