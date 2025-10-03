# Epic Technical Review - Action Items

**Date**: 2025-01-23
**Status**: Ready for Review
**Priority**: High

---

## 🚨 Critical Actions (Must Complete Before Implementation)

### 1. Add Missing Backend Dependencies

Update `backend/requirements.txt` with:

```python
# Pattern Retrieval (Epic 3)
rank-bm25>=0.2.2

# Quality Validation (Epic 5)
colour>=0.1.5  # For color contrast calculations

# Production Infrastructure (Epic 6)
boto3>=1.28.0  # For S3 storage
redis[asyncio]>=5.0.0  # For async Redis operations

# Regeneration & Versioning (Epic 8)
celery[redis]>=5.3.0  # For async task processing
# Alternative: arq>=0.25.0  # Simpler Redis-based queue

# Security & Authentication (Epic 9)
hvac>=1.2.0  # HashiCorp Vault client
authlib>=1.2.0  # OAuth implementation
python-jose[cryptography]>=3.3.0  # JWT handling
pyotp>=2.9.0  # TOTP/MFA support
bcrypt>=4.1.0  # Password hashing
bleach>=6.1.0  # HTML sanitization
python3-saml>=1.15.0  # SAML SSO

# Team & Enterprise (Epic 10)
stripe>=7.0.0  # Payment processing
```

**Estimated Time**: 30 minutes  
**Assignee**: Backend team lead  
**Deadline**: Before Epic 3 implementation starts

---

### 2. Add Missing Frontend Dependencies

Update `app/package.json` with:

```json
{
  "dependencies": {
    "next-auth": "^5.0.0-beta",
    "zod": "^3.22.0",
    "react-hook-form": "^7.49.0"
  }
}
```

**Estimated Time**: 15 minutes  
**Assignee**: Frontend team lead  
**Deadline**: Before Epic 2 implementation starts

---

### 3. Architectural Decision: Python/Node.js Boundary

**Issue**: Epics 4 (Code Generation) and 5 (Quality Validation) require TypeScript AST parsing and formatting, which currently use subprocess calls from Python to Node.js tools.

**Impact**:
- Performance overhead from subprocess communication
- Deployment complexity (requires both Python and Node.js runtimes)
- Error handling complexity

**Options**:

**Option A**: TypeScript Microservice (Recommended)
- Create dedicated TypeScript service for AST operations
- Communicate via gRPC or REST
- **Pros**: Clean separation, better performance, easier testing
- **Cons**: Additional service to maintain
- **Estimated Effort**: 2-3 days

**Option B**: Accept Subprocess Overhead
- Continue with subprocess approach
- Optimize with connection pooling and caching
- **Pros**: Simpler initially, uses existing tools
- **Cons**: Performance impact, deployment complexity
- **Estimated Effort**: 1 day to optimize

**Option C**: Python-Only AST
- Use tree-sitter or similar Python library
- Generate Python code instead of TypeScript
- **Pros**: Single language stack
- **Cons**: Doesn't match React/TypeScript ecosystem
- **Estimated Effort**: 3-4 days

**Decision Required**: Architecture review meeting  
**Participants**: Tech lead, backend team, DevOps  
**Deadline**: End of this week  
**Recommendation**: Option A (TypeScript Microservice)

---

### 4. Add HashiCorp Vault to Docker Compose

Update `docker-compose.yml`:

```yaml
services:
  vault:
    image: hashicorp/vault:1.15
    container_name: componentforge-vault
    ports:
      - "8200:8200"
    environment:
      VAULT_DEV_ROOT_TOKEN_ID: "dev-token"
      VAULT_DEV_LISTEN_ADDRESS: "0.0.0.0:8200"
    cap_add:
      - IPC_LOCK
    volumes:
      - vault_data:/vault/data
    networks:
      - componentforge-network
    healthcheck:
      test: ["CMD", "vault", "status"]
      interval: 10s
      timeout: 5s
      retries: 3

volumes:
  vault_data:
    driver: local
```

**Estimated Time**: 1 hour (including testing)  
**Assignee**: DevOps engineer  
**Deadline**: Before Epic 9 implementation starts

---

## ⚠️ High Priority Actions (Should Complete Soon)

### 5. Pin Python Dependency Versions

Current `requirements.txt` doesn't pin specific versions for some packages.

**Action**: Update to:
```python
# Instead of:
pillow

# Use:
pillow>=10.0.0,<11.0.0
```

**Packages to pin**:
- Pillow
- OpenAI
- LangChain packages
- Security-critical packages (hvac, authlib, python-jose, bcrypt)

**Tool**: Consider using `pip-tools` or `poetry` for dependency locking

**Estimated Time**: 2 hours  
**Assignee**: Backend team lead  
**Deadline**: Within 1 week

---

### 6. Add CORS Configuration

Epic 0 should include explicit CORS setup for FastAPI.

**File**: `backend/src/main.py`

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Development
        "https://yourdomain.com",  # Production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Estimated Time**: 30 minutes  
**Assignee**: Backend engineer  
**Deadline**: During Epic 0 implementation

---

### 7. Add CSP Headers Configuration

**File**: `app/next.config.ts`

```typescript
const nextConfig = {
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'Content-Security-Policy',
            value: "default-src 'self'; script-src 'self' 'unsafe-eval' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
          },
          {
            key: 'X-Frame-Options',
            value: 'DENY'
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff'
          }
        ]
      }
    ];
  }
};
```

**Estimated Time**: 1 hour  
**Assignee**: Frontend engineer  
**Deadline**: During Epic 0 implementation

---

### 8. Performance Profiling Plan

**Goal**: Validate latency targets before full implementation

**Actions**:
1. Create performance test suite for each epic
2. Profile AST operations (Epic 4)
3. Profile LLM calls (Epics 2, 4)
4. Test caching effectiveness (Epic 6)

**Tools**:
- `cProfile` for Python profiling
- LangSmith for LLM observability
- Locust or k6 for load testing

**Estimated Time**: 1 day per epic  
**Assignee**: Performance engineer  
**Deadline**: During each epic implementation

---

## 📋 Medium Priority Actions (Nice to Have)

### 9. Add CI/CD Pipeline

**Missing**: Automated testing and deployment workflows

**File**: `.github/workflows/ci.yml`

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          pytest tests/ -v
      - name: Lint
        run: |
          cd backend
          black --check .
          isort --check .

  test-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '18'
      - name: Install dependencies
        run: |
          cd app
          npm ci
      - name: Lint
        run: |
          cd app
          npm run lint
      - name: Type check
        run: |
          cd app
          npx tsc --noEmit
      - name: Test
        run: |
          cd app
          npm test
```

**Estimated Time**: 1 day  
**Assignee**: DevOps engineer  
**Deadline**: After Epic 0 completion

---

### 10. Consider Celery Alternative

**Issue**: Celery adds complexity for async job processing

**Alternative**: `arq` (Redis-based, simpler)

**Comparison**:

| Feature | Celery | arq |
|---------|--------|-----|
| Complexity | High | Low |
| Dependencies | Many | Few (just Redis) |
| Learning Curve | Steep | Gentle |
| Performance | Good | Excellent |
| Monitoring | Flower | Built-in |

**Recommendation**: Evaluate `arq` for simpler use cases

**Estimated Time**: 4 hours (evaluation + POC)  
**Assignee**: Backend architect  
**Deadline**: Before Epic 8 implementation

---

### 11. Add Load Testing

**Tool**: Locust or k6

**Example**: `backend/tests/load/test_generation.py`

```python
from locust import HttpUser, task, between

class ComponentForgeUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def generate_component(self):
        self.client.post("/api/v1/generate", json={
            "figma_url": "https://figma.com/file/test",
            "component_type": "Button"
        })

    @task(1)
    def validate_component(self):
        self.client.post("/api/v1/validate", json={
            "code": "/* test code */"
        })
```

**Estimated Time**: 2 days  
**Assignee**: QA engineer  
**Deadline**: After Epic 4 implementation

---

### 12. Add Visual Regression Testing

**Tool**: Percy or Chromatic

**Benefits**:
- Catch UI regressions automatically
- Review visual changes in PRs
- Component library validation

**Setup**: `app/playwright.config.ts`

```typescript
import { defineConfig } from '@playwright/test';

export default defineConfig({
  use: {
    screenshot: 'on',
    video: 'retain-on-failure',
  },
  reporter: [
    ['html'],
    ['@percy/playwright']  // Add Percy reporter
  ],
});
```

**Estimated Time**: 1 day  
**Assignee**: Frontend QA  
**Deadline**: After Epic 5 implementation

---

## 📝 Documentation Actions

### 13. Update CLAUDE.md

Add newly identified dependencies and patterns:

```markdown
## Tech Stack Dependencies

### Security & Authentication
- HashiCorp Vault for secrets management
- Auth.js v5 for authentication flows
- JWT with RS256 for API authentication

### Task Processing
- Celery or arq for async job processing
- Redis as message broker

### Payments & Billing
- Stripe for subscription management
```

**Estimated Time**: 1 hour  
**Assignee**: Tech writer  
**Deadline**: After action items 1-4 completed

---

### 14. Create Architecture Decision Records (ADRs)

Document key architectural decisions:

**File**: `docs/architecture/decisions/`

1. `001-python-nodejs-boundary.md`
2. `002-task-queue-selection.md`
3. `003-secrets-management.md`
4. `004-caching-strategy.md`

**Template**:
```markdown
# ADR-001: Python/Node.js Boundary for AST Operations

**Status**: Proposed
**Date**: 2025-01-23
**Decision Makers**: Tech Lead, Backend Team

## Context
[Describe the problem...]

## Decision
[Describe the chosen solution...]

## Consequences
[Describe implications...]

## Alternatives Considered
[List other options...]
```

**Estimated Time**: 4 hours  
**Assignee**: Tech lead  
**Deadline**: Within 2 weeks

---

## 🎯 Success Criteria

### Phase 1: Pre-Implementation (Week 1)
- ✅ All critical dependencies added
- ✅ Python/Node.js architectural decision made
- ✅ Docker Compose updated with Vault
- ✅ CORS and CSP configured

### Phase 2: During Implementation (Ongoing)
- ✅ Performance profiling for each epic
- ✅ CI/CD pipeline operational
- ✅ Dependency versions pinned

### Phase 3: Post-Implementation (Week 8+)
- ✅ Load testing completed
- ✅ Visual regression testing operational
- ✅ ADRs documented
- ✅ CLAUDE.md updated

---

## 📊 Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Missing dependencies cause delays | High | Medium | Complete actions 1-2 immediately |
| Python/Node.js overhead impacts latency | Medium | High | Make architectural decision (action 3) |
| Vault complexity slows security epic | Medium | Medium | Start early, use dev mode initially |
| Ambitious latency targets not met | Medium | High | Early profiling (action 8) |

---

## 📞 Point of Contact

**Technical Review**: AI Technical Architect  
**Questions**: Open GitHub issue with label `epic-review`  
**Urgent**: Contact tech lead directly

---

## 🔄 Next Steps

1. **Immediate** (Today):
   - Review this document with tech lead
   - Assign owners to critical actions (1-4)
   - Schedule architectural decision meeting (action 3)

2. **This Week**:
   - Complete critical actions (1-4)
   - Begin high priority actions (5-8)
   - Set up CI/CD pipeline (action 9)

3. **Next Week**:
   - Continue with medium priority actions
   - Begin documentation updates
   - Start Epic 0 implementation

---

**Document Status**: READY FOR REVIEW  
**Last Updated**: 2025-01-23  
**Version**: 1.0
