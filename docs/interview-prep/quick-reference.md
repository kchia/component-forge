# Quick Reference: Technical Challenges Cheat Sheet

> **2-page quick reference for last-minute interview prep**
> Print this and review 30 minutes before your interview

---

## Top 6 Talking Points

### 1. Custom Multi-Agent System (Rejected LangChain)

**One-liner**: "Built custom 6-agent system using OpenAI SDK directly; rejected LangChain for 2-3x better performance"

**Key Facts**:
- **Performance**: 20-30s → 8-12s (2-3x faster)
- **Latency**: 200ms lower per LLM call (no abstraction overhead)
- **Technique**: `asyncio.gather()` for parallel execution
- **Why**: LangGraph state machines were overkill for linear-then-parallel workflow

**File**: `backend/src/agents/requirement_orchestrator.py:202-207`

**30-second pitch**:
> "We needed to extract design requirements from screenshots using multiple specialized agents. Initially considered LangChain/LangGraph, but after prototyping found it added 200ms overhead per call with 10+ abstraction layers. Built a custom system using OpenAI SDK directly with manual asyncio orchestration. This gave us 2-3x performance improvement (20-30s → 8-12s) and simpler debugging. The key was using asyncio.gather() to run 4 requirement proposers in parallel after a sequential classification step."

---

### 2. Hybrid Retrieval System (30% BM25 + 70% Semantic)

**One-liner**: "Tuned hybrid retrieval via A/B testing; achieved 94% Top-3 accuracy vs 81% with pure semantic search"

**Key Facts**:
- **Improvement**: 81% → 94% Top-3 accuracy (+13 pp)
- **Weights**: 30% BM25 (keyword precision) + 70% Semantic (conceptual recall)
- **Methodology**: A/B tested 6 weight combinations on 150 queries
- **Why**: Semantic search over-matched concepts, missed exact keywords

**File**: `backend/src/retrieval/hybrid_retriever.py`

**30-second pitch**:
> "Pure semantic search was failing on exact keyword matches like 'primary variant' while over-matching on general concepts. We implemented hybrid retrieval combining BM25 (lexical) and semantic search with weighted fusion. A/B tested 6 weight combinations on 150 component queries and found 30% BM25 + 70% semantic gave us 94% Top-3 accuracy vs 81% with pure semantic. The key insight was BM25 provides precision while semantic provides recall - the 30/70 split balances both."

---

### 3. Token Normalization (Schema Mismatch Solution)

**One-liner**: "Built 362-line TokenNormalizer to solve schema mismatch; revealed true accuracy was 78% not 45%"

**Key Facts**:
- **Impact**: 45% → 78% measured accuracy (+33 pp)
- **Problem**: GPT-4V extracts generic tokens, ground truth expects component-specific
- **Solution**: Context-aware mapping (e.g., "primary" → "button.primary" vs "alert.info_border")
- **Why**: Same token name means different things for different components

**File**: `backend/src/evaluation/token_normalizer.py` (362 lines)

**30-second pitch**:
> "The hardest evaluation challenge was token schema mismatch. GPT-4V extracted generic tokens like 'primary color' but ground truth expected component-specific schemas like 'button.primary' or 'alert.info_border'. Built a 362-line TokenNormalizer with context-aware mapping - same token name maps differently based on component type. This revealed our actual extraction accuracy was 78%, not the 45% we initially measured. Critical for achieving accurate evaluation metrics and iterating on prompt improvements."

---

### 4. Data-Driven Caching (Rejected Prompt/Embedding Caching)

**One-liner**: "Measured cache hit rates; rejected low-ROI prompt caching (<2% hits) for high-ROI result caching (30-90s saved)"

**Key Facts**:
- **REJECTED**: Prompt caching (<2% hit rate), Embedding caching ($0.000001 cost)
- **IMPLEMENTED**: Figma API caching (35% hit rate, 200-500ms saved)
- **RECOMMENDED**: Result caching (22% hit rate, 30-90s + $0.03-0.10 saved)
- **Why**: Data-driven decisions vs premature optimization

**File**: `docs/backend/caching-analysis.md`

**30-second pitch**:
> "We analyzed actual usage patterns before implementing caching. Found prompt caching would have <2% hit rate (prompts are unique per screenshot) and embedding caching saves negligible cost ($0.000001 per query). Instead, focused on result caching - caching final generated code saves 30-90s latency and $0.03-0.10 per hit with 22% hit rate. This is a great example of using data to drive architecture decisions rather than prematurely optimizing."

---

### 5. Connection Pool Profiling (20 Base + 10 Overflow)

**One-liner**: "Load tested to find optimal pool size (20); improved P95 latency from 950ms to 680ms (-28%)"

**Key Facts**:
- **Result**: pool_size=20, max_overflow=10 (30 max concurrent)
- **Impact**: P95 latency 950ms → 680ms (-28%)
- **Methodology**: Load tested pool sizes 5/10/20/30/50 under realistic traffic
- **Why**: 10 was too small (blocking), 30+ had diminishing returns

**File**: `backend/src/core/database.py`

**30-second pitch**:
> "We needed to optimize async database performance. Load tested pool sizes from 5 to 50 under realistic traffic patterns. Found pool_size=10 caused blocking (P95 latency 950ms), while 20 gave us 680ms with no blocking. Profiling showed we rarely exceed 18 concurrent connections, so 20 base + 10 overflow (30 max) handles traffic spikes without overwhelming Postgres. This is a good example of profiling-driven optimization rather than guessing."

---

### 6. Security Guardrails (B+ Grade, 17 Forbidden Patterns)

**One-liner**: "Implemented B+ (85/100) security with multi-layer validation, 17 forbidden patterns, GPT-4V PII detection"

**Key Facts**:
- **Grade**: B+ (85/100) - production-ready, room for improvement
- **Code Sanitization**: 17 forbidden patterns (eval, XSS, prototype pollution, SQL injection)
- **PII Detection**: GPT-4V context-aware (92% accuracy vs 60% with regex)
- **Rate Limiting**: Redis-backed, tiered limits (10 req/min for token extraction)
- **Not Yet**: Prompt injection protection (planned v2)

**Files**: `backend/src/security/code_sanitizer.py`, `docs/backend/guardrails-analysis.md`

**30-second pitch**:
> "Implemented comprehensive guardrails for code generation security. Built multi-layer input validation (magic numbers, size limits, SVG sanitization), code sanitization with 17 forbidden patterns (eval, XSS, prototype pollution), and Redis-backed rate limiting with tiered limits. Most interesting was GPT-4V-based PII detection - uses context awareness to distinguish real PII from UI placeholders, achieving 92% accuracy vs 60% with regex. Currently B+ security grade, intentionally deferring prompt injection protection to v2 to ship securely without blocking on perfection."

---

## Key Metrics at a Glance

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| **E2E Latency** | 30-90s | 18-25s | -40% |
| **Requirements Proposal** | 20-30s | 8-12s | -60% (2-3x) |
| **Retrieval Top-3 Accuracy** | 81% | 94% | +13 pp |
| **Token Extraction Accuracy** | 45% | 78% | +33 pp (with normalization) |
| **Frontend Bundle Size** | 1.2MB | 780KB | -35% |
| **First Contentful Paint** | 1200ms | 700ms | -42% |
| **Database P95 Latency** | 950ms | 680ms | -28% |
| **PII Detection Accuracy** | 60% (regex) | 92% (GPT-4V) | +32 pp |

---

## Architecture Trade-offs (Quick Summary)

### Custom Agents vs LangGraph
- **Chose**: Custom agents with asyncio
- **Why**: 2-3x faster, simpler debugging
- **Trade-off**: More code to maintain vs ecosystem loss

### Hybrid vs Pure Semantic Retrieval
- **Chose**: 30% BM25 + 70% Semantic
- **Why**: 94% vs 81% accuracy
- **Trade-off**: More complex scoring vs better precision/recall

### Result Caching vs Prompt Caching
- **Chose**: Result caching only
- **Why**: <2% prompt hit rate, 100x better ROI
- **Trade-off**: Miss potential savings vs simpler implementation

### Server vs Client Components
- **Chose**: Server-first strategy
- **Why**: 35% smaller bundle, 500ms faster FCP
- **Trade-off**: More boundary management vs free performance

### pool_size=20 vs 10/30/50
- **Chose**: 20 base + 10 overflow
- **Why**: P95 <2s, no blocking under normal load
- **Trade-off**: More memory vs better latency

### Docker Compose vs Managed Services
- **Chose**: Docker for now, plan migration
- **Why**: Free, simple local dev
- **Trade-off**: Not production-ready at scale vs cost savings

---

## File Paths (Quick Reference)

**Multi-Agent System**:
- `backend/src/agents/requirement_orchestrator.py:202-207` (parallel execution)
- `backend/src/agents/base_proposer.py` (base class)

**Hybrid Retrieval**:
- `backend/src/retrieval/hybrid_retriever.py` (weighted fusion)

**Evaluation**:
- `backend/src/evaluation/token_normalizer.py` (362 lines, context-aware)
- `backend/src/evaluation/e2e_evaluator.py` (end-to-end pipeline)

**Security**:
- `backend/src/security/code_sanitizer.py` (17 patterns)
- `backend/src/security/pii_detector.py` (GPT-4V-based)
- `docs/backend/guardrails-analysis.md` (B+ grade)

**Performance**:
- `backend/src/core/database.py` (pool_size=20)
- `docs/backend/caching-analysis.md` (data-driven decisions)

**Frontend**:
- `app/src/components/evaluation/EvaluationDashboard.tsx` (30,642 bytes)
- `.claude/BASE-COMPONENTS.md` (950 lines, design system)

---

## Interview Strategy

### If asked: "What was the biggest technical challenge?"

**Choose ONE of**: Multi-agent system, Hybrid retrieval, Token normalization

**Structure**:
1. **Context** (10s): "We needed to extract design requirements from screenshots..."
2. **Problem** (10s): "Initially tried X, but found Y issue..."
3. **Solution** (20s): "Built custom Z with A, B, C features..."
4. **Impact** (10s): "This gave us X% improvement / Y seconds faster / Z% accuracy"
5. **Learning** (10s): "Key insight was... / What I learned was..."

### If asked: "How did you make technical decisions?"

**Talk about**: Caching analysis (data-driven vs premature optimization)

**Structure**:
1. "We analyzed actual usage patterns before implementing caching"
2. "Found prompt caching would have <2% hit rate based on real data"
3. "Instead focused on result caching with 100x better ROI"
4. "This shows importance of measuring first, optimizing second"

### If asked: "How do you handle trade-offs?"

**Pick ONE trade-off from above**, explain:
1. What you chose
2. Why you chose it (quantitative reasons)
3. What you gave up
4. When you'd reconsider

### If asked: "Tell me about a time you optimized performance"

**Talk about**: Connection pool profiling OR Parallel agent execution

**Structure**:
1. "Initial performance was unacceptable (30-90s E2E)"
2. "Load tested pool sizes 5/10/20/30/50 to find optimal"
3. "Found 20 gave us P95 <2s with no blocking"
4. "This is profiling-driven optimization, not guessing"

### If asked: "How do you ensure security?"

**Talk about**: Guardrails system (B+ grade)

**Structure**:
1. "Implemented multi-layer security (validation + sanitization + rate limiting)"
2. "Most interesting was GPT-4V PII detection (92% vs 60% with regex)"
3. "Currently B+ security, intentionally deferring prompt injection to v2"
4. "Shows gradual rollout strategy - ship securely without blocking on perfection"

---

## 30-Second Elevator Pitch (Project Overview)

> "ComponentForge is a full-stack AI engineering project that generates production-ready React components from UI screenshots. The interesting technical challenges were: (1) building a custom multi-agent system with OpenAI SDK directly for 2-3x better performance than LangChain, (2) implementing hybrid retrieval with A/B tested weights achieving 94% accuracy, and (3) building comprehensive evaluation infrastructure with context-aware token normalization. The project demonstrates senior-level systems thinking - data-driven decisions, performance profiling, security guardrails, and thoughtful architecture trade-offs."

---

## Red Flags to Avoid

❌ "We used LangChain because everyone uses it"
✅ "We evaluated LangChain but chose custom agents for 2-3x better performance"

❌ "We cached everything for better performance"
✅ "We measured cache hit rates and found prompt caching had <2% ROI"

❌ "We achieved 78% token extraction accuracy"
✅ "We achieved 78% accuracy after building a TokenNormalizer to solve schema mismatch"

❌ "We implemented all the security features"
✅ "We're at B+ security grade, intentionally deferring prompt injection to v2"

❌ "It's much faster now"
✅ "We improved E2E latency from 30-90s to 18-25s, a 40% reduction"

---

## Follow-up Question Preparedness

**If they ask for more details on multi-agent system**:
- Explain 6 agents: Classifier, TokenExtractor, PropsProposer, EventsProposer, StatesProposer, AccessibilityProposer
- Show asyncio.gather() code example
- Explain confidence scoring (0.0-1.0, auto-approve >0.8)

**If they ask about trade-offs**:
- Pick ONE trade-off from the list
- Explain what you chose, why, what you gave up, when you'd reconsider
- Use quantitative data (not "much better", say "2-3x faster")

**If they ask about evaluation**:
- Explain E2E pipeline evaluator (4 stages)
- Focus on TokenNormalizer (362 lines, context-aware)
- Show real-time dashboard with 60 FPS log streaming

**If they ask about production readiness**:
- Docker Compose → Managed services migration path
- Connection pooling (20+10)
- Rate limiting (Redis-backed, tiered)
- Security guardrails (B+ grade, roadmap for A)
