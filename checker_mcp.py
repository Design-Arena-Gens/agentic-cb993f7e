"""
Checker MCP - Content Audit Agent
Analyzes Shopify content and identifies quality issues.
"""

from typing import Dict, List, Any


class CheckerMCP:
    """
    Audit agent that analyzes product content and detects issues.
    Does NOT generate or rewrite content - only identifies problems.
    """

    # Quality thresholds
    MIN_DESCRIPTION_LENGTH = 100
    MIN_SEO_TITLE_LENGTH = 30
    MIN_SEO_DESCRIPTION_LENGTH = 80
    MAX_SEO_DESCRIPTION_LENGTH = 160

    # Required elements for premium content
    PREMIUM_KEYWORDS = ["premium", "luxury", "exclusive", "professional", "exceptional"]
    CTA_KEYWORDS = ["discover", "experience", "transform", "elevate", "shop now", "order", "buy"]
    BENEFIT_KEYWORDS = ["benefits", "results", "improves", "enhances", "reduces", "promotes"]

    def __init__(self):
        """Initialize the Checker MCP agent."""
        self.name = "CheckerMCP"

    def audit_product(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a product and return structured issues.

        Args:
            product: Product dictionary with title, description, SEO fields

        Returns:
            Dictionary containing product_id and list of issues found
        """
        issues = []

        # Audit description
        description = product.get("description", "")
        issues.extend(self._check_description(description))

        # Audit SEO fields
        issues.extend(self._check_seo_fields(product))

        # Audit tone and messaging
        issues.extend(self._check_tone(description))

        # Audit conversion elements
        issues.extend(self._check_conversion_elements(description))

        return {
            "product_id": product["id"],
            "product_title": product["title"],
            "issues_found": len(issues),
            "issues": issues,
            "severity": self._calculate_severity(issues)
        }

    def _check_description(self, description: str) -> List[Dict[str, str]]:
        """Check product description for quality issues."""
        issues = []

        if len(description) < self.MIN_DESCRIPTION_LENGTH:
            issues.append({
                "type": "description_length",
                "severity": "high",
                "message": f"Description too short ({len(description)} chars). Minimum: {self.MIN_DESCRIPTION_LENGTH}"
            })

        if not description or description.strip() == "":
            issues.append({
                "type": "missing_description",
                "severity": "critical",
                "message": "Product description is missing"
            })

        # Check for vague language
        vague_terms = ["good", "nice", "stuff", "things", "really"]
        found_vague = [term for term in vague_terms if term.lower() in description.lower()]
        if found_vague:
            issues.append({
                "type": "vague_language",
                "severity": "medium",
                "message": f"Contains vague terms: {', '.join(found_vague)}"
            })

        return issues

    def _check_seo_fields(self, product: Dict[str, Any]) -> List[Dict[str, str]]:
        """Check SEO title and description."""
        issues = []

        seo_title = product.get("seo_title", "")
        seo_description = product.get("seo_description", "")

        if not seo_title or len(seo_title) < self.MIN_SEO_TITLE_LENGTH:
            issues.append({
                "type": "seo_title",
                "severity": "high",
                "message": "SEO title missing or too short"
            })

        if not seo_description:
            issues.append({
                "type": "seo_description_missing",
                "severity": "high",
                "message": "SEO description is missing"
            })
        elif len(seo_description) < self.MIN_SEO_DESCRIPTION_LENGTH:
            issues.append({
                "type": "seo_description_short",
                "severity": "medium",
                "message": f"SEO description too short ({len(seo_description)} chars)"
            })
        elif len(seo_description) > self.MAX_SEO_DESCRIPTION_LENGTH:
            issues.append({
                "type": "seo_description_long",
                "severity": "low",
                "message": f"SEO description too long ({len(seo_description)} chars). Max: {self.MAX_SEO_DESCRIPTION_LENGTH}"
            })

        return issues

    def _check_tone(self, description: str) -> List[Dict[str, str]]:
        """Check for premium brand tone."""
        issues = []

        description_lower = description.lower()

        # Check for premium language
        has_premium_tone = any(keyword in description_lower for keyword in self.PREMIUM_KEYWORDS)
        if not has_premium_tone:
            issues.append({
                "type": "tone_not_premium",
                "severity": "medium",
                "message": "Missing premium/luxury brand tone"
            })

        return issues

    def _check_conversion_elements(self, description: str) -> List[Dict[str, str]]:
        """Check for conversion-optimized elements."""
        issues = []

        description_lower = description.lower()

        # Check for call-to-action
        has_cta = any(keyword in description_lower for keyword in self.CTA_KEYWORDS)
        if not has_cta:
            issues.append({
                "type": "missing_cta",
                "severity": "medium",
                "message": "Missing clear call-to-action"
            })

        # Check for benefit-focused language
        has_benefits = any(keyword in description_lower for keyword in self.BENEFIT_KEYWORDS)
        if not has_benefits:
            issues.append({
                "type": "missing_benefits",
                "severity": "low",
                "message": "Could emphasize customer benefits more clearly"
            })

        return issues

    def _calculate_severity(self, issues: List[Dict[str, str]]) -> str:
        """Calculate overall severity based on issues found."""
        if not issues:
            return "none"

        severities = [issue["severity"] for issue in issues]

        if "critical" in severities:
            return "critical"
        elif "high" in severities:
            return "high"
        elif "medium" in severities:
            return "medium"
        else:
            return "low"
