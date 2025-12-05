# 색상 시스템 (Color System)

## 주요 색상 (Primary Colors)

### 에메랄드 그린 (Emerald Green)
블로그의 시그니처 색상. 숲, 성장, 알고리즘을 상징.

```scss
--color-accent: #047857;        // Emerald 700 (메인)
--color-accent-hover: #065f46;  // Emerald 800 (호버)
--color-accent-light: #10b981;  // Emerald 600 (밝음)
--color-accent-bg: #f0fdf4;     // Emerald 50 (배경)
```

**사용처**:
- 링크 호버 상태
- TOC 활성 항목
- 버튼 강조
- AI Level 2 (협업) 배지

### 색상 의미
| 색상 | Hex | 의미 | 사용 예시 |
|------|-----|------|-----------|
| Emerald 700 | `#047857` | 주요 강조, 상호작용 | 호버 상태, 활성 링크 |
| Emerald 800 | `#065f46` | 강한 강조 | 버튼 누름 상태 |
| Emerald 50 | `#f0fdf4` | 은은한 배경 | 호버 배경, 강조 영역 |

## 텍스트 색상 (Text Colors)

```scss
--color-text: #111827;        // Gray 900 (본문)
--color-text-light: #6b7280;  // Gray 500 (부가정보)
--color-text-muted: #9ca3af;  // Gray 400 (비활성)
```

**사용 원칙**:
- 본문: `#111827` (순수 검정보다 부드러움)
- 메타 정보, TOC: `#6b7280`
- 비활성 요소: `#9ca3af`

## 배경 색상 (Background Colors)

```scss
--color-bg-primary: #ffffff;    // 기본 배경
--color-bg-secondary: #f9fafb;  // Gray 50 (섹션 구분)
--color-bg-code: #1e1e1e;       // 코드 블록 다크
```

## 테두리 색상 (Border Colors)

```scss
--color-border: #e5e7eb;       // Gray 200 (기본)
--color-border-light: #f3f4f6; // Gray 100 (은은함)
--color-border-dark: #d1d5db;  // Gray 300 (강조)
```

## AI 레벨 색상 (AI Contribution Level Colors)

각 AI 기여도 레벨마다 고유 색상:

| Level | Icon | 색상 | Hex | 의미 |
|-------|------|------|-----|------|
| 0 | ✍️ | Blue | `#3b82f6` | 순수함, 신뢰 |
| 1 | 📝 | Purple | `#8b5cf6` | 혼합, 조화 |
| 2 | 🤝 | Green | `#10b981` | 협업, 성장 |
| 3 | 🤖 | Orange | `#f59e0b` | 기술, 에너지 |
| 4 | 🌟 | Red | `#ef4444` | 혁신, 대담함 |

## 코드 블록 색상 (Code Syntax Highlighting)

VS Code Dark+ 테마 기반:

```scss
// 배경
background: #1e1e1e;
border: #333333;

// 신택스
--syntax-keyword: #569cd6;    // 파란색
--syntax-string: #ce9178;     // 주황색
--syntax-number: #b5cea8;     // 연두색
--syntax-comment: #6a9955;    // 녹색
--syntax-function: #dcdcaa;   // 노란색
--syntax-variable: #9cdcfe;   // 하늘색
```

## 다크 모드 (향후 구현)

```scss
// 다크 모드 변수 (미래)
@media (prefers-color-scheme: dark) {
  --color-accent: #10b981;      // 밝은 에메랄드
  --color-text: #f9fafb;        // 밝은 텍스트
  --color-bg-primary: #111827;  // 어두운 배경
}
```

## 접근성 (Accessibility)

### 명암비 (Contrast Ratios)

WCAG AA 기준 충족:

- 본문 텍스트: `#111827` on `#ffffff` = **15.2:1** ✅
- 부가 텍스트: `#6b7280` on `#ffffff` = **4.6:1** ✅
- 에메랄드 강조: `#047857` on `#ffffff` = **4.5:1** ✅

### 색맹 고려

- 색상만으로 정보 전달하지 않음
- 아이콘 + 텍스트 병행
- 패턴과 형태로 차별화

## 사용 예시

### 링크 호버
```scss
a {
  color: #111827;
  border-bottom: 1px solid #e5e7eb;
}

a:hover {
  color: #047857;
  border-bottom-color: #047857;
}
```

### 배지 (AI Contribution Badge)
```scss
.badge-level-2 {
  background: linear-gradient(135deg, #10b98110, #10b98105);
  border-left: 4px solid #10b981;
  color: #047857;
}
```

### 버튼
```scss
.button {
  background: transparent;
  border: 2px solid #e5e7eb;
  color: #111827;
}

.button:hover {
  border-color: #047857;
  color: #047857;
  background: #f0fdf4;
}
```

## 컬러 팔레트 전체

```
Emerald (Primary)
50:  #f0fdf4
100: #dcfce7
200: #bbf7d0
300: #86efac
400: #4ade80
500: #22c55e
600: #16a34a
700: #047857 ← 메인
800: #065f46
900: #064e3b

Gray (Neutral)
50:  #f9fafb
100: #f3f4f6
200: #e5e7eb ← 테두리
300: #d1d5db
400: #9ca3af
500: #6b7280 ← 부가 텍스트
600: #4b5563
700: #374151
800: #1f2937
900: #111827 ← 본문
```
