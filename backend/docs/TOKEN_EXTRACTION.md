# Design Token Extraction API

## Overview

This module provides screenshot upload and GPT-4V-based design token extraction capabilities for ComponentForge. It extracts colors, typography, and spacing tokens from uploaded screenshots with confidence scoring and automatic fallback to shadcn/ui defaults.

## Features

- ✅ Screenshot upload (PNG, JPG, JPEG up to 10MB)
- ✅ Image validation and preprocessing (resize, format conversion)
- ✅ GPT-4V vision-based token extraction
- ✅ Per-token confidence scoring (0-1 scale)
- ✅ Automatic fallback to shadcn/ui defaults (confidence < 0.7)
- ✅ Error handling with retries (3 attempts)
- ✅ Comprehensive test coverage (39 tests)

## API Endpoints

### POST /api/v1/tokens/extract/screenshot

Extract design tokens from an uploaded screenshot.

**Request:**
```bash
curl -X POST http://localhost:8000/api/v1/tokens/extract/screenshot \
  -F "file=@screenshot.png"
```

**Response:**
```json
{
  "tokens": {
    "colors": {
      "primary": "#3B82F6",
      "background": "#FFFFFF",
      "foreground": "#09090B"
    },
    "typography": {
      "fontFamily": "Inter",
      "fontSize": "16px",
      "fontWeight": 500
    },
    "spacing": {
      "padding": "16px",
      "gap": "8px"
    }
  },
  "confidence": {
    "colors": {
      "primary": 0.95,
      "background": 0.92,
      "foreground": 0.88
    },
    "typography": {
      "fontFamily": 0.65,
      "fontSize": 0.85,
      "fontWeight": 0.78
    },
    "spacing": {
      "padding": 0.82,
      "gap": 0.79
    }
  },
  "fallbacks_used": ["typography.fontFamily"],
  "review_needed": ["spacing.gap"],
  "metadata": {
    "filename": "screenshot.png",
    "image": {
      "width": 1200,
      "height": 800,
      "format": "PNG"
    },
    "extraction_method": "gpt-4v"
  }
}
```

**Validation Rules:**
- File size: Maximum 10MB
- Formats: PNG, JPG, JPEG only
- Dimensions: Minimum 50x50 pixels, maximum 2000px width (auto-resized)

**Error Responses:**

400 Bad Request - Invalid file:
```json
{
  "detail": "File too large (11.5MB). Maximum size is 10MB."
}
```

500 Internal Server Error - Extraction failed:
```json
{
  "detail": "Failed to extract tokens: Extraction failed after 3 attempts"
}
```

### GET /api/v1/tokens/defaults

Get shadcn/ui default design tokens.

**Request:**
```bash
curl http://localhost:8000/api/v1/tokens/defaults
```

**Response:**
```json
{
  "tokens": {
    "colors": {
      "primary": "#3B82F6",
      "background": "#FFFFFF",
      "foreground": "#09090B"
    },
    "typography": {
      "fontFamily": "Inter",
      "fontSize": "16px",
      "fontWeight": 500
    },
    "spacing": {
      "padding": "16px",
      "gap": "8px"
    }
  },
  "source": "shadcn/ui",
  "description": "Default design tokens used as fallbacks"
}
```

## Confidence Scoring

### Thresholds

- **0.9 - 1.0**: Auto-accepted (high confidence)
- **0.7 - 0.9**: Flagged for review (moderate confidence)
- **0.0 - 0.7**: Fallback applied (low confidence)

### Calculation

Confidence scores are derived from GPT-4V's log probabilities:

```python
confidence = exp(average_logprob)
```

Higher log probabilities indicate the model is more certain about its extraction.

### Fallback Behavior

When confidence < 0.7, the system automatically uses shadcn/ui defaults:

| Token | Fallback Value |
|-------|---------------|
| colors.primary | #3B82F6 |
| colors.background | #FFFFFF |
| colors.foreground | #09090B |
| typography.fontFamily | Inter |
| typography.fontSize | 16px |
| typography.fontWeight | 500 |
| spacing.padding | 16px |
| spacing.gap | 8px |

## Module Structure

```
backend/src/
├── api/v1/routes/
│   └── tokens.py              # API endpoints
├── agents/
│   └── token_extractor.py     # GPT-4V integration
├── prompts/
│   └── token_extraction.py    # Prompt template
├── services/
│   └── image_processor.py     # Image validation & processing
└── core/
    ├── confidence.py          # Confidence scoring
    └── defaults.py            # Shadcn/ui defaults
```

## Usage Example

### Python Client

```python
import httpx
from pathlib import Path

async def extract_tokens(image_path: str):
    async with httpx.AsyncClient() as client:
        with open(image_path, 'rb') as f:
            files = {'file': ('screenshot.png', f, 'image/png')}
            response = await client.post(
                'http://localhost:8000/api/v1/tokens/extract/screenshot',
                files=files
            )
        return response.json()

# Usage
result = await extract_tokens('design_system.png')
print(f"Primary color: {result['tokens']['colors']['primary']}")
print(f"Confidence: {result['confidence']['colors']['primary']}")
```

### JavaScript/TypeScript Client

```typescript
async function extractTokens(file: File) {
  const formData = new FormData();
  formData.append('file', file);
  
  const response = await fetch('http://localhost:8000/api/v1/tokens/extract/screenshot', {
    method: 'POST',
    body: formData,
  });
  
  return await response.json();
}

// Usage
const fileInput = document.querySelector('input[type="file"]');
const result = await extractTokens(fileInput.files[0]);
console.log('Extracted tokens:', result.tokens);
```

## Testing

Run the test suite:

```bash
cd backend
source venv/bin/activate
pytest tests/test_confidence.py -v       # Confidence scoring tests
pytest tests/test_image_processor.py -v  # Image processing tests
pytest tests/test_api_tokens.py -v       # API endpoint tests
pytest tests/ -v                         # All tests
```

### Integration Test

Run with a real OpenAI API key:

```bash
export OPENAI_API_KEY=your-api-key
python tests/integration_test_extraction.py
```

## Configuration

Required environment variables:

```bash
OPENAI_API_KEY=sk-...  # OpenAI API key for GPT-4V
```

Optional configuration (defaults shown):

```python
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_IMAGE_WIDTH = 2000             # pixels
CONFIDENCE_THRESHOLD_FALLBACK = 0.7
CONFIDENCE_THRESHOLD_AUTO_ACCEPT = 0.9
```

## Error Handling

The system handles various error scenarios:

1. **Oversized files** (>10MB) - Rejected with clear message
2. **Invalid formats** (not PNG/JPG) - Rejected with format list
3. **Corrupted images** - Detected and rejected
4. **GPT-4V errors** - Retries up to 3 times with exponential backoff
5. **Invalid JSON response** - Logged and retried
6. **Missing tokens** - Fallback to defaults

## Performance

- **Image preprocessing**: <100ms for typical images
- **GPT-4V extraction**: 3-8 seconds (depends on image complexity)
- **Total latency**: <10 seconds (target met)

## Limitations

1. **Font family detection**: Lower confidence (0.5-0.7) due to visual inference
2. **Complex designs**: May require manual review for accuracy
3. **Rate limits**: OpenAI API limits apply (10,000 RPM for Tier 2)
4. **Cost**: ~$0.01-0.03 per extraction (GPT-4V pricing)

## Future Enhancements

- [ ] Batch processing for multiple screenshots
- [ ] Support for Figma file extraction
- [ ] Custom confidence thresholds per user
- [ ] Token history and versioning
- [ ] Manual override UI
- [ ] Export to JSON/CSS formats

## References

- [Epic 1: Design Token Extraction](../../.claude/epics/01-design-token-extraction.md)
- [OpenAI Vision API](https://platform.openai.com/docs/guides/vision)
- [shadcn/ui Design Tokens](https://ui.shadcn.com/docs)
