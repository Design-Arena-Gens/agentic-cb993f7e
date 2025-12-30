"""
Vercel Serverless API for Shopify MCP System
"""

from http.server import BaseHTTPRequestHandler
import json
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from mcp_server import MCPServer
from shopify_mock import get_mock_products


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/':
            self.serve_html()
        elif self.path == '/api/process':
            self.process_products()
        elif self.path == '/api/health':
            self.health_check()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

    def do_POST(self):
        """Handle POST requests."""
        if self.path == '/api/process':
            self.process_products()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

    def serve_html(self):
        """Serve the main HTML interface."""
        html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shopify MCP System - Content Optimization</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        .header {
            background: white;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }

        h1 {
            color: #667eea;
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        .subtitle {
            color: #666;
            font-size: 1.1em;
        }

        .controls {
            background: white;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }

        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 40px;
            font-size: 16px;
            border-radius: 8px;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
            font-weight: 600;
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }

        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .loading {
            display: inline-block;
            margin-left: 10px;
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .stat-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            text-align: center;
        }

        .stat-value {
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 5px;
        }

        .stat-label {
            color: #666;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .results {
            background: white;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }

        .product-card {
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            padding: 25px;
            margin-bottom: 25px;
            transition: border-color 0.3s;
        }

        .product-card:hover {
            border-color: #667eea;
        }

        .product-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            flex-wrap: wrap;
            gap: 10px;
        }

        .product-title {
            font-size: 1.5em;
            color: #333;
            font-weight: 600;
        }

        .priority-badge {
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .priority-high {
            background: #fee;
            color: #c33;
        }

        .priority-medium {
            background: #ffeaa7;
            color: #d63031;
        }

        .priority-low {
            background: #dfe6e9;
            color: #636e72;
        }

        .issues-section {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
        }

        .issue-item {
            padding: 10px;
            margin: 8px 0;
            background: white;
            border-radius: 6px;
            border-left: 4px solid #667eea;
        }

        .issue-type {
            font-weight: 600;
            color: #667eea;
            margin-bottom: 5px;
        }

        .issue-message {
            color: #666;
            font-size: 0.95em;
        }

        .content-comparison {
            display: grid;
            grid-template-columns: 1fr;
            gap: 20px;
            margin-top: 20px;
        }

        .content-box {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
        }

        .content-box h4 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.1em;
        }

        .content-text {
            color: #333;
            line-height: 1.6;
            white-space: pre-wrap;
        }

        .improvements {
            background: #e8f5e9;
            border-radius: 8px;
            padding: 15px;
            margin-top: 15px;
        }

        .improvement-item {
            padding: 8px 0;
            color: #2e7d32;
        }

        .improvement-item:before {
            content: '✓ ';
            font-weight: bold;
        }

        .no-results {
            text-align: center;
            padding: 60px 20px;
            color: #999;
        }

        .error {
            background: #fee;
            color: #c33;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Shopify MCP System</h1>
            <p class="subtitle">AI-Powered Multi-Agent Content Optimization Platform</p>
        </div>

        <div class="controls">
            <button id="processBtn" onclick="processProducts()">
                🚀 Analyze & Optimize Products
                <span id="loading" class="loading" style="display:none;">⏳</span>
            </button>
        </div>

        <div id="stats" class="stats" style="display:none;"></div>
        <div id="results" class="results" style="display:none;"></div>
    </div>

    <script>
        async function processProducts() {
            const btn = document.getElementById('processBtn');
            const loading = document.getElementById('loading');
            const statsDiv = document.getElementById('stats');
            const resultsDiv = document.getElementById('results');

            btn.disabled = true;
            loading.style.display = 'inline-block';

            try {
                const response = await fetch('/api/process');
                const data = await response.json();

                if (data.error) {
                    resultsDiv.innerHTML = `<div class="error">${data.error}</div>`;
                    resultsDiv.style.display = 'block';
                    return;
                }

                displayStats(data.statistics);
                displayResults(data.results);

            } catch (error) {
                resultsDiv.innerHTML = `<div class="error">Error: ${error.message}</div>`;
                resultsDiv.style.display = 'block';
            } finally {
                btn.disabled = false;
                loading.style.display = 'none';
            }
        }

        function displayStats(stats) {
            const statsDiv = document.getElementById('stats');
            statsDiv.innerHTML = `
                <div class="stat-card">
                    <div class="stat-value">${stats.total_products_processed}</div>
                    <div class="stat-label">Products Processed</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${stats.products_with_issues}</div>
                    <div class="stat-label">Issues Found</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${stats.products_optimized}</div>
                    <div class="stat-label">Products Optimized</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${stats.total_issues_found}</div>
                    <div class="stat-label">Total Issues</div>
                </div>
            `;
            statsDiv.style.display = 'grid';
        }

        function displayResults(results) {
            const resultsDiv = document.getElementById('results');

            if (!results || results.length === 0) {
                resultsDiv.innerHTML = '<div class="no-results">No results to display</div>';
                resultsDiv.style.display = 'block';
                return;
            }

            let html = '<h2 style="margin-bottom: 25px; color: #333;">📊 Optimization Results</h2>';

            results.forEach(result => {
                const priorityClass = `priority-${result.priority}`;
                const audit = result.audit;
                const optimization = result.optimization;

                html += `
                    <div class="product-card">
                        <div class="product-header">
                            <div class="product-title">${result.product_title}</div>
                            <div class="priority-badge ${priorityClass}">${result.priority} Priority</div>
                        </div>

                        <div class="issues-section">
                            <h4 style="margin-bottom: 15px; color: #333;">
                                🔍 ${audit.issues_found} Issue${audit.issues_found !== 1 ? 's' : ''} Detected
                            </h4>
                `;

                audit.issues.forEach(issue => {
                    html += `
                        <div class="issue-item">
                            <div class="issue-type">${issue.type.replace(/_/g, ' ').toUpperCase()}</div>
                            <div class="issue-message">${issue.message}</div>
                        </div>
                    `;
                });

                html += '</div>';

                if (optimization) {
                    html += `
                        <div class="content-comparison">
                            <div class="content-box">
                                <h4>📝 Original Description</h4>
                                <div class="content-text">${optimization.original_description}</div>
                            </div>
                            <div class="content-box">
                                <h4>✨ Optimized Description</h4>
                                <div class="content-text">${optimization.optimized_description}</div>
                            </div>
                        </div>

                        <div class="improvements">
                            <h4 style="margin-bottom: 10px; color: #2e7d32;">Improvements Made:</h4>
                    `;

                    optimization.improvements_made.forEach(improvement => {
                        html += `<div class="improvement-item">${improvement}</div>`;
                    });

                    html += '</div>';
                }

                html += '</div>';
            });

            resultsDiv.innerHTML = html;
            resultsDiv.style.display = 'block';
        }
    </script>
</body>
</html>
        """

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())

    def process_products(self):
        """Process products through the MCP system."""
        try:
            # Initialize MCP Server
            mcp_server = MCPServer()

            # Get mock products
            products = get_mock_products()

            # Process products
            results = mcp_server.process_products(products)

            # Get statistics
            stats = mcp_server.get_statistics(results)

            # Send response
            response_data = {
                'status': 'success',
                'results': results,
                'statistics': stats
            }

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode())

        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_response = {
                'status': 'error',
                'error': str(e)
            }
            self.wfile.write(json.dumps(error_response).encode())

    def health_check(self):
        """Health check endpoint."""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {
            'status': 'healthy',
            'service': 'Shopify MCP System',
            'version': '1.0.0'
        }
        self.wfile.write(json.dumps(response).encode())
