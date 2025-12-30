"""
MCP Server - Multi-Component Process Coordinator
Orchestrates agent execution and manages workflow.
"""

from typing import Dict, List, Any
from checker_mcp import CheckerMCP
from generator_mcp import GeneratorMCP


class MCPServer:
    """
    Central coordinator that manages agent interactions.
    Routes tasks, applies business logic, and aggregates results.
    """

    def __init__(self):
        """Initialize the MCP Server with agent instances."""
        self.checker = CheckerMCP()
        self.generator = GeneratorMCP()
        self.name = "MCPServer"

    def process_products(self, products: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Main workflow: audit and optimize multiple products.

        Args:
            products: List of product dictionaries from Shopify

        Returns:
            List of processing results for each product
        """
        results = []

        for product in products:
            result = self.process_single_product(product)
            results.append(result)

        return results

    def process_single_product(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single product through the agent pipeline.

        Workflow:
        1. Send to Checker MCP for audit
        2. If issues found, send to Generator MCP for optimization
        3. Apply business rules
        4. Return consolidated result

        Args:
            product: Product dictionary

        Returns:
            Processing result with audit and optimized content
        """
        # Step 1: Audit the product
        audit_result = self.checker.audit_product(product)

        # Step 2: Initialize result structure
        result = {
            "product_id": product["id"],
            "product_title": product["title"],
            "audit": audit_result,
            "optimization": None,
            "action_required": False,
            "priority": self._determine_priority(audit_result)
        }

        # Step 3: Determine if optimization is needed
        if audit_result["issues_found"] > 0:
            result["action_required"] = True

            # Send to Generator MCP for optimization
            optimization = self.generator.generate_optimized_content(
                product,
                audit_result["issues"]
            )

            result["optimization"] = optimization

        return result

    def _determine_priority(self, audit_result: Dict[str, Any]) -> str:
        """
        Apply business logic to determine processing priority.

        Args:
            audit_result: Audit results from Checker MCP

        Returns:
            Priority level: critical, high, medium, low, none
        """
        severity = audit_result.get("severity", "none")
        issue_count = audit_result.get("issues_found", 0)

        # Business rules for prioritization
        if severity == "critical":
            return "critical"
        elif severity == "high" or issue_count >= 5:
            return "high"
        elif severity == "medium" or issue_count >= 3:
            return "medium"
        elif issue_count > 0:
            return "low"
        else:
            return "none"

    def get_statistics(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate summary statistics from processing results.

        Args:
            results: List of processing results

        Returns:
            Statistics dictionary
        """
        total_products = len(results)
        products_with_issues = sum(1 for r in results if r["audit"]["issues_found"] > 0)
        total_issues = sum(r["audit"]["issues_found"] for r in results)

        priority_counts = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "none": 0
        }

        for result in results:
            priority = result.get("priority", "none")
            priority_counts[priority] += 1

        return {
            "total_products_processed": total_products,
            "products_with_issues": products_with_issues,
            "products_optimized": products_with_issues,
            "total_issues_found": total_issues,
            "priority_breakdown": priority_counts,
            "completion_rate": f"{(total_products / total_products * 100) if total_products > 0 else 0:.1f}%"
        }

    def process_batch_with_filters(
        self,
        products: List[Dict[str, Any]],
        min_priority: str = "low"
    ) -> List[Dict[str, Any]]:
        """
        Process products and filter by priority.

        Args:
            products: List of products to process
            min_priority: Minimum priority level to include in results

        Returns:
            Filtered results
        """
        priority_order = ["none", "low", "medium", "high", "critical"]
        min_priority_index = priority_order.index(min_priority)

        all_results = self.process_products(products)

        # Filter by priority
        filtered_results = [
            result for result in all_results
            if priority_order.index(result["priority"]) >= min_priority_index
        ]

        return filtered_results

    def export_for_shopify(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format result for Shopify API update.

        Args:
            result: Processing result

        Returns:
            Shopify-ready update payload
        """
        if not result.get("optimization"):
            return None

        optimization = result["optimization"]

        payload = {
            "product_id": result["product_id"],
            "updates": {}
        }

        # Add fields that were optimized
        if optimization.get("optimized_description"):
            payload["updates"]["description"] = optimization["optimized_description"]

        if optimization.get("optimized_seo_title"):
            payload["updates"]["seo_title"] = optimization["optimized_seo_title"]

        if optimization.get("optimized_seo_description"):
            payload["updates"]["seo_description"] = optimization["optimized_seo_description"]

        return payload if payload["updates"] else None
