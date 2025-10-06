# Epic 004: LangSmith Monitoring & Observability

**Priority:** P1 - MISSING BOOTCAMP REQUIREMENT
**Estimated Effort:** 2-3 days
**Value:** Enables debugging, optimization, and demonstration of AI quality
**Bootcamp Requirement:** Week 2 - LangSmith for AI observability

## Problem Statement

ComponentForge mentions LangSmith but lacks comprehensive AI observability. Demo day judges expect to see:
- Real-time traces of multi-agent workflows
- Token usage and cost optimization
- Latency breakdowns per agent
- Error tracking and debugging capabilities
- Comparison of prompt iterations

## Success Metrics

- **Full Trace Coverage:** 100% of AI operations traced in LangSmith
- **Latency Monitoring:** P95 latency <20 seconds for end-to-end generation
- **Cost Tracking:** Token usage per component <100K tokens
- **Error Rate:** <5% AI operation failures
- **Prompt Iterations:** A/B test 3+ prompt variants per agent

## User Stories

### Story 4.1: LangSmith Integration
**As an AI engineer**, I want comprehensive LangSmith tracing so I can debug and optimize the multi-agent workflow.

**Acceptance Criteria:**
- [ ] Configure LangSmith API keys in environment
- [ ] Instrument all LangChain/LangGraph operations
- [ ] Create project per environment: dev, staging, prod
- [ ] Tag traces with: user_id, component_type, session_id
- [ ] Capture inputs, outputs, and intermediate steps for all agents
- [ ] Link traces across agent handoffs

**LangSmith Setup:**
```python
# backend/src/config/langsmith.py
import os
from langsmith import Client

LANGSMITH_CONFIG = {
    "api_key": os.getenv("LANGSMITH_API_KEY"),
    "project": f"component-forge-{os.getenv('ENVIRONMENT', 'dev')}",
    "tracing_enabled": True,
}

client = Client(api_key=LANGSMITH_CONFIG["api_key"])
```

**Instrumented Agent Example:**
```python
# backend/src/agents/token_extractor.py
from langchain.callbacks.tracers import LangChainTracer
from langsmith import traceable

@traceable(
    name="token_extraction",
    tags=["agent:token_extractor", "version:v2.1"],
    metadata={"agent_type": "vision_model"}
)
async def extract_tokens(screenshot_path: str, user_id: str):
    with LangChainTracer(
        project_name="component-forge-prod",
        tags=[f"user:{user_id}", "stage:extraction"]
    ):
        # Vision model call
        response = await vision_chain.ainvoke({
            "image": screenshot_path,
            "prompt": EXTRACTION_PROMPT
        })

        return {
            "tokens": response.tokens,
            "confidence": response.confidence,
            "latency_ms": response.latency
        }
```

**Files to Create:**
- `backend/src/config/langsmith.py`
- `backend/src/middleware/langsmith_middleware.py`
- `backend/tests/monitoring/test_langsmith_integration.py`

---

### Story 4.2: Multi-Agent Workflow Visualization
**As a product manager**, I want to see the complete agent workflow in LangSmith so I can understand where time and tokens are spent.

**Acceptance Criteria:**
- [ ] Create named traces for each of the 7 agents
- [ ] Show parent-child relationships in trace hierarchy
- [ ] Capture latency and token usage per agent
- [ ] Tag failures with error type and recovery action
- [ ] Create LangSmith dashboard for key metrics

**Agent Workflow Trace Structure:**
```
📊 Component Generation (trace_id: abc123)
├─ 🔍 Token Extraction Agent (12.3s, 15K tokens)
│  └─ GPT-4V API Call (11.1s, 14.8K tokens)
├─ 🏷️ Classification Agent (1.2s, 500 tokens)
│  └─ GPT-4 API Call (1.0s, 450 tokens)
├─ 💡 Pattern Proposer 1 (3.4s, 8K tokens)
│  ├─ Vector Search (0.5s)
│  └─ GPT-4 API Call (2.8s, 7.8K tokens)
├─ 💡 Pattern Proposer 2 (3.1s, 7.5K tokens)
├─ 💡 Pattern Proposer 3 (3.6s, 8.2K tokens)
├─ 🎯 Pattern Matcher Agent (2.1s, 3K tokens)
├─ 🏗️ Code Generator Agent (8.7s, 25K tokens)
│  └─ GPT-4 API Call (8.2s, 24.5K tokens)
└─ ✅ Validator Agent (2.3s, 5K tokens)
   ├─ Accessibility Check (0.8s)
   └─ Code Quality Check (1.5s)

Total: 36.7s, 72K tokens, $0.42 cost
```

**LangSmith Dashboard Metrics:**
- Average latency per agent
- Token usage distribution
- Most expensive operations
- Error rate by agent
- Throughput (components/hour)

**Files to Create:**
- `backend/src/monitoring/trace_formatter.py`
- `.claude/docs/langsmith-dashboard-setup.md`

---

### Story 4.3: Prompt Engineering & A/B Testing
**As an AI researcher**, I want to test multiple prompt variants so I can optimize accuracy and cost.

**Acceptance Criteria:**
- [ ] Version control prompts with semantic versioning
- [ ] A/B test 2-3 variants per agent simultaneously
- [ ] Measure success metrics: accuracy, latency, token usage
- [ ] Compare prompt performance in LangSmith
- [ ] Automatically promote winning variant

**Prompt Versioning:**
```python
# backend/src/prompts/versions.py
from typing import Literal

PromptVersion = Literal["v1.0", "v2.0", "v2.1-experiment"]

EXTRACTION_PROMPTS = {
    "v1.0": """
    Analyze this UI screenshot and extract design tokens.
    Focus on colors, spacing, typography, and interactive states.
    """,

    "v2.0": """
    You are an expert design system engineer. Analyze this UI screenshot
    and extract precise design tokens in the following categories:
    - Colors (hex codes with semantic names)
    - Spacing (padding, margins, gaps in px/rem)
    - Typography (font family, size, weight, line-height)
    - Borders (radius, width, color)
    - Shadows (box-shadow values)
    - Interactive states (hover, focus, active, disabled)

    Return results in JSON format with confidence scores.
    """,

    "v2.1-experiment": """
    <system>You are a design token extraction specialist.</system>

    <task>
    Analyze the UI component screenshot and extract ALL design tokens with:
    1. Precise measurements (use browser DevTools accuracy)
    2. Semantic naming (primary-color, not blue)
    3. Confidence scores (0-1) per token
    4. Contextual groupings (button-primary, button-secondary)
    </task>

    <format>
    Return JSON following this schema:
    {
      "colors": {"semantic_name": {"hex": "#...", "confidence": 0.95}},
      "spacing": {"semantic_name": {"value": "12px", "confidence": 0.90}},
      ...
    }
    </format>
    """
}

def get_prompt(version: PromptVersion = "v2.0") -> str:
    return EXTRACTION_PROMPTS[version]
```

**A/B Testing Framework:**
```python
# backend/src/monitoring/ab_testing.py
import random
from langsmith import Client

class PromptABTest:
    def __init__(self, experiment_name: str, variants: dict):
        self.experiment_name = experiment_name
        self.variants = variants
        self.client = Client()

    async def get_variant(self, user_id: str) -> tuple[str, str]:
        # Consistent assignment based on user_id
        variant_id = hash(user_id) % len(self.variants)
        variant_name = list(self.variants.keys())[variant_id]

        return variant_name, self.variants[variant_name]

    async def record_result(self, variant: str, metrics: dict):
        await self.client.create_feedback(
            run_id=metrics["trace_id"],
            key=f"{self.experiment_name}_{variant}",
            score=metrics["accuracy"],
            value={
                "latency": metrics["latency"],
                "token_count": metrics["tokens"],
                "cost": metrics["cost"]
            }
        )

# Usage
ab_test = PromptABTest(
    experiment_name="extraction_v2_vs_v2.1",
    variants={
        "control": EXTRACTION_PROMPTS["v2.0"],
        "experimental": EXTRACTION_PROMPTS["v2.1-experiment"]
    }
)
```

**Success Criteria for Promotion:**
- Accuracy improvement: >5%
- Latency reduction: >10% OR no degradation
- Token usage: <20% increase
- Sample size: 100+ comparisons

**Files to Create:**
- `backend/src/prompts/versions.py`
- `backend/src/monitoring/ab_testing.py`
- `backend/tests/monitoring/test_ab_testing.py`

---

### Story 4.4: Cost Optimization & Budget Alerts
**As a finance lead**, I want to track AI costs and set budgets so we don't exceed spending limits.

**Acceptance Criteria:**
- [ ] Calculate cost per component generated
- [ ] Track token usage by: agent, user, component type
- [ ] Set budget alerts: daily, monthly thresholds
- [ ] Identify most expensive operations
- [ ] Suggest optimization opportunities
- [ ] Dashboard showing cost trends

**Cost Tracking:**
```python
# backend/src/monitoring/cost_tracker.py
from decimal import Decimal

TOKEN_COSTS = {
    "gpt-4-vision-preview": {
        "input": Decimal("0.01") / 1000,   # $0.01 per 1K tokens
        "output": Decimal("0.03") / 1000
    },
    "gpt-4-turbo-2024-04-09": {
        "input": Decimal("0.01") / 1000,
        "output": Decimal("0.03") / 1000
    },
    "text-embedding-3-large": {
        "input": Decimal("0.00013") / 1000,
        "output": Decimal("0")
    }
}

class CostTracker:
    def calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> Decimal:
        pricing = TOKEN_COSTS[model]
        cost = (input_tokens * pricing["input"]) + (output_tokens * pricing["output"])
        return cost.quantize(Decimal("0.0001"))

    async def track_operation(self, operation_id: str, details: dict):
        cost = self.calculate_cost(
            model=details["model"],
            input_tokens=details["input_tokens"],
            output_tokens=details["output_tokens"]
        )

        await self.db.execute("""
            INSERT INTO cost_tracking (
                operation_id, user_id, agent_name, model,
                input_tokens, output_tokens, cost_usd, timestamp
            ) VALUES ($1, $2, $3, $4, $5, $6, $7, NOW())
        """, operation_id, details["user_id"], details["agent"],
             details["model"], details["input_tokens"], details["output_tokens"], cost)

        # Check budget alerts
        await self.check_budget_alerts(details["user_id"])
```

**Budget Alerts:**
```python
BUDGET_THRESHOLDS = {
    "daily": Decimal("100.00"),   # $100/day
    "monthly": Decimal("2000.00")  # $2K/month
}

async def check_budget_alerts(self, user_id: str):
    today_spend = await self.get_daily_spend(user_id)
    month_spend = await self.get_monthly_spend(user_id)

    if today_spend > BUDGET_THRESHOLDS["daily"]:
        await self.send_alert(
            user_id,
            f"⚠️ Daily budget exceeded: ${today_spend} / ${BUDGET_THRESHOLDS['daily']}"
        )

    if month_spend > BUDGET_THRESHOLDS["monthly"] * 0.8:  # 80% warning
        await self.send_alert(
            user_id,
            f"📊 Monthly budget at 80%: ${month_spend} / ${BUDGET_THRESHOLDS['monthly']}"
        )
```

**Cost Dashboard Metrics:**
- Cost per component: $0.42 average
- Most expensive agent: Code Generator ($0.18)
- Daily spend trend
- Cost by component type (buttons cheaper than forms)
- Top 10 most expensive operations

**Files to Create:**
- `backend/src/monitoring/cost_tracker.py`
- `backend/alembic/versions/add_cost_tracking_table.py`
- `app/src/app/admin/costs/page.tsx`

---

### Story 4.5: Error Tracking & Debugging
**As a site reliability engineer**, I want comprehensive error tracking so I can quickly diagnose and fix AI failures.

**Acceptance Criteria:**
- [ ] Integrate Sentry for error tracking
- [ ] Capture AI-specific errors: rate limits, timeouts, validation failures
- [ ] Link Sentry errors to LangSmith traces
- [ ] Create error dashboard with trends
- [ ] Set up alerting for critical errors
- [ ] Implement automatic retries with exponential backoff

**Error Categories:**
```python
# backend/src/monitoring/errors.py
from enum import Enum

class AIErrorType(Enum):
    RATE_LIMIT_EXCEEDED = "rate_limit"          # OpenAI 429
    TIMEOUT = "timeout"                          # >30s response
    INVALID_RESPONSE = "invalid_response"        # Parsing failure
    LOW_CONFIDENCE = "low_confidence"            # <0.7 confidence score
    VALIDATION_FAILURE = "validation_failed"     # Generated code unsafe
    UPSTREAM_API_ERROR = "upstream_error"        # OpenAI 5xx

class AIError(Exception):
    def __init__(self, error_type: AIErrorType, message: str, context: dict):
        self.error_type = error_type
        self.message = message
        self.context = context
        super().__init__(message)
```

**Sentry Integration:**
```python
# backend/src/monitoring/sentry_integration.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.asyncio import AsyncioIntegration

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    environment=os.getenv("ENVIRONMENT", "development"),
    integrations=[
        FastApiIntegration(),
        AsyncioIntegration()
    ],
    traces_sample_rate=0.1,  # 10% of traces
    profiles_sample_rate=0.1,
    before_send=enrich_with_langsmith_trace
)

def enrich_with_langsmith_trace(event, hint):
    # Link to LangSmith trace
    if "trace_id" in hint.get("context", {}):
        event["extra"]["langsmith_trace"] = (
            f"https://smith.langchain.com/o/component-forge/projects/"
            f"component-forge-prod/traces/{hint['context']['trace_id']}"
        )
    return event
```

**Retry Logic:**
```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(AIError),
    before_sleep=log_retry_attempt
)
async def call_ai_agent_with_retry(agent_name: str, input_data: dict):
    try:
        return await agent.ainvoke(input_data)
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise AIError(
            error_type=AIErrorType.UPSTREAM_API_ERROR,
            message=str(e),
            context={"agent": agent_name, "input": input_data}
        )
```

**Files to Create:**
- `backend/src/monitoring/errors.py`
- `backend/src/monitoring/sentry_integration.py`
- `backend/src/middleware/error_handler.py`

---

### Story 4.6: Performance Dashboard
**As a CTO**, I want a real-time dashboard showing system health so I can ensure SLA compliance.

**Acceptance Criteria:**
- [ ] Dashboard at `/admin/monitoring` showing key metrics
- [ ] Real-time metrics: requests/sec, latency, error rate
- [ ] AI-specific metrics: tokens/sec, cost/hour, agent throughput
- [ ] Link to LangSmith and Sentry from dashboard
- [ ] Historical trends (7d, 30d, 90d)
- [ ] Export metrics as CSV/JSON

**Dashboard Metrics:**
```typescript
// app/src/components/monitoring/PerformanceDashboard.tsx
interface SystemMetrics {
  realtime: {
    requestsPerSecond: number;
    avgLatencyMs: number;
    errorRate: number;
    activeUsers: number;
  };
  ai: {
    tokensPerSecond: number;
    costPerHour: number;
    componentsGenerated: number;
    avgConfidence: number;
  };
  agents: {
    name: string;
    avgLatencyMs: number;
    successRate: number;
    tokensUsed: number;
  }[];
  trends: {
    date: string;
    requests: number;
    cost: number;
    errors: number;
  }[];
}
```

**Key Visualizations:**
1. **Latency Heatmap** - P50, P95, P99 by hour
2. **Cost Trend** - Daily spend over 30 days
3. **Agent Performance** - Bar chart of latency per agent
4. **Error Rate** - Time series of errors by type
5. **Token Usage** - Pie chart by agent

**Files to Create:**
- `app/src/app/admin/monitoring/page.tsx`
- `app/src/components/monitoring/PerformanceDashboard.tsx`
- `app/src/components/monitoring/LatencyHeatmap.tsx`
- `backend/src/api/v1/routes/monitoring.py`

---

## Technical Dependencies

- **LangSmith:** `langsmith`, `langchain-core`
- **Monitoring:** `sentry-sdk`, `prometheus-client`
- **Retry Logic:** `tenacity`
- **Visualization:** `recharts`, `tremor` (React)

## LangSmith Projects Structure

```
component-forge-dev/
  ├─ token-extraction-experiments/
  ├─ generation-workflow/
  └─ validation-testing/

component-forge-staging/
  └─ end-to-end-tests/

component-forge-prod/
  ├─ component-generation/
  └─ error-tracking/
```

## Demo Day Presentation

**LangSmith Showcase:**
1. **Live Trace:** Show real component generation in LangSmith
2. **Optimization Story:** "We reduced latency 40% by optimizing Token Extractor"
3. **Cost Analysis:** "Average $0.42 per component, 72K tokens"
4. **A/B Test Results:** "Prompt v2.1 increased accuracy 8% with 15% fewer tokens"

---

## Success Criteria

- [ ] LangSmith integrated with 100% trace coverage
- [ ] All 7 agents instrumented with detailed traces
- [ ] Cost tracking operational with budget alerts
- [ ] Sentry error tracking linked to LangSmith
- [ ] Performance dashboard deployed at `/admin/monitoring`
- [ ] 3+ prompt variants A/B tested per agent
- [ ] Documentation: LangSmith setup and best practices
- [ ] Demo day deck includes LangSmith screenshots

## Timeline

- **Day 1:** LangSmith integration + agent instrumentation
- **Day 2:** Cost tracking + A/B testing framework
- **Day 3:** Error tracking + performance dashboard

## References

- Bootcamp Week 2: LangSmith for Production AI
- LangSmith documentation: https://docs.smith.langchain.com/
- OnCall Lens demo (showed comprehensive monitoring)
- Sentry LangChain integration guide
