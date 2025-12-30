"""
Mock Shopify data for testing the MCP system.
Simulates product data that would come from Shopify API.
"""

from typing import Dict, List, Any


def get_mock_products() -> List[Dict[str, Any]]:
    """
    Returns a list of mock Shopify products with realistic but flawed content.

    Returns:
        List of product dictionaries with id, title, description, and metadata
    """
    return [
        {
            "id": "prod_001",
            "title": "Organic Face Cream",
            "description": "Good cream for your face. Made with natural stuff.",
            "vendor": "LuxeBeauty",
            "product_type": "Skincare",
            "tags": ["organic", "skincare"],
            "seo_title": "",
            "seo_description": "",
            "price": 49.99
        },
        {
            "id": "prod_002",
            "title": "Anti-Aging Serum Premium Formula",
            "description": "Our serum is really good and will make you look younger. "
                          "It has vitamins and other ingredients that are beneficial. "
                          "Many customers like it. Buy now.",
            "vendor": "LuxeBeauty",
            "product_type": "Skincare",
            "tags": ["anti-aging", "serum", "premium"],
            "seo_title": "Anti-Aging Serum",
            "seo_description": "Good serum",
            "price": 89.99
        }
    ]


def get_product_by_id(product_id: str) -> Dict[str, Any]:
    """
    Retrieve a single product by ID.

    Args:
        product_id: The product identifier

    Returns:
        Product dictionary or None if not found
    """
    products = get_mock_products()
    for product in products:
        if product["id"] == product_id:
            return product
    return None
