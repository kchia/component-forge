# Token Extraction API Cost Estimation

## Overview

This document provides accurate cost estimates for the token extraction feature using OpenAI's GPT-4o vision API.

## API Configuration

From `token_extractor.py`:

- **Model**: `gpt-4o` (GPT-4 Omni with vision)
- **Image Detail**: `high` (most expensive option)
- **Max Output Tokens**: 2000
- **Temperature**: 0.1
- **Retry Logic**: Up to 3 retries (max 4 attempts total)

## Image Processing Constraints

From `image_processor.py`:

- **Max Width**: 2000px (images resized if larger)
- **Max Pixels**: 25,000,000 pixels (~5000x5000)
- **Format**: PNG (base64 encoded)
- **Typical Screenshot Size**: 1920x1080 (2,073,600 pixels) or smaller

## Cost Components

### 1. Text Input Tokens

**Prompt Size**: ~2,000 characters (~500 tokens)

- The extraction prompt is approximately 2,000 characters
- Estimated at ~500 tokens (using 4 chars/token ratio)

### 2. Image Input Tokens

For GPT-4o with `detail: "high"`:

- Images are processed at higher resolution
- Token cost depends on image dimensions
- Formula: `(width * height) / 512^2 * 170` tokens (approximate)

**Common Scenarios**:

| Image Size            | Pixels    | Estimated Image Tokens | Cost (Input) |
| --------------------- | --------- | ---------------------- | ------------ |
| 1920x1080 (Full HD)   | 2,073,600 | ~1,400 tokens          | $0.0035      |
| 1440x900 (Common)     | 1,296,000 | ~875 tokens            | $0.0022      |
| 2000x1200 (Max width) | 2,400,000 | ~1,625 tokens          | $0.0041      |
| 1280x720 (HD)         | 921,600   | ~625 tokens            | $0.0016      |

### 3. Output Tokens

**Expected Output**: ~800-1,200 tokens

- JSON response with design tokens
- Includes colors, typography, spacing, borderRadius
- Each token has value + confidence score
- Actual output typically 800-1,200 tokens (well below 2000 max)

## Pricing (GPT-4o as of 2024)

**Note**: Prices may vary. Check [OpenAI Pricing](https://openai.com/api/pricing/) for current rates.

- **Input**: $2.50 per 1M tokens
- **Output**: $10.00 per 1M tokens

### Image Processing with High Detail

For `detail: "high"`:

- Base cost: ~$0.01 per image (for images up to 2048x2048)
- Additional cost for larger images: ~$0.00001 per 512x512 tile

## Cost Calculation Examples

### Example 1: Standard Screenshot (1920x1080)

**Per Request**:

- Text input: 500 tokens × $2.50/1M = $0.00125
- Image input: ~1,400 tokens × $2.50/1M = $0.0035
- Output: ~1,000 tokens × $10.00/1M = $0.01
- **Total per request**: ~$0.01475

**With Retry Logic** (worst case: 4 attempts):

- **Worst case total**: ~$0.059

### Example 2: Smaller Screenshot (1280x720)

**Per Request**:

- Text input: 500 tokens × $2.50/1M = $0.00125
- Image input: ~625 tokens × $2.50/1M = $0.00156
- Output: ~1,000 tokens × $10.00/1M = $0.01
- **Total per request**: ~$0.0128

### Example 3: Maximum Size (2000x1200)

**Per Request**:

- Text input: 500 tokens × $2.50/1M = $0.00125
- Image input: ~1,625 tokens × $2.50/1M = $0.00406
- Output: ~1,000 tokens × $10.00/1M = $0.01
- **Total per request**: ~$0.0153

## Monthly Cost Projections

### Low Usage (100 extractions/month)

- Average cost per extraction: $0.014
- **Monthly cost**: ~$1.40
- **Annual cost**: ~$16.80

### Medium Usage (1,000 extractions/month)

- Average cost per extraction: $0.014
- **Monthly cost**: ~$14.00
- **Annual cost**: ~$168.00

### High Usage (10,000 extractions/month)

- Average cost per extraction: $0.014
- **Monthly cost**: ~$140.00
- **Annual cost**: ~$1,680.00

### Enterprise Usage (100,000 extractions/month)

- Average cost per extraction: $0.014
- **Monthly cost**: ~$1,400.00
- **Annual cost**: ~$16,800.00

## Cost Optimization Strategies

### 1. Reduce Image Size

- **Current**: Max 2000px width
- **Optimization**: Consider reducing to 1600px or 1280px
- **Savings**: ~20-30% on image token costs

### 2. Use Lower Detail Level

- **Current**: `detail: "high"`
- **Optimization**: Test `detail: "low"` (if quality acceptable)
- **Savings**: ~50-70% on image processing costs
- **Trade-off**: May reduce extraction accuracy

### 3. Reduce Max Output Tokens

- **Current**: 2000 tokens
- **Optimization**: Reduce to 1500 tokens (if sufficient)
- **Savings**: Minimal (output is typically <1200 tokens)

### 4. Implement Caching

- Cache results for identical images
- Use image hash to detect duplicates
- **Savings**: 100% for duplicate requests

### 5. Batch Processing

- Process multiple images in single request (if API supports)
- **Savings**: Reduced overhead per request

## Cost Breakdown by Component

For a typical extraction (1920x1080 image):

| Component   | Tokens    | Cost         | Percentage |
| ----------- | --------- | ------------ | ---------- |
| Text Input  | 500       | $0.00125     | 8.5%       |
| Image Input | 1,400     | $0.0035      | 23.7%      |
| Output      | 1,000     | $0.01        | 67.8%      |
| **Total**   | **2,900** | **$0.01475** | **100%**   |

## Monitoring Recommendations

1. **Track Usage Metrics**:

   - Number of extractions per day/month
   - Average image size processed
   - Retry rate (indicates failures)
   - Average tokens per request

2. **Set Alerts**:

   - Daily cost threshold
   - Monthly budget limit
   - Unusual spike detection

3. **Log Cost Data**:
   - Log token usage per request
   - Track costs by image size
   - Monitor retry costs

## Implementation Notes

The current implementation includes:

- Automatic retry logic (up to 3 retries)
- Image size optimization (max 2000px width)
- Efficient base64 encoding
- Error handling to prevent unnecessary retries

## Future Considerations

1. **Model Updates**: GPT-4o pricing may change
2. **Volume Discounts**: OpenAI may offer discounts for high-volume usage
3. **Alternative Models**: Consider GPT-4o-mini for cost-sensitive use cases
4. **Local Processing**: For very high volume, consider local vision models

## References

- [OpenAI API Pricing](https://openai.com/api/pricing/)
- [GPT-4o Documentation](https://platform.openai.com/docs/guides/vision)
- Token extraction implementation: `backend/src/agents/token_extractor.py`
- Image processing: `backend/src/services/image_processor.py`
