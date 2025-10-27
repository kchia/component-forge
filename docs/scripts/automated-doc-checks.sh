#!/bin/bash
# Automated Documentation Checks Script
# Purpose: Run automated checks to identify documentation issues
# Output: Creates initial findings and reference files

set -e  # Exit on error

REPO_ROOT="/home/runner/work/component-forge/component-forge"
DOCS_DIR="$REPO_ROOT/docs"
TMP_DIR="/tmp/doc-review"
OUTPUT_FILE="$TMP_DIR/automated-checks-output.txt"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Create temp directory
mkdir -p "$TMP_DIR"

echo "========================================="
echo "Documentation Review - Automated Checks"
echo "========================================="
echo ""

# Clear output file
> "$OUTPUT_FILE"

# ==========================================
# CHECK 1: Documentation Inventory
# ==========================================
echo -e "${YELLOW}[1/10]${NC} Creating documentation inventory..."
echo "=== DOCUMENTATION INVENTORY ===" >> "$OUTPUT_FILE"
find "$DOCS_DIR" -name "*.md" -type f | \
  grep -v "archive\|project-history" | \
  sort > "$TMP_DIR/doc-inventory.txt"

DOC_COUNT=$(wc -l < "$TMP_DIR/doc-inventory.txt")
echo "Found $DOC_COUNT main documentation files" | tee -a "$OUTPUT_FILE"
cat "$TMP_DIR/doc-inventory.txt" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# ==========================================
# CHECK 2: Code Structure Mapping
# ==========================================
echo -e "${YELLOW}[2/10]${NC} Mapping code structure..."
echo "=== CODE STRUCTURE ===" >> "$OUTPUT_FILE"

# Backend modules
echo "Backend modules:" | tee -a "$OUTPUT_FILE"
find "$REPO_ROOT/backend/src" -type d -maxdepth 1 | sort >> "$OUTPUT_FILE"

# Generation modules
echo -e "\nGeneration modules:" | tee -a "$OUTPUT_FILE"
ls -1 "$REPO_ROOT/backend/src/generation/"*.py 2>/dev/null | wc -l | \
  xargs -I {} echo "  {} files found" | tee -a "$OUTPUT_FILE"

# Service modules
echo -e "\nService modules:" | tee -a "$OUTPUT_FILE"
ls -1 "$REPO_ROOT/backend/src/services/"*.py 2>/dev/null | wc -l | \
  xargs -I {} echo "  {} files found" | tee -a "$OUTPUT_FILE"

# API routes
echo -e "\nAPI routes:" | tee -a "$OUTPUT_FILE"
ls -1 "$REPO_ROOT/backend/src/api/v1/routes/"*.py 2>/dev/null | wc -l | \
  xargs -I {} echo "  {} files found" | tee -a "$OUTPUT_FILE"

echo "" >> "$OUTPUT_FILE"

# ==========================================
# CHECK 3: API Endpoints Extraction
# ==========================================
echo -e "${YELLOW}[3/10]${NC} Extracting API endpoints..."
echo "=== API ENDPOINTS ===" >> "$OUTPUT_FILE"

# Documented endpoints
echo "Documented endpoints:" >> "$OUTPUT_FILE"
grep -rh "POST\|GET\|PUT\|DELETE\|PATCH" "$DOCS_DIR/api/" 2>/dev/null | \
  grep -E "^\s*-\s*\*\*|^###|/api/" | head -20 >> "$OUTPUT_FILE" || \
  echo "  (No clear endpoint list found)" >> "$OUTPUT_FILE"

echo "" >> "$OUTPUT_FILE"

# Actual endpoints from code
echo "Actual endpoints (from route files):" >> "$OUTPUT_FILE"
for file in "$REPO_ROOT/backend/src/api/v1/routes/"*.py; do
  if [ -f "$file" ]; then
    basename "$file" >> "$OUTPUT_FILE"
    grep -E "@router\.(get|post|put|delete|patch)" "$file" | head -5 >> "$OUTPUT_FILE" || true
  fi
done

echo "" >> "$OUTPUT_FILE"

# ==========================================
# CHECK 4: Port Numbers Verification
# ==========================================
echo -e "${YELLOW}[4/10]${NC} Verifying port numbers..."
echo "=== PORT NUMBERS ===" >> "$OUTPUT_FILE"

# Documented ports
echo "Documented ports:" >> "$OUTPUT_FILE"
grep -rh "localhost:[0-9]" "$DOCS_DIR/" "$REPO_ROOT/README.md" 2>/dev/null | \
  sort -u | head -10 >> "$OUTPUT_FILE" || true

echo "" >> "$OUTPUT_FILE"

# Actual ports from docker-compose
echo "Docker Compose ports:" >> "$OUTPUT_FILE"
if [ -f "$REPO_ROOT/docker-compose.yml" ]; then
  grep -B 1 "ports:" "$REPO_ROOT/docker-compose.yml" | \
    grep -v "^--$" >> "$OUTPUT_FILE" || true
else
  echo "  docker-compose.yml not found" >> "$OUTPUT_FILE"
fi

echo "" >> "$OUTPUT_FILE"

# ==========================================
# CHECK 5: Version Consistency
# ==========================================
echo -e "${YELLOW}[5/10]${NC} Checking version consistency..."
echo "=== VERSION REFERENCES ===" >> "$OUTPUT_FILE"

# Next.js versions
echo "Next.js versions:" >> "$OUTPUT_FILE"
echo "  In package.json:" >> "$OUTPUT_FILE"
grep "\"next\"" "$REPO_ROOT/app/package.json" 2>/dev/null >> "$OUTPUT_FILE" || \
  echo "  package.json not found" >> "$OUTPUT_FILE"
echo "  In documentation:" >> "$OUTPUT_FILE"
grep -rh "Next\.js.*15" "$DOCS_DIR/" "$REPO_ROOT/README.md" 2>/dev/null | \
  sort -u | head -5 >> "$OUTPUT_FILE" || echo "  No mentions found" >> "$OUTPUT_FILE"

echo "" >> "$OUTPUT_FILE"

# React versions
echo "React versions:" >> "$OUTPUT_FILE"
echo "  In package.json:" >> "$OUTPUT_FILE"
grep "\"react\"" "$REPO_ROOT/app/package.json" 2>/dev/null | head -2 >> "$OUTPUT_FILE" || \
  echo "  package.json not found" >> "$OUTPUT_FILE"
echo "  In documentation:" >> "$OUTPUT_FILE"
grep -rh "React.*19" "$DOCS_DIR/" "$REPO_ROOT/README.md" 2>/dev/null | \
  sort -u | head -5 >> "$OUTPUT_FILE" || echo "  No mentions found" >> "$OUTPUT_FILE"

echo "" >> "$OUTPUT_FILE"

# Python versions
echo "Python versions:" >> "$OUTPUT_FILE"
echo "  In documentation:" >> "$OUTPUT_FILE"
grep -rh "Python.*3\.[0-9]" "$DOCS_DIR/" "$REPO_ROOT/README.md" 2>/dev/null | \
  sort -u | head -5 >> "$OUTPUT_FILE" || echo "  No mentions found" >> "$OUTPUT_FILE"

echo "" >> "$OUTPUT_FILE"

# ==========================================
# CHECK 6: Internal Links Validation
# ==========================================
echo -e "${YELLOW}[6/10]${NC} Checking internal links..."
echo "=== INTERNAL LINKS ===" >> "$OUTPUT_FILE"

# Extract all markdown links
grep -roh "\[.*\](\.\/[^)]*)" "$DOCS_DIR/" 2>/dev/null | \
  sort -u > "$TMP_DIR/internal-links.txt" || true

LINK_COUNT=$(wc -l < "$TMP_DIR/internal-links.txt" 2>/dev/null || echo "0")
echo "Found $LINK_COUNT unique internal links" | tee -a "$OUTPUT_FILE"

# Check for broken links (sample)
echo "Checking sample links..." >> "$OUTPUT_FILE"
head -10 "$TMP_DIR/internal-links.txt" 2>/dev/null >> "$OUTPUT_FILE" || \
  echo "  No links found" >> "$OUTPUT_FILE"

echo "" >> "$OUTPUT_FILE"

# ==========================================
# CHECK 7: External Links
# ==========================================
echo -e "${YELLOW}[7/10]${NC} Extracting external links..."
echo "=== EXTERNAL LINKS ===" >> "$OUTPUT_FILE"

grep -roh "https\?://[^)]*" "$DOCS_DIR/" "$REPO_ROOT/README.md" 2>/dev/null | \
  sort -u > "$TMP_DIR/external-links.txt" || true

EXT_LINK_COUNT=$(wc -l < "$TMP_DIR/external-links.txt" 2>/dev/null || echo "0")
echo "Found $EXT_LINK_COUNT unique external links" | tee -a "$OUTPUT_FILE"

# Show first 15
echo "Sample external links:" >> "$OUTPUT_FILE"
head -15 "$TMP_DIR/external-links.txt" 2>/dev/null >> "$OUTPUT_FILE" || \
  echo "  No links found" >> "$OUTPUT_FILE"

echo "" >> "$OUTPUT_FILE"

# ==========================================
# CHECK 8: Component Inventory
# ==========================================
echo -e "${YELLOW}[8/10]${NC} Checking UI components..."
echo "=== UI COMPONENTS ===" >> "$OUTPUT_FILE"

# Documented components
echo "Documented in BASE-COMPONENTS.md:" >> "$OUTPUT_FILE"
if [ -f "$REPO_ROOT/.claude/BASE-COMPONENTS.md" ]; then
  grep -E "^###? (Button|Card|Badge|Input|Alert|Progress|Dialog|Accordion|Tabs)" \
    "$REPO_ROOT/.claude/BASE-COMPONENTS.md" | head -15 >> "$OUTPUT_FILE" || \
    echo "  No component headers found" >> "$OUTPUT_FILE"
else
  echo "  BASE-COMPONENTS.md not found" >> "$OUTPUT_FILE"
fi

echo "" >> "$OUTPUT_FILE"

# Actual implemented components
echo "Implemented components:" >> "$OUTPUT_FILE"
if [ -d "$REPO_ROOT/app/src/components/ui" ]; then
  ls -1 "$REPO_ROOT/app/src/components/ui/"*.tsx 2>/dev/null | \
    grep -v ".stories\|.test" | \
    xargs -I {} basename {} .tsx | \
    sort >> "$OUTPUT_FILE" || echo "  No components found" >> "$OUTPUT_FILE"
else
  echo "  UI components directory not found" >> "$OUTPUT_FILE"
fi

echo "" >> "$OUTPUT_FILE"

# ==========================================
# CHECK 9: Service Layer Files
# ==========================================
echo -e "${YELLOW}[9/10]${NC} Verifying service layer..."
echo "=== SERVICE LAYER ===" >> "$OUTPUT_FILE"

if [ -d "$REPO_ROOT/backend/src/services" ]; then
  echo "Service files found:" >> "$OUTPUT_FILE"
  ls -1 "$REPO_ROOT/backend/src/services/"*.py 2>/dev/null | \
    xargs -I {} basename {} .py | \
    sed 's/^/  - /' >> "$OUTPUT_FILE" || echo "  No service files" >> "$OUTPUT_FILE"
else
  echo "  Services directory not found" >> "$OUTPUT_FILE"
fi

echo "" >> "$OUTPUT_FILE"

# ==========================================
# CHECK 10: Deprecated Modules Check
# ==========================================
echo -e "${YELLOW}[10/10]${NC} Checking deprecated modules..."
echo "=== DEPRECATED MODULES CHECK ===" >> "$OUTPUT_FILE"

deprecated_modules=(
  "token_injector.py"
  "tailwind_generator.py"
  "requirement_implementer.py"
  "a11y_enhancer.py"
  "type_generator.py"
  "storybook_generator.py"
)

echo "Checking for modules that should be removed (per Epic 4.5):" >> "$OUTPUT_FILE"
for module in "${deprecated_modules[@]}"; do
  if [ -f "$REPO_ROOT/backend/src/generation/$module" ]; then
    echo -e "  ${RED}❌ FOUND${NC}: $module (should be removed)" | tee -a "$OUTPUT_FILE"
  else
    echo "  ✅ REMOVED: $module" >> "$OUTPUT_FILE"
  fi
done

echo "" >> "$OUTPUT_FILE"

# ==========================================
# Summary
# ==========================================
echo ""
echo "========================================="
echo "Automated Checks Complete!"
echo "========================================="
echo ""
echo "Results saved to:"
echo "  $OUTPUT_FILE"
echo ""
echo "Reference files created:"
echo "  $TMP_DIR/doc-inventory.txt"
echo "  $TMP_DIR/internal-links.txt"
echo "  $TMP_DIR/external-links.txt"
echo ""
echo "Next steps:"
echo "  1. Review the output file"
echo "  2. Follow DOCUMENTATION_REVIEW_EXECUTION_GUIDE.md for manual checks"
echo "  3. Record findings in DOCUMENTATION_REVIEW_FINDINGS.md"
echo ""

# Display summary
echo -e "${GREEN}Summary:${NC}"
echo "  Documentation files: $DOC_COUNT"
echo "  Internal links: $LINK_COUNT"
echo "  External links: $EXT_LINK_COUNT"
echo ""

# Open output file for review
cat "$OUTPUT_FILE"
