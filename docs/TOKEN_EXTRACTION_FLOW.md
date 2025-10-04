# Token Extraction Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                    SCREENSHOT UPLOAD & TOKEN EXTRACTION              │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────┐
│   Client     │
│  (Browser)   │
└──────┬───────┘
       │
       │ POST /api/v1/tokens/extract/screenshot
       │ Content-Type: multipart/form-data
       │ Body: file (PNG/JPG)
       │
       ↓
┌────────────────────────────────────────┐
│   FastAPI Endpoint                     │
│   tokens.py::extract_tokens_from_screenshot()
└──────┬─────────────────────────────────┘
       │
       │ 1. Read file
       ↓
┌────────────────────────────────────────┐
│   Image Processor                      │
│   image_processor.py                   │
│                                        │
│   ✓ Validate file size (<10MB)        │
│   ✓ Validate MIME type (PNG/JPG)      │
│   ✓ Open & validate image             │
│   ✓ Check dimensions (min 50x50)      │
│   ✓ Resize if needed (max 2000px)     │
│   ✓ Convert to RGB                    │
│   ✓ Convert to base64 data URL        │
└──────┬─────────────────────────────────┘
       │
       │ 2. Processed image
       ↓
┌────────────────────────────────────────┐
│   Token Extractor Agent                │
│   token_extractor.py                   │
│                                        │
│   ┌──────────────────────────────┐   │
│   │  Prompt Template             │   │
│   │  token_extraction.py         │   │
│   │  - Structured instructions   │   │
│   │  - JSON schema               │   │
│   │  - Confidence guidelines     │   │
│   └──────────┬───────────────────┘   │
│              │                         │
│              ↓                         │
│   ┌──────────────────────────────┐   │
│   │  OpenAI GPT-4V API           │   │
│   │  model: gpt-4o               │   │
│   │  - Image + Prompt            │   │
│   │  - Temperature: 0.1          │   │
│   │  - Max tokens: 2000          │   │
│   └──────────┬───────────────────┘   │
│              │                         │
│              │ Retry up to 3 times     │
│              │ on error                │
└──────────────┼─────────────────────────┘
               │
               │ 3. Raw JSON response
               ↓
┌────────────────────────────────────────┐
│   Response Parser                      │
│   - Strip markdown blocks              │
│   - Parse JSON                         │
│   - Validate structure                 │
│   - Verify required fields             │
└──────┬─────────────────────────────────┘
       │
       │ 4. Parsed tokens with confidence
       ↓
┌────────────────────────────────────────┐
│   Confidence Processor                 │
│   confidence.py                        │
│                                        │
│   For each token:                      │
│   ┌─────────────────────────────┐    │
│   │ confidence ≥ 0.9?            │    │
│   │   → Auto-accept              │    │
│   └────┬────────────────────┬────┘    │
│        │ No                 │ Yes      │
│        ↓                    ↓          │
│   ┌─────────────────────────────┐    │
│   │ confidence ≥ 0.7?            │    │
│   │   → Flag for review          │    │
│   └────┬────────────────────┬────┘    │
│        │ No                 │ Yes      │
│        ↓                    ↓          │
│   ┌─────────────────────────────┐    │
│   │ Use fallback from           │    │
│   │ defaults.py (shadcn/ui)     │    │
│   └─────────────────────────────┘    │
└──────┬─────────────────────────────────┘
       │
       │ 5. Processed tokens
       ↓
┌────────────────────────────────────────┐
│   Response Builder                     │
│   - tokens: Final values               │
│   - confidence: Original scores        │
│   - fallbacks_used: List of tokens     │
│   - review_needed: List of tokens      │
│   - metadata: Image & extraction info  │
└──────┬─────────────────────────────────┘
       │
       │ JSON response
       ↓
┌──────────────┐
│   Client     │
│  (Browser)   │
└──────────────┘


═══════════════════════════════════════════════════════════════════════
EXAMPLE RESPONSE
═══════════════════════════════════════════════════════════════════════

{
  "tokens": {
    "colors": {
      "primary": "#3B82F6",      ← Used (confidence 0.95)
      "background": "#FFFFFF",   ← Used (confidence 0.92)
      "foreground": "#09090B"    ← Used (confidence 0.88)
    },
    "typography": {
      "fontFamily": "Inter",     ← Fallback (confidence 0.65 < 0.7)
      "fontSize": "16px",        ← Used (confidence 0.85)
      "fontWeight": 500          ← Flagged (confidence 0.78, needs review)
    },
    "spacing": {
      "padding": "16px",         ← Used (confidence 0.82)
      "gap": "8px"               ← Flagged (confidence 0.79, needs review)
    }
  },
  "confidence": {
    "colors": {"primary": 0.95, "background": 0.92, "foreground": 0.88},
    "typography": {"fontFamily": 0.65, "fontSize": 0.85, "fontWeight": 0.78},
    "spacing": {"padding": 0.82, "gap": 0.79}
  },
  "fallbacks_used": ["typography.fontFamily"],
  "review_needed": ["typography.fontWeight", "spacing.gap"],
  "metadata": {
    "filename": "design-system.png",
    "image": {"width": 1200, "height": 800, "format": "PNG"},
    "extraction_method": "gpt-4v"
  }
}

═══════════════════════════════════════════════════════════════════════
ERROR HANDLING
═══════════════════════════════════════════════════════════════════════

Oversized File (>10MB)
  → 400 Bad Request
  → "File too large (11.5MB). Maximum size is 10MB."

Invalid Format
  → 400 Bad Request
  → "Invalid file type: image/gif. Allowed types: PNG, JPG, JPEG."

Corrupted Image
  → 400 Bad Request
  → "Corrupted or invalid image file: cannot identify image file"

GPT-4V Error
  → Retry up to 3 times with exponential backoff
  → If all retries fail:
    → 500 Internal Server Error
    → "Failed to extract tokens after 3 attempts: <error>"

═══════════════════════════════════════════════════════════════════════
CONFIDENCE THRESHOLDS
═══════════════════════════════════════════════════════════════════════

 1.0 ─┬─────────────────────────────  Perfect
      │  AUTO-ACCEPT
      │  (No review needed)
 0.9 ─┼─────────────────────────────  High confidence
      │
      │  FLAG FOR REVIEW
      │  (Manual verification recommended)
 0.7 ─┼─────────────────────────────  Moderate confidence
      │
      │  USE FALLBACK
      │  (Replace with shadcn/ui defaults)
 0.0 ─┴─────────────────────────────  Low confidence


═══════════════════════════════════════════════════════════════════════
TESTING
═══════════════════════════════════════════════════════════════════════

Unit Tests (51 total)
  ├── API Endpoints (7 tests)
  │   ✓ Successful extraction
  │   ✓ Oversized file rejection
  │   ✓ Invalid format rejection
  │   ✓ Corrupted image rejection
  │   ✓ Extraction error handling
  │   ✓ Missing file validation
  │   └── Default tokens endpoint
  │
  ├── Confidence Scoring (17 tests)
  │   ✓ Logprob calculation
  │   ✓ Fallback decision logic
  │   ✓ Review flagging
  │   ✓ Fallback application
  │   └── Token processing
  │
  └── Image Processing (15 tests)
      ✓ File size validation
      ✓ MIME type validation
      ✓ Image resizing
      ✓ Format conversion
      └── Base64 encoding

Integration Tests
  ├── API test script (test_token_api.sh)
  │   ✓ Server health check
  │   ✓ Defaults endpoint
  │   ✓ Screenshot upload
  │   ✓ Validation tests
  │   └── Error handling
  │
  └── End-to-end extraction (integration_test_extraction.py)
      ✓ Create test image
      ✓ Extract with GPT-4V
      └── Verify response structure
```
