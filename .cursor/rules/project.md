# Project-Wide Cursor Rules for AI Engineering Starter

## Project Overview

This is a full-stack AI engineering project with Next.js frontend, FastAPI backend, and containerized services.

## Architecture Constraints

- Frontend: Next.js 15.5.4 with App Router (NOT Pages Router)
- Backend: FastAPI with async/await patterns
- Database: PostgreSQL with async SQLAlchemy
- Vector DB: Qdrant for AI operations
- Cache: Redis for high-performance caching
- Auth: Auth.js v5 (Next-auth)

## Project-Specific Rules

1. **NEVER** suggest Pages Router - this project uses App Router
2. **ALWAYS** use TypeScript - no JavaScript suggestions
3. **PREFER** server components over client components
4. **USE** the existing auth system (Auth.js v5)
5. **FOLLOW** the established folder structure
6. **MAINTAIN** the three-tier architecture
7. **USE** Docker Compose for services
8. **IMPLEMENT** proper error handling and logging
9. **FOLLOW** existing API patterns in `/backend/src/api/`
10. **USE** existing component patterns in `/app/src/components/`

## File Structure Context

- `/app/` - Next.js frontend with App Router
- `/backend/` - FastAPI backend with async patterns
- `/docs/` - Architecture and API documentation
- `docker-compose.yml` - Service containers
- `Makefile` - Development commands

## Development Workflow

- Use `make install` to install dependencies
- Use `make dev` to start development environment
- Use `make test` to run all tests
- Use `make demo` to prepare demo environment

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
