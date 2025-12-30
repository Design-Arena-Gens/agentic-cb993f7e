# Shopify MCP System - Architecture Documentation

## 🏗️ System Architecture

### Overview
The Shopify MCP (Multi-Component Process) System is a modular AI agent architecture designed to audit and optimize e-commerce content at scale. The system follows the MCP pattern where a central coordinator orchestrates specialized agents that perform specific tasks.

### Core Design Principles

1. **Stateless Agents**: All agents are stateless and can be called independently
2. **Single Responsibility**: Each agent has one clearly defined purpose
3. **Loose Coupling**: Agents communicate only through the MCP Server
4. **Extensibility**: New agents can be added without modifying existing code
5. **Testability**: Deterministic logic with mock data for testing
6. **Production-Ready**: Error handling, logging, and API-ready exports

---

## 🎯 System Components

### 1. MCP Server (Coordinator)
**File**: `mcp_server.py`

**Purpose**: Central orchestrator that manages the entire workflow

**Responsibilities**:
- Receives product data from Shopify (or mock data)
- Routes products to appropriate agents
- Applies business logic and prioritization rules
- Aggregates results from multiple agents
- Formats data for external systems (Shopify API, databases, etc.)

**Key Methods**:
- `process_products()`: Main entry point for batch processing
- `process_single_product()`: Processes one product through the pipeline
- `_determine_priority()`: Business logic for issue prioritization
- `get_statistics()`: Generates summary statistics
- `export_for_shopify()`: Formats results for Shopify API updates

**Does NOT**:
- Generate content directly
- Perform content analysis
- Make LLM API calls

---

### 2. Checker MCP (Audit Agent)
**File**: `checker_mcp.py`

**Purpose**: Content quality auditor that identifies issues

**Audit Categories**:
1. **Description Quality**
   - Length validation (min 100 chars)
   - Vague language detection ("good", "stuff", "really")
   - Empty/missing content

2. **SEO Fields**
   - SEO title completeness (min 30 chars)
   - Meta description length (80-160 chars optimal)
   - Keyword presence

3. **Brand Tone**
   - Premium language detection
   - Professional positioning
   - Trust-building elements

4. **Conversion Elements**
   - Call-to-action presence
   - Benefit-focused messaging
   - Customer-centric language

**Output Format**:
```python
{
    "product_id": "prod_001",
    "product_title": "Product Name",
    "issues_found": 5,
    "severity": "high",
    "issues": [
        {
            "type": "description_length",
            "severity": "high",
            "message": "Description too short"
        }
    ]
}
```

**Extensibility**:
- Add new audit rules by creating methods like `_check_new_rule()`
- Adjust thresholds via class constants
- Configure severity levels per issue type

---

### 3. Generator MCP (Content Agent)
**File**: `generator_mcp.py`

**Purpose**: Creates optimized content based on audit feedback

**Content Types**:
1. **Product Descriptions**
   - Premium, warm, trustworthy tone
   - Benefit-focused structure
   - 150-250 words optimal
   - Clear CTA

2. **SEO Titles**
   - 50-60 characters
   - Format: Product | Benefit | Brand
   - Keyword optimized

3. **SEO Meta Descriptions**
   - 120-160 characters
   - Compelling and action-oriented
   - Search-optimized

**Generation Strategy**:
- Rule-based templates (current implementation)
- Ready for LLM integration (see llm_client.py)
- Context-aware based on product type
- Issue-driven improvements

**Output Format**:
```python
{
    "product_id": "prod_001",
    "original_description": "...",
    "optimized_description": "...",
    "optimized_seo_title": "...",
    "optimized_seo_description": "...",
    "improvements_made": [
        "Rewrote description with premium tone",
        "Created SEO-optimized title"
    ]
}
```

---

### 4. LLM Client (Future Integration)
**File**: `llm_client.py`

**Purpose**: Wrapper for external LLM APIs (OpenAI, Anthropic, etc.)

**Current Status**: Placeholder implementation

**Integration Path**:
```python
# Enable LLM
llm = LLMClient(api_key="sk-...", model="gpt-4")
llm.enabled = True

# Use in Generator MCP
description = llm.generate_content(
    prompt=f"Create premium description for {product['title']}",
    max_tokens=500,
    temperature=0.7
)
```

**Planned Features**:
- Content generation
- Sentiment analysis
- Keyword extraction
- Style transformation

---

## 🔄 Workflow & Data Flow

### Standard Processing Pipeline

```
Shopify Products
       ↓
┌──────────────────┐
│   MCP Server     │ ← Entry Point
└──────────────────┘
       ↓
┌──────────────────┐
│  Checker MCP     │ ← Audit Phase
└──────────────────┘
       ↓
    [Issues?]
       ↓
┌──────────────────┐
│ Generator MCP    │ ← Optimization Phase
└──────────────────┘
       ↓
┌──────────────────┐
│   MCP Server     │ ← Aggregation
└──────────────────┘
       ↓
   Export Results
```

### Detailed Step-by-Step

1. **Input**: Load products from Shopify (or mock data)
2. **Routing**: MCP Server sends each product to Checker MCP
3. **Audit**: Checker MCP analyzes content and returns issues
4. **Decision**: MCP Server determines if optimization is needed
5. **Generation**: If needed, Generator MCP creates optimized content
6. **Priority**: MCP Server applies business logic for prioritization
7. **Output**: Results exported in Shopify-compatible format

---

## 🎨 Extensibility Guide

### Adding a New Agent

Example: SEO Analyzer Agent

```python
# seo_analyzer_mcp.py
class SEOAnalyzerMCP:
    def __init__(self):
        self.name = "SEOAnalyzerMCP"
    
    def analyze_keywords(self, product):
        # Implementation
        return {
            "keywords": [...],
            "density": 0.05,
            "recommendations": [...]
        }

# In mcp_server.py
class MCPServer:
    def __init__(self):
        self.checker = CheckerMCP()
        self.generator = GeneratorMCP()
        self.seo_analyzer = SEOAnalyzerMCP()  # New agent
    
    def process_single_product(self, product):
        # Add to workflow
        seo_analysis = self.seo_analyzer.analyze_keywords(product)
        # Use results...
```

### Adding New Content Types

Example: Blog Post Generator

```python
# In generator_mcp.py
def generate_blog_post(self, topic, keywords):
    return {
        "title": self._generate_blog_title(topic),
        "content": self._generate_blog_content(topic, keywords),
        "seo_description": self._generate_blog_seo(topic)
    }

# In mcp_server.py
def process_blog_topic(self, topic, keywords):
    blog = self.generator.generate_blog_post(topic, keywords)
    return blog
```

### Extending Audit Rules

```python
# In checker_mcp.py
def _check_mobile_readability(self, description):
    """Check if content is mobile-friendly."""
    issues = []
    
    sentences = description.split('.')
    avg_length = sum(len(s.split()) for s in sentences) / len(sentences)
    
    if avg_length > 20:
        issues.append({
            "type": "mobile_readability",
            "severity": "medium",
            "message": "Sentences too long for mobile readers"
        })
    
    return issues

# Add to audit_product() method
issues.extend(self._check_mobile_readability(description))
```

---

## 🔌 Integration Points

### Shopify API Integration

```python
import shopify

# Configure Shopify
shopify.ShopifyResource.set_site("https://your-store.myshopify.com")
shopify.Session.setup(api_key="...", secret="...")

# Fetch products
products = shopify.Product.find(limit=50)

# Process through MCP
results = mcp_server.process_products(products)

# Apply updates
for result in results:
    if result['optimization']:
        product = shopify.Product.find(result['product_id'])
        product.body_html = result['optimization']['optimized_description']
        product.save()
```

### Database Integration

```python
# Store audit history
def save_audit_results(result):
    cursor.execute("""
        INSERT INTO audits (product_id, issues_found, severity, created_at)
        VALUES (?, ?, ?, ?)
    """, (result['product_id'], result['audit']['issues_found'], 
          result['audit']['severity'], datetime.now()))
```

### Webhook Integration

```python
# Listen for Shopify product updates
@app.route('/webhooks/products/update', methods=['POST'])
def product_update_webhook():
    product = request.json
    result = mcp_server.process_single_product(product)
    
    if result['action_required']:
        # Send to review queue or auto-apply
        apply_optimizations(result)
    
    return {'status': 'processed'}
```

---

## 📊 Prioritization Logic

### Priority Levels

| Priority | Criteria | Action |
|----------|----------|--------|
| **Critical** | Missing descriptions, broken content | Immediate fix |
| **High** | Poor SEO, no CTA, < 100 chars | High priority queue |
| **Medium** | Tone issues, vague language, 3+ issues | Standard optimization |
| **Low** | Minor improvements, 1-2 small issues | Batch processing |
| **None** | No issues detected | No action needed |

### Business Rules

```python
def _determine_priority(self, audit_result):
    severity = audit_result['severity']
    issue_count = audit_result['issues_found']
    
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
```

---

## 🚀 Deployment Options

### 1. Vercel (Current)
- Serverless functions
- Automatic scaling
- Zero configuration
- Web interface included

### 2. AWS Lambda
```python
def lambda_handler(event, context):
    products = json.loads(event['body'])
    results = mcp_server.process_products(products)
    return {
        'statusCode': 200,
        'body': json.dumps(results)
    }
```

### 3. Docker Container
```dockerfile
FROM python:3.10
WORKDIR /app
COPY . .
CMD ["python", "main.py"]
```

### 4. Scheduled Jobs (Cron)
```bash
# Process all products daily at 2 AM
0 2 * * * /usr/bin/python3 /path/to/main.py
```

---

## 🧪 Testing Strategy

### Unit Tests
```python
# test_checker_mcp.py
def test_description_length():
    checker = CheckerMCP()
    product = {"description": "Short", ...}
    result = checker.audit_product(product)
    assert "description_length" in [i['type'] for i in result['issues']]
```

### Integration Tests
```python
def test_full_pipeline():
    mcp = MCPServer()
    products = get_mock_products()
    results = mcp.process_products(products)
    assert len(results) == len(products)
    assert all('audit' in r for r in results)
```

### Performance Tests
```python
def test_batch_processing_speed():
    products = [generate_mock_product() for _ in range(100)]
    start = time.time()
    results = mcp_server.process_products(products)
    duration = time.time() - start
    assert duration < 10  # Should process 100 products in < 10s
```

---

## 📈 Monitoring & Observability

### Key Metrics

1. **Processing Metrics**
   - Products processed per hour
   - Average processing time
   - Error rate

2. **Quality Metrics**
   - Issues detected per product
   - Issue severity distribution
   - Optimization success rate

3. **Business Metrics**
   - Content quality score trends
   - SEO improvement percentage
   - Conversion rate changes (A/B test)

### Logging Strategy

```python
import logging

logging.info(f"Processing product {product_id}")
logging.warning(f"High priority issues found: {issue_count}")
logging.error(f"Failed to process product {product_id}: {error}")
```

---

## 🔐 Security Considerations

1. **API Keys**: Store in environment variables, never in code
2. **Rate Limiting**: Implement request throttling for external APIs
3. **Input Validation**: Sanitize all product data inputs
4. **Output Sanitization**: Escape HTML in generated content
5. **Access Control**: Authenticate all API endpoints

---

## 🎯 Future Enhancements

### Short-term (1-3 months)
- [ ] Real Shopify API integration
- [ ] LLM API integration (GPT-4, Claude)
- [ ] Database for audit history
- [ ] Batch processing queue

### Medium-term (3-6 months)
- [ ] A/B testing framework
- [ ] Multi-language support
- [ ] Image analysis agent
- [ ] Competitive analysis agent

### Long-term (6-12 months)
- [ ] Auto-apply optimizations
- [ ] Real-time analytics dashboard
- [ ] ML-based quality prediction
- [ ] Multi-store management

---

## 📚 Additional Resources

- [MCP Architecture Pattern](https://example.com/mcp-pattern)
- [Shopify API Documentation](https://shopify.dev/api)
- [Content Optimization Best Practices](https://example.com/content-best-practices)
- [E-commerce SEO Guide](https://example.com/ecommerce-seo)

---

Built with MCP Architecture | Modular • Scalable • Production-Ready
