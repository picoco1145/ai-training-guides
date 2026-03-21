# HTML 위젯 디자인 스펙

## 전체 구조
- max-width: 680px, 배경 투명, font-family: var(--font-sans)
- 상단: 태그 pill(검정 배경, 흰 글씨) + 제목 텍스트 한 줄
- 소개 박스: 연보라(#f0edff) 배경, border-radius: 10px, 텍스트 내 핵심어는 <b> 강조
- 섹션 레이블: 12px, color: var(--color-text-secondary)
- 모든 카드: border: 0.5px solid var(--color-border-tertiary), border-radius: 10~12px, 그림자 없음, 배경 var(--color-background-primary)

## 사전 준비 영역 (선택)
- 2열 그리드 카드
- 좌측 카드: 아이콘 박스(연보라 #e8e6fe, 글씨 #5b4fd4) + 텍스트
- 우측 카드: 아이콘 박스(연초록 #d4f4e6, 체크 아이콘 #1a8a5c) + 텍스트

## 단계별 실습 카드
- 각 단계는 별도 카드
- 단계 번호 badge 색상: 1번=#7b6cf7, 2번=#3dba8c, 3번=#f5a623, 4번=#e05c5c, 5번=#4a90d9 (그 이상은 순환)
- 흰 글씨, 원형 badge
- 제목: font-size 15px, font-weight 500
- 본문: bullet point 리스트, font-size 13px, line-height 1.7
- 중요 텍스트: <b> 태그로 강조
- 하위 박스: background: var(--color-background-secondary), border-radius: 8px, padding: 12px 14px, font-size: 12px

## 실무 팁 영역 (선택)
- 3열 그리드 카드 (gap: 12px)
- 각 카드: 제목(14px, font-weight 500) + 본문(13px, color: var(--color-text-secondary), line-height 1.6)
- 팁이 없으면 섹션 전체 생략

## 절대 금지
- box-shadow, drop-shadow 금지
- 한쪽 border만 두껍게 입체감 주는 효과 금지
- 그라디언트 배경 금지
- 외부 폰트 로드 금지
- 하드코딩 색상 최소화 (배경색 계열만 예외)

## CSS 변수
var(--font-sans) / var(--color-text-primary) / var(--color-text-secondary)
var(--color-background-primary) / var(--color-background-secondary) / var(--color-border-tertiary)
