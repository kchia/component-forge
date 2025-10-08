# Documentation Review Execution Guide

**Purpose**: Step-by-step guide for executing the documentation review  
**Companion Documents**: 
- `DOCUMENTATION_REVIEW_PLAN.md` - Overall methodology and phases
- `DOCUMENTATION_REVIEW_FINDINGS.md` - Template for recording findings

---

## Quick Start

```bash
# 1. Navigate to repository root
cd /home/runner/work/component-forge/component-forge

# 2. Run automated checks (creates initial findings)
bash docs/scripts/automated-doc-checks.sh

# 3. Begin manual review using this guide

# 4. Record findings in DOCUMENTATION_REVIEW_FINDINGS.md

# 5. Generate final report
bash docs/scripts/generate-doc-report.sh
```

---

## Phase 1: Structural Analysis

### Step 1.1: Document Inventory
Create complete list of documentation files:

```bash
# List all markdown documentation (exclude archives)
find docs -name "*.md" -type f | \
  grep -v "archive\|project-history" | \
  sort > /tmp/doc-inventory.txt

# Count files
wc -l /tmp/doc-inventory.txt

# Expected: ~36 main documentation files
```

**✓ Checkpoint**: Verify count matches expected (~36 files)

---

### Step 1.2: Code Structure Mapping
Map documentation to actual code structure:

```bash
# Backend module structure
echo "=== BACKEND MODULES ===" > /tmp/code-structure.txt
find backend/src -type d -maxdepth 1 >> /tmp/code-structure.txt

# Backend submodules
echo -e "\n=== GENERATION MODULES ===" >> /tmp/code-structure.txt
ls -1 backend/src/generation/*.py >> /tmp/code-structure.txt

echo -e "\n=== SERVICE MODULES ===" >> /tmp/code-structure.txt
ls -1 backend/src/services/*.py >> /tmp/code-structure.txt

echo -e "\n=== API ROUTES ===" >> /tmp/code-structure.txt
ls -1 backend/src/api/v1/routes/*.py >> /tmp/code-structure.txt

# Frontend structure
echo -e "\n=== FRONTEND COMPONENTS ===" >> /tmp/code-structure.txt
ls -1 app/src/components/ui/*.tsx | grep -v ".stories\|.test" >> /tmp/code-structure.txt

cat /tmp/code-structure.txt
```

**✓ Checkpoint**: Structure file created for reference

---

### Step 1.3: Documentation Gap Analysis
Identify undocumented code and unimplemented docs:

```bash
# Extract documented modules from architecture.md
grep -E "^####? \*\*.*\*\*|^### \`.*\.py\`" docs/backend/architecture.md > /tmp/documented-modules.txt

# Compare with actual files
echo "Documented modules:"
cat /tmp/documented-modules.txt

echo -e "\nActual modules:"
ls -1 backend/src/generation/*.py backend/src/services/*.py
```

**Manual Task**: Compare lists and note gaps

**✓ Checkpoint**: Gaps documented in findings file

---

## Phase 2: API Documentation Review

### Step 2.1: Extract Documented Endpoints

```bash
# Extract endpoints from API documentation
echo "=== DOCUMENTED ENDPOINTS ===" > /tmp/api-endpoints.txt

# From docs/api/overview.md
grep -E "POST|GET|PUT|DELETE|PATCH" docs/api/overview.md | \
  grep -v "```" >> /tmp/api-endpoints.txt || true

# From docs/api/README.md
grep -E "POST|GET|PUT|DELETE|PATCH" docs/api/README.md | \
  grep -v "```" >> /tmp/api-endpoints.txt || true

cat /tmp/api-endpoints.txt
```

---

### Step 2.2: Extract Actual Endpoints

```bash
# Extract routes from FastAPI code
echo "=== ACTUAL ENDPOINTS ===" > /tmp/actual-endpoints.txt

# Find all @router decorators and their paths
for file in backend/src/api/v1/routes/*.py; do
  echo -e "\n=== $(basename $file) ===" >> /tmp/actual-endpoints.txt
  grep -E "@router\.(get|post|put|delete|patch)" "$file" -A 1 | \
    grep -E "^\s*@router|def " >> /tmp/actual-endpoints.txt || true
done

cat /tmp/actual-endpoints.txt
```

---

### Step 2.3: Compare Endpoints

**Manual Task**: Compare `/tmp/api-endpoints.txt` with `/tmp/actual-endpoints.txt`

**Checklist**:
- [ ] All documented endpoints exist in code
- [ ] All code endpoints are documented
- [ ] HTTP methods match (POST/GET/PUT/DELETE)
- [ ] Path parameters match
- [ ] Query parameters match

**Record**: Any discrepancies in `DOCUMENTATION_REVIEW_FINDINGS.md` → API-001

---

### Step 2.4: Verify Base URLs and Ports

```bash
# Check documented URLs
echo "=== DOCUMENTED URLS/PORTS ===" > /tmp/urls-check.txt
grep -r "localhost:[0-9]" docs/ README.md >> /tmp/urls-check.txt || true
grep -r "http://.*:[0-9]" docs/ README.md >> /tmp/urls-check.txt || true

# Check actual configurations
echo -e "\n=== ACTUAL CONFIGS ===" >> /tmp/urls-check.txt
echo "Frontend (package.json):" >> /tmp/urls-check.txt
grep -A 3 "\"dev\"" app/package.json >> /tmp/urls-check.txt || true

echo -e "\nBackend (main.py):" >> /tmp/urls-check.txt
grep -E "port|host" backend/src/main.py >> /tmp/urls-check.txt || true

echo -e "\nDocker compose:" >> /tmp/urls-check.txt
grep -E "ports:" docker-compose.yml -A 1 >> /tmp/urls-check.txt || true

cat /tmp/urls-check.txt
```

**Expected Ports**:
- Frontend: 3000
- Backend: 8000
- PostgreSQL: 5432
- Redis: 6379
- Qdrant: 6333, 6334

**✓ Checkpoint**: Port numbers verified → Record any issues in SETUP-005

---

## Phase 3: Backend Architecture Review

### Step 3.1: Verify Service Layer

```bash
# List documented services from architecture.md
echo "=== DOCUMENTED SERVICES ===" > /tmp/services-check.txt
grep -A 2 "^\*\*Services:\*\*" docs/backend/architecture.md | \
  grep -E "^[0-9]\." >> /tmp/services-check.txt || true

# List actual service files
echo -e "\n=== ACTUAL SERVICES ===" >> /tmp/services-check.txt
ls -1 backend/src/services/*.py | \
  xargs -I {} basename {} .py >> /tmp/services-check.txt

cat /tmp/services-check.txt
```

**Manual Review**: For each service, verify:
- [ ] **RetrievalService** (`retrieval_service.py`)
  - Check: Class exists, methods match docs
  - Docs: `docs/backend/architecture.md` lines ~61-65
  
- [ ] **ImageProcessor** (`image_processor.py`)
  - Check: Image preprocessing methods
  - Docs: `docs/backend/architecture.md` lines ~67-70
  
- [ ] **FigmaClient** (`figma_client.py`)
  - Check: Figma API integration methods
  - Docs: `docs/backend/architecture.md` lines ~72-75
  
- [ ] **RequirementExporter** (`requirement_exporter.py`)
  - Check: Export methods
  - Docs: `docs/backend/architecture.md` lines ~77-79
  
- [ ] **TokenExporter** (`token_exporter.py`)
  - Check: Token export formats
  - Docs: `docs/backend/architecture.md` lines ~81-83

**Record**: Findings in BACKEND-002

---

### Step 3.2: Verify Generation Pipeline

```bash
# List generation modules
echo "=== GENERATION MODULES ===" > /tmp/generation-check.txt
ls -1 backend/src/generation/*.py >> /tmp/generation-check.txt

cat /tmp/generation-check.txt
```

**Manual Review**: For each module in `docs/backend/generation-service.md`:

- [ ] **GeneratorService** (`generator_service.py`)
  - Verify: 3-stage pipeline (LLM Generation, Validation, Post-Processing)
  - Check: Class methods, pipeline stages
  - Open: `backend/src/generation/generator_service.py`
  - Compare with: `docs/backend/generation-service.md` "Architecture" section
  
- [ ] **PromptBuilder** (`prompt_builder.py`)
  - Verify: Prompt construction methods
  - Check: build_prompt method exists
  - Open: `backend/src/generation/prompt_builder.py`
  
- [ ] **LLMGenerator** (`llm_generator.py`)
  - Verify: OpenAI GPT-4 usage
  - Check: generate method, retry logic
  - Open: `backend/src/generation/llm_generator.py`
  
- [ ] **CodeValidator** (`code_validator.py`)
  - Verify: TypeScript + ESLint validation
  - Check: Parallel validation, LLM fixing
  - Open: `backend/src/generation/code_validator.py`
  
- [ ] **PatternParser** (`pattern_parser.py`)
  - Verify: shadcn/ui pattern loading
  - Check: parse method
  - Open: `backend/src/generation/pattern_parser.py`
  
- [ ] **CodeAssembler** (`code_assembler.py`)
  - Verify: Final assembly logic
  - Open: `backend/src/generation/code_assembler.py`

**Record**: Findings in BACKEND-003

---

### Step 3.3: Verify Deprecated Modules

According to `docs/backend/generation-service.md`, these should be removed:

```bash
# Check if deprecated modules still exist
echo "=== CHECKING DEPRECATED MODULES ===" > /tmp/deprecated-check.txt

deprecated_modules=(
  "token_injector.py"
  "tailwind_generator.py"
  "requirement_implementer.py"
  "a11y_enhancer.py"
  "type_generator.py"
  "storybook_generator.py"
)

for module in "${deprecated_modules[@]}"; do
  if [ -f "backend/src/generation/$module" ]; then
    echo "❌ FOUND: $module (should be removed)" >> /tmp/deprecated-check.txt
  else
    echo "✅ REMOVED: $module" >> /tmp/deprecated-check.txt
  fi
done

cat /tmp/deprecated-check.txt
```

**✓ Checkpoint**: All deprecated modules should be removed → Record in BACKEND-005

---

## Phase 4: Features Documentation Review

### Step 4.1: Token Extraction Feature

**Review File**: `docs/features/token-extraction.md`

**Verification Steps**:
1. Open `docs/features/token-extraction.md`
2. Open `backend/src/api/v1/routes/tokens.py`
3. Check extraction endpoints exist
4. Verify token types mentioned in docs

**Checklist**:
- [ ] Extraction endpoints documented correctly
- [ ] Token types match implementation (colors, typography, spacing)
- [ ] GPT-4V usage documented correctly
- [ ] Examples accurate

**Record**: Findings in FEATURE-001

---

### Step 4.2: Figma Integration Feature

**Review File**: `docs/features/figma-integration.md`

**Verification Steps**:
1. Open `docs/features/figma-integration.md`
2. Open `backend/src/services/figma_client.py`
3. Open `backend/src/api/v1/routes/figma.py`
4. Verify Figma API integration methods

**Checklist**:
- [ ] Figma API usage documented
- [ ] File/node fetching documented
- [ ] Token extraction from Figma documented
- [ ] Example Figma URLs match expected format

**Record**: Findings in FEATURE-002

---

### Step 4.3: Pattern Retrieval Feature

**Review File**: `docs/features/pattern-retrieval.md`

**Verification Steps**:
1. Open `docs/features/pattern-retrieval.md`
2. Open `backend/src/services/retrieval_service.py`
3. Open `backend/src/retrieval/` directory
4. Verify BM25 + semantic search

**Checklist**:
- [ ] Retrieval pipeline documented (BM25 + semantic)
- [ ] Qdrant integration documented
- [ ] Top-K retrieval documented
- [ ] Explanations feature documented

**Record**: Findings in FEATURE-003

---

### Step 4.4: Code Generation Feature

**Review File**: `docs/features/code-generation.md`

**Verification Steps**:
1. Open `docs/features/code-generation.md`
2. Compare with `docs/backend/generation-service.md`
3. Verify consistency across docs

**Checklist**:
- [ ] LLM-first approach documented
- [ ] 3-stage pipeline documented
- [ ] TypeScript output documented
- [ ] Storybook stories documented
- [ ] Showcase files documented

**Record**: Findings in FEATURE-004

---

### Step 4.5: Quality Validation Feature

**Review File**: `docs/features/quality-validation.md`

**Verification Steps**:
1. Open `docs/features/quality-validation.md`
2. Open `backend/src/validation/`
3. Open `backend/src/generation/code_validator.py`

**Checklist**:
- [ ] TypeScript validation documented
- [ ] ESLint validation documented
- [ ] axe-core accessibility documented
- [ ] Auto-fix feature documented
- [ ] Report generation documented

**Record**: Findings in FEATURE-005

---

### Step 4.6: Accessibility Feature

**Review File**: `docs/features/accessibility.md`

**Verification Steps**:
1. Open `docs/features/accessibility.md`
2. Check frontend axe-core setup: `app/package.json`
3. Check WCAG compliance mentions

**Checklist**:
- [ ] axe-core integration documented
- [ ] WCAG 2.1 compliance documented
- [ ] A11y testing documented
- [ ] Keyboard navigation documented
- [ ] Screen reader support documented

**Record**: Findings in FEATURE-006

---

### Step 4.7: Observability Feature

**Review File**: `docs/features/observability.md`

**Verification Steps**:
1. Open `docs/features/observability.md`
2. Check LangSmith usage in code: `grep -r "langsmith" backend/`
3. Check `@traceable` decorators in generation pipeline

**Checklist**:
- [ ] LangSmith integration documented
- [ ] Tracing documented
- [ ] Metrics documented
- [ ] Debugging workflow documented

**Record**: Findings in FEATURE-007

---

## Phase 5: Frontend Documentation Review

### Step 5.1: Verify Next.js Version

```bash
# Check package.json
echo "=== NEXT.JS VERSION ===" > /tmp/frontend-versions.txt
grep "\"next\"" app/package.json >> /tmp/frontend-versions.txt

# Check all documentation mentions
echo -e "\n=== DOCUMENTED NEXT.JS VERSIONS ===" >> /tmp/frontend-versions.txt
grep -rh "Next\.js.*15" docs/ README.md | sort -u >> /tmp/frontend-versions.txt

cat /tmp/frontend-versions.txt
```

**Expected**: Next.js 15.5.4 everywhere

**✓ Checkpoint**: Version consistency → Record in FRONTEND-001

---

### Step 5.2: Verify React Version

```bash
# Check package.json
echo "=== REACT VERSION ===" > /tmp/react-version.txt
grep "\"react\"" app/package.json >> /tmp/react-version.txt

# Check documentation mentions
echo -e "\n=== DOCUMENTED REACT VERSIONS ===" >> /tmp/react-version.txt
grep -rh "React.*19" docs/ README.md | sort -u >> /tmp/react-version.txt

cat /tmp/react-version.txt
```

**Expected**: React 19.1.0 or React 19

**✓ Checkpoint**: Version consistency → Record in FRONTEND-002

---

### Step 5.3: Verify shadcn/ui Components

```bash
# List documented base components
echo "=== DOCUMENTED BASE COMPONENTS ===" > /tmp/components-check.txt
grep -E "^###? (Button|Card|Badge|Input|Alert|Progress|Dialog|Accordion)" \
  .claude/BASE-COMPONENTS.md >> /tmp/components-check.txt || true

# List actual UI components
echo -e "\n=== IMPLEMENTED COMPONENTS ===" >> /tmp/components-check.txt
ls -1 app/src/components/ui/*.tsx | \
  grep -v ".stories\|.test" | \
  xargs -I {} basename {} .tsx >> /tmp/components-check.txt

cat /tmp/components-check.txt
```

**Manual Review**: Compare lists

**Checklist**:
- [ ] Button component
- [ ] Card component
- [ ] Badge component
- [ ] Input component
- [ ] Alert component
- [ ] Progress component
- [ ] Dialog component
- [ ] Accordion component
- [ ] Tabs component
- [ ] Code Block component

**Record**: Findings in FRONTEND-003

---

### Step 5.4: Verify State Management

```bash
# Check Zustand usage
echo "=== ZUSTAND STORES ===" > /tmp/state-management.txt
find app/src/stores -name "*.ts" >> /tmp/state-management.txt || true

# Check TanStack Query usage
echo -e "\n=== TANSTACK QUERY ===" >> /tmp/state-management.txt
grep -r "useQuery\|useMutation" app/src --include="*.tsx" --include="*.ts" | \
  head -5 >> /tmp/state-management.txt || true

cat /tmp/state-management.txt
```

**Checklist**:
- [ ] Zustand stores exist
- [ ] TanStack Query usage confirmed
- [ ] Documentation matches implementation

**Record**: Findings in FRONTEND-004

---

### Step 5.5: Verify Auth System

```bash
# Check next-auth version
echo "=== AUTH SYSTEM ===" > /tmp/auth-check.txt
grep "next-auth" app/package.json >> /tmp/auth-check.txt || true

# Check Auth.js v5 mentions in docs
echo -e "\n=== DOCUMENTED AUTH ===" >> /tmp/auth-check.txt
grep -rh "Auth\.js\|next-auth.*5" docs/ README.md | head -5 >> /tmp/auth-check.txt || true

cat /tmp/auth-check.txt
```

**Expected**: next-auth v5 or Auth.js v5

**✓ Checkpoint**: Auth version verified → Record in FRONTEND-005

---

### Step 5.6: Verify Testing Setup

```bash
# Check Playwright config exists
echo "=== E2E TESTING ===" > /tmp/testing-check.txt
if [ -f "app/playwright.config.ts" ]; then
  echo "✅ Playwright config exists" >> /tmp/testing-check.txt
else
  echo "❌ Playwright config missing" >> /tmp/testing-check.txt
fi

# List E2E tests
echo -e "\n=== E2E TEST FILES ===" >> /tmp/testing-check.txt
find app/e2e -name "*.spec.ts" >> /tmp/testing-check.txt || true

cat /tmp/testing-check.txt
```

**Checklist**:
- [ ] Playwright configured
- [ ] E2E tests exist
- [ ] Documentation matches setup

**Record**: Findings in FRONTEND-006

---

## Phase 6: Getting Started & Setup Review

### Step 6.1: Test Prerequisites

**Manual Test**: Verify documented prerequisites are accurate

```bash
# Check Node.js requirement
node --version
# Expected: v18.x or higher

# Check Python requirement
python --version
# Expected: 3.11.x or higher

# Check Docker
docker --version
```

**Checklist**:
- [ ] Node.js 18+ documented correctly
- [ ] Python 3.11+ documented correctly
- [ ] Docker Desktop mentioned
- [ ] OpenAI API Key mentioned

**Record**: Findings in SETUP-001

---

### Step 6.2: Test Installation Commands

**Manual Test**: Execute documented commands

```bash
# Test make install (DRY RUN - just check Makefile)
grep -A 20 "^install:" Makefile

# Test make dev (DRY RUN - just check Makefile)
grep -A 20 "^dev:" Makefile

# Test make test (DRY RUN - just check Makefile)
grep -A 20 "^test:" Makefile
```

**Checklist**:
- [ ] `make install` target exists and looks correct
- [ ] `make dev` target exists and looks correct
- [ ] `make test` target exists and looks correct
- [ ] Commands match documentation

**Record**: Findings in SETUP-002

---

### Step 6.3: Verify Environment Files

```bash
# Check for example environment files
echo "=== ENVIRONMENT FILES ===" > /tmp/env-check.txt
ls -1 backend/.env* app/.env* 2>/dev/null >> /tmp/env-check.txt || true

cat /tmp/env-check.txt
```

**Expected Files**:
- `backend/.env.example`
- `app/.env.local.example` or `app/.env.example`

**✓ Checkpoint**: Env files exist and match docs → Record in SETUP-003

---

### Step 6.4: Verify Docker Services

```bash
# Extract services from docker-compose
echo "=== DOCKER SERVICES ===" > /tmp/docker-services.txt
grep -E "^\s+[a-z-]+:" docker-compose.yml >> /tmp/docker-services.txt

# Extract versions
echo -e "\n=== SERVICE VERSIONS ===" >> /tmp/docker-services.txt
grep "image:" docker-compose.yml >> /tmp/docker-services.txt

cat /tmp/docker-services.txt
```

**Expected Services**:
- PostgreSQL 16
- Qdrant
- Redis 7

**✓ Checkpoint**: Services match documentation → Record in SETUP-004

---

## Phase 7: Code Examples Review

### Step 7.1: Test API Examples

**Manual Test**: Try documented API examples

Example from `docs/api/README.md`:

```bash
# Health check example (requires backend running)
# DRY RUN: Just verify syntax
echo "curl http://localhost:8000/health"

# Generate example (requires auth)
# DRY RUN: Just verify curl syntax is correct
cat << 'EOF'
curl -X POST http://localhost:8000/api/v1/generate/screenshot \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@screenshot.png"
EOF
```

**Checklist**:
- [ ] curl syntax correct
- [ ] Endpoints match actual routes
- [ ] Headers correct
- [ ] Parameters correct

**Record**: Findings in EXAMPLES-001

---

### Step 7.2: Verify Python Examples

**Manual Review**: Check Python code snippets in docs

From `docs/backend/architecture.md` and other backend docs:

```bash
# Extract Python code blocks
grep -A 20 "```python" docs/backend/*.md | head -50
```

**Checklist**:
- [ ] Import statements correct
- [ ] Class names match actual classes
- [ ] Method signatures match
- [ ] No deprecated API usage

**Record**: Findings in EXAMPLES-002

---

### Step 7.3: Verify TypeScript Examples

**Manual Review**: Check TypeScript/React examples

```bash
# Extract TypeScript code blocks
grep -A 20 "```typescript\|```tsx" docs/**/*.md | head -50
```

**Checklist**:
- [ ] Import paths correct
- [ ] Component props match actual components
- [ ] Hooks usage correct
- [ ] No deprecated patterns

**Record**: Findings in EXAMPLES-003

---

## Phase 8: Links & Cross-References Review

### Step 8.1: Check Internal Links

```bash
# Extract all markdown links
echo "=== INTERNAL LINKS ===" > /tmp/links-check.txt
grep -roh "\[.*\](\.\/[^)]*)" docs/ | sort -u >> /tmp/links-check.txt

# Count total links
echo -e "\n=== LINK COUNT ===" >> /tmp/links-check.txt
wc -l /tmp/links-check.txt >> /tmp/links-check.txt

cat /tmp/links-check.txt | head -50
```

**Manual Task**: Verify each link target exists

**✓ Checkpoint**: Record broken links in LINKS-001

---

### Step 8.2: Check External Links

```bash
# Extract external links
echo "=== EXTERNAL LINKS ===" > /tmp/external-links.txt
grep -roh "https\?://[^)]*" docs/ README.md | \
  sort -u >> /tmp/external-links.txt

cat /tmp/external-links.txt | head -20
```

**Manual Task**: Test critical external links

**✓ Checkpoint**: Record broken external links in LINKS-003

---

## Phase 9: Versioning Review

### Step 9.1: Collect All Version References

```bash
# Create version summary
cat > /tmp/version-summary.txt << 'EOF'
=== VERSION AUDIT ===

Next.js:
EOF

grep -rh "Next\.js.*[0-9]" docs/ README.md | sort -u >> /tmp/version-summary.txt

echo -e "\nReact:" >> /tmp/version-summary.txt
grep -rh "React.*[0-9]" docs/ README.md | sort -u >> /tmp/version-summary.txt

echo -e "\nPython:" >> /tmp/version-summary.txt
grep -rh "Python.*3\.[0-9]" docs/ README.md | sort -u >> /tmp/version-summary.txt

echo -e "\nFastAPI:" >> /tmp/version-summary.txt
grep -rh "FastAPI.*[0-9]" docs/ README.md | sort -u >> /tmp/version-summary.txt

cat /tmp/version-summary.txt
```

**Manual Task**: Verify all versions match package.json/requirements.txt

**✓ Checkpoint**: Record inconsistencies in VERSION-001

---

## Completion Checklist

- [ ] Phase 1: Structural Analysis completed
- [ ] Phase 2: API Documentation reviewed
- [ ] Phase 3: Backend Architecture reviewed
- [ ] Phase 4: Features Documentation reviewed
- [ ] Phase 5: Frontend Documentation reviewed
- [ ] Phase 6: Setup & Getting Started reviewed
- [ ] Phase 7: Code Examples verified
- [ ] Phase 8: Links & References checked
- [ ] Phase 9: Versions verified

- [ ] All findings recorded in `DOCUMENTATION_REVIEW_FINDINGS.md`
- [ ] Priority issues identified
- [ ] Recommendations documented
- [ ] Summary statistics calculated

---

## Final Report Generation

Once all phases complete:

1. Fill in summary statistics in `DOCUMENTATION_REVIEW_FINDINGS.md`
2. Prioritize action items
3. Calculate accuracy scores
4. Create executive summary
5. Submit findings document

---

## Tips for Efficient Review

1. **Use dual monitors**: Documentation on one side, code on the other
2. **Take notes immediately**: Don't rely on memory
3. **Use search**: Ctrl+F in VS Code to find references quickly
4. **Test examples**: Don't assume they work
5. **Ask questions**: If unsure, mark for follow-up
6. **Be systematic**: Follow phases in order
7. **Take breaks**: Accuracy degrades with fatigue

---

## Questions or Issues?

If you encounter:
- **Ambiguous documentation**: Note it and flag for clarification
- **Missing source code**: May indicate implementation gap
- **Extra source code**: May need documentation
- **Conflicting information**: Record both versions and source

Add all questions/issues to findings document with "NEEDS CLARIFICATION" tag.
