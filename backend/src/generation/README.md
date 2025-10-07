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
│  5. Code Assembler      → Combine & format code         │
│                                                          │
└──────────────────────────┬──────────────────────────────┘
                           │
                           ▼
                  ┌────────────────┐
                  │Generated Code  │
                  │  - Component   │
                  │  - Stories     │
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

### 5. Code Assembler (`code_assembler.py`)
- **Purpose**: Assemble final component code and format with Prettier
- **Input**: All code parts (imports, CSS vars, types, component)
- **Output**: Formatted component.tsx and stories.tsx files
- **Performance**: <2s for formatting

### 6. Generator Service (`generator_service.py`)
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
5. **ASSEMBLING** - Combine code parts
6. **FORMATTING** - Format with Prettier
7. **COMPLETE** - Generation finished

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
```

### Integration Tests
```bash
# Run end-to-end generation tests
pytest backend/tests/generation/test_generator_service.py -v

# Run with coverage
pytest backend/tests/generation/ --cov=src.generation --cov-report=html
```

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

## References

- [Epic 4 Specification](/.claude/epics/04-code-generation.md)
- [Epic 4 Commit Strategy](/.claude/epics/04-commit-strategy.md)
- [Pattern Library](/backend/data/patterns/)
- [LangSmith Documentation](https://docs.smith.langchain.com/)
