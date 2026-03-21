---
name: guide-review
description: |
  교육 가이드를 초보자 관점에서 검수. 체크리스트 기반 Pass/Fail 판정.
  Triggers: /review-guide, 가이드 검수, 검수해줘, 리뷰해줘
---

# 가이드 검수

## Step 1: 검수 대상 확인
인자로 가이드 번호를 받거나, "미검수 전체"를 선택.

```bash
# 번호 지정
/review-guide 23

# 미검수 전체
/review-guide all
```

대상이 없으면 registry에서 상태가 "작성완료"인 항목 목록을 보여준다.

## Step 2: 검수 실행
reviewer 에이전트를 사용하여:
1. `templates/review-checklist.md` 기반 체크리스트 검수
2. 콘텐츠 MD + 이미지 파일 모두 확인
3. 각 항목에 Pass/Fail 판정

## Step 3: 결과 저장 및 출력
```
📋 검수 결과: #{번호} {제목}

✅ Pass (7/8 항목 통과)

체크리스트:
[✅] 전제조건 명시
[✅] 용어 설명
[✅] 단계 누락 없음
[✅] 이미지-텍스트 정합
[✅] 클릭 경로 명확
[✅] 결과 확인 가능
[❌] 에러 대응 — 3단계에서 권한 부족 시 안내 없음
[✅] 이미지 품질

권고사항:
- 3단계에 "권한이 없다는 메시지가 나오면..." 트러블슈팅 추가

판정: Fail (에러 대응 미흡)
```

`outputs/reviews/{번호}_{제목}_review.md`에 저장.
registry 상태 업데이트.
