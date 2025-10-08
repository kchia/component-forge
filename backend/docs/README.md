# Backend Documentation

Backend-specific technical documentation for ComponentForge.

## Contents

- [Agent Architecture](./agent-architecture.md) - AI agent design and LangGraph workflows
- [Database Operations](./database-operations.md) - PostgreSQL patterns and migrations
- [Vector Operations](./vector-operations.md) - Qdrant integration and semantic search
- [Generation Service](./generation-service.md) - Code generation system architecture
- [Prompting Guide](./prompting-guide.md) - Prompt engineering best practices
- [Monitoring](./monitoring.md) - Observability and LangSmith setup
- [Troubleshooting](./troubleshooting.md) - Common issues and solutions

## Quick Reference

### Running the Backend

```bash
# Start Docker services
docker-compose up -d

# Activate virtual environment
cd backend && source venv/bin/activate

# Run development server
uvicorn src.main:app --reload

# Run tests
pytest tests/ -v

# Run migrations
alembic upgrade head
```

### Key Technologies

- **Framework**: FastAPI with async/await
- **AI**: LangChain, LangGraph, LangSmith
- **Database**: PostgreSQL with SQLAlchemy (async)
- **Vector DB**: Qdrant for semantic search
- **Cache**: Redis for sessions and rate limiting
- **Models**: OpenAI GPT-4, GPT-4V, text-embedding-3-small

## Architecture

The backend follows a layered architecture:

1. **API Layer** (`src/api/v1/`) - REST endpoints
2. **Service Layer** (`src/services/`) - Business logic
3. **Agent Layer** (`src/agents/`) - LangGraph AI agents
4. **Data Layer** (`src/models/`) - Database models
5. **RAG Layer** (`src/rag/`) - Vector operations

## See Also

- [Main Documentation](../../docs/README.md)
- [API Reference](../../docs/api/overview.md)
- [Architecture Overview](../../docs/architecture/overview.md)
- [Features Documentation](../../docs/features/README.md)
