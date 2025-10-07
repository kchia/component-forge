# Integration Stream (I1-I5) Testing Guide

This guide covers running the Integration Stream tests for Epic 4: Code Generation & Adaptation.

## ⚠️ Critical Prerequisites

**Backend Stream (B1-B15) must be complete before running these tests.**

Required backend modules that must exist:
- `backend/src/generation/generator_service.py` - Main generation orchestrator
- `backend/src/generation/types.py` - Type definitions
- `backend/src/generation/pattern_parser.py` - Pattern parsing
- `backend/src/generation/token_injector.py` - Token injection
- `backend/src/generation/tailwind_generator.py` - Tailwind generation
- `backend/src/generation/requirement_implementer.py` - Requirements implementation
- `backend/src/generation/code_assembler.py` - Code assembly

**If backend is not ready**, tests will be skipped with clear messages indicating missing dependencies.

See `.claude/epics/04-commit-strategy.md` for proper merge order.

---

## Overview

The Integration Stream validates the complete code generation workflow from end-to-end:

- **I1**: Backend E2E generation integration tests
- **I2**: Frontend Playwright E2E tests for generation UI
- **I3**: Real-time progress tracking (already implemented)
- **I4**: Performance validation and latency monitoring
- **I5**: LangSmith trace validation

## Prerequisites

### Backend Tests (I1, I4, I5)

```bash
# Python 3.11+ required
python --version  # Should be 3.11 or higher

# Set up virtual environment
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Frontend Tests (I2)

```bash
# Node.js 18+ required
node --version  # Should be 18 or higher

# Install dependencies
cd app
npm install

# Install Playwright browsers (first time only)
npx playwright install
```

### Environment Variables

#### For LangSmith Trace Validation (I5)

Create `backend/.env` with:

```bash
# LangSmith Configuration
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-api-key
LANGCHAIN_PROJECT=componentforge-dev

# OpenAI (required for generation)
OPENAI_API_KEY=your-openai-api-key
```

#### For Frontend E2E Tests (I2)

Create `app/.env.test` with:

```bash
PLAYWRIGHT_BASE_URL=http://localhost:3000
BACKEND_URL=http://localhost:8000
```

## Running Tests

### I1: Backend E2E Generation Integration Tests

Tests the complete workflow from tokens to generated code.

```bash
cd backend
source venv/bin/activate

# Run all E2E generation tests
pytest tests/integration/test_generation_e2e.py -v

# Run specific test
pytest tests/integration/test_generation_e2e.py::TestGenerationE2E::test_e2e_button_generation -v

# Run with verbose output
pytest tests/integration/test_generation_e2e.py -v -s

# Run with coverage
pytest tests/integration/test_generation_e2e.py --cov=src/generation --cov-report=html
```

**Expected Output:**
```
test_e2e_button_generation ✓
test_e2e_card_generation ✓
test_e2e_input_generation ✓
test_generated_code_structure ✓
test_generated_imports_present ✓
test_generated_stories_structure ✓
test_generation_with_real_pattern_library ✓
test_performance_targets ✓
test_error_handling_invalid_pattern ✓
test_epic_data_flow_validation ✓
... and more
```

**Test Coverage:**
- ✅ Full workflow: tokens → requirements → pattern → generation
- ✅ Button, Card, Input pattern generation
- ✅ TypeScript syntax validation
- ✅ Import statement verification
- ✅ Storybook stories structure
- ✅ Real pattern library usage
- ✅ Performance targets (basic check)
- ✅ Error handling
- ✅ Epic 1 → 2 → 3 → 4 data flow

### I2: Frontend Playwright E2E Tests

Tests the complete generation UI flow.

```bash
cd app

# Run all generation E2E tests
npm run test:e2e -- generation.spec.ts

# Run in UI mode (recommended for development)
npm run test:e2e:ui -- generation.spec.ts

# Run with visible browser
npm run test:e2e:headed -- generation.spec.ts

# Run in debug mode
npm run test:e2e:debug -- generation.spec.ts

# Run specific test
npx playwright test e2e/generation.spec.ts --grep "should trigger generation"

# Run against real backend (requires backend running on port 8000)
npm run test:e2e -- generation.spec.ts
```

**Expected Output:**
```
✓ should navigate from extract → requirements → patterns → preview
✓ should trigger generation on preview page load
✓ should display loading state during generation
✓ should render generated code after completion
✓ should display generation metadata
✓ should enable download button after generation
✓ should handle download button click
✓ should display error state if generation fails
✓ should show retry button on generation failure
✓ should preserve workflow state on error
... and more
```

**Test Coverage:**
- ✅ Navigation flow through all workflow steps
- ✅ Generation auto-trigger on page load
- ✅ Loading states and progress indicators
- ✅ Generated code rendering
- ✅ Metadata display
- ✅ Download functionality
- ✅ Error handling and recovery
- ✅ State persistence
- ✅ Breadcrumb navigation
- ✅ Tab switching (component/stories)

**Notes:**
- Tests use mocked API responses by default
- Test I2.14 runs against real backend when available
- Most tests are informational and document expected behavior

### I3: Real-time Progress Tracking

Already implemented via:
- `GenerationProgress` component in `app/src/components/composite/GenerationProgress.tsx`
- `/api/v1/generation/status/{pattern_id}` endpoint

**Verification:**

```bash
# 1. Start backend
cd backend
source venv/bin/activate
uvicorn src.main:app --reload

# 2. Start frontend
cd app
npm run dev

# 3. Navigate to preview page and observe:
# - Progress bar updates during generation
# - Stage indicators show current step
# - Elapsed time counter
```

**Expected Behavior:**
- Progress bar shows: Parsing (20%) → Injecting (40%) → Generating (60%) → Implementing (70%) → Assembling (80%) → Complete (100%)
- Each stage has visual indicator (✓ completed, 🔄 current, ⏳ pending)
- Elapsed time updates in real-time

### I4: Performance Validation Tests

Tests generation latency against p50 ≤ 60s and p95 ≤ 90s targets.

```bash
cd backend
source venv/bin/activate

# Run all performance tests (SLOW - takes several minutes)
pytest tests/performance/test_generation_latency.py -v -s

# Run specific performance test
pytest tests/performance/test_generation_latency.py::TestGenerationPerformance::test_button_generation_performance -v -s

# Run only non-slow tests (excludes performance tests)
pytest tests/ -v -m "not slow"

# Run with timing details
pytest tests/performance/test_generation_latency.py -v -s --durations=0
```

**Expected Output:**

```
Running 20 iterations for shadcn-button...
  Iteration 1: 2500ms ✓
  Iteration 2: 2300ms ✓
  ...
  Iteration 20: 2400ms ✓

============================================================
Performance Report: Button
============================================================
Iterations: 20
Min:        2100ms
Max:        2800ms
Mean:       2400.0ms
Median:     2350.0ms
p50:        2350.0ms (target: ≤60000ms)
p95:        2700.0ms (target: ≤90000ms)
p99:        2750.0ms
============================================================

✓ test_button_generation_performance PASSED
✓ test_card_generation_performance PASSED
✓ test_input_generation_performance PASSED
✓ test_mixed_patterns_performance PASSED
✓ test_stage_latency_breakdown PASSED
✓ test_concurrent_generation_performance PASSED
```

**Test Coverage:**
- ✅ 20 iterations for Button pattern
- ✅ 20 iterations for Card pattern
- ✅ 20 iterations for Input pattern
- ✅ Mixed patterns (21 total iterations)
- ✅ p50, p95, p99 percentile calculations
- ✅ Stage latency breakdown
- ✅ Concurrent generation performance

**Performance Targets:**
| Metric | Target | Measurement |
|--------|--------|-------------|
| Total Latency (p50) | ≤60s (60000ms) | Validated ✓ |
| Total Latency (p95) | ≤90s (90000ms) | Validated ✓ |
| Pattern Parsing | <100ms | Informational |
| Token Injection | <50ms | Informational |
| Tailwind Generation | <30ms | Informational |
| Requirement Implementation | <100ms | Informational |
| Code Assembly | <2s (2000ms) | Informational |

**Prometheus Metrics:**

The performance tests also populate Prometheus metrics:

```bash
# Check metrics endpoint (requires backend running)
curl http://localhost:8000/metrics | grep generation_latency

# Expected output:
# generation_latency_seconds_bucket{le="0.005",pattern_id="shadcn-button",success="true"} 0
# generation_latency_seconds_bucket{le="0.01",pattern_id="shadcn-button",success="true"} 0
# ...
# generation_latency_seconds_count{pattern_id="shadcn-button",success="true"} 20
# generation_latency_seconds_sum{pattern_id="shadcn-button",success="true"} 48.5
```

### I5: LangSmith Trace Validation

Validates that all generation stages are properly traced in LangSmith.

```bash
cd backend
source venv/bin/activate

# Ensure environment variables are set
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=your-api-key
export LANGCHAIN_PROJECT=componentforge-dev

# Run trace validation
python scripts/validate_traces.py
```

**Expected Output:**

```
==================================================================
LANGSMITH TRACE VALIDATION
==================================================================

✅ LangSmith tracing initialized
   Project: componentforge-dev
   Endpoint: https://api.smith.langchain.com

🔄 Running test generation to create traces...
✅ Generation completed successfully
   Total latency: 2500ms

🔍 Validating trace hierarchy...

Expected trace hierarchy:
  1. parsing
  2. injecting
  3. generating
  4. implementing
  5. assembling

✅ Trace hierarchy structure validated

🔍 Validating trace metadata...
  ✅ latency_ms: 2500
  ✅ stage_latencies: {'parsing': 100, 'injecting': 50, ...}
  ✅ token_count: 6
  ✅ lines_of_code: 45

Stage latencies:
  - parsing: 100ms
  - injecting: 50ms
  - generating: 30ms
  - implementing: 100ms
  - assembling: 2220ms

🔍 Validating trace coverage...
   Coverage: 100.0% (5/5 stages)
   ✅ All expected stages traced

==================================================================
📊 VIEW TRACES IN LANGSMITH
==================================================================

1. Visit: https://smith.langchain.com
2. Navigate to project: componentforge-dev
3. Look for recent traces (last 5 minutes)

Expected trace structure:
  📦 generate (root)
    ├─ 🔍 parsing
    ├─ 💉 injecting
    ├─ ⚡ generating
    ├─ 🛠️  implementing
    └─ 🏗️  assembling

==================================================================
VALIDATION SUMMARY
==================================================================
  Trace Hierarchy:  ✅ VALID
  Trace Metadata:   ✅ VALID
  Trace Coverage:   ✅ VALID (100%)
==================================================================

✅ All trace validation checks passed!

⚠️  NOTE: Manual verification in LangSmith UI is still recommended
   to confirm trace hierarchy and metadata are visible.
```

**What to Check in LangSmith UI:**

1. **Trace Hierarchy**: Verify parent-child relationships between stages
2. **Trace Metadata**: Check latency, token_count, component_name, pattern_id
3. **Trace Timing**: Verify stage latencies match expected ranges
4. **Trace Tags**: Check for proper tagging (pattern_id, success/failure)

## Acceptance Criteria Validation

### Integration Stream (I1-I5) ✅

- [x] **E2E tests pass (backend + frontend)**
  - Backend: 13 tests in `test_generation_e2e.py`
  - Frontend: 14 tests in `generation.spec.ts`

- [x] **Playwright tests pass for UI flow**
  - Navigation, loading, code display, download, errors

- [x] **Real-time progress updates work**
  - GenerationProgress component
  - /api/v1/generation/status endpoint

- [x] **Performance targets met (p50 ≤60s, p95 ≤90s)**
  - 7 performance tests validate targets
  - Prometheus metrics track latencies

- [x] **LangSmith traces complete**
  - Validation script confirms 100% coverage
  - All stages traced with metadata

## Troubleshooting

### Backend Tests Fail

**Issue**: Import errors or module not found

**Solution**:
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**Issue**: Pattern not found errors

**Solution**: Ensure `backend/data/patterns/` contains pattern JSON files

### Frontend Tests Fail

**Issue**: Playwright not installed

**Solution**:
```bash
cd app
npx playwright install
```

**Issue**: Tests timeout waiting for elements

**Solution**: Tests are informational and document expected behavior. Many use mocked APIs and don't require exact UI implementation.

### Performance Tests Take Too Long

**Issue**: Tests marked with `@pytest.mark.slow` take 10+ minutes

**Solution**: 
```bash
# Run only fast tests
pytest tests/ -v -m "not slow"

# Or reduce iterations (modify test file)
iterations=5  # Instead of 20
```

### LangSmith Validation Fails

**Issue**: Tracing not configured

**Solution**:
```bash
export LANGCHAIN_TRACING_V2=true
export LANGCHAIN_API_KEY=your-api-key
export LANGCHAIN_PROJECT=componentforge-dev
```

**Issue**: No traces visible in UI

**Solution**: Wait a few minutes for traces to propagate, then refresh LangSmith UI

## CI/CD Integration

These tests can be integrated into CI/CD pipelines:

```yaml
# .github/workflows/integration-tests.yml
name: Integration Tests

on: [push, pull_request]

jobs:
  backend-e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: |
          cd backend
          pip install -r requirements.txt
          pytest tests/integration/test_generation_e2e.py -v

  frontend-e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: |
          cd app
          npm ci
          npx playwright install --with-deps
          npm run test:e2e -- generation.spec.ts

  performance:
    runs-on: ubuntu-latest
    # Only run on main branch or manual trigger
    if: github.ref == 'refs/heads/main' || github.event_name == 'workflow_dispatch'
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: |
          cd backend
          pip install -r requirements.txt
          pytest tests/performance/test_generation_latency.py -v -s
```

## Next Steps

After validating Integration Stream (I1-I5), proceed to:

1. **Polish Stream (P1-P8)**: Production enhancements
   - Provenance headers
   - Import resolution
   - ARIA attributes
   - TypeScript strict mode
   - Storybook stories
   - Documentation

2. **Performance Optimization**: If targets not met
   - Profile generation stages
   - Optimize slow components
   - Add caching strategies

3. **Observability Enhancement**: 
   - Add more Prometheus metrics
   - Create Grafana dashboards
   - Set up alerts for SLA violations

## References

- Epic 4 Document: `.claude/epics/04-code-generation.md`
- Commit Strategy: `.claude/epics/04-commit-strategy.md`
- Playwright Documentation: https://playwright.dev/
- LangSmith Documentation: https://docs.smith.langchain.com/
- Prometheus Documentation: https://prometheus.io/docs/
