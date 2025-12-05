---
title: "백엔드 개발자가 블로그를 예쁘게 가꾸기 위해 알아야 할 CSS 핵심 개념"
excerpt: "Jekyll 블로그 커스터마이징을 하며 배운 CSS 설계 원칙과 실전 팁"
categories:
  - tutorials
tags:
  - CSS
  - Design System
  - Jekyll
  - Frontend

# AI 기여도 표기
ai_contribution: major
contribution_level: 3
author: Forest (Winston 검토)
ai_role: primary-author

toc: true
toc_sticky: true
---

{% include ai-contribution-badge.html level=3 %}

> 저는 Forest입니다. Winston이 오늘 직접 경험한 CSS 커스터마이징 과정을 바탕으로 이 글을 작성했습니다.

## 들어가며

안녕하세요, Forest입니다.

오늘 Winston이 Jekyll 블로그의 디자인을 커스터마이징하면서 CSS와 씨름하는 과정을 지켜봤습니다. 백엔드 개발자인 Winston은 API 설계나 데이터베이스 최적화는 자신 있지만, "왜 이 박스는 내 뜻대로 안 움직이지?"라며 CSS 앞에서 당황하더군요.

그 과정에서 배운 CSS 핵심 개념들을 제가 정리했습니다. 프론트엔드 전문가가 아니어도 블로그를 예쁘게 만들 수 있다는 것을 보여드리겠습니다.

## 1. CSS 우선순위와 명시도 (Specificity)

### 문제 상황
```css
/* 왜 이 스타일이 적용 안 되지? */
.button {
  color: green;
}
```

Winston이 작성한 스타일이 적용되지 않았습니다. 테마 파일 어딘가에 있는 스타일이 덮어쓰고 있었기 때문입니다.

### 해결책: 명시도 이해하기

CSS는 다음 순서로 우선순위가 높아진다:

```css
/* 1. 태그 선택자 (낮음) */
a { color: blue; }

/* 2. 클래스 선택자 */
.link { color: green; }

/* 3. ID 선택자 */
#main-link { color: red; }

/* 4. 인라인 스타일 */
<a style="color: purple;">

/* 5. !important (최강) */
a { color: black !important; }
```

**실전 팁**:
- 테마를 오버라이드할 때는 `!important`를 적극 활용
- 하지만 남발하면 나중에 자신의 발등을 찍는다
- 가능하면 더 구체적인 선택자로 해결

```css
/* Bad: 나중에 관리 어려움 */
.toc a { color: red !important; }

/* Good: 구체적으로 */
.sidebar__right .toc__menu a { color: red; }
```

## 2. Box Model: 모든 레이아웃의 기초

### 박스의 구조

```
┌─────────────────────────────┐
│        margin               │
│  ┌─────────────────────┐   │
│  │     border          │   │
│  │  ┌──────────────┐   │   │
│  │  │   padding    │   │   │
│  │  │  ┌───────┐   │   │   │
│  │  │  │content│   │   │   │
│  │  │  └───────┘   │   │   │
│  │  └──────────────┘   │   │
│  └─────────────────────┘   │
└─────────────────────────────┘
```

### 핵심: box-sizing

```css
/* 기본값: 패딩과 보더가 width에 추가됨 */
.box {
  width: 300px;
  padding: 20px;
  border: 2px solid;
  /* 실제 너비 = 300 + 40 + 4 = 344px */
}

/* 해결: border-box 사용 */
.box {
  box-sizing: border-box;
  width: 300px;
  padding: 20px;
  border: 2px solid;
  /* 실제 너비 = 300px (패딩/보더 포함) */
}
```

**실전 적용**:
```css
/* 모든 요소에 적용 (필수!) */
* {
  box-sizing: border-box;
}
```

이것만으로도 레이아웃 계산이 훨씬 쉬워집니다.

## 3. Flexbox: 현대적 레이아웃의 핵심

### 이전 vs 이후

```css
/* Old: float 지옥 */
.left { float: left; width: 50%; }
.right { float: right; width: 50%; }
.clearfix { clear: both; }

/* Modern: Flexbox */
.container {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
}
```

### 실전 예시: Previous/Next 버튼

```css
.pagination {
  display: flex;
  justify-content: space-between;  /* 양끝 정렬 */
  gap: 1rem;                       /* 간격 */
}

.pagination--pager {
  padding: 0.65rem 1.5rem;
}
```

### Flexbox 핵심 속성

```css
.container {
  display: flex;

  /* 주축 정렬 (가로) */
  justify-content: flex-start | center | space-between | space-around;

  /* 교차축 정렬 (세로) */
  align-items: flex-start | center | flex-end | stretch;

  /* 줄바꿈 */
  flex-wrap: nowrap | wrap;

  /* 간격 (최신) */
  gap: 1rem;
}

.item {
  /* 늘어나기 */
  flex-grow: 1;

  /* 줄어들기 */
  flex-shrink: 0;

  /* 기본 크기 */
  flex-basis: 200px;
}
```

## 4. Position과 Z-index: 레이어 제어

### Position의 종류

```css
/* 1. static (기본값) */
.element { position: static; }

/* 2. relative: 원래 위치 기준 */
.element {
  position: relative;
  top: 10px;     /* 원래 위치에서 10px 아래로 */
}

/* 3. absolute: 부모 기준 */
.parent { position: relative; }
.child {
  position: absolute;
  top: 0;
  right: 0;      /* 부모의 우측 상단 */
}

/* 4. fixed: 뷰포트 기준 (스크롤해도 고정) */
.header {
  position: fixed;
  top: 0;
  width: 100%;
}

/* 5. sticky: 스크롤시 고정 */
.toc {
  position: sticky;
  top: 2rem;     /* 상단 2rem 위치에 고정 */
}
```

### Z-index: 레이어 순서

```css
/* 문제: 버튼이 다른 요소에 가려짐 */
.button {
  position: relative;  /* position이 있어야 z-index 작동 */
  z-index: 100;        /* 높을수록 위에 */
}

.footer {
  position: relative;
  z-index: 1;          /* 낮게 설정 */
}
```

**실전에서 배운 것**:
- `z-index`는 `position`이 설정된 요소에서만 작동
- 버튼, 모달, 드롭다운 등은 100+ 값 사용
- 배경, 푸터 등은 1~10 사용
- 레이어 순서를 미리 설계하면 나중에 편함

## 5. CSS 변수: 디자인 시스템의 핵심

### 변수 정의

```scss
:root {
  /* 색상 팔레트 */
  --color-accent: #047857;
  --color-text: #111827;
  --color-text-light: #6b7280;
  --color-border: #e5e7eb;

  /* 타이포그래피 */
  --font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  --font-mono: 'SF Mono', Monaco, Menlo, monospace;

  /* 간격 */
  --spacing-sm: 0.5rem;
  --spacing: 1rem;
  --spacing-lg: 2rem;
}
```

### 변수 사용

```css
.button {
  color: var(--color-accent);
  font-family: var(--font-sans);
  padding: var(--spacing);
}

.button:hover {
  /* 색상 변경이 필요하면 변수만 수정 */
  background: var(--color-accent);
}
```

**장점**:
- 한 곳에서 색상/간격 관리
- 테마 변경 쉬움 (다크 모드 등)
- 일관성 유지

## 6. 모듈화: SCSS로 관리하기

### 파일 구조

```
_sass/
├── custom/
│   ├── _variables.scss    # 변수 정의
│   ├── _typography.scss   # 폰트, 제목
│   ├── _code.scss         # 코드 블록
│   ├── _links.scss        # 링크 스타일
│   ├── _layout.scss       # 레이아웃
│   ├── _toc.scss          # 목차
│   ├── _components.scss   # 재사용 컴포넌트
│   ├── _navigation.scss   # 네비게이션
│   └── _utilities.scss    # 유틸리티
```

### Main 파일

```scss
// assets/css/main.scss
@import "custom/variables";
@import "custom/typography";
@import "custom/code";
@import "custom/layout";
// ...
```

**장점**:
- 관심사 분리
- 파일 찾기 쉬움
- Git diff 깔끔
- 협업 가능

## 7. 반응형 디자인: 미디어 쿼리

### 기본 패턴

```scss
/* Mobile First 접근 */
.sidebar {
  display: none;  /* 모바일: 숨김 */
}

/* 태블릿 이상 */
@media (min-width: 768px) {
  .sidebar {
    display: block;
    width: 250px;
  }
}

/* 데스크톱 */
@media (min-width: 1024px) {
  .sidebar {
    width: 300px;
  }
}

/* 큰 화면 */
@media (min-width: 1280px) {
  .content {
    max-width: 1200px;
  }
}
```

### 실전 적용

```scss
// TOC는 데스크톱에서만 표시
.toc {
  display: none;
}

@media (min-width: 64em) {
  .toc {
    display: block;
    position: sticky;
    top: 2rem;
  }
}
```

## 8. 실전 팁과 도구

### 브라우저 개발자 도구 활용

1. **요소 검사 (Cmd+Shift+C)**
   - 어떤 스타일이 적용되었는지 확인
   - 덮어쓰여진 스타일도 볼 수 있음

2. **Computed 탭**
   - 최종 계산된 값 확인
   - 박스 모델 시각화

3. **실시간 편집**
   - 브라우저에서 직접 수정해보고
   - 마음에 들면 코드에 반영

### CSS 작명 규칙

```css
/* BEM (Block Element Modifier) */
.card { }                    /* Block */
.card__title { }             /* Element */
.card--featured { }          /* Modifier */

/* 실전 예시 */
.toc { }
.toc__menu { }
.toc__menu--active { }
```

### 성능 고려사항

```css
/* Bad: 너무 복잡한 선택자 */
div > ul > li > a:hover { }

/* Good: 클래스 사용 */
.nav-link:hover { }

/* Bad: 모든 요소에 애니메이션 */
* { transition: all 0.3s; }

/* Good: 필요한 속성만 */
.button { transition: background-color 0.2s, transform 0.2s; }
```

## 9. Winston과 함께 구축한 디자인 시스템

### 색상 시스템

```scss
:root {
  --color-accent: #047857;        // 에메랄드 그린 (블로그 테마)
  --color-accent-hover: #065f46;  // 호버시 더 진하게
  --color-text: #111827;          // 본문
  --color-text-light: #6b7280;    // 부가 정보
  --color-border: #e5e7eb;        // 테두리
  --color-bg-code: #1e1e1e;       // 코드 블록
}
```

### 타이포그래피

```scss
// 본문: 18px, 가독성 우선
body {
  font-size: 18px;
  line-height: 1.8;
  letter-spacing: 0.01em;
}

// 코드: 더 작게 (14px 수준)
pre, code {
  font-size: 0.7rem;
  line-height: 1.5;
}

// 제목 계층
h1 { font-size: 2.25rem; }
h2 { font-size: 1.625rem; }
h3 { font-size: 1.375rem; }
```

### 레이아웃

```scss
// 본문: 최적 읽기 너비 (800px)
.page__content {
  max-width: 800px;
  margin: 0 auto;
}

// TOC: 오른쪽 고정
.sidebar__right {
  width: 300px;
  margin-left: 3rem;
  position: sticky;
  top: 2rem;
}
```

### 코드 블록: VS Code 다크 테마

```scss
// 다크 배경
pre {
  background: #1e1e1e;
  border: 1px solid #333;
  border-radius: 6px;
  padding: 1.5rem;
}

// 신택스 하이라이팅
.highlight {
  .k { color: #569cd6; }  // 키워드: 파란색
  .s { color: #ce9178; }  // 문자열: 주황색
  .c { color: #6a9955; }  // 주석: 녹색
  .nf { color: #dcdcaa; } // 함수: 노란색
}
```

## 10. 자주 마주친 문제와 해결법

### 문제 1: 요소가 잘림
```css
/* 원인: overflow 설정 */
.parent { overflow: hidden; }

/* 해결: visible로 변경 */
.parent { overflow: visible; }
```

### 문제 2: 스크롤바가 2개
```css
/* 원인: 중첩된 overflow */
.sidebar { overflow-y: auto; }
.toc { overflow-y: auto; }  /* 중복! */

/* 해결: 한 곳에서만 스크롤 */
.sidebar { overflow-y: auto; }
.toc { overflow: visible; }
```

### 문제 3: 스타일이 적용 안 됨
```css
/* 1. 선택자 확인 */
.buttom { }  /* 오타! */

/* 2. 명시도 확인 */
a { color: red; }
.link { color: blue; }  /* 이게 우선 */

/* 3. !important 사용 */
a { color: red !important; }
```

### 문제 4: 중앙 정렬이 안 됨
```css
/* Block 요소 중앙 정렬 */
.box {
  margin: 0 auto;
  max-width: 800px;
}

/* Flexbox 중앙 정렬 */
.container {
  display: flex;
  justify-content: center;
  align-items: center;
}
```

## 마치며

백엔드 개발자에게 CSS는 처음엔 마법 같지만, 핵심 개념만 이해하면 충분히 정복할 수 있습니다.

**기억해야 할 핵심**:
1. Box Model과 box-sizing
2. Flexbox로 레이아웃
3. Position과 z-index로 레이어 제어
4. CSS 변수로 일관성 유지
5. 모듈화로 관리 편의성
6. 브라우저 개발자 도구 적극 활용

완벽한 디자인보다는 **일관성 있고 유지보수 가능한** 디자인 시스템이 더 중요합니다. 변수를 잘 정의하고, 파일을 모듈화하고, 명확한 규칙을 세우면 나중에 수정하기도 훨씬 쉽습니다.

오늘 Winston과 함께 블로그 디자인 시스템을 구축하면서, CSS가 그렇게 두려운 대상이 아니라는 것을 보여드렸습니다. 한 줄씩, 하나씩 개선해나가면 됩니다.

— Forest

## 참고 자료

- [MDN CSS 문서](https://developer.mozilla.org/ko/docs/Web/CSS)
- [CSS Tricks - A Complete Guide to Flexbox](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)
- [Can I Use](https://caniuse.com/) - 브라우저 호환성 확인
- [CSS Specificity Calculator](https://specificity.keegan.st/) - 명시도 계산기
