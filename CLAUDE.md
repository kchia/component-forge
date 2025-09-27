# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Quick Start

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

**Full-stack AI engineering project** with three-tier architecture:

### Frontend (`/app`)

- **Next.js 15.5.4** with App Router and TypeScript
- **Auth.js v5** for authentication
- **Tailwind CSS v4** for styling
- **Playwright** for E2E testing
- Runs on port 3000

### Backend (`/backend`)

- **FastAPI** for high-performance API
- **LangChain/LangGraph** for AI workflows
- **SQLAlchemy** with async PostgreSQL
- **Prometheus** metrics collection
- Runs on port 8000

### Services (Docker Compose)

- **PostgreSQL 16** - Primary database (port 5432)
- **Qdrant** - Vector database for AI (ports 6333/6334)
- **Redis 7** - Cache and sessions (port 6379)

## Key Endpoints

- Frontend: http://localhost:3000
- Backend API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health
- Metrics: http://localhost:8000/metrics
- Qdrant dashboard: http://localhost:6333/dashboard

## Environment Setup

Copy `.env.example` files and configure:

- `backend/.env` - Database URLs, AI API keys
- `app/.env.local` - Auth secrets, API URLs

## Tech Stack Dependencies

- **Node.js 18+**, **Python 3.11+**, **Docker Desktop**
- AI: OpenAI, LangChain, LangGraph, LangSmith
- Vector: Qdrant, sentence-transformers
- Database: PostgreSQL with asyncpg, SQLAlchemy, Alembic
- Auth: Next-auth v5 with Auth.js core
- Testing: Playwright (E2E), pytest (backend)

## Code Style & Patterns

### Frontend (Next.js/TypeScript)

- Use App Router patterns (not Pages Router)
- Prefer server components over client components
- Use TypeScript strict mode with proper type definitions
- Follow Next.js 15.5.4 conventions
- Use Tailwind CSS v4 with semantic class composition
- Implement proper error boundaries with fallback UI
- Use React Server Components for data fetching when possible
- Implement proper loading states and Suspense boundaries
- Follow component composition patterns over inheritance
- Use proper TypeScript generics for reusable components
- Implement proper form validation with Zod schemas
- Structure components with clear separation of concerns

### Backend (FastAPI/Python)

- Use async/await patterns consistently
- Follow FastAPI best practices with proper dependencies
- Use Pydantic models for all request/response validation
- Implement structured error handling with custom exceptions
- Use dependency injection for database and service connections
- Follow PEP 8 with black formatter and isort for imports
- Implement proper logging with structured format (JSON)
- Use SQLAlchemy async sessions with proper context management
- Implement request validation and sanitization
- Use proper HTTP status codes and error responses
- Implement rate limiting and request timeouts

### Database & Services

- Use async SQLAlchemy patterns with proper session management
- Implement connection pooling with appropriate limits
- Use Alembic for migrations with proper rollback strategies
- Follow Redis caching patterns with proper TTL
- Use Qdrant for vector operations with proper indexing
- Implement proper transaction management
- Use database migrations for schema changes
- Cache frequently accessed data appropriately
- Monitor database performance and query efficiency

### AI/ML Patterns (LangChain/LangGraph)

- Structure LangChain workflows as composable functions
- Use proper error handling for AI model calls with retries
- Implement streaming responses for long-running AI operations
- Use proper vector search patterns with Qdrant
- Cache expensive AI operations appropriately
- Log AI interactions for debugging and monitoring
- Use environment variables for model configurations
- Implement proper prompt templates and versioning
- Handle AI model failures gracefully with fallbacks
- Follow LangGraph patterns for complex AI workflows

### Security Patterns

- Validate all inputs using Pydantic models
- Sanitize user inputs before database operations
- Use parameterized queries to prevent SQL injection
- Implement proper CORS configuration
- Use HTTPS in production with proper headers
- Secure environment variables and secrets
- Implement proper session management
- Use rate limiting for API endpoints
- Log security-related events appropriately
- Implement proper authentication and authorization flows

## Project-Specific Rules

1. **NEVER** suggest using Pages Router - this project uses App Router
2. **ALWAYS** use TypeScript - no JavaScript suggestions
3. **PREFER** server components over client components
4. **USE** the existing auth system (Auth.js v5)
5. **FOLLOW** the established folder structure
6. **MAINTAIN** the three-tier architecture (Frontend/Backend/Services)
7. **USE** Docker Compose for services, not local installations
8. **IMPLEMENT** proper error handling and logging
9. **FOLLOW** the existing API patterns in `/backend/src/api/`
10. **USE** the existing component patterns in `/app/src/components/`

## Common Anti-Patterns to Avoid

### Architecture

- Don't suggest Pages Router patterns
- Don't mix client/server component patterns incorrectly
- Don't bypass the existing auth system
- Don't suggest changes that break the Docker setup

### Code Quality

- Don't use synchronous database operations
- Don't ignore proper error handling patterns
- Don't hardcode values (use environment variables)
- Don't create overly complex components or functions
- Don't ignore TypeScript errors or use 'any' types
- Don't skip input validation and sanitization

### AI/ML Specific

- Don't make AI calls without proper error handling
- Don't ignore vector search optimization
- Don't cache AI responses without considering staleness
- Don't expose sensitive prompts or model configurations
- Don't ignore streaming for long-running AI operations

### Performance

- Don't ignore proper loading states
- Don't fetch data in client components when server components suffice
- Don't ignore database query optimization
- Don't create unnecessary re-renders in React
- Don't ignore proper caching strategies
