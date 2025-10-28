# Golden Dataset for E2E Evaluation

This dataset provides ground truth examples for evaluating the complete screenshot-to-code pipeline in ComponentForge.

## Overview

The golden dataset consists of:
- **Screenshots**: Component images representing real UI elements
- **Ground Truth**: JSON files defining expected extraction and generation results

## Purpose

This dataset validates the end-to-end pipeline:
1. **Token Extraction** - GPT-4V extracts design tokens from screenshots
2. **Pattern Retrieval** - Hybrid search finds matching component patterns
3. **Code Generation** - LLM generates code from patterns and tokens
4. **Validation** - TypeScript compiler validates generated code

## Directory Structure

```
golden_dataset/
├── README.md                    # This file
├── screenshots/                 # Component screenshots
│   ├── README.md               # Screenshot guidelines
│   ├── button_primary.png
│   ├── button_secondary.png
│   ├── card_default.png
│   ├── badge_success.png
│   ├── input_text.png
│   └── ...                     # Additional screenshots (15 total)
└── ground_truth/               # Expected results
    ├── button_primary.json
    ├── button_secondary.json
    ├── card_default.json
    ├── badge_success.json
    ├── input_text.json
    └── ...                     # Additional ground truth (15 total)
```

## Ground Truth Format

Each ground truth JSON file contains:

```json
{
  "screenshot_id": "button_primary",
  "component_name": "Primary Button",
  "expected_tokens": {
    "colors": {
      "primary": "#3B82F6",
      "text": "#FFFFFF"
    },
    "spacing": {
      "padding": "12px 24px"
    },
    "typography": {
      "fontSize": "14px",
      "fontWeight": "500"
    }
  },
  "expected_pattern_id": "button",
  "expected_code_properties": {
    "has_variant_prop": true,
    "has_accessibility": true,
    "compiles": true
  },
  "notes": "Human-readable description"
}
```

### Field Descriptions

- **`screenshot_id`** (string): Unique identifier matching screenshot filename (without extension)
- **`component_name`** (string): Human-readable component name
- **`expected_tokens`** (object): Design tokens that should be extracted from the screenshot
  - **`colors`**: Color values in hex format
  - **`spacing`**: Padding, margin, gap values with units
  - **`typography`**: Font size, weight, family
  - **`border`**: Border radius, width, style
- **`expected_pattern_id`** (string): The component pattern ID that should be retrieved
- **`expected_code_properties`** (object): Properties the generated code should have
  - **`compiles`**: Must be `true` (code must be valid TypeScript)
  - **`has_variant_prop`**: Component should support variant prop
  - **`has_accessibility`**: Component should have ARIA attributes
  - Custom properties specific to component type
- **`notes`** (string): Additional context or requirements

## Current Dataset

### Commit 1: Initial 5 Samples
1. **button_primary** - Primary button (blue background)
2. **button_secondary** - Secondary button (gray background)
3. **card_default** - Default card with title and content
4. **badge_success** - Success badge (green background)
5. **input_text** - Text input field with placeholder

### Commit 2: Additional 10 Samples (Planned)
- button_outline
- card_with_image
- badge_warning
- badge_error
- input_with_icon
- checkbox
- alert_info
- alert_error
- select_dropdown
- Additional variants

## Usage

### Loading the Dataset

```python
from src.evaluation.golden_dataset import GoldenDataset

# Load dataset
dataset = GoldenDataset()

# Iterate over samples
for sample in dataset:
    screenshot = sample['image']  # PIL Image
    ground_truth = sample['ground_truth']  # Dict
    screenshot_id = sample['id']  # String
```

### Running Evaluation

```bash
# CLI script
cd backend
python scripts/run_e2e_evaluation.py

# Pytest suite
pytest tests/evaluation/test_e2e_pipeline.py -v

# API endpoint
curl http://localhost:8000/api/v1/evaluation/metrics
```

## Evaluation Metrics

The golden dataset enables calculation of:

### Token Extraction Metrics
- **Accuracy**: % of tokens correctly extracted
- **Missing Tokens**: Tokens present in ground truth but not extracted
- **Incorrect Tokens**: Tokens extracted with wrong values

### Retrieval Metrics
- **MRR** (Mean Reciprocal Rank): Context precision
- **Hit@3**: Context recall (correct pattern in top 3)
- **Precision@1**: Top-1 accuracy

### Generation Metrics
- **Compilation Rate**: % of code that compiles
- **Quality Score**: Average quality score from validator
- **Success Rate**: % of attempts that produced code

### End-to-End Metrics
- **Pipeline Success Rate**: % of screenshots that produced valid code
- **Average Latency**: Time from screenshot to valid code
- **Stage Failures**: Breakdown of failures by pipeline stage

## Target Metrics

- Pipeline Success Rate: **>80%**
- Token Extraction Accuracy: **>85%**
- Pattern Retrieval MRR: **>90%**
- Code Compilation Rate: **>90%**
- Average Latency: **<20 seconds**

## Maintenance

### Adding New Samples

1. Obtain component screenshot (from shadcn/ui or Figma)
2. Save to `screenshots/{component}_{variant}.png`
3. Create ground truth JSON in `ground_truth/{component}_{variant}.json`
4. Follow the format specification above
5. Update this README with the new sample

### Updating Ground Truth

- Update JSON files as component specifications evolve
- Re-run evaluation to validate changes
- Document breaking changes in git commit messages

## References

- Epic: `.claude/epics/epic-001-evaluation-framework.md`
- Evaluation Code: `backend/src/evaluation/`
- Tests: `backend/tests/evaluation/`
- CLI Script: `backend/scripts/run_e2e_evaluation.py`

## Version

- **v1.0** - Initial 5 samples (Commit 1)
- **v1.1** - Complete 15 samples (Commit 2, planned)
