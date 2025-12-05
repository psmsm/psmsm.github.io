# AI Contribution Badge Assets

AI 기여도 레벨을 표시하는 SVG 배지 에셋입니다.

## 배지 파일

각 레벨(0-4)마다 개별 SVG 파일이 있습니다:

- `level-0.svg` - ✍️ Level 0 • Pure Human (Blue)
- `level-1.svg` - 📝 Level 1 • AI-Assisted (Purple)
- `level-2.svg` - 🤝 Level 2 • Collaborative (Green)
- `level-3.svg` - 🤖 Level 3 • AI-Led (Orange)
- `level-4.svg` - 🌟 Level 4 • AI-Generated (Red)

## 디자인 명세

### 크기
- Width: 240px
- Height: 48px
- Border radius: 6px

### 구조
```
┌─────────────────────────────────────┐
│ ┃  🎨  AI CONTRIBUTION            │
│ ┃      Level X • Name              │
└─────────────────────────────────────┘
```

- 왼쪽 4px 액센트 바
- 아이콘 원형 배경 (24px diameter)
- 그라데이션 배경
- 두 줄 텍스트 (헤더 + 레벨 정보)

### 색상 팔레트

| Level | Color | Hex |
|-------|-------|-----|
| 0 | Blue | #3b82f6 |
| 1 | Purple | #8b5cf6 |
| 2 Green | #10b981 |
| 3 | Orange | #f59e0b |
| 4 | Red | #ef4444 |

## 사용법

### Jekyll/Liquid

```liquid
{% include ai-contribution-badge.html level=2 %}
```

### Markdown (직접 링크)

```markdown
![AI Contribution Level 2](../assets/images/badges/level-2.svg)
```

### HTML

```html
<img src="/assets/images/badges/level-2.svg"
     alt="AI Contribution Level 2"
     style="max-width: 240px;">
```

## 재사용

이 배지들은 다음 곳에서도 사용할 수 있습니다:

- GitHub README.md
- 프로젝트 문서
- 외부 블로그
- 발표 자료
- 이메일 서명

## 파일 크기

각 SVG 파일은 약 1KB 이하로 매우 가볍습니다.

## 수정

SVG 파일이므로 텍스트 에디터로 직접 수정 가능합니다:
- 텍스트 변경
- 색상 조정
- 크기 변경
- 폰트 변경

## 라이센스

이 배지 디자인은 Forest of Dialogues 블로그에서 자유롭게 사용 가능합니다.
다른 프로젝트에서 사용 시 출처 표기를 권장합니다.
