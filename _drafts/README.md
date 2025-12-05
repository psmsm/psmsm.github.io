# Drafts

이 폴더에는 작업 중인 글들을 보관합니다.

## 사용법

### Draft 작성
```bash
# _drafts/algorithms/ 또는 _drafts/essays/에 파일 생성
# 파일명에 날짜 불필요 (예: my-draft.md)
```

### Draft 미리보기
```bash
bundle exec jekyll serve --drafts
```

### 출간하기
```bash
# 완성된 draft를 _posts/로 이동하고 날짜 추가
mv _drafts/algorithms/my-draft.md _posts/algorithms/2025-12-05-my-draft.md
```

## 폴더 구조
- `algorithms/` - 알고리즘 관련 작업 중인 글
- `essays/` - 에세이 작업 중인 글
