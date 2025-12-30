"""
Main Entry Point for Shopify MCP System
Demonstrates the complete workflow of the multi-agent system.
"""

import json
from typing import List, Dict, Any
from mcp_server import MCPServer
from shopify_mock import get_mock_products


def print_separator(char: str = "=", length: int = 80):
    """Print a visual separator."""
    print(char * length)


def print_section_header(title: str):
    """Print a formatted section header."""
    print_separator()
    print(f"  {title}")
    print_separator()
    print()


def print_product_audit(result: Dict[str, Any]):
    """Display audit results for a product."""
    audit = result["audit"]

    print(f"Product: {result['product_title']} (ID: {result['product_id']})")
    print(f"Priority: {result['priority'].upper()}")
    print(f"Issues Found: {audit['issues_found']} (Severity: {audit['severity']})")

    if audit["issues"]:
        print("\nDetected Issues:")
        for i, issue in enumerate(audit["issues"], 1):
            severity_symbol = {
                "critical": "🔴",
                "high": "🟠",
                "medium": "🟡",
                "low": "🟢"
            }.get(issue["severity"], "⚪")

            print(f"  {i}. {severity_symbol} [{issue['severity'].upper()}] {issue['type']}")
            print(f"     {issue['message']}")

    print()


def print_optimization_result(result: Dict[str, Any]):
    """Display optimization results."""
    optimization = result.get("optimization")

    if not optimization:
        print("✓ No optimization needed - content is already high quality\n")
        return

    print("Optimization Applied:")
    print(f"Improvements: {len(optimization['improvements_made'])}")

    for improvement in optimization["improvements_made"]:
        print(f"  ✓ {improvement}")

    print()


def print_before_after(result: Dict[str, Any]):
    """Display before/after comparison."""
    optimization = result.get("optimization")

    if not optimization:
        return

    print_separator("-")
    print("BEFORE / AFTER COMPARISON")
    print_separator("-")

    # Description comparison
    if optimization.get("optimized_description"):
        print("\n📝 DESCRIPTION:")
        print("\nOriginal:")
        print(f"  {optimization['original_description'][:200]}...")
        print(f"\n  Length: {len(optimization['original_description'])} characters")

        print("\nOptimized:")
        optimized_desc = optimization['optimized_description']
        # Show first 300 chars for preview
        preview = optimized_desc[:300] + "..." if len(optimized_desc) > 300 else optimized_desc
        print(f"  {preview}")
        print(f"\n  Length: {len(optimized_desc)} characters")

    # SEO Title
    if optimization.get("optimized_seo_title"):
        print("\n🔍 SEO TITLE:")
        print(f"  New: {optimization['optimized_seo_title']}")

    # SEO Description
    if optimization.get("optimized_seo_description"):
        print("\n🔍 SEO META DESCRIPTION:")
        print(f"  New: {optimization['optimized_seo_description']}")
        print(f"  Length: {len(optimization['optimized_seo_description'])} characters")

    print()


def print_statistics(stats: Dict[str, Any]):
    """Display processing statistics."""
    print_section_header("PROCESSING STATISTICS")

    print(f"Total Products Processed: {stats['total_products_processed']}")
    print(f"Products with Issues: {stats['products_with_issues']}")
    print(f"Products Optimized: {stats['products_optimized']}")
    print(f"Total Issues Found: {stats['total_issues_found']}")
    print(f"Completion Rate: {stats['completion_rate']}")

    print("\nPriority Breakdown:")
    for priority, count in stats['priority_breakdown'].items():
        if count > 0:
            print(f"  {priority.capitalize()}: {count}")

    print()


def display_full_optimized_content(result: Dict[str, Any]):
    """Display the complete optimized content."""
    optimization = result.get("optimization")

    if not optimization or not optimization.get("optimized_description"):
        return

    print_section_header(f"FULL OPTIMIZED CONTENT - {result['product_title']}")

    print("OPTIMIZED DESCRIPTION:")
    print(optimization['optimized_description'])
    print()

    if optimization.get("optimized_seo_title"):
        print(f"SEO TITLE: {optimization['optimized_seo_title']}")
        print()

    if optimization.get("optimized_seo_description"):
        print(f"SEO DESCRIPTION: {optimization['optimized_seo_description']}")
        print()


def export_results_to_json(results: List[Dict[str, Any]], filename: str = "optimization_results.json"):
    """Export results to JSON file for further processing."""
    export_data = {
        "results": results,
        "summary": {
            "total_processed": len(results),
            "optimized": sum(1 for r in results if r.get("optimization"))
        }
    }

    with open(filename, 'w') as f:
        json.dump(export_data, f, indent=2)

    print(f"✓ Results exported to {filename}\n")


def main():
    """
    Main execution flow demonstrating the MCP system.
    """
    print_section_header("SHOPIFY MCP SYSTEM - CONTENT OPTIMIZATION")

    # Initialize MCP Server
    print("Initializing MCP Server...")
    mcp_server = MCPServer()
    print("✓ MCP Server ready")
    print(f"✓ Checker MCP loaded: {mcp_server.checker.name}")
    print(f"✓ Generator MCP loaded: {mcp_server.generator.name}")
    print()

    # Load mock products
    print("Loading Shopify products...")
    products = get_mock_products()
    print(f"✓ Loaded {len(products)} products\n")

    # Process products through MCP pipeline
    print_section_header("PROCESSING PRODUCTS")

    results = mcp_server.process_products(products)

    # Display results for each product
    for i, result in enumerate(results, 1):
        print(f"\n{'='*80}")
        print(f"PRODUCT {i} of {len(results)}")
        print('='*80)
        print()

        # Show audit
        print_product_audit(result)

        # Show optimization summary
        print_optimization_result(result)

        # Show before/after
        if result.get("optimization"):
            print_before_after(result)

    # Display full optimized content for products that were changed
    for result in results:
        if result.get("optimization"):
            display_full_optimized_content(result)

    # Show statistics
    stats = mcp_server.get_statistics(results)
    print_statistics(stats)

    # Export results
    print_section_header("EXPORT")
    export_results_to_json(results)

    # Show Shopify-ready payloads
    print_section_header("SHOPIFY UPDATE PAYLOADS")
    print("Ready for Shopify API integration:\n")

    for result in results:
        payload = mcp_server.export_for_shopify(result)
        if payload:
            print(f"Product ID: {payload['product_id']}")
            print(f"Fields to update: {', '.join(payload['updates'].keys())}")
            print()

    # Demonstration of filtered processing
    print_section_header("FILTERED PROCESSING DEMO")
    print("Processing only HIGH priority issues:\n")

    high_priority_results = mcp_server.process_batch_with_filters(
        products,
        min_priority="high"
    )

    print(f"Found {len(high_priority_results)} products requiring immediate attention")
    for result in high_priority_results:
        print(f"  - {result['product_title']} ({result['priority']} priority)")

    print()
    print_separator()
    print("✓ MCP System processing complete!")
    print_separator()


if __name__ == "__main__":
    main()
