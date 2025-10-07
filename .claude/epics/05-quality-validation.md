# Epic 5: Quality Validation & Testing

**Status**: Not Started
**Priority**: Critical
**Epic Owner**: QA/Frontend Team
**Estimated Tasks**: 9
**Depends On**: Epic 4 (Code Generation)

---

## Overview

Build automated quality validation system that ensures every generated component meets accessibility standards, type safety requirements, code quality guidelines, and design token adherence. Validation runs in the **frontend** using existing Next.js/TypeScript tooling, with backend API endpoints for validation orchestration and results storage. Includes auto-fix capabilities with retry logic and comprehensive quality reporting.

**Architecture Note**: Validation leverages the frontend's existing TypeScript compiler, ESLint, Prettier, and axe-core setup. Backend provides validation orchestration API and stores results, but does NOT run Node.js tooling via subprocess.

---

## Goals

1. Validate TypeScript compilation (strict mode)
2. Run ESLint and Prettier validation
3. Execute axe-core accessibility testing (0 critical violations)
4. Test keyboard navigation and focus management
5. Verify focus indicators are visible
6. Check color contrast compliance (WCAG AA)
7. Calculate token adherence meter (≥90% target)
8. Implement auto-fix with single retry for failures
9. Generate comprehensive quality reports

---

## Success Criteria

- ✅ TypeScript strict compilation succeeds (required)
- ✅ ESLint validation passes with zero errors
- ✅ Prettier formatting verified
- ✅ axe-core audit shows 0 critical violations (required)
- ✅ 0 serious violations (required)
- ✅ Keyboard navigation works (Tab, Enter, Space, Escape)
- ✅ Focus indicators visible with ≥3:1 contrast
- ✅ Color contrast meets WCAG AA (4.5:1 text, 3:1 UI)
- ✅ Token adherence ≥90% (colors, typography, spacing)
- ✅ Auto-fix resolves 80%+ of fixable issues
- ✅ Quality report generated with all metrics
- ✅ Validation completes in <10s

---

## Wireframe

### Interactive Prototype
**View HTML:** [component-preview-page.html](../wireframes/component-preview-page.html) *(shares same page with Epic 4, validation section)*

![Component Preview Page - Validation](../wireframes/screenshots/04-component-preview-desktop.png)

### Key UI Elements

**Validation Progress** (Runs after generation)
- Progress bar with validation stages
  - TypeScript Compilation → Task 1
  - ESLint & Prettier → Task 2
  - axe-core A11y Test → Task 3
  - Keyboard Navigation → Task 4
  - Focus Indicators → Task 5
  - Color Contrast → Task 6
  - Token Adherence → Task 7
- Auto-fix indicator → Task 8: Auto-Fix & Retry Logic
- Elapsed time (target: <10s)

**Quality Scorecard** (Top summary)
- Overall status: PASS / FAIL
- Critical checks:
  - ✓ TypeScript: Compiled successfully
  - ✓ ESLint: 0 errors, 2 warnings
  - ✓ Accessibility: 0 critical/serious violations
  - ✓ Token Adherence: 94%
- Auto-fixes applied: 3 issues resolved

**Validation Results** (Tabbed sections)

**TypeScript Tab** → Task 1: TypeScript Compilation Check
- Compilation status
- Errors/warnings with line numbers
- Type coverage report
- Auto-fixes applied (unused imports removed)

**Code Quality Tab** → Task 2: ESLint & Prettier Validation
- ESLint results by severity
- Prettier formatting status
- Auto-fixed issues list

**Accessibility Tab** → Task 3, 4, 5, 6
- axe-core audit summary → Task 3: axe-core Accessibility Testing
  - 0 critical violations ✓
  - 0 serious violations ✓
  - 2 moderate issues (warnings only)
- Keyboard navigation results → Task 4: Keyboard Navigation Testing
  - Tab order visualization
  - Enter/Space activation test
- Focus indicators → Task 5: Focus Indicator Validation
  - Contrast ratio: 3.2:1 ✓
  - Visibility check passed
- Color contrast → Task 6: Color Contrast Validation
  - All text: 4.8:1 (WCAG AA ✓)
  - UI components: 3.5:1 ✓
  - Violations: None

**Token Adherence Tab** → Task 7: Token Adherence Meter
- Overall score: 94% ✓ (target: ≥90%)
- By category:
  - Colors: 96% (23/24 matches)
  - Typography: 95% (19/20 matches)
  - Spacing: 91% (21/23 matches)
- Violations list with expected vs actual
- ΔE tolerance visualization (≤2.0)

**Quality Report** → Task 9: Quality Report Generation
- Downloadable HTML/JSON report
- All metrics and details
- Timestamp and component metadata
- Recommendations for improvements

**Auto-Fix Summary** → Task 8: Auto-Fix & Retry Logic
- Issues automatically fixed: 3
  - Removed unused import (React)
  - Added aria-label to icon button
  - Formatted with Prettier
- Retry validation: Passed ✓
- Manual fixes needed: 0

**Action Buttons**
- "Download Report" (HTML/JSON)
- "Accept & Export Component"
- "Fix Issues Manually" (if validation failed)
- "Regenerate Component" (if major issues)

### User Flow
1. Validation starts automatically after code generation
2. Progress bar shows real-time validation stages
3. Auto-fix attempts to resolve common issues
4. Validation retries after auto-fixes
5. Quality scorecard displays overall status
6. User reviews detailed results by category
7. User downloads quality report
8. User accepts component (if PASS) or fixes issues (if FAIL)

**Validation Requirements:**
- **Blockers** (must pass):
  - TypeScript compilation
  - 0 critical/serious a11y violations
  - Token adherence ≥90%
- **Warnings** (allow but flag):
  - ESLint warnings
  - Moderate a11y issues
  - Minor token deviations

**Performance Display:**
- Validation latency (target: <10s)
- Auto-fix success rate (target: ≥80%)

**Quick Test:**
```bash
# View wireframe locally
open .claude/wireframes/component-preview-page.html
```

---

## Tasks

**IMPORTANT UPDATE (2025-01-XX)**: Tasks 1-3 have been updated with correct architecture. Tasks 4-9 still contain old Python-based code examples and need updates:

**Tasks Requiring Updates:**
- **Task 4**: Keyboard Navigation - Change from Python/Playwright to TypeScript/Playwright
- **Task 5**: Focus Indicator - Change from Python to TypeScript, use Playwright getComputedStyle
- **Task 6**: Color Contrast - Remove Python `colour` library, use TypeScript color math
- **Task 7**: Token Adherence - Change to frontend TypeScript implementation
- **Task 8**: Auto-Fix Logic - Update to use frontend validators (already partially in Tasks 1-3)
- **Task 9**: Quality Report - Update to frontend report generation or backend API approach

**Key Changes Needed:**
- Replace `backend/src/validation/*.py` with `app/src/services/validation/*.ts`
- Remove all `asyncio.create_subprocess_exec()` calls to `tsc`, `eslint`, `npx`
- Remove Python `playwright.async_api` imports, use `@playwright/test`
- Remove `colour` library (doesn't exist), use `colormath` or custom WCAG formulas
- Update file paths from `backend/` to `app/src/`
- Change all code examples from Python to TypeScript

---

### Task 1: TypeScript Compilation Check (✓ UPDATED)
**Acceptance Criteria**:
- [ ] Create frontend validation service at `app/src/services/validation/typescript-validator.ts`
- [ ] Write generated component to temp file in `app/.tmp/` directory
- [ ] Run TypeScript compiler programmatically using `ts.createProgram` API
- [ ] Use strict mode configuration from existing `app/tsconfig.json`:
  - `strict: true`
  - `noImplicitAny: true`
  - `strictNullChecks: true`
  - `noUnusedLocals: true`
  - `noUnusedParameters: true`
- [ ] Capture compilation diagnostics with line numbers and categories
- [ ] Parse error messages for actionable feedback
- [ ] Return detailed error report if compilation fails
- [ ] Auto-fix: Remove unused imports, add missing type annotations (using AST manipulation)
- [ ] Retry compilation after auto-fix
- [ ] Block component delivery if compilation fails after retry
- [ ] Backend API: `POST /api/v1/validation/typescript` receives validation results

**Files**:
- `app/src/services/validation/typescript-validator.ts` (NEW)
- `app/src/services/validation/types.ts` (NEW - shared validation types)
- `backend/src/api/v1/routes/validation.py` (NEW - validation result storage)
- `app/tsconfig.json` (EXISTING - already has strict mode)

**TypeScript Validation**:
```typescript
// app/src/services/validation/typescript-validator.ts
import * as ts from 'typescript';
import * as fs from 'fs';
import * as path from 'path';
import type { ValidationResult, TypeScriptDiagnostic } from './types';

export class TypeScriptValidator {
  private configPath: string;
  private compilerOptions: ts.CompilerOptions;

  constructor(configPath: string = './tsconfig.json') {
    this.configPath = configPath;

    // Load compiler options from tsconfig.json
    const configFile = ts.readConfigFile(configPath, ts.sys.readFile);
    const parsedConfig = ts.parseJsonConfigFileContent(
      configFile.config,
      ts.sys,
      path.dirname(configPath)
    );
    this.compilerOptions = parsedConfig.options;
  }

  async validate(code: string, fileName: string = 'Component.tsx'): Promise<ValidationResult> {
    // Write code to temporary file
    const tmpDir = path.join(process.cwd(), '.tmp');
    if (!fs.existsSync(tmpDir)) {
      fs.mkdirSync(tmpDir, { recursive: true });
    }

    const tmpFilePath = path.join(tmpDir, fileName);
    fs.writeFileSync(tmpFilePath, code, 'utf-8');

    // Create program and get diagnostics
    const program = ts.createProgram([tmpFilePath], this.compilerOptions);
    const diagnostics = ts.getPreEmitDiagnostics(program);

    if (diagnostics.length === 0) {
      // Clean up
      fs.unlinkSync(tmpFilePath);
      return {
        valid: true,
        errors: [],
        warnings: []
      };
    }

    // Parse diagnostics
    const errors = this.parseDiagnostics(diagnostics);

    // Attempt auto-fix
    const fixedCode = this.autoFix(code, errors);
    if (fixedCode !== code) {
      // Retry validation with fixed code
      fs.writeFileSync(tmpFilePath, fixedCode, 'utf-8');
      const retryProgram = ts.createProgram([tmpFilePath], this.compilerOptions);
      const retryDiagnostics = ts.getPreEmitDiagnostics(retryProgram);

      if (retryDiagnostics.length === 0) {
        fs.unlinkSync(tmpFilePath);
        return {
          valid: true,
          errors: [],
          warnings: [],
          autoFixed: true,
          fixedCode
        };
      }
    }

    // Clean up
    fs.unlinkSync(tmpFilePath);

    return {
      valid: false,
      errors,
      warnings: [],
      autoFixAttempted: true
    };
  }

  private parseDiagnostics(diagnostics: readonly ts.Diagnostic[]): TypeScriptDiagnostic[] {
    return diagnostics.map(diagnostic => {
      const message = ts.flattenDiagnosticMessageText(diagnostic.messageText, '\n');
      let line = 0;
      let column = 0;

      if (diagnostic.file && diagnostic.start !== undefined) {
        const { line: lineNum, character } = diagnostic.file.getLineAndCharacterOfPosition(
          diagnostic.start
        );
        line = lineNum + 1;
        column = character + 1;
      }

      return {
        code: `TS${diagnostic.code}`,
        message,
        line,
        column,
        category: ts.DiagnosticCategory[diagnostic.category].toLowerCase() as 'error' | 'warning'
      };
    });
  }

  private autoFix(code: string, errors: TypeScriptDiagnostic[]): string {
    let fixedCode = code;

    // Remove unused imports
    if (errors.some(e => e.message.includes('is declared but never used'))) {
      fixedCode = this.removeUnusedImports(fixedCode);
    }

    // Add missing React import for JSX
    if (errors.some(e => e.message.includes("'React' refers to a UMD global"))) {
      if (!fixedCode.includes("import React from 'react'")) {
        fixedCode = "import React from 'react';\n" + fixedCode;
      }
    }

    return fixedCode;
  }

  private removeUnusedImports(code: string): string {
    // Simple regex-based removal (can be enhanced with AST manipulation)
    const lines = code.split('\n');
    return lines.filter(line => {
      // Keep non-import lines
      if (!line.trim().startsWith('import')) return true;
      // This is simplified - real implementation should use TS AST
      return true;
    }).join('\n');
  }
}
```

**Tests**:
- Valid TypeScript compiles successfully
- Compilation errors detected correctly
- Auto-fix removes unused imports
- Auto-fix adds type annotations
- Retry logic works

---

### Task 2: ESLint & Prettier Validation (✓ UPDATED)
**Acceptance Criteria**:
- [ ] Create frontend validation service at `app/src/services/validation/eslint-validator.ts`
- [ ] Use ESLint programmatically via `eslint` package (already in `app/package.json`)
- [ ] Use existing ESLint config from `app/eslint.config.mjs`
- [ ] Check code formatting with Prettier programmatically
- [ ] Report errors by severity (error, warning)
- [ ] Auto-fix: Apply ESLint fixes and Prettier formatting
- [ ] Retry validation after auto-fix
- [ ] Allow warnings but block on errors
- [ ] Generate formatted code output

**Files**:
- `app/src/services/validation/eslint-validator.ts` (NEW)
- `app/eslint.config.mjs` (EXISTING - already has Next.js config)
- `app/.prettierrc` (EXISTING or create if needed)

**ESLint Validation**:
```typescript
// app/src/services/validation/eslint-validator.ts
import { ESLint } from 'eslint';
import prettier from 'prettier';
import * as fs from 'fs';
import * as path from 'path';
import type { ValidationResult, LintMessage } from './types';

export class ESLintValidator {
  private eslint: ESLint;

  constructor() {
    this.eslint = new ESLint({
      fix: false, // We'll handle fixes separately
      useEslintrc: true, // Use project's eslint.config.mjs
    });
  }

  async validate(code: string, fileName: string = 'Component.tsx'): Promise<ValidationResult> {
    // Write code to temp file
    const tmpDir = path.join(process.cwd(), '.tmp');
    if (!fs.existsSync(tmpDir)) {
      fs.mkdirSync(tmpDir, { recursive: true });
    }

    const tmpFilePath = path.join(tmpDir, fileName);
    fs.writeFileSync(tmpFilePath, code, 'utf-8');

    try {
      // Run ESLint
      const results = await this.eslint.lintFiles([tmpFilePath]);
      const result = results[0];

      if (!result) {
        return { valid: true, errors: [], warnings: [] };
      }

      const errors = result.messages.filter(m => m.severity === 2);
      const warnings = result.messages.filter(m => m.severity === 1);

      // If there are errors, attempt auto-fix
      if (errors.length > 0) {
        const fixedCode = await this.autoFix(code, tmpFilePath);

        if (fixedCode !== code) {
          // Retry validation with fixed code
          fs.writeFileSync(tmpFilePath, fixedCode, 'utf-8');
          const retryResults = await this.eslint.lintFiles([tmpFilePath]);
          const retryResult = retryResults[0];

          const retryErrors = retryResult.messages.filter(m => m.severity === 2);
          const retryWarnings = retryResult.messages.filter(m => m.severity === 1);

          if (retryErrors.length === 0) {
            return {
              valid: true,
              errors: [],
              warnings: retryWarnings.map(this.formatMessage),
              autoFixed: true,
              fixedCode
            };
          }

          return {
            valid: false,
            errors: retryErrors.map(this.formatMessage),
            warnings: retryWarnings.map(this.formatMessage),
            autoFixAttempted: true
          };
        }
      }

      return {
        valid: errors.length === 0,
        errors: errors.map(this.formatMessage),
        warnings: warnings.map(this.formatMessage)
      };
    } finally {
      // Clean up
      if (fs.existsSync(tmpFilePath)) {
        fs.unlinkSync(tmpFilePath);
      }
    }
  }

  private async autoFix(code: string, filePath: string): Promise<string> {
    // Apply ESLint fixes
    const eslintWithFix = new ESLint({ fix: true, useEslintrc: true });
    const results = await eslintWithFix.lintFiles([filePath]);
    await ESLint.outputFixes(results);

    // Apply Prettier formatting
    const formatted = await prettier.format(code, {
      parser: 'typescript',
      filepath: filePath
    });

    return formatted;
  }

  private formatMessage(message: any): LintMessage {
    return {
      line: message.line,
      column: message.column,
      message: message.message,
      ruleId: message.ruleId || '',
      severity: message.severity === 2 ? 'error' : 'warning'
    };
  }
}
```

**Tests**:
- ESLint detects errors correctly
- ESLint auto-fix resolves issues
- Prettier formatting works
- Auto-fix and retry logic correct

---

### Task 3: axe-core Accessibility Testing (✓ UPDATED)
**Acceptance Criteria**:
- [ ] Create `app/src/services/validation/a11y-validator.ts` using Playwright (already in `app/package.json`)
- [ ] Leverage existing `@axe-core/react` (already in `app/package.json`)
- [ ] Render component in headless browser using Playwright
- [ ] Run axe-core accessibility audit
- [ ] Test all component variants and states
- [ ] Report violations by severity:
  - Critical (0 allowed)
  - Serious (0 allowed)
  - Moderate (warn only)
  - Minor (warn only)
- [ ] Capture violation details:
  - Rule ID (e.g., `button-name`, `color-contrast`)
  - Impact level
  - Element selector
  - Fix suggestions from axe
- [ ] Block component delivery on critical/serious violations
- [ ] Generate accessibility report with remediation steps

**Files**:
- `app/src/services/validation/a11y-validator.ts` (NEW)
- `app/package.json` (EXISTING - has @axe-core/react, @playwright/test)

**axe-core Validation**:
```typescript
// app/src/services/validation/a11y-validator.ts
import { chromium, Browser, Page } from 'playwright';
import type { Result as AxeResults } from 'axe-core';
import type { ValidationResult, A11yViolation } from './types';

export class A11yValidator {
  private browser: Browser | null = null;

  async validate(
    componentCode: string,
    componentName: string,
    variants: string[] = ['default']
  ): Promise<ValidationResult> {
    try {
      this.browser = await chromium.launch({ headless: true });
      const page = await this.browser.newPage();

      // Create test page with component
      const html = this.createTestPage(componentCode, componentName, variants);
      await page.setContent(html);

      // Wait for React to render
      await page.waitForSelector('#root > *', { timeout: 5000 });

      // Inject axe-core
      await page.addScriptTag({
        url: 'https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.0/axe.min.js'
      });

      // Run axe accessibility tests
      const results = await page.evaluate(() => {
        return (window as any).axe.run();
      }) as AxeResults;

      await this.browser.close();
      this.browser = null;

      return this.processResults(results);
    } catch (error) {
      if (this.browser) {
        await this.browser.close();
      }
      throw error;
    }
  }

  private createTestPage(
    componentCode: string,
    componentName: string,
    variants: string[]
  ): string {
    return `
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>A11y Test - ${componentName}</title>
  <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
  <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
</head>
<body>
  <div id="root"></div>
  <script type="module">
    ${componentCode}

    // Render component variants for testing
    const container = document.getElementById('root');
    const root = ReactDOM.createRoot(container);

    root.render(
      React.createElement('div', null, [
        ${variants.map(variant => `
          React.createElement(${componentName}, {
            key: '${variant}',
            variant: '${variant}',
            children: '${variant} variant'
          })
        `).join(',\n')}
      ])
    );
  </script>
</body>
</html>
    `;
  }

  private processResults(results: AxeResults): ValidationResult {
    const violations = results.violations || [];

    const critical = violations.filter(v => v.impact === 'critical');
    const serious = violations.filter(v => v.impact === 'serious');
    const moderate = violations.filter(v => v.impact === 'moderate');
    const minor = violations.filter(v => v.impact === 'minor');

    const errors: A11yViolation[] = [
      ...this.formatViolations(critical, 'critical'),
      ...this.formatViolations(serious, 'serious')
    ];

    const warnings: A11yViolation[] = [
      ...this.formatViolations(moderate, 'moderate'),
      ...this.formatViolations(minor, 'minor')
    ];

    return {
      valid: errors.length === 0, // Block on critical/serious only
      errors,
      warnings,
      summary: {
        critical: critical.length,
        serious: serious.length,
        moderate: moderate.length,
        minor: minor.length,
        total: violations.length
      }
    };
  }

  private formatViolations(violations: any[], severity: string): A11yViolation[] {
    return violations.map(v => ({
      id: v.id,
      impact: v.impact,
      description: v.description,
      help: v.help,
      helpUrl: v.helpUrl,
      nodes: v.nodes.map((n: any) => ({
        html: n.html,
        target: n.target,
        failureSummary: n.failureSummary
      })),
      severity
    }));
  }
}
```

**Tests**:
- axe-core detects violations
- Critical violations block delivery
- All variants tested
- Report format correct

---

### Task 4: Keyboard Navigation Testing
**Acceptance Criteria**:
- [ ] Test Tab key navigation through interactive elements
- [ ] Verify correct tab order
- [ ] Test Enter/Space activation for buttons
- [ ] Test Escape key for dismissible components
- [ ] Test Arrow keys for navigation (tabs, select, etc.)
- [ ] Verify focus trap for modals
- [ ] Test skip links if present
- [ ] Ensure no keyboard traps
- [ ] Report keyboard navigation issues

**Files**:
- `backend/src/validation/keyboard_validator.py`

**Keyboard Testing**:
```python
class KeyboardValidator:
    async def validate(self, component_code: str,
                      component_name: str,
                      component_type: str) -> dict:
        """Test keyboard navigation."""
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            html = self._create_test_page(component_code, component_name)
            await page.set_content(html)

            issues = []

            # Test Tab navigation
            tab_issues = await self._test_tab_navigation(page, component_type)
            issues.extend(tab_issues)

            # Test activation keys (Enter/Space)
            if component_type in ['button', 'link']:
                activation_issues = await self._test_activation(page)
                issues.extend(activation_issues)

            await browser.close()

            return {
                "valid": len(issues) == 0,
                "issues": issues
            }

    async def _test_tab_navigation(self, page, component_type: str):
        """Test Tab key navigation."""
        issues = []

        # Press Tab
        await page.keyboard.press('Tab')

        # Check if component received focus
        focused = await page.evaluate('document.activeElement.tagName')

        if component_type == 'button' and focused != 'BUTTON':
            issues.append({
                "type": "tab_navigation",
                "message": "Button not focusable with Tab key",
                "severity": "critical"
            })

        return issues

    async def _test_activation(self, page):
        """Test Enter/Space activation."""
        issues = []

        # Setup click listener
        await page.evaluate('''
            window.clicked = false;
            document.activeElement.addEventListener('click', () => {
                window.clicked = true;
            });
        ''')

        # Press Enter
        await page.keyboard.press('Enter')
        clicked = await page.evaluate('window.clicked')

        if not clicked:
            issues.append({
                "type": "keyboard_activation",
                "message": "Element not activated by Enter key",
                "severity": "serious"
            })

        return issues
```

**Tests**:
- Tab navigation works correctly
- Enter/Space activates elements
- Keyboard traps detected
- Focus order validated

---

### Task 5: Focus Indicator Validation
**Acceptance Criteria**:
- [ ] Verify focus indicator is visible
- [ ] Check focus indicator contrast (≥3:1 against background)
- [ ] Test focus indicator on all interactive elements
- [ ] Verify focus-visible styles applied
- [ ] Check focus indicator is not removed with `outline: none`
- [ ] Ensure custom focus styles meet WCAG standards
- [ ] Test focus indicator in different states (hover, active)
- [ ] Report missing or insufficient focus indicators

**Files**:
- `backend/src/validation/focus_validator.py`

**Focus Indicator Testing**:
```python
class FocusValidator:
    async def validate(self, component_code: str,
                      component_name: str) -> dict:
        """Validate focus indicators."""
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()

            html = self._create_test_page(component_code, component_name)
            await page.set_content(html)

            # Focus element
            await page.keyboard.press('Tab')

            # Get computed styles
            styles = await page.evaluate('''
                () => {
                    const el = document.activeElement;
                    const computed = window.getComputedStyle(el);
                    return {
                        outline: computed.outline,
                        outlineWidth: computed.outlineWidth,
                        outlineColor: computed.outlineColor,
                        boxShadow: computed.boxShadow
                    };
                }
            ''')

            # Check for focus indicator
            has_indicator = (
                styles['outlineWidth'] != '0px' or
                'ring' in styles['boxShadow']
            )

            issues = []
            if not has_indicator:
                issues.append({
                    "type": "missing_focus_indicator",
                    "message": "No visible focus indicator detected",
                    "severity": "critical"
                })

            # Check contrast if indicator present
            if has_indicator:
                contrast_issues = await self._check_focus_contrast(page)
                issues.extend(contrast_issues)

            await browser.close()

            return {
                "valid": len(issues) == 0,
                "issues": issues,
                "styles": styles
            }

    async def _check_focus_contrast(self, page):
        """Check focus indicator contrast ratio."""
        # Get colors and calculate contrast
        # Implementation depends on color parsing library
        pass
```

**Tests**:
- Focus indicators detected
- Contrast ratio calculated correctly
- Missing indicators reported
- Custom focus styles validated

---

### Task 6: Color Contrast Validation
**Acceptance Criteria**:
- [ ] Extract all text and UI element colors from component
- [ ] Calculate contrast ratios using WCAG formula
- [ ] Validate against WCAG AA standards:
  - Normal text: ≥4.5:1
  - Large text (≥18pt or 14pt bold): ≥3:1
  - UI components: ≥3:1
- [ ] Test contrast in all states (default, hover, focus, disabled)
- [ ] Report violations with actual vs required ratios
- [ ] Suggest alternative colors that meet standards
- [ ] Auto-fix: Adjust colors to meet minimum contrast

**Files**:
- `backend/src/validation/contrast_validator.py`

**Contrast Validation**:
```python
from colour import Color
import math

class ContrastValidator:
    def validate(self, component_code: str, tokens: dict) -> dict:
        """Validate color contrast ratios."""
        violations = []

        # Extract color pairs from component
        color_pairs = self._extract_color_pairs(component_code, tokens)

        for pair in color_pairs:
            ratio = self._calculate_contrast_ratio(
                pair['foreground'],
                pair['background']
            )

            required_ratio = self._get_required_ratio(pair['context'])

            if ratio < required_ratio:
                violations.append({
                    "type": "insufficient_contrast",
                    "element": pair['element'],
                    "foreground": pair['foreground'],
                    "background": pair['background'],
                    "actual_ratio": round(ratio, 2),
                    "required_ratio": required_ratio,
                    "severity": "critical" if ratio < 3.0 else "serious"
                })

        return {
            "valid": len(violations) == 0,
            "violations": violations
        }

    def _calculate_contrast_ratio(self, fg: str, bg: str) -> float:
        """Calculate WCAG contrast ratio."""
        fg_color = Color(fg)
        bg_color = Color(bg)

        fg_luminance = self._get_relative_luminance(fg_color)
        bg_luminance = self._get_relative_luminance(bg_color)

        lighter = max(fg_luminance, bg_luminance)
        darker = min(fg_luminance, bg_luminance)

        return (lighter + 0.05) / (darker + 0.05)

    def _get_relative_luminance(self, color: Color) -> float:
        """Calculate relative luminance."""
        r, g, b = color.rgb

        def adjust(c):
            if c <= 0.03928:
                return c / 12.92
            return ((c + 0.055) / 1.055) ** 2.4

        r = adjust(r)
        g = adjust(g)
        b = adjust(b)

        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    def _get_required_ratio(self, context: str) -> float:
        """Get required contrast ratio for context."""
        if context == 'large_text':
            return 3.0
        elif context == 'ui_component':
            return 3.0
        else:  # normal_text
            return 4.5

    def _extract_color_pairs(self, code: str, tokens: dict):
        """Extract foreground/background color pairs from code."""
        # Parse code to find text elements and their colors
        pairs = []
        # Implementation depends on AST parsing
        return pairs
```

**Tests**:
- Contrast ratios calculated correctly
- WCAG standards enforced
- Violations detected accurately
- Auto-fix suggestions valid

---

### Task 7: Token Adherence Meter
**Acceptance Criteria**:
- [ ] Compare generated component against approved tokens
- [ ] Check token usage for:
  - Colors (all color values)
  - Typography (font family, sizes, weights)
  - Spacing (padding, margin, gap values)
- [ ] Calculate adherence percentage per category
- [ ] Calculate overall adherence score (≥90% target)
- [ ] Report non-compliant values with expected vs actual
- [ ] Generate visual adherence report
- [ ] Allow tolerance for minor variations (ΔE ≤2 for colors)

**Files**:
- `backend/src/validation/token_validator.py`

**Token Adherence**:
```python
class TokenValidator:
    def validate(self, component_code: str, approved_tokens: dict) -> dict:
        """Calculate token adherence."""
        # Extract tokens from generated code
        used_tokens = self._extract_used_tokens(component_code)

        adherence = {
            "colors": self._check_color_adherence(
                used_tokens.get("colors", {}),
                approved_tokens.get("colors", {})
            ),
            "typography": self._check_typography_adherence(
                used_tokens.get("typography", {}),
                approved_tokens.get("typography", {})
            ),
            "spacing": self._check_spacing_adherence(
                used_tokens.get("spacing", {}),
                approved_tokens.get("spacing", {})
            )
        }

        # Calculate overall score
        scores = [cat["score"] for cat in adherence.values()]
        overall_score = sum(scores) / len(scores) if scores else 0

        return {
            "valid": overall_score >= 0.90,
            "overall_score": overall_score,
            "adherence": adherence,
            "violations": self._collect_violations(adherence)
        }

    def _check_color_adherence(self, used: dict, approved: dict) -> dict:
        """Check color token adherence."""
        matches = 0
        total = len(used)

        violations = []
        for name, used_value in used.items():
            approved_value = approved.get(name)
            if not approved_value:
                violations.append({
                    "token": name,
                    "issue": "not_in_approved_tokens",
                    "used": used_value
                })
                continue

            # Calculate color difference (ΔE)
            delta_e = self._calculate_delta_e(used_value, approved_value)

            if delta_e <= 2.0:  # Tolerance
                matches += 1
            else:
                violations.append({
                    "token": name,
                    "issue": "color_mismatch",
                    "used": used_value,
                    "approved": approved_value,
                    "delta_e": round(delta_e, 2)
                })

        return {
            "score": matches / total if total > 0 else 1.0,
            "matches": matches,
            "total": total,
            "violations": violations
        }

    def _calculate_delta_e(self, color1: str, color2: str) -> float:
        """Calculate ΔE color difference (CIEDE2000)."""
        # Use colour library for ΔE calculation
        from colour import delta_E
        return delta_E(color1, color2, method='CIE 2000')

    def _extract_used_tokens(self, code: str) -> dict:
        """Extract token values from generated code."""
        # Parse CSS variables and inline values
        # Implementation depends on CSS parser
        return {}
```

**Tests**:
- Token extraction correct
- Adherence calculated accurately
- ΔE tolerance works
- Overall score matches expectations

---

### Task 8: Auto-Fix & Retry Logic
**Acceptance Criteria**:
- [ ] Implement auto-fix for common issues:
  - TypeScript: Remove unused imports, add type annotations
  - ESLint: Run `eslint --fix`
  - Prettier: Run `prettier --write`
  - Accessibility: Add missing ARIA labels
  - Contrast: Adjust colors to meet minimum ratios
- [ ] Retry validation after auto-fix (one attempt)
- [ ] Track which issues were auto-fixed
- [ ] Report auto-fix success rate
- [ ] Generate diff showing changes
- [ ] Provide manual fix suggestions for unfixable issues
- [ ] Target: 80%+ auto-fix success rate

**Files**:
- `backend/src/validation/auto_fixer.py`

**Auto-Fix Logic**:
```python
class AutoFixer:
    async def fix_and_retry(self, code: str,
                           validation_result: dict) -> dict:
        """Attempt to auto-fix issues and retry validation."""
        fixed_code = code
        fixes_applied = []

        # Fix TypeScript issues
        if not validation_result.get("typescript", {}).get("valid"):
            fixed_code, ts_fixes = await self._fix_typescript(
                fixed_code,
                validation_result["typescript"]["errors"]
            )
            fixes_applied.extend(ts_fixes)

        # Fix ESLint issues
        if not validation_result.get("eslint", {}).get("valid"):
            fixed_code, lint_fixes = await self._fix_eslint(fixed_code)
            fixes_applied.extend(lint_fixes)

        # Format with Prettier
        fixed_code = await self._format_prettier(fixed_code)
        fixes_applied.append("prettier_format")

        # Fix accessibility issues
        if validation_result.get("a11y", {}).get("violations"):
            fixed_code, a11y_fixes = await self._fix_a11y(
                fixed_code,
                validation_result["a11y"]["violations"]
            )
            fixes_applied.extend(a11y_fixes)

        # Retry validation
        retry_result = await self.validator.validate_all(fixed_code)

        return {
            "fixed_code": fixed_code,
            "fixes_applied": fixes_applied,
            "retry_result": retry_result,
            "success": retry_result["valid"]
        }

    async def _fix_a11y(self, code: str, violations: dict) -> tuple[str, list]:
        """Fix accessibility violations."""
        fixes = []

        # Add missing aria-labels
        for violation in violations.get("critical", []):
            if violation["id"] == "button-name":
                # Add aria-label to buttons without text
                code = self._add_aria_label(code, violation)
                fixes.append("add_aria_label")

        return code, fixes
```

**Tests**:
- Auto-fix resolves common issues
- Retry validation works
- Fixes tracked correctly
- Success rate measured

---

### Task 9: Quality Report Generation
**Acceptance Criteria**:
- [ ] Generate comprehensive quality report with:
  - Overall pass/fail status
  - TypeScript compilation result
  - ESLint/Prettier results
  - Accessibility audit summary
  - Keyboard navigation results
  - Focus indicator validation
  - Color contrast results
  - Token adherence score
  - Auto-fix summary
- [ ] Include visualizations (charts, badges)
- [ ] Export report in JSON and HTML formats
- [ ] Store report in S3
- [ ] Display report in UI
- [ ] Track quality metrics over time

**Files**:
- `backend/src/validation/report_generator.py`

**Report Generation**:
```python
class QualityReportGenerator:
    def generate(self, validation_results: dict) -> dict:
        """Generate quality report."""
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "overall_status": self._determine_status(validation_results),
            "summary": {
                "typescript": validation_results["typescript"]["valid"],
                "eslint": validation_results["eslint"]["valid"],
                "accessibility": validation_results["a11y"]["valid"],
                "keyboard": validation_results["keyboard"]["valid"],
                "focus": validation_results["focus"]["valid"],
                "contrast": validation_results["contrast"]["valid"],
                "token_adherence": validation_results["tokens"]["overall_score"]
            },
            "details": validation_results,
            "auto_fixes": validation_results.get("auto_fixes", []),
            "recommendations": self._generate_recommendations(validation_results)
        }

        # Generate HTML report
        html_report = self._generate_html(report)

        return {
            "json": report,
            "html": html_report
        }

    def _determine_status(self, results: dict) -> str:
        """Determine overall pass/fail status."""
        critical_checks = [
            results["typescript"]["valid"],
            results["eslint"]["valid"],
            results["a11y"]["valid"]
        ]

        if all(critical_checks) and results["tokens"]["overall_score"] >= 0.90:
            return "PASS"
        else:
            return "FAIL"

    def _generate_html(self, report: dict) -> str:
        """Generate HTML quality report."""
        # Use Jinja2 template
        pass
```

**Tests**:
- Reports generated correctly
- JSON and HTML formats valid
- Status determination correct
- Metrics tracked over time

---

## Dependencies

**Requires**:
- Epic 4: Generated components to validate

**Blocks**:
- Component delivery (cannot ship without validation)

---

## Technical Architecture

### Validation Pipeline (Updated Architecture)

```
Epic 4: Code Generation (Backend)
         ↓
   Generated Code
         ↓
┌─────────────────────────────────────────────────┐
│       Frontend Validation Service               │
│    (app/src/services/validation/)               │
│                                                  │
│  ┌──────────────────────────────────────┐      │
│  │ TypeScript Compiler API              │ ✓    │
│  │ (ts.createProgram)                   │      │
│  └──────────────────────────────────────┘      │
│           ↓                                      │
│  ┌──────────────────────────────────────┐      │
│  │ ESLint API + Prettier                │ ✓    │
│  │ (existing app/eslint.config.mjs)     │      │
│  └──────────────────────────────────────┘      │
│           ↓                                      │
│  ┌──────────────────────────────────────┐      │
│  │ Playwright + axe-core                │ ✓    │
│  │ (existing @playwright/test)          │      │
│  └──────────────────────────────────────┘      │
│           ↓                                      │
│  ┌──────────────────────────────────────┐      │
│  │ Keyboard Navigation Tests            │      │
│  │ (Playwright page.keyboard)           │      │
│  └──────────────────────────────────────┘      │
│           ↓                                      │
│  ┌──────────────────────────────────────┐      │
│  │ Focus & Contrast Validators          │      │
│  │ (getComputedStyle + WCAG formulas)   │      │
│  └──────────────────────────────────────┘      │
│           ↓                                      │
│  ┌──────────────────────────────────────┐      │
│  │ Token Adherence Calculator           │      │
│  │ (AST parsing + color math)           │      │
│  └──────────────────────────────────────┘      │
└─────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────┐
│  Backend Validation API (Optional)               │
│  POST /api/v1/validation/results                 │
│  - Store validation results                      │
│  - Generate quality reports                      │
│  - Track metrics over time                       │
└─────────────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────────────┐
│  Frontend Validation Results UI                  │
│  - Quality scorecard display                     │
│  - Detailed validation tabs                      │
│  - Download reports (JSON/HTML)                  │
│  - Accept/Reject component                       │
└─────────────────────────────────────────────────┘
```

**Key Architectural Decisions:**

1. **Frontend-First Validation**: All validation runs in the frontend using existing Node.js tooling (TypeScript, ESLint, Prettier, Playwright). No Python subprocess calls to `tsc`/`npx`.

2. **Existing Dependencies**: Leverages packages already in `app/package.json`:
   - `typescript` (5.9.3)
   - `eslint` (^9)
   - `@playwright/test` (^1.55.1)
   - `@axe-core/react` (^4.10.2)

3. **Backend Role**: Backend provides:
   - Validation result storage API
   - Quality report generation
   - Historical metrics tracking
   - S3 upload for reports (Epic 6)

4. **No Python-to-Node.js Bridge**: Validation does not require backend to spawn Node.js processes.

---

## Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| **Critical A11y Violations** | 0 | axe-core audit |
| **Serious A11y Violations** | 0 | axe-core audit |
| **TypeScript Compilation** | 100% pass | tsc --noEmit |
| **Token Adherence** | ≥90% | Token validator |
| **Auto-Fix Success Rate** | ≥80% | Fixes resolved / Total issues |
| **Validation Latency** | <10s | Total validation time |

---

## Risks & Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Validation too slow (>10s) | Medium | Parallelize checks, optimize AST operations |
| Auto-fix breaks code | High | Validate after fix, provide manual override |
| False positives in a11y tests | Low | Manual review, adjust rules |
| Token adherence too strict | Low | Allow configurable tolerance |

---

## Definition of Done

- [ ] All 9 tasks completed with acceptance criteria met
- [ ] TypeScript validation works correctly
- [ ] ESLint and Prettier validation functional
- [ ] axe-core testing detects violations
- [ ] Keyboard navigation tested
- [ ] Focus indicators validated
- [ ] Color contrast checked (WCAG AA)
- [ ] Token adherence meter implemented (≥90%)
- [ ] Auto-fix resolves 80%+ of issues
- [ ] Quality reports generated
- [ ] Validation completes in <10s
- [ ] Integration tests passing
- [ ] Documentation updated

---

## Related Epics

- **Depends On**: Epic 4
- **Blocks**: Component delivery
- **Related**: Epic 8 (regeneration uses same validation)

---

## Notes

**Zero Tolerance**: Critical accessibility violations are non-negotiable. No component ships without passing.

**Auto-Fix**: Focus on high-impact, low-risk fixes. Don't break working code trying to fix minor issues.

**Performance**: 10s validation target is tight. Parallelize checks where possible.

---

## Implementation Summary (2025-01-XX Update)

### What Changed
Epic 5 has been **architecturally updated** to align with the actual codebase after completing Epics 1-4:

**Original Plan (Incorrect)**:
- ❌ Backend Python validators in `backend/src/validation/`
- ❌ Python subprocess calls to `tsc`, `eslint`, `prettier`, `npx`
- ❌ Python Playwright (`playwright.async_api`)
- ❌ Non-existent `colour` library
- ❌ Backend running Node.js tooling

**Updated Plan (Correct)**:
- ✅ Frontend TypeScript validators in `app/src/services/validation/`
- ✅ Use existing `typescript`, `eslint`, `@playwright/test` packages
- ✅ TypeScript Playwright API
- ✅ Proper color math libraries (`colormath` or custom WCAG formulas)
- ✅ Backend provides API endpoints for results storage only

### What's Completed
- ✅ Overview and architecture updated
- ✅ Task 1 (TypeScript validation) rewritten in TypeScript
- ✅ Task 2 (ESLint/Prettier validation) rewritten in TypeScript
- ✅ Task 3 (axe-core accessibility) rewritten in TypeScript
- ✅ Technical architecture diagram updated
- ✅ Key architectural decisions documented

### What Needs Completion
**Tasks 4-9 still contain Python code examples** and need similar updates:

1. **Task 4**: Keyboard Navigation Testing
   - Convert from Python to TypeScript
   - Use `@playwright/test` instead of `playwright.async_api`

2. **Task 5**: Focus Indicator Validation
   - Convert from Python to TypeScript
   - Use Playwright's `page.evaluate()` with `getComputedStyle`

3. **Task 6**: Color Contrast Validation
   - Remove Python `colour` library references
   - Implement WCAG contrast formulas in TypeScript
   - Use proper color parsing library

4. **Task 7**: Token Adherence Meter
   - Convert from Python to TypeScript
   - Frontend AST parsing or regex-based extraction
   - Color difference calculations (ΔE)

5. **Task 8**: Auto-Fix & Retry Logic
   - Partially done in Tasks 1-3
   - Consolidate auto-fix patterns
   - Add coordinator service

6. **Task 9**: Quality Report Generation
   - Choose between frontend or backend report generation
   - If frontend: Use React components
   - If backend: Create API endpoint for report storage
   - HTML template generation

### Dependencies Status
**No new dependencies needed!** All required packages are already in `app/package.json`:
- ✅ `typescript` (5.9.3)
- ✅ `eslint` (^9)
- ✅ `@playwright/test` (^1.55.1)
- ✅ `@axe-core/react` (^4.10.2)
- ✅ `prettier` (via eslint config)

**Optional additions for Tasks 6-7**:
- Color math library (e.g., `chroma-js`, `color`, or custom WCAG formulas)
- AST parsing (if needed beyond TypeScript Compiler API)

### Next Steps for Implementation
1. Complete remaining task code examples (Tasks 4-9)
2. Create shared types file: `app/src/services/validation/types.ts`
3. Create validation orchestrator service
4. Build frontend validation results UI
5. Add backend validation storage API (optional)
6. Integrate with Epic 4 generation flow
