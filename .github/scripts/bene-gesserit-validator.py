#!/usr/bin/env python3
"""
Bene Gesserit - AI Contribution Truth Validator

"I must not fear. Fear is the mind-killer."
But lies are the trust-killer.

The Truthsayer examines each post with the Voice,
detecting inconsistencies between claimed and actual AI contribution.

Uses a Factor Model to quantify AI authorship likelihood.
"""

import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, NamedTuple
from dataclasses import dataclass
import yaml


@dataclass
class Factor:
    """AI 작성 가능성을 나타내는 개별 팩터"""
    name: str
    weight: float
    threshold: int
    description: str

    def calculate_score(self, count: int) -> float:
        """팩터 점수 계산"""
        if count >= self.threshold:
            return self.weight
        elif count > 0:
            # 부분 점수: threshold에 가까울수록 weight에 근접
            return self.weight * (count / self.threshold)
        return 0.0


class AIAuthorshipFactorModel:
    """
    AI 작성 가능성을 정량화하는 팩터 모델

    각 팩터는 독립적으로 평가되며, 가중 합산을 통해 최종 점수를 산출합니다.
    """

    # 팩터 정의: 각 팩터의 이름, 가중치, 임계값, 설명
    FACTORS = [
        Factor(
            name="ai_signature",
            weight=30.0,
            threshold=1,
            description="AI 고유 서명 구문 (Forest, '정리했습니다' 등)"
        ),
        Factor(
            name="emoji_diversity",
            weight=15.0,
            threshold=3,
            description="다양한 종류의 이모지 마커 (✅📝💡🚀⚠️)"
        ),
        Factor(
            name="systematic_markers",
            weight=15.0,
            threshold=3,
            description="체계적 구분 마커 (Case A:, 예시:, 핵심: 등)"
        ),
        Factor(
            name="multilevel_structure",
            weight=12.0,
            threshold=2,
            description="다층 구조 번호 (1.1, 2.3.1 등)"
        ),
        Factor(
            name="code_block_density",
            weight=10.0,
            threshold=5,
            description="코드 블록의 높은 밀도"
        ),
        Factor(
            name="structured_headings",
            weight=8.0,
            threshold=3,
            description="구조화된 마크다운 제목 (## 1. 제목)"
        ),
        Factor(
            name="document_length",
            weight=5.0,
            threshold=200,
            description="문서의 길이 (줄 수)"
        ),
        Factor(
            name="front_matter_indication",
            weight=5.0,
            threshold=1,
            description="Front matter의 AI 관련 표기"
        ),
    ]

    # 패턴 정의
    PATTERNS = {
        'ai_signature': [
            r'안녕하세요[,.]?\s*Forest',
            r'저는\s*Forest',
            r'Winston.*요청',
            r'정리했습니다',
            r'설명하겠습니다',
            r'도움이\s*되[었기길|기를]\s*바랍니다',
        ],
        'emoji_markers': r'[✅📝💡🚀⚠️ℹ️🎯🔍]',
        'systematic_markers': [
            r'Case\s+[A-Z][\s:]',
            r'예시[\s:：]',
            r'핵심[\s:：]',
            r'해결책[\s:：]',
            r'중요[\s:：]',
            r'참고[\s:：]',
            r'문제[\s:：]',
            r'방법\s*\d+[\s:]',
            r'Step\s+\d+[\s:]',
            r'단계\s+\d+[\s:]',
        ],
        'multilevel_structure': [
            r'^\d+\.\d+\.?\s+',  # "1.1 " or "1.1. "
            r'^\d+\.\d+\.\d+\.?\s+',  # "1.1.1 " or "1.1.1. "
        ],
        'structured_headings': [
            r'^#{1,6}\s+\d+\.\s+',  # "## 1. 제목"
            r'^#{1,6}\s+\d+\.\d+\s+',  # "### 1.1 제목"
        ],
        'code_blocks': r'```',
    }

    def __init__(self):
        self.factor_scores = {}
        self.raw_counts = {}

    def analyze_content(self, content: str, front_matter: Dict) -> Dict[str, int]:
        """컨텐츠를 분석하여 각 팩터의 원시 카운트 추출"""
        counts = {}

        # 1. AI 서명 구문
        counts['ai_signature'] = sum(
            len(re.findall(pattern, content, re.MULTILINE))
            for pattern in self.PATTERNS['ai_signature']
        )

        # 2. 이모지 다양성 (고유한 이모지 종류 수)
        unique_emojis = set(re.findall(self.PATTERNS['emoji_markers'], content))
        counts['emoji_diversity'] = len(unique_emojis)

        # 3. 체계적 마커
        counts['systematic_markers'] = sum(
            len(re.findall(pattern, content, re.MULTILINE | re.IGNORECASE))
            for pattern in self.PATTERNS['systematic_markers']
        )

        # 4. 다층 구조
        counts['multilevel_structure'] = sum(
            len(re.findall(pattern, content, re.MULTILINE))
            for pattern in self.PATTERNS['multilevel_structure']
        )

        # 5. 코드 블록 밀도
        code_block_count = len(re.findall(self.PATTERNS['code_blocks'], content)) // 2
        counts['code_block_density'] = code_block_count

        # 6. 구조화된 제목
        counts['structured_headings'] = sum(
            len(re.findall(pattern, content, re.MULTILINE))
            for pattern in self.PATTERNS['structured_headings']
        )

        # 7. 문서 길이
        lines = [l for l in content.split('\n') if l.strip()]
        counts['document_length'] = len(lines)

        # 8. Front matter 표시
        author = front_matter.get('author', '')
        ai_role = front_matter.get('ai_role', '')
        score = 0
        if 'Forest' in author:
            score = 2
        elif 'AI' in author or 'ai' in author.lower():
            score = 1
        if ai_role in ['primary-author', 'co-author']:
            score += 1
        counts['front_matter_indication'] = score

        return counts

    def calculate_total_score(self, counts: Dict[str, int]) -> Tuple[float, Dict[str, float]]:
        """
        팩터별 점수를 계산하고 총점을 반환

        Returns:
            (총점, 팩터별 점수 딕셔너리)
        """
        factor_scores = {}
        total_score = 0.0

        for factor in self.FACTORS:
            count = counts.get(factor.name, 0)
            score = factor.calculate_score(count)
            factor_scores[factor.name] = score
            total_score += score

        self.factor_scores = factor_scores
        self.raw_counts = counts

        return total_score, factor_scores

    def get_breakdown(self) -> str:
        """팩터별 기여도를 상세하게 출력"""
        lines = []
        lines.append("📊 Factor Breakdown:")

        for factor in self.FACTORS:
            count = self.raw_counts.get(factor.name, 0)
            score = self.factor_scores.get(factor.name, 0.0)

            # 시각적 바 표시
            bar_length = int(score / factor.weight * 20)
            bar = "█" * bar_length + "░" * (20 - bar_length)

            lines.append(
                f"   {factor.name:25s} │ {bar} │ "
                f"{score:5.1f}/{factor.weight:4.1f} pts (count: {count}/{factor.threshold})"
            )
            lines.append(f"      ↳ {factor.description}")

        return "\n".join(lines)


class BeneGesseritValidator:
    """The Truthsayer - AI 기여도 표기 진실성 검증기"""

    # Contribution level별 AI 점수 임계값
    LEVEL_THRESHOLDS = {
        1: {  # Minimal AI
            'max_score': 40.0,
            'name': 'minimal',
            'description': '사람이 주도적으로 작성, AI는 편집/교정만'
        },
        2: {  # Moderate AI
            'min_score': 30.0,
            'max_score': 70.0,
            'name': 'moderate',
            'description': '사람과 AI가 협력하여 작성'
        },
        3: {  # Major AI
            'min_score': 50.0,
            'name': 'major',
            'description': 'AI가 주도적으로 작성, 사람은 검토/수정'
        }
    }

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.issues = []
        self.warnings = []

    def log(self, message: str, prefix: str = "  "):
        """상세 로그 출력"""
        if self.verbose:
            print(f"{prefix}{message}")

    def extract_front_matter(self, content: str) -> Tuple[Dict, str]:
        """포스트에서 front matter와 본문 분리"""
        match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
        if not match:
            return {}, content

        front_matter_str, body = match.groups()
        try:
            front_matter = yaml.safe_load(front_matter_str)
            return front_matter or {}, body
        except yaml.YAMLError as e:
            self.issues.append(f"Front matter parsing error: {e}")
            return {}, body

    def use_the_voice(self, front_matter: Dict, body: str) -> List[str]:
        """
        The Voice - 진실을 말하도록 강제하는 검증

        팩터 모델을 사용하여 AI 작성 가능성을 정량화하고,
        선언된 contribution_level과 비교합니다.
        """
        issues = []

        contribution_level = front_matter.get('contribution_level')
        ai_contribution = front_matter.get('ai_contribution', '')
        author = front_matter.get('author', '')
        ai_role = front_matter.get('ai_role', '')

        if contribution_level is None:
            self.log("⚠️  contribution_level 없음 - 검증 건너뜀")
            return []

        # 팩터 모델로 AI 점수 계산
        model = AIAuthorshipFactorModel()
        counts = model.analyze_content(body, front_matter)
        total_score, factor_scores = model.calculate_total_score(counts)

        # Verbose 모드에서 상세 분석 출력
        if self.verbose:
            self.log(f"🎯 AI Authorship Score: {total_score:.1f}/100")
            breakdown = model.get_breakdown()
            for line in breakdown.split('\n'):
                self.log(line, prefix="     ")

        # Level별 검증
        threshold = self.LEVEL_THRESHOLDS.get(contribution_level, {})
        expected_contribution = threshold.get('name', '')

        # 1. ai_contribution과 contribution_level 일치 검사
        if ai_contribution != expected_contribution:
            issues.append(
                f"❌ ai_contribution='{ai_contribution}' ≠ contribution_level={contribution_level}\n"
                f"   → '{expected_contribution}'로 수정 필요"
            )

        # 2. AI 점수와 선언된 레벨의 일치성 검증
        if contribution_level == 1:
            max_allowed = threshold.get('max_score', 40.0)
            if total_score > max_allowed:
                issues.append(
                    f"❌ Level 1 (minimal)이지만 AI 점수가 {total_score:.1f}점 (임계값: {max_allowed})\n"
                    f"   → 주요 기여 팩터:\n"
                    f"      • AI 서명: {factor_scores.get('ai_signature', 0):.1f}pts\n"
                    f"      • 이모지 다양성: {factor_scores.get('emoji_diversity', 0):.1f}pts\n"
                    f"      • 체계적 마커: {factor_scores.get('systematic_markers', 0):.1f}pts\n"
                    f"   → Level 2 또는 3으로 상향 조정 필요"
                )

        elif contribution_level == 2:
            min_allowed = threshold.get('min_score', 30.0)
            max_allowed = threshold.get('max_score', 70.0)

            if total_score > max_allowed:
                issues.append(
                    f"❌ Level 2 (moderate)이지만 AI 점수가 {total_score:.1f}점 (상한: {max_allowed})\n"
                    f"   → Level 3 (major)으로 상향 조정 필요"
                )
            elif total_score < min_allowed:
                self.warnings.append(
                    f"⚠️  Level 2이지만 AI 점수가 {total_score:.1f}점 (하한: {min_allowed})\n"
                    f"   → Level 1 (minimal) 고려"
                )

        elif contribution_level == 3:
            min_allowed = threshold.get('min_score', 50.0)

            if ai_role != 'primary-author':
                issues.append(
                    f"❌ Level 3이면 ai_role='primary-author'여야 함 (현재: '{ai_role}')"
                )

            if 'Forest' not in author:
                issues.append(
                    f"❌ Level 3이면 author에 'Forest'가 주 저자로 표기되어야 함 (현재: '{author}')"
                )

            if total_score < min_allowed:
                self.warnings.append(
                    f"⚠️  Level 3이지만 AI 점수가 {total_score:.1f}점으로 낮음 (하한: {min_allowed})"
                )

        return issues

    def examine_post(self, file_path: Path) -> bool:
        """단일 포스트 검증 (Gom Jabbar Test)"""
        try:
            rel_path = file_path.relative_to(Path.cwd())
        except ValueError:
            rel_path = file_path

        print(f"\n🔍 Examining: {rel_path}")

        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            print(f"  ❌ 파일 읽기 오류: {e}")
            return False

        front_matter, body = self.extract_front_matter(content)

        if not front_matter:
            print("  ⏭️  Front matter 없음 (검증 건너뜀)")
            return True

        if 'contribution_level' not in front_matter:
            print("  ⏭️  contribution_level 없음 (검증 건너뜀)")
            return True

        # The Voice를 사용한 진실 검증
        file_issues = self.use_the_voice(front_matter, body)

        if file_issues:
            print("  🚨 진실성 문제 발견:")
            for issue in file_issues:
                for line in issue.split('\n'):
                    print(f"     {line}")
            self.issues.extend(file_issues)
            return False
        else:
            print("  ✅ 진실 검증 통과")
            return True

    def run_trial(self, posts_dir: Path) -> bool:
        """모든 포스트 검증 (The Trial)"""
        print("=" * 70)
        print("🏛️  BENE GESSERIT - AI Contribution Truth Validator")
        print("=" * 70)
        print("\n\"Truth is the first casualty of convenience.\"")
        print("The Truthsayer will examine all posts for inconsistencies.")
        print("\nUsing Factor Model for quantitative AI authorship analysis.\n")

        md_files = list(posts_dir.rglob("*.md"))

        if not md_files:
            print(f"⚠️  {posts_dir}에서 마크다운 파일을 찾을 수 없습니다")
            return True

        print(f"📚 {len(md_files)}개의 포스트를 검증합니다")

        results = []
        for md_file in sorted(md_files):
            result = self.examine_post(md_file)
            results.append(result)

        # 결과 요약
        print("\n" + "=" * 70)
        print("📊 검증 결과")
        print("=" * 70)

        total = len(results)
        passed = sum(results)
        failed = total - passed

        print(f"\n총 {total}개 파일:")
        print(f"  ✅ 통과: {passed}")
        print(f"  ❌ 실패: {failed}")

        if self.warnings:
            print(f"\n💡 경고 {len(self.warnings)}개:")
            for warning in self.warnings:
                print(f"  {warning}")

        if failed > 0:
            print("\n" + "=" * 70)
            print("🚨 진실성 검증 실패")
            print("=" * 70)
            print("\nAI 기여도 표기가 실제 콘텐츠와 일치하지 않습니다.")
            print("신뢰성을 위해 front matter를 수정해주세요.")
            print("\n\"The truth must flow.\"")
            return False
        else:
            print("\n" + "=" * 70)
            print("✅ 모든 포스트가 진실성 검증을 통과했습니다")
            print("=" * 70)
            print("\n\"Truth is the mind-killer's antidote.\"")
            return True


def main():
    """메인 실행 함수"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Bene Gesserit - AI 기여도 표기 진실성 검증 (Factor Model)',
        epilog='"I must not lie. Lies are the trust-killer."'
    )
    parser.add_argument(
        '--posts-dir',
        type=Path,
        default=Path('_posts'),
        help='포스트 디렉토리 경로 (기본: _posts)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='상세 로그 출력 (팩터별 분석 포함)'
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='엄격 모드: 경고도 오류로 처리'
    )

    args = parser.parse_args()

    # PyYAML 필수 확인
    try:
        import yaml
    except ImportError:
        print("❌ PyYAML이 필요합니다: pip install pyyaml")
        sys.exit(1)

    validator = BeneGesseritValidator(verbose=args.verbose)
    success = validator.run_trial(args.posts_dir)

    if args.strict and validator.warnings:
        print("\n⚠️  엄격 모드: 경고가 있어 실패 처리합니다")
        success = False

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
