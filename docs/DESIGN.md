# Forest of Dialogues - Design Specification

블로그의 디자인 철학과 구현 명세를 기록합니다.

## 디자인 철학

### 핵심 가치
- **미니멀리즘**: 필요한 것만, 깔끔하게
- **가독성 우선**: 콘텐츠에 집중할 수 있는 환경
- **금융 회사 스타일**: 절제되고 전문적인 느낌
- **철학적 깊이**: 하이데거적 사유의 공간

### 색상 철학
사색의 숲을 연상시키는 차분한 톤

## 브랜딩

### 블로그 정체성
- **이름**: Forest of Dialogues
- **태그라인**: Exploring the essence of markets and systems through meaningful conversations.
- **프로필**: Quant Engineer & Philosopher

### 파비콘
- **디자인**: 추상적 대화 + 말풍선
- **색상**: Forest Green (#1a4d2e)
- **의미**: 대화의 숲 + 협업적 사유

## 색상 시스템

```css
--color-accent: #2563eb;        /* 링크, 강조 */
--color-text: #111827;          /* 본문 텍스트 */
--color-text-light: #6b7280;    /* 부가 정보 */
--color-border: #e5e7eb;        /* 구분선 */
```

### 배경
- 기본: 흰색 (#ffffff)
- 코드 블록: 연한 회색 (#f9fafb)
- 테이블 헤더: #fafafa

## 타이포그래피

### 폰트 스택
```css
/* 본문 */
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI',
             'Apple SD Gothic Neo', 'Malgun Gothic', sans-serif;

/* 코드 */
font-family: 'SF Mono', 'Monaco', 'Menlo', 'Courier New', monospace;
```

### 폰트 크기
- **본문**: 16px (모바일 15px)
- **H1**: 2rem (모바일 1.75rem)
- **H2**: 1.5rem (모바일 1.375rem)
- **H3**: 1.25rem (모바일 1.125rem)
- **코드**: 0.875rem

### 행간
- **본문**: 1.75
- **헤딩**: 1.3 (H1)
- **코드**: 1.6

### 글자 간격
- **본문**: -0.003em
- **헤딩**: -0.015em

## 레이아웃

### 본문 너비
```css
/* 모바일/태블릿 */
max-width: 800px;

/* 데스크톱 (64em 이상) */
max-width: 900px;
```

### 전체 컨테이너
```css
max-width: 1280px;
padding: 0 2rem;
```

### 좌우 구조
```
[본문 콘텐츠 (900px)] | [구분선] | [목차 (320px)]
```

## 컴포넌트

### 1. 헤더 (Masthead)
- **블로그 제목 크기**: 1.5rem (모바일 1.25rem)
- **폰트 굵기**: 600
- **네비게이션**: 오른쪽 정렬, Home

### 2. 목차 (Table of Contents)
```css
/* 위치 */
오른쪽 사이드바
width: 320px
padding-left: 3rem  /* 구분선과의 간격 */
padding-right: 2rem
margin-left: 3rem

/* 구분선 */
border-left: 1px solid #e5e7eb

/* Sticky */
position: sticky
top: 2rem
```

**스타일**:
- 투명한 배경
- 제목: 작은 대문자 (CONTENTS)
- 링크 색상: 회색 → 호버 시 진하게 → Active 파란색
- 계층 구조: 들여쓰기로 표현

### 3. 본문 (Content)
**프로필 사이드바**: 비활성화 (author_profile: false)

**간격**:
- 문단 여백: 1.25rem
- 헤딩 상단: 2rem (H2는 2.5rem)
- 헤딩 하단: 1rem

### 4. 코드 블록
```css
/* 인라인 코드 */
background: #f9fafb
border: 1px solid #e5e7eb
border-radius: 3px
padding: 0.15em 0.4em
color: #374151

/* 블록 코드 */
background: #f9fafb
border: 1px solid #e5e7eb
border-radius: 4px
padding: 1.25rem
```

**스타일**: 라이트 테마 (다크 X)

### 5. 링크
```css
/* 기본 */
color: #111827
border-bottom: 1px solid #e5e7eb
transition: color 0.15s ease

/* 호버 */
color: #2563eb
border-bottom-color: #2563eb
```

### 6. 인용구 (Blockquote)
```css
border-left: 3px solid #e5e7eb
padding: 0.5rem 1.25rem
color: #6b7280
font-style: normal
background: transparent
```

### 7. 테이블
```css
border: 1px solid #e5e7eb
font-size: 0.9rem

/* 헤더 */
background: #fafafa
font-weight: 600
padding: 0.75rem 1rem
border-bottom: 1px solid #e5e7eb

/* 셀 */
padding: 0.75rem 1rem
border-bottom: 1px solid #e5e7eb
```

### 8. Related Posts (You May Also Enjoy)
```css
max-width: 900px  /* 본문과 동일 */
margin: 0 auto
padding: 0
```

**중요**: 항상 본문과 동일한 너비 유지

## 반응형

### 브레이크포인트
- **모바일**: < 64em (1024px)
- **데스크톱**: ≥ 64em

### 모바일 처리
- 목차 구분선 제거
- 목차 width: 100%
- 폰트 크기 축소
- 여백 조정

## 파일 구조

```
_includes/head/custom.html    # 중요 스타일 인라인
assets/css/custom.scss         # 전체 커스텀 스타일
_config.yml                    # 기본 설정
```

## 설정 값 (_config.yml)

```yaml
title: "Forest of Dialogues"
description: "Exploring the essence of markets and systems through meaningful conversations."
theme: minimal-mistakes-jekyll
minimal_mistakes_skin: "default"

author:
  name: "Winston"
  bio: "Quant Engineer & Philosopher"

defaults:
  - scope:
      type: posts
    values:
      author_profile: false    # 왼쪽 프로필 제거
      toc: true
      toc_sticky: true
      toc_label: "Contents"
```

## 디자인 원칙

### DO
✅ 미니멀하게 유지
✅ 가독성 최우선
✅ 일관된 간격 (본문 = Related Posts)
✅ 절제된 색상
✅ 시스템 폰트 사용

### DON'T
❌ 화려한 효과
❌ 불필요한 장식
❌ 다크 모드 (현재 단계)
❌ 과도한 여백
❌ 본문과 다른 너비의 섹션

## 수식 (MathJax)

```javascript
MathJax = {
  tex: {
    inlineMath: [['$', '$'], ['\\(', '\\)']],
    displayMath: [['$$', '$$'], ['\\[', '\\]']]
  }
}
```

**폰트 크기**: 1.1em

## 향후 고려사항

- [ ] 다크 모드 (옵션)
- [ ] About 페이지 디자인
- [ ] Essays 카테고리 페이지
- [ ] 검색 기능
- [ ] 댓글 시스템 (utterances)

---

*Last updated: 2025-12-05*
*이 문서는 디자인 변경 시 함께 업데이트됩니다.*
