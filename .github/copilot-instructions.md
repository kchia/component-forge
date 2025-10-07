# Copilot Instructions

This file provides guidance to GitHub Copilot when working with code in this repository.

## Project Overview

ComponentForge is a full-stack AI engineering project that generates React components from design screenshots and Figma files using AI. It features a three-tier architecture with Next.js frontend, FastAPI backend, and Docker-based services.

## Development Environment

### Quick Start Commands

```bash
make install    # Install all dependencies
make dev        # Start development environment
make test       # Run all tests
make demo       # Prepare demo environment
```

### Manual Development

```bash
# Start services
docker-compose up -d

# Backend (in separate terminal)
cd backend && source venv/bin/activate && uvicorn src.main:app --reload

# Frontend (in separate terminal)
cd app && npm run dev
```

### Testing

```bash
# Backend tests
cd backend && source venv/bin/activate && pytest tests/ -v

# Frontend tests
cd app && npm test

# E2E tests
cd app && npm run test:e2e
```

## Architecture

### Frontend (`/app`)

- **Next.js 15.5.4** with App Router (not Pages Router)
- **TypeScript** strict mode
- **shadcn/ui** with Radix UI primitives for component library
- **Tailwind CSS v4** for styling with CSS variables
- **Zustand** for client state management
- **TanStack Query** for server state and caching
- **axe-core/react** for accessibility testing
- **Playwright** for E2E testing
- **Auth.js v5** for authentication
- Runs on port 3000

### Backend (`/backend`)

- **FastAPI** for high-performance API
- **LangChain/LangGraph** for AI workflows and multi-agent orchestration
- **LangSmith** for AI observability and monitoring
- **Pillow** for image processing and screenshot analysis
- **SQLAlchemy** with async PostgreSQL
- **Qdrant client** for vector database operations
- **Prometheus** metrics collection
- Runs on port 8000

### Services (Docker Compose)

- **PostgreSQL 16** - Primary database (port 5432)
- **Qdrant** - Vector database for AI (ports 6333/6334)
- **Redis 7** - Cache and sessions (port 6379)

## Code Style & Patterns

### Frontend (Next.js/TypeScript)

#### Component Library Usage (CRITICAL)

**BEFORE creating any new component:**

1. Check `.claude/BASE-COMPONENTS.md` for the complete component library specification
2. Search existing components in `app/src/components/ui/`
3. Reuse existing components whenever possible - DO NOT recreate from scratch
4. Extend existing components with composition rather than creating duplicates

**Available Base Components:**
- Button - variants: primary, secondary, ghost, success, warning
- Card - variants: outlined, elevated, interactive
- Badge - variants: success, warning, error, info, neutral
- Tabs, Progress, Alert/Banner, Input, Code Block, Modal/Dialog, Accordion

**Component Discovery:**
```bash
# Check if component exists
ls app/src/components/ui/ | grep -i "component-name"

# If not exists, install from shadcn/ui
npx shadcn-ui@latest add component-name
```

#### General Frontend Patterns

- **Always** use App Router patterns (NEVER Pages Router)
- **Prefer** server components over client components
- **Use** TypeScript strict mode with proper type definitions
- **Follow** Next.js 15.5.4 conventions
- **Use** Tailwind CSS v4 with semantic class composition and CSS variables
- **Use** shadcn/ui components as base, extend with Radix UI primitives
- **Implement** proper error boundaries with fallback UI
- **Use** React Server Components for data fetching when possible
- **Implement** proper loading states and Suspense boundaries
- **Follow** component composition patterns over inheritance
- **Use** Zustand for client state, TanStack Query for server state
- **Implement** accessibility testing with axe-core in development
- **Use** Lucide React for consistent iconography

### Backend (FastAPI/Python)

- **Use** async/await patterns consistently
- **Follow** FastAPI best practices with proper dependencies
- **Use** Pydantic models for all request/response validation
- **Implement** structured error handling with custom exceptions
- **Use** dependency injection for database and service connections
- **Follow** PEP 8 with black formatter and isort for imports
- **Implement** proper logging with structured format (JSON)
- **Use** SQLAlchemy async sessions with proper context management
- **Implement** request validation and sanitization
- **Use** proper HTTP status codes and error responses
- **Implement** rate limiting and request timeouts

### Database & Services

- **Use** async SQLAlchemy patterns with proper session management
- **Implement** connection pooling with appropriate limits
- **Use** Alembic for migrations with proper rollback strategies
- **Follow** Redis caching patterns with proper TTL
- **Use** Qdrant for vector operations with proper indexing
- **Implement** proper transaction management

### AI/ML Patterns (LangChain/LangGraph)

- **Structure** LangChain workflows as composable functions
- **Use** LangGraph for multi-agent orchestration and state management
- **Use** LangSmith for comprehensive AI observability and tracing
- **Implement** proper error handling for AI model calls with retries
- **Implement** streaming responses for long-running AI operations
- **Use** proper vector search patterns with Qdrant
- **Cache** expensive AI operations appropriately
- **Use** environment variables for model configurations
- **Implement** proper prompt templates and versioning
- **Handle** AI model failures gracefully with fallbacks
- **Use** Pillow for image preprocessing before vision model calls

### Security Patterns

- **Validate** all inputs using Pydantic models
- **Sanitize** user inputs before database operations
- **Use** parameterized queries to prevent SQL injection
- **Implement** proper CORS configuration
- **Secure** environment variables and secrets
- **Implement** proper session management
- **Use** rate limiting for API endpoints
- **Log** security-related events appropriately

## Critical Rules

### Component Development (HIGHEST PRIORITY)

1. **ALWAYS** check `.claude/BASE-COMPONENTS.md` before creating any UI component
2. **NEVER** recreate components that already exist in the base library
3. **REUSE** and compose existing components instead of building from scratch
4. **SEARCH** `app/src/components/ui/` to verify component implementation status
5. **INSTALL** from shadcn/ui if the component is specified but not yet implemented
6. **FOLLOW** the exact variant specifications from BASE-COMPONENTS.md

### Architecture & Stack

7. **NEVER** suggest using Pages Router - this project uses App Router
8. **ALWAYS** use TypeScript - no JavaScript suggestions
9. **PREFER** server components over client components
10. **USE** the existing auth system (Auth.js v5)
11. **MAINTAIN** the three-tier architecture (Frontend/Backend/Services)
12. **USE** Docker Compose for services, not local installations

### Patterns & Quality

13. **IMPLEMENT** proper error handling and logging
14. **FOLLOW** the existing API patterns in `/backend/src/api/`
15. **USE** the existing component patterns in `/app/src/components/`
16. **USE** shadcn/ui components as the primary UI building blocks
17. **IMPLEMENT** proper accessibility with axe-core testing
18. **USE** LangSmith for all AI operation monitoring and debugging

## Anti-Patterns to Avoid

### Component Development

- ❌ Creating custom Button components when `@/components/ui/button` exists
- ❌ Recreating Card, Badge, Input, or other base components from scratch
- ❌ Ignoring the component specifications in `.claude/BASE-COMPONENTS.md`
- ❌ Creating inconsistent component variants
- ❌ Skipping checks for existing components before implementation
- ❌ Duplicating component logic that already exists

### Architecture

- ❌ Using Pages Router patterns
- ❌ Mixing client/server component patterns incorrectly
- ❌ Bypassing the existing auth system
- ❌ Suggesting changes that break the Docker setup

### Code Quality

- ❌ Using synchronous database operations
- ❌ Ignoring proper error handling patterns
- ❌ Hardcoding values (use environment variables)
- ❌ Creating overly complex components or functions
- ❌ Using TypeScript 'any' types
- ❌ Skipping input validation and sanitization

### AI/ML Specific

- ❌ Making AI calls without proper error handling
- ❌ Ignoring vector search optimization
- ❌ Caching AI responses without considering staleness
- ❌ Exposing sensitive prompts or model configurations
- ❌ Ignoring streaming for long-running AI operations

### Performance

- ❌ Ignoring proper loading states
- ❌ Fetching data in client components when server components suffice
- ❌ Ignoring database query optimization
- ❌ Creating unnecessary re-renders in React
- ❌ Ignoring proper caching strategies

## Environment Variables

Required environment variables:

**Backend** (`backend/.env`):
- Database URLs (PostgreSQL, Redis, Qdrant)
- AI API keys (OpenAI, LangSmith)

**Frontend** (`app/.env.local`):
- Auth secrets (NextAuth)
- API URLs (Backend API endpoint)

## Key Endpoints

- Frontend: http://localhost:3000
- Backend API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health
- Metrics: http://localhost:8000/metrics
- Qdrant dashboard: http://localhost:6333/dashboard

## Dependencies

- **Node.js 18+**
- **Python 3.11+**
- **Docker Desktop**

## Additional Resources

- See `CLAUDE.md` for more detailed guidance
- See `.claude/BASE-COMPONENTS.md` for complete component specifications
- See `CONTRIBUTING.md` for contribution guidelines
- See `README.md` for project overview and setup instructions
