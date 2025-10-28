# Security Module

This module implements safety guardrails for ComponentForge as specified in Epic 003 - Story 3.1.

## Components

### Input Validator (`input_validator.py`)

Provides comprehensive validation for file uploads and text inputs:

**Features:**
- Image file validation (PNG, JPG, JPEG, SVG)
- File size limits (10MB max)
- Image dimension validation (min 50x50, max 25MP)
- SVG security checks (detects embedded scripts, event handlers)
- Text input sanitization using nh3
- Protection against decompression bombs

**Classes:**
- `ImageUploadValidator`: Main validator for image uploads
- `RequirementInputValidator`: Validates and sanitizes requirement text inputs
- `PatternNameValidator`: Validates pattern/component names
- `DescriptionValidator`: Validates and sanitizes descriptions

**Example Usage:**

```python
from src.security.input_validator import ImageUploadValidator, InputValidationError
from fastapi import UploadFile

# Validate image upload
try:
    metadata = await ImageUploadValidator.validate_upload(file)
    print(f"✓ Image validated: {metadata}")
except InputValidationError as e:
    print(f"✗ Validation failed: {e}")

# Validate text input
from src.security.input_validator import RequirementInputValidator

validator = RequirementInputValidator(text="Create a button component")
sanitized_text = validator.text  # HTML tags removed
```

### PII Detector (`pii_detector.py`)

Uses GPT-4V to detect personally identifiable information (PII) in uploaded images:

**Features:**
- OCR and PII detection in a single API call
- Detects: emails, phone numbers, SSNs, credit cards, addresses, etc.
- Contextual analysis (distinguishes real PII from UI placeholders)
- Auto-block capability for uploads containing PII
- Compliance logging for audit trails

**Configuration:**
- Set `PII_DETECTION_ENABLED=true` in `.env` to enable PII scanning
- Uses OpenAI API key from `OPENAI_API_KEY` environment variable

**Example Usage:**

```python
from src.security.pii_detector import PIIDetector, PIIDetectionError
from PIL import Image

detector = PIIDetector()

# Scan image (auto-block if PII found)
try:
    result = await detector.scan_image(image, auto_block=True)
    if result.has_pii:
        print(f"Warning: PII detected - {result.entities_found}")
except PIIDetectionError as e:
    print(f"Blocked: {e}")

# Scan without blocking (for logging/warnings)
result = await detector.scan_image(image, auto_block=False)
if result.has_pii:
    logger.warning(f"PII detected: {result.entities_found}")
```

## Integration with API Endpoints

The security module is integrated into the token extraction endpoint (`/api/v1/tokens/extract/screenshot`):

1. **Security Validation**: File type, size, and content validation
2. **Image Processing**: Standard image validation and processing
3. **PII Detection**: Optional scanning for sensitive data (controlled by env var)
4. **Token Extraction**: Proceed with GPT-4V token extraction

## Environment Variables

```bash
# Enable PII detection (optional, defaults to false)
PII_DETECTION_ENABLED=true

# Required for PII detection
OPENAI_API_KEY=your_api_key_here
```

## Testing

Run security tests:

```bash
cd backend
source venv/bin/activate
pytest tests/security/ -v
```

**Test Coverage:**
- File type validation (PNG, JPG, JPEG, SVG)
- File size limits
- SVG script detection
- Image dimension validation
- Text sanitization
- PII detection with mocked responses
- Error handling

## Security Considerations

### Input Validation
- **File Type Whitelist**: Only PNG, JPG, JPEG, SVG allowed
- **Size Limits**: 10MB max file size, 25MP max resolution
- **SVG Sanitization**: Blocks `<script>`, `javascript:`, event handlers
- **Text Sanitization**: Removes all HTML tags using nh3

### PII Detection
- **Privacy**: Images are sent to OpenAI API for analysis
- **Auto-Block**: Optionally block uploads containing PII
- **Logging**: All PII detections are logged for compliance
- **Context-Aware**: Distinguishes real PII from UI placeholders

### Best Practices
1. Always validate inputs before processing
2. Use auto-block for sensitive uploads (e.g., user-generated content)
3. Monitor PII detection logs for compliance
4. Keep nh3 library updated for security patches
5. Review security logs regularly

## Dependencies

Required packages (in `requirements.txt`):
```
nh3>=0.2.0           # Modern HTML sanitizer
python-magic>=0.4.27 # File type detection
slowapi>=0.1.9       # Rate limiting (for future use)
Pillow               # Image processing
fastapi              # Web framework
pydantic             # Data validation
openai               # GPT-4V API (for PII detection)
```

## Future Enhancements

Story 3.1 is complete. Future stories will add:

- **Story 3.2**: Code sanitization (detect XSS, eval(), etc. in generated code)
- **Story 3.3**: Rate limiting with Redis
- **Story 3.4**: Prompt injection protection
- **Story 3.5**: Security monitoring dashboard

## References

- Epic: `.claude/epics/epic-003-safety-guardrails.md`
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- nh3 docs: https://github.com/messense/nh3
