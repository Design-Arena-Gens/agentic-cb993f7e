"""
Generator MCP - Content Generation Agent
Creates optimized product content based on audit feedback.
"""

from typing import Dict, List, Any


class GeneratorMCP:
    """
    Content generation agent that produces optimized Shopify content.
    Uses premium brand tone and SEO best practices.
    """

    def __init__(self):
        """Initialize the Generator MCP agent."""
        self.name = "GeneratorMCP"
        self.brand_tone = "premium, warm, trustworthy"

    def generate_optimized_content(
        self,
        product: Dict[str, Any],
        issues: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Generate optimized content for a product based on identified issues.

        Args:
            product: Original product data
            issues: List of issues identified by Checker MCP

        Returns:
            Dictionary with optimized content fields
        """
        issue_types = [issue["type"] for issue in issues]

        optimized = {
            "product_id": product["id"],
            "original_description": product.get("description", ""),
            "optimized_description": None,
            "optimized_seo_title": None,
            "optimized_seo_description": None,
            "improvements_made": []
        }

        # Generate optimized description if needed
        if self._needs_description_rewrite(issue_types):
            optimized["optimized_description"] = self._generate_description(product)
            optimized["improvements_made"].append("Rewrote product description with premium tone")

        # Generate SEO title if needed
        if "seo_title" in issue_types:
            optimized["optimized_seo_title"] = self._generate_seo_title(product)
            optimized["improvements_made"].append("Created SEO-optimized title")

        # Generate SEO description if needed
        if any(t.startswith("seo_description") for t in issue_types):
            optimized["optimized_seo_description"] = self._generate_seo_description(product)
            optimized["improvements_made"].append("Created SEO meta description")

        return optimized

    def _needs_description_rewrite(self, issue_types: List[str]) -> bool:
        """Determine if description needs rewriting."""
        rewrite_triggers = [
            "description_length",
            "missing_description",
            "vague_language",
            "tone_not_premium",
            "missing_cta",
            "missing_benefits"
        ]
        return any(trigger in issue_types for trigger in rewrite_triggers)

    def _generate_description(self, product: Dict[str, Any]) -> str:
        """
        Generate an optimized product description.
        Uses premium tone, clear benefits, and strong CTA.
        """
        title = product.get("title", "Product")
        product_type = product.get("product_type", "item")
        price = product.get("price", 0)

        # Build description with premium tone
        description_parts = []

        # Opening hook - premium positioning
        description_parts.append(
            f"Discover the exceptional quality of our {title}, "
            f"a premium {product_type.lower()} crafted for those who appreciate excellence."
        )

        # Benefits section - what it does
        if "cream" in title.lower() or "skincare" in product_type.lower():
            description_parts.append(
                "\n\nExperience transformative results with our carefully formulated blend of "
                "natural ingredients. This luxurious formula deeply nourishes your skin, "
                "promoting a radiant, healthy complexion while reducing the visible signs of aging."
            )
        elif "serum" in title.lower():
            description_parts.append(
                "\n\nThis professional-grade serum delivers powerful anti-aging benefits through "
                "a concentrated blend of scientifically-proven ingredients. Enhances skin elasticity, "
                "reduces fine lines, and restores your skin's natural luminosity."
            )
        else:
            description_parts.append(
                "\n\nMeticulously designed to deliver exceptional results, this product combines "
                "premium ingredients with expert craftsmanship to exceed your expectations."
            )

        # Key features
        description_parts.append(
            "\n\n**Key Benefits:**\n"
            "• Premium, professionally-formulated ingredients\n"
            "• Visible results you can see and feel\n"
            "• Suitable for all skin types\n"
            "• Cruelty-free and ethically sourced"
        )

        # Trust building
        description_parts.append(
            f"\n\nTrusted by discerning customers worldwide, our {title} represents "
            "the perfect balance of luxury and effectiveness."
        )

        # Strong CTA
        description_parts.append(
            "\n\nElevate your skincare routine today. Experience the difference that premium quality makes."
        )

        return "".join(description_parts)

    def _generate_seo_title(self, product: Dict[str, Any]) -> str:
        """
        Generate SEO-optimized title.
        Format: Product Name | Key Benefit | Brand
        """
        title = product.get("title", "")
        vendor = product.get("vendor", "")
        product_type = product.get("product_type", "")

        # Create benefit-focused SEO title
        if "cream" in title.lower():
            benefit = "Nourishing & Anti-Aging"
        elif "serum" in title.lower():
            benefit = "Professional Anti-Aging Treatment"
        else:
            benefit = "Premium Quality"

        seo_title = f"{title} | {benefit}"
        if vendor:
            seo_title += f" | {vendor}"

        # Ensure optimal length (50-60 chars ideal)
        if len(seo_title) > 60:
            seo_title = f"{title} | {benefit}"

        return seo_title

    def _generate_seo_description(self, product: Dict[str, Any]) -> str:
        """
        Generate SEO meta description.
        Should be 120-160 characters, compelling, and include key terms.
        """
        title = product.get("title", "")
        product_type = product.get("product_type", "")

        # Create compelling meta description
        if "cream" in title.lower():
            seo_desc = (
                f"Experience premium {title.lower()} with natural ingredients. "
                f"Nourishes, protects, and rejuvenates your skin. Shop our luxury skincare collection."
            )
        elif "serum" in title.lower():
            seo_desc = (
                f"Professional-grade {title.lower()} delivers powerful anti-aging results. "
                f"Reduce fine lines and restore radiance. Premium quality guaranteed."
            )
        else:
            seo_desc = (
                f"Discover our premium {title.lower()} - exceptional quality and results. "
                f"Trusted by customers worldwide. Shop now for exclusive offers."
            )

        # Ensure within optimal range
        if len(seo_desc) > 160:
            seo_desc = seo_desc[:157] + "..."

        return seo_desc

    def generate_blog_content(self, topic: str, keywords: List[str]) -> Dict[str, str]:
        """
        Placeholder for future blog content generation.

        Args:
            topic: Blog post topic
            keywords: SEO keywords to include

        Returns:
            Dictionary with blog title, content, and metadata
        """
        return {
            "title": f"Expert Guide: {topic}",
            "content": "Blog content generation coming soon...",
            "keywords": keywords,
            "status": "not_implemented"
        }
