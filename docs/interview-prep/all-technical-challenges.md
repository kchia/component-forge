# All Technical Challenges: Comprehensive List

> **Master list of every technical challenge in ComponentForge**
> Pick 3-5 based on your interview focus and practice explaining them with metrics

---

## Table of Contents

1. [AI/ML Engineering Challenges](#aiml-engineering-challenges)
2. [Performance Optimization](#performance-optimization)
3. [Architecture & Design](#architecture--design)
4. [Security & Reliability](#security--reliability)
5. [DevOps & Infrastructure](#devops--infrastructure)
6. [Data & Evaluation](#data--evaluation)
7. [Testing & Quality](#testing--quality)
8. [Frontend Challenges](#frontend-challenges)
9. [Cost Optimization](#cost-optimization)
10. [Decision-Making & Trade-offs](#decision-making--trade-offs)
11. [How to Choose Which to Mention](#-how-to-choose-which-to-mention)

---

## AI/ML Engineering Challenges

### Agent Architecture

- **Built custom 6-agent system** instead of using LangChain/LangGraph
  - Agents: Classifier, TokenExtractor, PropsProposer, EventsProposer, StatesProposer, AccessibilityProposer
  - File: `backend/src/agents/requirement_orchestrator.py:202-207`

- **Rejected LangChain for performance**
  - 200ms lower latency per LLM call (no abstraction overhead)
  - Stack traces: 2-3 frames vs 10+ with LangChain
  - Easier debugging and type safety with Pydantic models

- **Manual orchestration with asyncio**
  - Used `asyncio.gather()` for parallel agent execution
  - 2-3x speedup: 20-30s → 8-12s for requirements proposal
  - Sequential classification → Parallel proposers pattern

- **Implemented confidence scoring**
  - Each agent returns confidence 0.0-1.0 for human review
  - Auto-approve proposals >0.8, surface <0.6 for manual review
  - Enables human-in-loop workflows

- **Graceful degradation with LangSmith**
  - Optional tracing with `@traced` decorator
  - 0ms overhead when disabled (verified with profiling)
  - Works perfectly without LangSmith configured
  - File: `backend/src/core/tracing.py`

---

### Retrieval & RAG

- **Hybrid retrieval system**
  - Combines BM25 (lexical) + Semantic (embeddings)
  - 30% BM25 (precision for exact matches) + 70% Semantic (recall for concepts)
  - File: `backend/src/retrieval/hybrid_retriever.py`

- **A/B tested weight combinations**
  - Tested 6 combinations: 100/0, 80/20, 70/30, 60/40, 50/50, 0/100
  - Golden dataset: 150 component queries with known correct answers
  - Empirically found 30/70 split optimal (94% vs 81% Top-3 accuracy)

- **Min-max normalization for score fusion**
  - BM25 scores: 0-10 range
  - Cosine similarity: 0-1 range
  - Normalized both to 0-1 before weighted combination

- **Over-fetching strategy**
  - Fetch top-20 from each retriever
  - Fuse scores and return top-5
  - Prevents losing high-scoring results from minority retriever (30% BM25)

- **Built RetrievalExplainer**
  - Generates human-readable match explanations
  - Example: "Exact match on keywords: primary, variant | Semantically similar (0.88)"
  - Builds user trust in retrieval system

---

### Evaluation & Testing

- **TokenNormalizer for schema alignment**
  - 362 lines of context-aware mapping logic
  - Solves: GPT-4V extracts generic tokens, ground truth expects component-specific
  - Example: "primary" → "button.primary" vs "alert.info_border"
  - File: `backend/src/evaluation/token_normalizer.py`

- **Context-aware token mapping**
  - Same token name means different things for different components
  - Button vs Alert vs Card have different schema expectations
  - Maps colors, typography, spacing, borders, border radius

- **E2E pipeline evaluator**
  - 4 stages: Token extraction → Requirements proposal → Pattern retrieval → Code generation
  - Measures accuracy at each stage independently
  - File: `backend/src/evaluation/e2e_evaluator.py`

- **Real-time evaluation dashboard**
  - Streams logs at 50+ entries/sec without blocking UI
  - Live metrics visualization during evaluation runs
  - Debounced updates to maintain 60 FPS
  - File: `app/src/components/evaluation/EvaluationDashboard.tsx` (30,642 bytes)

- **AST-based code similarity**
  - Structural similarity, not string matching
  - Compares component structure, props, event handlers
  - Allows for valid implementation variations (73% similarity target)

---

### Prompt Engineering

- **GPT-4V prompt optimization**
  - Vision-specific prompts for token extraction and classification
  - Iterative refinement based on evaluation metrics
  - Context injection: design tokens + classification + screenshot

- **Structured output with JSON mode**
  - Reliable parsing with `response_format={"type": "json_object"}`
  - Pydantic validation for all LLM outputs
  - Reduces parsing errors to near-zero

- **Context injection strategies**
  - Provide classification context to downstream agents
  - Include extracted tokens in requirement proposals
  - Chain of thought for complex reasoning

- **Prompt versioning and A/B testing**
  - Track prompt changes and measure impact on accuracy
  - A/B test different prompt strategies
  - Rollback capability for prompt regressions

---

## Performance Optimization

### Backend Performance

- **Connection pool tuning**
  - Load tested pool sizes: 5, 10, 20, 30, 50
  - Chose 20 base + 10 overflow (30 max concurrent)
  - P95 latency: 950ms → 680ms (-28%)
  - File: `backend/src/core/database.py`

- **Async SQLAlchemy patterns throughout**
  - No blocking I/O in request handlers
  - Async sessions with proper context management
  - `pool_pre_ping=True` for stale connection detection

- **Parallel agent execution**
  - Sequential: 20-30s (5 calls × 4-6s each)
  - Parallel: 8-12s (1 sequential + 4 parallel)
  - Improvement: -60% latency, 2-3x faster

- **Streaming responses for LLM operations**
  - Stream GPT-4 code generation token-by-token
  - Better perceived performance for users
  - Allows early cancellation if needed

---

### Frontend Performance

- **Server-first component strategy**
  - Bundle size: 1.2MB → 780KB (-35%)
  - Moved static layouts, data fetching to server components
  - Only interactive components use 'use client'

- **Core Web Vitals improvements**
  - First Contentful Paint (FCP): 1200ms → 700ms (-42%)
  - Time to Interactive (TTI): 2100ms → 1400ms (-33%)
  - Largest Contentful Paint (LCP): 1800ms → 1100ms (-39%)
  - Hydration time: 450ms → 280ms (-38%)

- **Lazy loading and code splitting**
  - Route-based code splitting with Next.js App Router
  - Dynamic imports for heavy components
  - Suspense boundaries for loading states

- **TanStack Query optimization**
  - 5-minute staleTime for most queries
  - Automatic refetching on window focus
  - Optimistic updates for mutations
  - Debounced log updates (100ms) for 60 FPS streaming

---

### Caching Strategy

- **Data-driven caching analysis**
  - Measured actual cache hit rates, not assumptions
  - 2-week production traffic analysis
  - File: `docs/backend/caching-analysis.md`

- **Rejected prompt caching**
  - Hit rate: <2% (prompts unique per screenshot)
  - Savings: ~$0.001 per hit
  - ROI: Near-zero, not worth 6 hours implementation

- **Rejected embedding caching**
  - Hit rate: 8%
  - Cost per query: $0.000001 (negligible)
  - Savings even with 100% hit rate: pennies

- **Implemented Figma API caching**
  - Hit rate: 35% (users iterate on same designs)
  - Latency saved: 200-500ms per hit
  - TTL: 5 minutes with Redis
  - Average reduction: 70-175ms per request

- **Designed result caching strategy**
  - Hit rate: 22% estimated (users regenerate with tweaks)
  - Latency saved: 30-90s per hit
  - Cost saved: $0.03-0.10 per hit
  - ROI: 675%-1,075% annual ROI (not yet implemented)

---

### Database Optimization

- **Connection pooling with pre-ping**
  - Verifies connections before use (stale connection handling)
  - `pool_size=20, max_overflow=10`
  - Rarely exceeds 18 concurrent connections (10% headroom)

- **Async sessions with context management**
  - Proper session lifecycle (acquire → use → release)
  - `expire_on_commit=False` to prevent lazy loading issues
  - Transaction rollback on errors

- **Query optimization and indexing**
  - Indexed foreign keys and frequently queried columns
  - Avoid N+1 queries with proper eager loading
  - Monitor slow queries in production

- **Read replica planning**
  - Separate analytics queries from transactional queries
  - Future: Read replicas for heavy reporting
  - Write to primary, read from replicas

---

## Architecture & Design

### System Architecture

- **Three-tier architecture**
  - Frontend: Next.js 15 with App Router (port 3000)
  - Backend: FastAPI with async patterns (port 8000)
  - Services: PostgreSQL 16, Qdrant, Redis 7 (Docker Compose)

- **Clear state separation**
  - Client state: Zustand (workflow, proposals, file uploads)
  - Server state: TanStack Query (API responses, caching)
  - Auth/Theme: React Context (rarely changing)

- **Docker Compose orchestration**
  - Health checks for all services (5 retries × 10s intervals)
  - Graceful startup ordering (services wait for dependencies)
  - Redis LRU eviction (256MB, allkeys-lru policy)

- **Migration path planned**
  - Development: Docker Compose (free, simple)
  - Staging: Managed Postgres + Self-hosted Qdrant + Managed Redis
  - Production: Managed Aurora + Qdrant Cloud + ElastiCache
  - Estimated cost: $180-530/month for production

---

### API Design

- **FastAPI with Pydantic v2**
  - Request/response validation with type safety
  - Automatic OpenAPI/Swagger documentation
  - Proper HTTP status codes (200, 201, 400, 401, 404, 429, 500)

- **Dependency injection**
  - Database sessions injected via `Depends(get_db)`
  - Service clients (OpenAI, Redis, Qdrant) as dependencies
  - Easy mocking for tests

- **Structured error responses**
  - Consistent error format: `{"error": "message", "detail": {...}}`
  - Error codes for client-side handling
  - Stack traces in development, hidden in production

- **REST API conventions**
  - Resource-based URLs (`/api/components`, `/api/tokens`)
  - Proper HTTP methods (GET, POST, PUT, DELETE)
  - Pagination for list endpoints

---

### State Management

- **Zustand for client state**
  - Simpler than Redux (no reducers, no actions)
  - Better TypeScript inference
  - 3KB bundle vs 15KB for Redux Toolkit
  - File: `app/src/stores/useWorkflowStore.ts` (293 lines)

- **TanStack Query for server state**
  - Automatic caching with 5-minute staleTime
  - Automatic refetching on window focus
  - Optimistic updates for mutations
  - Loading/error states built-in

- **Persistence middleware**
  - Zustand persist middleware for localStorage
  - Workflow state survives page refresh
  - Partialize to exclude non-serializable data (File objects)

- **React Context for globals**
  - Theme (light/dark mode)
  - Auth session (Auth.js v5)
  - Rarely changing data only

---

### Component Architecture

- **950-line design system specification**
  - Complete component library documented
  - Props, variants, usage examples
  - File: `.claude/BASE-COMPONENTS.md`

- **Component reusability enforcement**
  - P0 components: Button (60+ uses), Card (35+), Badge (25+)
  - P1 components: Tabs, Progress, Alert, Input
  - Prevents duplication and inconsistency

- **shadcn/ui + Radix UI primitives**
  - shadcn/ui as base component library
  - Radix UI for accessible primitives (Dialog, Dropdown, Tooltip)
  - Tailwind CSS v4 for styling with CSS variables

- **Composition over inheritance**
  - Composite components: RequirementCard, PatternCard, MetricCard
  - Wrap base components, don't recreate
  - Example: RequirementCard wraps Card + Badge + Button

---

## Security & Reliability

### Input Validation

- **Multi-layer validation**
  - Layer 1: File size limit (10MB max)
  - Layer 2: Magic number detection (content-based, prevents MIME spoofing)
  - Layer 3: Resolution limit (25MP max, prevents decompression bombs)
  - Layer 4: SVG script detection (blocks malicious SVG)
  - File: `backend/src/security/input_validator.py`

- **Magic number detection**
  - Checks file header bytes, not just extension
  - Prevents .exe renamed to .png attacks
  - Supports: PNG, JPEG, GIF, WebP

- **Decompression bomb prevention**
  - Limits image resolution to 25 megapixels
  - Prevents 1KB file decompressing to 10GB in memory
  - Early detection before full image load

- **SVG security checks**
  - Detects: `<script>`, `onclick=`, `onerror=`, `onload=`, `javascript:`
  - Blocks SVG files with embedded scripts or event handlers
  - Prevents XSS via malicious SVG uploads

---

### Code Security

- **CodeSanitizer with 17 forbidden patterns**
  - Arbitrary code execution: `eval()`, `Function()`, `new Function()`
  - XSS: `dangerouslySetInnerHTML`, `innerHTML=`
  - Prototype pollution: `__proto__`, `constructor.prototype`
  - SQL injection: String concatenation in SQL queries
  - File system: `readFileSync`, `writeFileSync`, `child_process`
  - Hardcoded secrets: `api_key=`, `password=`, `secret=`
  - Other: HTTP (not HTTPS), string refs
  - File: `backend/src/security/code_sanitizer.py`

- **False positive rate: <2%**
  - Tested on 150 generated components
  - Manual review of flagged code
  - Legitimate uses rarely flagged

- **Detection rate: 100%**
  - On synthetic malicious examples
  - Catches all known dangerous patterns

---

### PII Protection

- **GPT-4V-based context-aware detection**
  - Detects: emails, phone numbers, SSNs, credit cards, addresses, names
  - Context-aware: distinguishes real PII from UI placeholders
  - Accuracy: 92% vs 60% with regex-based detection
  - File: `backend/src/security/pii_detector.py`

- **Reduces false positives 5x**
  - Regex: 40% false positive rate
  - GPT-4V: 8% false positive rate
  - Examples: "user@example.com" (placeholder), "555-1234" (placeholder)

- **Configurable auto-block vs warning**
  - Auto-block mode: Reject uploads with PII (confidence >0.8)
  - Warning mode: Log PII detection, continue processing
  - Production: Warning mode (minimize friction)

---

### Rate Limiting

- **Redis-backed sliding window algorithm**
  - Tracks requests in 60-second sliding window
  - Per-IP rate limiting
  - File: `backend/src/middleware/rate_limiter.py`

- **Tiered limits by endpoint**
  - Token extraction: 10 req/min (expensive GPT-4V)
  - Code generation: 20 req/min (expensive GPT-4)
  - Pattern retrieval: 50 req/min (cheaper, cached)
  - Health check: 1000 req/min (no limit)

- **Saves ~$500/month**
  - Prevents abuse of expensive LLM endpoints
  - Blocks ~5-10% of traffic (suspected abuse)

- **Proper HTTP responses**
  - 429 Too Many Requests
  - `Retry-After` header with seconds
  - `X-RateLimit-Limit` and `X-RateLimit-Remaining` headers

---

### Error Handling

- **Graceful degradation**
  - LangSmith tracing optional (works without API key)
  - Figma API caching falls back to direct fetch
  - Partial agent failures return warnings, not errors

- **Retry logic with exponential backoff**
  - LLM calls: 1 retry with 2x backoff
  - Database queries: 3 retries with exponential backoff
  - External APIs: Configurable retry policies

- **Structured logging**
  - JSON format for production (easy parsing)
  - Human-readable for development
  - Includes: timestamp, level, message, context (user_id, request_id)

---

## DevOps & Infrastructure

### Docker & Services

- **Docker Compose setup**
  - PostgreSQL 16 (Alpine) - Primary database
  - Qdrant - Vector database (ports 6333/6334)
  - Redis 7 (Alpine) - Cache and rate limiting

- **Health checks with retries**
  - PostgreSQL: `pg_isready` (5 retries, 10s intervals)
  - Qdrant: HTTP `/health` endpoint
  - Redis: `ping` command
  - 99.5%+ success rate

- **Graceful startup ordering**
  - Services wait for dependencies before starting
  - Backend waits for database + Qdrant + Redis
  - Max wait: 5 retries × 10s = 50s

- **Redis configuration**
  - LRU eviction policy: `allkeys-lru`
  - Max memory: 256MB
  - Optimized for rate limiting and caching

---

### Monitoring & Observability

- **Prometheus metrics collection**
  - `/metrics` endpoint for scraping
  - Tracks: request count, latency, error rate
  - Custom metrics: LLM call duration, token count

- **Structured JSON logging**
  - Production-ready log format
  - Easy parsing with log aggregation tools (ELK, Datadog)
  - Includes context: user_id, request_id, component_type

- **LangSmith tracing for AI operations**
  - Optional observability for LLM calls
  - Traces: prompts, completions, latency, cost
  - Gracefully degrades if unavailable

- **Real-time evaluation dashboard**
  - Live metrics during evaluation runs
  - Stage-by-stage accuracy tracking
  - Log streaming at 50+ entries/sec

---

### Database Management

- **Alembic for schema migrations**
  - Version-controlled database schema
  - Up/down migrations for rollback capability
  - Automatic migration generation from SQLAlchemy models

- **Async PostgreSQL with asyncpg**
  - High-performance async driver
  - Connection pooling for efficiency
  - Proper transaction management

- **Transaction management**
  - Atomic operations with ACID guarantees
  - Rollback on errors
  - Savepoints for nested transactions

---

## Data & Evaluation

### Evaluation Infrastructure

- **Golden dataset for A/B testing**
  - 150 component queries with known correct answers
  - Diverse component types: Button, Alert, Card, Input, Badge
  - Used for retrieval weight tuning and accuracy validation

- **Stage-by-stage accuracy metrics**
  - Token extraction: 78% (with normalization)
  - Requirements proposal: 85% human acceptance
  - Retrieval Top-3: 94%
  - Code generation: 73% structural similarity
  - E2E success: 68% usable without edits

- **Confidence score validation**
  - Each agent returns confidence 0.0-1.0
  - Auto-approve: >0.8 (high confidence)
  - Surface for review: <0.6 (low confidence)
  - Middle ground: 0.6-0.8 (optional review)

- **Human-in-loop workflows**
  - Manual review of low-confidence proposals
  - Thumbs up/down feedback on generated components
  - Feedback loop for prompt improvement

---

### Metrics Tracking

- **Token extraction accuracy: 78%**
  - With TokenNormalizer (schema alignment)
  - Without normalization: 45% (false measurement)
  - Target: >75% ✅

- **Requirements proposal accuracy: 85%**
  - Human acceptance rate in QA testing
  - Confidence score correlation: 0.82
  - Target: >80% ✅

- **Retrieval Top-3 accuracy: 94%**
  - After hybrid retrieval (30% BM25 + 70% Semantic)
  - Before (pure semantic): 81%
  - Target: >90% ✅

- **Code generation similarity: 73%**
  - AST-based structural similarity
  - Not exact string matching (allows valid variations)
  - Target: >70% ✅

- **E2E success rate: 68%**
  - Usable component without edits
  - Measured through user testing
  - Target: >60% ✅

---

### Data Normalization

- **Context-aware token mapping**
  - Colors: "primary" → "button.primary" vs "alert.info_border"
  - Typography: "small" → "button.fontSize_small" vs "alert.message_size"
  - Spacing: "medium" → "button.padding_medium" vs "alert.padding"
  - File: `backend/src/evaluation/token_normalizer.py` (362 lines)

- **Fuzzy matching with 80% threshold**
  - Handles schema variations: camelCase, snake_case, kebab-case
  - Example: "fontSize_small" matches "font_size_small" and "fontSizeSmall"
  - Uses Levenshtein distance for string similarity

- **Component-specific mappings**
  - Button: primary, secondary, text colors + small/medium/large sizes
  - Alert: info/success/warning/error borders + message/title sizes
  - Card: background, border, shadow colors + title/description sizes
  - Extensible for new component types

---

## Testing & Quality

### Testing Strategy

- **Playwright E2E tests**
  - Critical user flows: Upload → Extract → Approve → Generate
  - Cross-browser testing (Chrome, Firefox, Safari)
  - Visual regression testing

- **pytest for backend**
  - Unit tests for individual functions
  - Integration tests for API endpoints
  - Fixtures for database and service mocking

- **axe-core accessibility testing**
  - Automated a11y testing in development
  - Catches: missing ARIA labels, poor contrast, keyboard nav issues
  - Integrated into component development workflow

- **Load testing**
  - Connection pool sizing (tested 5/10/20/30/50)
  - Rate limit validation
  - Database query performance under load

---

### Quality Assurance

- **TypeScript strict mode**
  - No implicit `any` types
  - Strict null checks
  - Strict function types
  - Catches type errors at compile time

- **ESLint + Prettier**
  - Code style consistency
  - Auto-formatting on save
  - Pre-commit hooks for enforcement

- **Code sanitization for generated code**
  - 17 forbidden patterns detected
  - <2% false positive rate
  - 100% detection on synthetic malicious examples

- **Human review for low-confidence outputs**
  - AI proposals with confidence <0.6 flagged
  - QA team reviews before shipping
  - Feedback loop for prompt improvement

---

## Frontend Challenges

### Next.js 15 App Router

- **Server vs client component decision tree**
  - Server: Default (no hooks, no event handlers, no browser APIs)
  - Client: Only for interactivity (onClick, useState, useEffect)
  - Decision tree documented for team

- **Proper Suspense boundaries**
  - Loading states with `loading.tsx` files
  - Streaming with React Suspense
  - Error boundaries with `error.tsx` files

- **Error boundaries with fallback UI**
  - Catch errors in component tree
  - Display user-friendly error messages
  - Log errors for monitoring

- **Route-based code splitting**
  - Automatic with App Router
  - Dynamic imports for heavy components
  - Reduced initial bundle size

---

### Form Handling

- **React Hook Form integration**
  - Controlled forms with minimal re-renders
  - Built-in validation
  - TypeScript type inference

- **Zod schema validation**
  - Client-side validation with Zod schemas
  - Server-side validation with Pydantic (same schema logic)
  - Type-safe form data

- **File upload with drag-and-drop**
  - Custom upload zone component
  - Multiple file support
  - Progress indicators

---

### Accessibility

- **ARIA attributes and keyboard navigation**
  - Proper ARIA labels for screen readers
  - Keyboard focus management
  - Tab order optimization

- **axe-core testing in development**
  - Automated a11y checks during development
  - Catches common issues early
  - Integrated into CI/CD pipeline

- **Semantic HTML**
  - Proper heading hierarchy (h1 → h2 → h3)
  - Semantic elements (nav, main, article, aside)
  - Form labels and fieldsets

- **Focus management**
  - Modal focus trapping
  - Return focus on modal close
  - Skip links for navigation

---

### Image Processing

- **Pillow preprocessing**
  - Resize large images before GPT-4V calls
  - Format conversion (HEIC → JPEG)
  - Quality optimization for faster uploads

- **Screenshot analysis**
  - GPT-4V for visual token extraction
  - Component classification from screenshots
  - Design pattern recognition

- **Multi-format support**
  - PNG, JPEG, WebP, SVG (with security checks)
  - Magic number detection for validation
  - Automatic format detection

---

## Cost Optimization

### LLM Cost Management

- **Rate limiting prevents abuse**
  - Without: $2,400-3,600/month (1,000 unauthorized req/day)
  - With: $1,200-1,800/month (500 legitimate req/day)
  - Savings: ~$500/month

- **Result caching (projected)**
  - 22% cache hit rate on 500 req/day
  - Saves 110 req/day × $0.08-0.12 = $8.8-13.2/day
  - Monthly savings: $264-396

- **Total E2E cost per request**
  - GPT-4V calls: $0.071 (59% of total)
  - GPT-4 calls: $0.045 (37% of total)
  - Embeddings: $0.00005 (0.04% - negligible)
  - Total: $0.08-0.12 per request

- **Embedding costs negligible**
  - $0.00001 per embedding query
  - Even 100% cache hit rate saves pennies
  - Not worth optimizing

---

### Infrastructure Costs

- **Docker Compose saves $180-530/month**
  - Development: Free (Docker Compose)
  - Production: $180-530/month (managed services)
  - Clear ROI tradeoff for different stages

- **Migration path for scaling**
  - Start: Docker Compose (free, simple)
  - Grow: Managed Postgres ($50-150) + Self-hosted Qdrant ($0) + Managed Redis ($30-80)
  - Scale: Managed Aurora + Qdrant Cloud ($100-300) + ElastiCache

- **Cost monitoring and alerting**
  - Track LLM API spend daily
  - Alert on unusual spikes
  - Budget caps for development environments

---

## Decision-Making & Trade-offs

### Framework Decisions

- **Custom agents vs LangChain/LangGraph**
  - ✅ Chose: Custom agents with asyncio
  - Why: 2-3x faster, simpler debugging, lower overhead
  - Trade-off: More code to maintain vs ecosystem loss
  - When reconsidered: If we need multi-step refinement loops

- **Zustand vs Redux**
  - ✅ Chose: Zustand for client state
  - Why: Simpler API, better TypeScript, 3KB vs 15KB bundle
  - Trade-off: Less mature ecosystem vs simplicity
  - When reconsidered: If we need time-travel debugging

- **shadcn/ui vs Material-UI**
  - ✅ Chose: shadcn/ui for component library
  - Why: Full customization, Tailwind integration, copy-paste components
  - Trade-off: Manual updates vs pre-built ecosystem
  - When reconsidered: If we need extensive pre-built components

- **Docker Compose vs Managed Services**
  - ✅ Chose: Docker for development, plan migration
  - Why: Free, simple local dev, clear migration path
  - Trade-off: Not production-ready at scale vs cost savings
  - When reconsidered: At production scale (migration planned)

---

### Architectural Trade-offs

- **Server components vs Client components**
  - ✅ Chose: Server-first strategy
  - Why: 35% smaller bundle, 42% faster FCP
  - Trade-off: More boundary management vs free performance
  - Metrics: 1.2MB → 780KB bundle, 1200ms → 700ms FCP

- **Hybrid retrieval vs Pure semantic**
  - ✅ Chose: 30% BM25 + 70% Semantic
  - Why: 94% vs 81% Top-3 accuracy
  - Trade-off: More complex scoring logic vs better precision/recall
  - Metrics: +13 percentage points improvement

- **Result caching only vs All caching**
  - ✅ Chose: Selective caching (Figma + Result)
  - Why: Data showed <2% prompt hit rate, 100x better ROI for result caching
  - Trade-off: Miss potential savings vs simpler implementation
  - Metrics: 675-1,075% annual ROI for result caching

- **B+ security now vs A+ later**
  - ✅ Chose: B+ (85/100) with roadmap to A
  - Why: Ship securely without blocking on perfection
  - Trade-off: Deferred prompt injection protection vs faster time-to-market
  - Plan: Implement prompt injection in v2

---

### Scale Planning

- **Current capacity vs usage**
  - Capacity: 150 req/s = 12.96M req/day
  - Usage: 500 req/day = 0.004% of capacity
  - Headroom: 2,600x before hitting limits

- **Horizontal scaling path**
  - Current: Single FastAPI worker
  - Next: Multiple workers behind load balancer
  - Future: Auto-scaling based on traffic

- **Read replica strategy**
  - Current: Single PostgreSQL primary
  - Next: Read replicas for analytics queries
  - Future: Write to primary, read from replicas

- **Migration to managed services**
  - Phase 1: Managed Postgres (RDS/Aurora)
  - Phase 2: Qdrant Cloud for vector search
  - Phase 3: ElastiCache for Redis
  - Estimated cost: $180-530/month

---

## 🎯 How to Choose Which to Mention

### For AI/ML Engineering Roles

**Top picks**:
1. Custom multi-agent system (rejected LangChain for performance)
2. Hybrid retrieval with A/B tested weights (94% accuracy)
3. E2E evaluation pipeline with TokenNormalizer
4. GPT-4V prompt optimization and structured outputs
5. Context-aware PII detection with GPT-4V

**Why**: Demonstrates deep AI/ML expertise beyond API usage

---

### For Performance Engineering Roles

**Top picks**:
1. Connection pool profiling (load tested, chose 20+10)
2. Parallel agent execution (2-3x speedup with asyncio)
3. Data-driven caching analysis (rejected low-ROI caching)
4. Server-first component strategy (35% bundle reduction)
5. Frontend performance (42% FCP improvement)

**Why**: Shows systematic performance optimization with data

---

### For Architecture/System Design Roles

**Top picks**:
1. Three-tier architecture with clear state separation
2. Docker → Managed services migration path
3. Server components vs client components trade-off
4. Hybrid retrieval architecture with score fusion
5. Scalability planning (2,600x headroom)

**Why**: Demonstrates systems thinking and production planning

---

### For Security Engineering Roles

**Top picks**:
1. Multi-layer input validation (magic numbers, decompression bombs)
2. CodeSanitizer with 17 forbidden patterns (<2% false positives)
3. GPT-4V PII detection (92% vs 60% with regex)
4. Rate limiting with Redis (saves $500/month)
5. Security roadmap (B+ now, A+ later with prompt injection)

**Why**: Shows comprehensive security thinking and pragmatic prioritization

---

### For Full-Stack Engineering Roles

**Top picks**:
1. Next.js 15 App Router with server-first strategy
2. FastAPI backend with async patterns
3. State management (Zustand + TanStack Query)
4. E2E evaluation dashboard (60 FPS log streaming)
5. Docker Compose orchestration with health checks

**Why**: Demonstrates full-stack expertise from frontend to infrastructure

---

### For DevOps/Infrastructure Roles

**Top picks**:
1. Docker Compose with health checks and retry logic
2. Connection pool tuning (profiling-driven)
3. Migration path to managed services
4. Prometheus metrics and structured logging
5. Database management with Alembic migrations

**Why**: Shows infrastructure thinking and operational maturity

---

## 📝 Usage Tips

1. **Pick 3-5 challenges** that align with the job description
2. **Practice explaining each** with specific metrics (not "much better", say "2-3x faster")
3. **Know the file paths** for authenticity (`backend/src/agents/requirement_orchestrator.py:202-207`)
4. **Explain trade-offs** - what you chose, why, what you gave up, when you'd reconsider
5. **End with learnings** - "What I learned was..." shows growth mindset

---

## 🔗 Cross-References

- **Main Technical Guide**: [technical-challenges-guide.md](./technical-challenges-guide.md)
- **Quick Reference**: [quick-reference.md](./quick-reference.md)
- **Metrics Summary**: [metrics-summary.md](./metrics-summary.md)
- **Example Answers**: [example-answers.md](./example-answers.md)

---

**This is your master list. Pick 3-5 challenges, practice them with metrics, and own your interview!** 🚀
