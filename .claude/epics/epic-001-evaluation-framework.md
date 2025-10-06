# Epic 001: RAGAS Evaluation Framework

**Priority:** P0 - CRITICAL GAP
**Estimated Effort:** 3-5 days
**Value:** Transforms B+ project to A+ with quantified proof of AI performance
**Bootcamp Requirement:** Week 4 - Evaluation

## Problem Statement

ComponentForge has sophisticated multi-agent architecture but lacks quantified evaluation metrics. Demo day judges and bootcamp reviewers need concrete numbers proving AI accuracy, not just "it works."

## Success Metrics

- Token extraction accuracy: Target >90%
- Component generation quality score: Target >85%
- Accessibility compliance: Target 100% WCAG AA
- End-to-end latency: Target <15 seconds
- Synthetic test dataset: 100+ UI screenshots with ground truth

## User Stories

### Story 1.1: RAGAS Integration
**As a developer**, I want to measure token extraction accuracy so I can prove ComponentForge outperforms manual design-to-code conversion.

**Acceptance Criteria:**
- [ ] Install and configure RAGAS framework in backend
- [ ] Define custom metrics for token extraction precision/recall
- [ ] Define metrics for component generation quality
- [ ] Define metrics for accessibility compliance
- [ ] Create evaluation pipeline in `/backend/src/evaluation/`

**Technical Implementation:**
```python
# backend/src/evaluation/metrics.py
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision

custom_metrics = [
    token_extraction_precision,  # % of correctly extracted design tokens
    token_extraction_recall,      # % of tokens found vs ground truth
    component_accuracy,           # Generated code matches expected output
    accessibility_score,          # WCAG compliance percentage
    generation_latency            # Time to generate component
]
```

**Files to Create:**
- `backend/src/evaluation/metrics.py`
- `backend/src/evaluation/evaluator.py`
- `backend/tests/evaluation/test_metrics.py`

---

### Story 1.2: Synthetic Test Dataset Generation
**As a QA engineer**, I want a comprehensive test dataset so I can continuously validate ComponentForge accuracy.

**Acceptance Criteria:**
- [ ] Generate 100+ UI screenshots across component types (buttons, cards, forms, etc.)
- [ ] Create ground truth annotations for each screenshot
- [ ] Include edge cases: dark mode, different brands, complex layouts
- [ ] Store dataset in `/backend/src/evaluation/datasets/`
- [ ] Document dataset format and usage

**Dataset Structure:**
```json
{
  "screenshot_id": "btn_001",
  "component_type": "button",
  "ground_truth_tokens": {
    "colors": {"primary": "#3B82F6"},
    "spacing": {"padding": "12px 24px"},
    "typography": {"fontSize": "14px", "fontWeight": "500"}
  },
  "expected_component": "button_primary_blue.tsx",
  "accessibility_requirements": ["WCAG_AA", "keyboard_nav", "screen_reader"]
}
```

**Files to Create:**
- `backend/src/evaluation/datasets/synthetic_components.json`
- `backend/src/evaluation/dataset_generator.py`
- `backend/tests/evaluation/test_dataset.py`

---

### Story 1.3: Evaluation Dashboard
**As a product manager**, I want a dashboard showing ComponentForge performance metrics so I can communicate value to stakeholders.

**Acceptance Criteria:**
- [ ] Create `/api/v1/evaluation/metrics` endpoint
- [ ] Build evaluation results page at `/app/evaluation`
- [ ] Display key metrics: accuracy, latency, cost savings
- [ ] Show time-series graphs of performance over time
- [ ] Export metrics as JSON/CSV for demo day

**Dashboard Metrics:**
```typescript
interface EvaluationMetrics {
  tokenExtraction: {
    precision: number;      // 0.94
    recall: number;         // 0.92
    f1Score: number;        // 0.93
  };
  componentGeneration: {
    accuracy: number;       // 0.88
    avgLatency: number;     // 12.3 seconds
    successRate: number;    // 0.96
  };
  accessibility: {
    wcagCompliance: number; // 1.0 (100%)
    contrastRatio: number;  // 4.5:1
  };
  businessImpact: {
    timeSavedPerComponent: number;  // 120 minutes
    costReduction: number;          // $500
    componentsGenerated: number;    // 247
  };
}
```

**Files to Create:**
- `backend/src/api/v1/routes/evaluation.py`
- `app/src/app/evaluation/page.tsx`
- `app/src/components/evaluation/MetricsChart.tsx`
- `app/src/components/evaluation/EvaluationSummary.tsx`

---

### Story 1.4: Automated Evaluation Pipeline
**As a DevOps engineer**, I want automated evaluation on every deployment so we catch regressions before production.

**Acceptance Criteria:**
- [ ] Create evaluation script: `backend/scripts/run_evaluation.py`
- [ ] Integrate with CI/CD pipeline (GitHub Actions)
- [ ] Fail build if accuracy drops below threshold (90%)
- [ ] Generate evaluation report artifact
- [ ] Alert team on Slack if metrics degrade

**CI/CD Integration:**
```yaml
# .github/workflows/evaluation.yml
name: RAGAS Evaluation
on: [push, pull_request]
jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - name: Run RAGAS Evaluation
        run: python backend/scripts/run_evaluation.py
      - name: Check Thresholds
        run: |
          if [ "$TOKEN_ACCURACY" -lt "90" ]; then
            echo "Token extraction accuracy below threshold!"
            exit 1
          fi
```

**Files to Create:**
- `backend/scripts/run_evaluation.py`
- `.github/workflows/evaluation.yml`
- `backend/src/evaluation/ci_reporter.py`

---

## Technical Dependencies

- **Backend:** `ragas`, `langsmith`, `pytest-benchmark`
- **Frontend:** `recharts` for metrics visualization
- **Infrastructure:** GitHub Actions for CI/CD

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| RAGAS metrics don't align with component generation | High | Define custom metrics specific to design-to-code |
| Synthetic dataset not representative | Medium | Include real user screenshots from pilot |
| Evaluation too slow for CI/CD | Medium | Use subset of dataset for quick checks, full eval nightly |

## Demo Day Presentation

**Before Slide:**
"We built a multi-agent system to convert designs to accessible components."

**After Slide:**
"ComponentForge achieves 94% token extraction accuracy, generates production-ready components in 12 seconds, and saves developers 2 hours per component. Here's the data." ✅

## Success Criteria

- [ ] RAGAS framework integrated and running
- [ ] 100+ test cases with ground truth
- [ ] Evaluation dashboard accessible at `/evaluation`
- [ ] CI/CD pipeline fails on accuracy regression
- [ ] Quantified metrics ready for demo day deck
- [ ] Documentation: How to interpret and improve metrics

## References

- Bootcamp Week 4: Evaluation lecture notes
- Veritin AI demo (12% improvement in faithfulness)
- OnCall Lens demo (437% improvement in accuracy)
- RAGAS documentation: https://docs.ragas.io/
