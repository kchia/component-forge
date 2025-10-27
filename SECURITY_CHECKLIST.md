# Security Implementation Checklist

Quick reference for implementing security recommendations from the audit report.

## 🚨 CRITICAL - Before Production

- [ ] **Authentication & Authorization**
  - [ ] Implement JWT authentication middleware
  - [ ] Add API key authentication as fallback
  - [ ] Protect all `/api/v1/*` endpoints
  - [ ] Implement user session management
  - [ ] Add authorization checks for sensitive operations

- [ ] **Rate Limiting**
  - [ ] Install `slowapi` dependency
  - [ ] Configure rate limiter with Redis
  - [ ] Set endpoint-specific limits:
    - [ ] `/api/v1/tokens/extract` - 5/minute
    - [ ] `/api/v1/figma/*` - 10/minute
    - [ ] `/api/v1/retrieval/*` - 30/minute
  - [ ] Add rate limit logging and monitoring

- [ ] **XSS Protection**
  - [ ] Install `dompurify` in frontend
  - [ ] Sanitize `pattern.visualPreview` in `CodePreviewModal.tsx`
  - [ ] Add Content Security Policy headers
  - [ ] Review all `dangerouslySetInnerHTML` usage

## ⚠️ HIGH PRIORITY - Week 1-2

- [ ] **Security Headers**
  - [ ] Create `SecurityHeadersMiddleware`
  - [ ] Add HSTS header
  - [ ] Add X-Content-Type-Options
  - [ ] Add X-Frame-Options
  - [ ] Add Content-Security-Policy
  - [ ] Add Referrer-Policy

- [ ] **CORS Hardening**
  - [ ] Restrict `allow_methods` to `["GET", "POST", "OPTIONS"]`
  - [ ] Restrict `allow_headers` to specific headers
  - [ ] Restrict `expose_headers` to non-sensitive headers
  - [ ] Move allowed origins to environment variable

- [ ] **Dependency Management**
  - [ ] Pin all Python dependency versions in `requirements.txt`
  - [ ] Run `pip-audit` and fix vulnerabilities
  - [ ] Add `pip-audit` to CI/CD pipeline
  - [ ] Set up Dependabot/Renovate for auto-updates

- [ ] **File Upload Security**
  - [ ] Implement file size validation (10MB max)
  - [ ] Add magic byte validation with `python-magic`
  - [ ] Add file type whitelist check
  - [ ] Consider malware scanning for production

## 📋 MEDIUM PRIORITY - Week 3-4

- [ ] **Security Logging**
  - [ ] Log authentication failures
  - [ ] Log rate limit violations
  - [ ] Log file upload rejections
  - [ ] Log suspicious input patterns
  - [ ] Set up alerts for security events

- [ ] **Input Validation**
  - [ ] Add HTML sanitization with `bleach`
  - [ ] Validate JSON depth (max 10 levels)
  - [ ] Validate JSON size (max 50KB)
  - [ ] Add max length limits on text fields
  - [ ] Add request body size limits

- [ ] **Secrets Management**
  - [ ] Validate required secrets at startup
  - [ ] Check minimum secret lengths
  - [ ] Add pre-commit hooks (`detect-secrets`)
  - [ ] Plan for production secrets service (AWS Secrets Manager)

- [ ] **Production Configuration**
  - [ ] Ensure `DEBUG=false` in production env
  - [ ] Set `LOG_LEVEL=WARNING` or `ERROR` in production
  - [ ] Configure production CORS origins
  - [ ] Set up HTTPS in production

## 💡 NICE TO HAVE - Month 2+

- [ ] **Advanced Security**
  - [ ] Implement MFA (TOTP)
  - [ ] Add OAuth 2.0 for Figma
  - [ ] Add API key rotation
  - [ ] Implement audit logging

- [ ] **Testing & Monitoring**
  - [ ] Add security tests to test suite
  - [ ] Integrate OWASP ZAP in CI/CD
  - [ ] Set up security monitoring dashboard
  - [ ] Schedule regular penetration tests

- [ ] **Compliance**
  - [ ] Implement GDPR compliance (PII detection)
  - [ ] Add user data export/deletion
  - [ ] Document data retention policies
  - [ ] Review SOC 2 requirements

## Code Snippets

### 1. Rate Limiting Setup

```bash
# Install dependency
cd backend
source venv/bin/activate
pip install slowapi
echo "slowapi>=0.1.9" >> requirements.txt
```

```python
# backend/src/main.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379"
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
```

### 2. Security Headers Middleware

```python
# backend/src/api/middleware/security_headers.py
from starlette.middleware.base import BaseHTTPMiddleware

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Strict-Transport-Security"] = "max-age=31536000"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        return response
```

### 3. CORS Hardening

```python
# backend/src/main.py
import os

def get_allowed_origins():
    origins = os.getenv("CORS_ORIGINS", "http://localhost:3000")
    return [o.strip() for o in origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
    expose_headers=["X-Request-ID"],
)
```

### 4. XSS Protection (Frontend)

```bash
# Install DOMPurify
cd app
npm install dompurify
npm install --save-dev @types/dompurify
```

```tsx
// app/src/components/composite/CodePreviewModal.tsx
import DOMPurify from 'dompurify'

<div
  className="prose prose-sm max-w-none"
  dangerouslySetInnerHTML={{
    __html: DOMPurify.sanitize(pattern.visualPreview, {
      ALLOWED_TAGS: ['p', 'div', 'span', 'strong', 'em'],
      ALLOWED_ATTR: ['class']
    })
  }}
/>
```

### 5. Pin Python Dependencies

```bash
# Generate pinned requirements
cd backend
source venv/bin/activate
pip freeze > requirements.lock

# Or manually update requirements.txt
echo "fastapi==0.109.0" >> requirements.txt
echo "langchain==0.1.0" >> requirements.txt
# ... etc
```

### 6. File Upload Validation

```python
# backend/src/api/v1/routes/tokens.py
import magic

async def validate_file_upload(file: UploadFile):
    contents = await file.read()
    
    # Check file size
    if len(contents) > 10 * 1024 * 1024:  # 10MB
        raise HTTPException(400, "File too large (max 10MB)")
    
    # Verify magic bytes
    file_type = magic.from_buffer(contents, mime=True)
    if file_type not in ["image/png", "image/jpeg", "image/webp"]:
        raise HTTPException(400, f"Invalid file type: {file_type}")
    
    await file.seek(0)
    return file
```

## Testing Commands

```bash
# Run security audit on npm packages
cd app && npm audit

# Run security audit on Python packages (after pinning)
cd backend && source venv/bin/activate && pip-audit

# Check for secrets in code
git secrets --scan

# Test rate limiting
curl -X POST http://localhost:8000/api/v1/tokens/extract \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test.png" \
  # Repeat 6 times - should get 429 on 6th request

# Verify security headers
curl -I http://localhost:8000/api/v1/health
```

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Next.js Security](https://nextjs.org/docs/app/building-your-application/configuring/content-security-policy)
- [Epic 9: Security Implementation](.claude/epics/09-security-authentication.md)
- [Full Audit Report](./SECURITY_AUDIT_REPORT.md)

---

**Last Updated:** December 2024  
**Next Review:** After implementing critical items
