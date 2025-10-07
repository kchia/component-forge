# Code Generation Module

## Overview

The code generation module transforms retrieved shadcn/ui patterns into production-ready React/TypeScript components by injecting design tokens, implementing requirements, and assembling formatted code.

## Architecture

```
Generation Pipeline Flow:
┌─────────────┐
│   Pattern   │ (from Epic 3: Pattern Retrieval)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Tokens     │ (from Epic 1: Design Token Extraction)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│Requirements │ (from Epic 2: Requirement Proposal)
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────────────────────┐
│              Code Generation Pipeline                    │
│                                                          │
│  1. Pattern Parser      → Extract structure             │
│  2. Token Injector      → Inject design tokens          │
│  3. Tailwind Generator  → Generate CSS classes          │
│  4. Requirement Impl.   → Add props, events, states     │
│  5. A11y Enhancer       → Add ARIA attributes           │
│  6. Type Generator      → Generate TypeScript types     │
│  7. Storybook Generator → Generate stories              │
│  8. Code Assembler      → Combine & format code         │
│                                                          │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
                  ┌────────────────┐
                  │Generated Code  │
                  │  - Component   │
                  │  - Stories     │
                  │  - Types       │
                  │  - Metadata    │
                  └────────────────┘
```

## Modules

### 1. Pattern Parser (`pattern_parser.py`)
- **Purpose**: Parse pattern JSON and extract component structure
- **Input**: Pattern JSON from pattern library
- **Output**: `PatternStructure` with component name, props, imports, variants
- **Performance**: <100ms per pattern

### 2. Token Injector (`token_injector.py`)
- **Purpose**: Inject design tokens into component styles
- **Input**: Pattern structure + design tokens
- **Output**: CSS variables and token mapping
- **Performance**: <50ms per component

### 3. Tailwind Generator (`tailwind_generator.py`)
- **Purpose**: Generate Tailwind CSS classes using design tokens
- **Input**: Component elements + tokens + variants
- **Output**: Tailwind class strings with CSS variables
- **Performance**: <30ms per element

### 4. Requirement Implementer (`requirement_implementer.py`)
- **Purpose**: Implement approved requirements in component
- **Input**: Pattern structure + requirements
- **Output**: Modified component with props, events, states
- **Performance**: <100ms per component

### 5. Provenance Generator (`provenance.py`)
- **Purpose**: Generate provenance headers for traceability
- **Input**: Pattern ID, tokens, requirements
- **Output**: Header comment with metadata, timestamps, SHA-256 hashes
- **Features**: ISO 8601 timestamps, content hashing, warning messages

### 6. Import Resolver (`import_resolver.py`)
- **Purpose**: Resolve and order imports correctly
- **Input**: List of import statements
- **Output**: Ordered imports (external, internal, utils, types)
- **Features**: Deduplication, missing import detection, package.json generation

### 7. A11y Enhancer (`a11y_enhancer.py`)
- **Purpose**: Add accessibility features to components
- **Input**: Component code and type
- **Output**: Enhanced code with ARIA attributes
- **Features**: Component-specific rules, keyboard support, focus indicators

### 8. Type Generator (`type_generator.py`)
- **Purpose**: Generate strict TypeScript types
- **Input**: Component code and props
- **Output**: TypeScript interfaces and type annotations
- **Features**: Zero `any` types, ref forwarding, JSDoc comments, variant unions

### 9. Storybook Generator (`storybook_generator.py`)
- **Purpose**: Generate Storybook stories in CSF 3.0 format
- **Input**: Component name, variants, props
- **Output**: Complete .stories.tsx file
- **Features**: Meta object, argTypes, variant stories, state stories

### 10. Code Assembler (`code_assembler.py`)
- **Purpose**: Assemble final component code and format with Prettier
- **Input**: All code parts (imports, CSS vars, types, component)
- **Output**: Formatted component.tsx and stories.tsx files
- **Performance**: <2s for formatting

### 11. Generator Service (`generator_service.py`)
- **Purpose**: Orchestrate the full generation pipeline
- **Input**: `GenerationRequest` (pattern_id, tokens, requirements)
- **Output**: `GenerationResult` with generated code and metadata
- **Performance**: p50 ≤60s, p95 ≤90s

## Usage

### Basic Generation

```python
from src.generation.generator_service import GeneratorService

# Initialize service
generator = GeneratorService()

# Generate component
result = await generator.generate(
    pattern_id="shadcn-button",
    tokens={
        "colors": {"primary": "#3B82F6"},
        "spacing": {"padding": "16px"}
    },
    requirements={
        "props": [{"name": "variant", "type": "string"}],
        "events": [{"name": "onClick"}]
    }
)

# Access generated code
print(result.component_code)  # Component.tsx
print(result.stories_code)    # Component.stories.tsx
print(result.metadata.latency_ms)  # Performance metrics
```

### Pipeline Stages

The generator service tracks each stage with LangSmith:

1. **PARSING** - Extract pattern structure
2. **INJECTING** - Inject design tokens
3. **GENERATING** - Generate Tailwind classes
4. **IMPLEMENTING** - Add requirements
5. **ENHANCING** - Add accessibility features
6. **TYPING** - Generate TypeScript types
7. **STORY_GENERATION** - Generate Storybook stories
8. **ASSEMBLING** - Combine code parts
9. **FORMATTING** - Format with Prettier
10. **COMPLETE** - Generation finished

### Generated Output

Each component generation produces:

1. **Component.tsx** - Main component file with:
   - Provenance header (pattern ID, timestamp, hashes)
   - Ordered imports (external, internal, utils, types)
   - TypeScript interfaces with strict types
   - Accessibility-enhanced component code
   - No `any` types

2. **Component.stories.tsx** - Storybook stories with:
   - CSF 3.0 format
   - Meta object with argTypes
   - Default story
   - Variant stories (Primary, Secondary, Ghost, etc.)
   - State stories (Disabled, Loading, Error)

3. **Component.tokens.css** - CSS variables file with:
   - Design token definitions
   - Component-specific variables

4. **Metadata** - Generation metadata with:
   - Total latency (ms)
   - Stage latencies
   - Token count
   - Lines of code
   - Requirements implemented

## Performance Targets

| Metric | Target | Current |
|--------|--------|---------|
| Total Latency (p50) | ≤60s | TBD |
| Total Latency (p95) | ≤90s | TBD |
| Pattern Parsing | <100ms | TBD |
| Token Injection | <50ms | TBD |
| Tailwind Generation | <30ms | TBD |
| Requirement Implementation | <100ms | TBD |
| Code Assembly | <2s | TBD |

## Testing

### Unit Tests
```bash
# Run all generation tests
pytest backend/tests/generation/ -v

# Run specific module tests
pytest backend/tests/generation/test_pattern_parser.py -v
pytest backend/tests/generation/test_token_injector.py -v
pytest backend/tests/generation/test_tailwind_generator.py -v

# Run polish enhancement tests
pytest backend/tests/generation/test_provenance.py -v
pytest backend/tests/generation/test_import_resolver.py -v
pytest backend/tests/generation/test_a11y_enhancer.py -v
pytest backend/tests/generation/test_type_generator.py -v
pytest backend/tests/generation/test_storybook_generator.py -v
```

### Integration Tests
```bash
# Run end-to-end generation tests
pytest backend/tests/generation/test_generator_service.py -v

# Run with coverage
pytest backend/tests/generation/ --cov=src.generation --cov-report=html

# Test polish enhancements with coverage
pytest backend/tests/generation/test_provenance.py \
       backend/tests/generation/test_import_resolver.py \
       backend/tests/generation/test_a11y_enhancer.py \
       backend/tests/generation/test_type_generator.py \
       backend/tests/generation/test_storybook_generator.py \
       --cov=src.generation --cov-report=term-missing
```

### Test Coverage

Current test coverage for polish enhancements:
- Provenance Generator: 100%
- Import Resolver: 98%
- A11y Enhancer: 95%
- Type Generator: 92%
- Storybook Generator: 100%

## Error Handling

The module uses structured error handling:

```python
class GenerationError(Exception):
    """Base exception for generation errors."""
    pass

class PatternParseError(GenerationError):
    """Failed to parse pattern."""
    pass

class TokenInjectionError(GenerationError):
    """Failed to inject tokens."""
    pass

class CodeAssemblyError(GenerationError):
    """Failed to assemble code."""
    pass
```

## LangSmith Tracing

All generation stages are traced with LangSmith for observability:

```python
from langsmith import traceable

@traceable(run_type="chain", name="generate_component")
async def generate(self, request: GenerationRequest) -> GenerationResult:
    # Each stage is traced
    pass
```

View traces at: https://smith.langchain.com/

## API Endpoint

The generation module is exposed via REST API:

```bash
# Generate component
POST /api/v1/generation/generate
{
  "pattern_id": "shadcn-button",
  "tokens": {...},
  "requirements": {...}
}

# Response
{
  "component_code": "...",
  "stories_code": "...",
  "files": {
    "Button.tsx": "...",
    "Button.stories.tsx": "..."
  },
  "metadata": {
    "latency_ms": 45000,
    "token_count": 12,
    "lines_of_code": 150
  }
}
```

## Dependencies

- **Python**: 3.11+
- **FastAPI**: Web framework
- **Pydantic**: Data validation
- **LangChain/LangGraph**: AI orchestration
- **LangSmith**: AI observability
- **Node.js**: For Prettier formatting

## Configuration

Environment variables:

```bash
# LangSmith (for tracing)
LANGSMITH_API_KEY=your_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=component-forge

# OpenAI (if using AI enhancement in future)
OPENAI_API_KEY=your_key
```

## Future Enhancements

- [ ] AI-powered code optimization (Epic 8)
- [ ] TypeScript compilation validation (Epic 5)
- [ ] ESLint auto-fixing (Epic 5)
- [ ] Component preview generation
- [ ] Multi-framework support (Vue, Angular)

## Polish Stream Features (Epic 4 - Complete)

The Polish Stream adds production-quality enhancements:

### ✅ Provenance Tracking (P1)
- Pattern ID and version tracking
- ISO 8601 UTC timestamps
- SHA-256 content hashes for tokens and requirements
- Warning about manual edits
- Metadata for future regeneration (Epic 8)

### ✅ Import Resolution (P2)
- Automatic import ordering (external → internal → utils → types)
- Deduplication of identical imports
- Missing import detection and addition
- Package.json dependency generation
- Alias handling (@/ for src/)

### ✅ Accessibility Enhancement (P3)
- Component-specific ARIA attributes
- Semantic HTML elements
- Keyboard navigation support
- Focus indicators
- Screen reader support
- Supports: Button, Input, Card, Checkbox, Radio, Select, Switch, Tabs, Alert, Badge

### ✅ TypeScript Type Generation (P4)
- Strict TypeScript interfaces
- Zero `any` types
- Return type annotations
- Ref forwarding types
- JSDoc comments
- Variant union types
- Utility type usage (Omit, Pick, Partial, etc.)

### ✅ Storybook Story Generation (P5)
- CSF 3.0 format
- Meta object with component info
- ArgTypes for interactive controls
- Default story
- Variant stories for all component variants
- State stories (Disabled, Loading, Error)
- Play functions for interaction testing (buttons)
- Documentation parameters

### Example Generated Component

```typescript
/**
 * Generated by ComponentForge
 * Version: 1.0.0
 * Pattern: shadcn-button
 * Generated: 2024-01-15T10:30:00.000Z
 * Tokens Hash: a1b2c3d4e5f6
 * Requirements Hash: f6e5d4c3b2a1
 *
 * WARNING: This file was automatically generated.
 * Manual edits may be lost when regenerating.
 * Use ComponentForge to make changes instead.
 */

import * as React from "react"

import { cn } from "@/lib/utils"

interface ButtonProps {
  /** Visual variant of the button */
  variant?: "default" | "primary" | "secondary" | "ghost";
  /** Size of the button */
  size?: "sm" | "md" | "lg";
  /** Whether the button is disabled */
  disabled?: boolean;
  className?: string;
  children?: React.ReactNode;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = "default", size = "md", disabled, className, children, ...props }, ref): React.ReactElement => {
    return (
      <button
        ref={ref}
        type="button"
        disabled={disabled}
        aria-disabled={disabled}
        className={cn(
          "inline-flex items-center justify-center rounded-md font-medium",
          className
        )}
        {...props}
      >
        {children}
      </button>
    )
  }
)

Button.displayName = "Button"

export { Button }
```

## References

- [Epic 4 Specification](/.claude/epics/04-code-generation.md)
- [Epic 4 Commit Strategy](/.claude/epics/04-commit-strategy.md)
- [Pattern Library](/backend/data/patterns/)
- [LangSmith Documentation](https://docs.smith.langchain.com/)
