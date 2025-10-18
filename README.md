# 🧩 ComponentForge

**AI-powered design-to-code component generation** that transforms Figma designs and screenshots into production-ready, accessible React components using shadcn/ui patterns.

Transform design assets into high-quality TypeScript components in seconds, not hours.

[![Next.js](https://img.shields.io/badge/Next.js-15.5.4-black?style=flat-square&logo=next.js)](https://nextjs.org/)
[![shadcn/ui](https://img.shields.io/badge/shadcn%2Fui-Latest-black?style=flat-square)](https://ui.shadcn.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.6.8-blue?style=flat-square&logo=langchain)](https://github.com/langchain-ai/langgraph)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.9.3-blue?style=flat-square&logo=typescript)](https://www.typescriptlang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)

## ✨ Features

### 🎨 **AI-Powered Design-to-Code**

- **📷 Screenshot Processing**: Extract design tokens from any UI screenshot using GPT-4V
- **🎯 Figma Integration**: Direct token extraction from Figma files (colors, typography, spacing)
- **🤖 Multi-Agent Pipeline**: LangGraph orchestration for complex AI workflows
- **📐 Pattern Matching**: Intelligent retrieval of shadcn/ui component patterns
- **✨ Code Generation**: Production-ready TypeScript + Storybook components

### 🛠️ **Production-Ready Stack**

- **⚡ Modern Frontend**: Next.js 15.5.4 + React 19 + shadcn/ui + Tailwind CSS v4
- **🚀 Powerful Backend**: FastAPI + LangChain + LangGraph + LangSmith observability
- **♿ Accessibility First**: Built-in axe-core testing for WCAG compliance
- **📊 State Management**: Zustand (client) + TanStack Query (server state)
- **🗄️ Vector Database**: Qdrant for semantic search and pattern retrieval
- **🐳 Containerized**: PostgreSQL + Redis + Qdrant via Docker Compose

## 🚀 Quick Start

### Prerequisites

- **Node.js** 18+
- **Python** 3.11+
- **Docker Desktop** (for services)
- **OpenAI API Key** (for AI features)

### 1. Install Dependencies

```bash
make install
```

This will:

- Install npm packages (shadcn/ui, TanStack Query, Zustand, axe-core)
- Install Playwright browsers for E2E testing
- Create Python virtual environment
- Install AI dependencies (LangChain, LangGraph, LangSmith, Pillow)
- Copy environment templates (`.env` and `.env.local.example`)

### 2. Start Development Environment

```bash
make dev
```

Or manually in separate terminals:

```bash
# Terminal 1: Start Docker services
docker-compose up -d

# Terminal 2: Start backend
cd backend && source venv/bin/activate && uvicorn src.main:app --reload

# Terminal 3: Start frontend
cd app && npm run dev
```

### 2.5. Seed Qdrant Vector Database

**⚠️ CRITICAL: Required for hybrid retrieval (BM25 + semantic search)**

After starting Docker services, seed the Qdrant vector database with component pattern embeddings:

```bash
make seed-patterns
```

Or manually:

```bash
cd backend
source venv/bin/activate
python scripts/seed_patterns.py
```

**Expected output:**

```
INFO: Loading pattern library...
INFO: Loaded 10 patterns from library
INFO: Creating Qdrant collection 'patterns'...
INFO: Generating embeddings for 10 patterns...
INFO: Pattern seeding complete! (10 vectors)
```

**Why this is required:**

- Enables semantic search (70% of retrieval accuracy)
- Without seeding, system falls back to BM25-only mode (keyword search)

**Verify seeding succeeded:**

```bash
curl http://localhost:6333/collections/patterns | jq '.result.vectors_count'
# Should return: 10
```

### 3. Configure Environment

Copy and configure your environment files:

```bash
# Backend configuration
cp backend/.env.example backend/.env
# Add your OPENAI_API_KEY and other secrets

# Frontend configuration
cp app/.env.local.example app/.env.local
# Add your AUTH_SECRET and API URLs
```

### 4. Access Your Application

- **ComponentForge UI**: http://localhost:3000
- **Backend API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Qdrant Dashboard**: http://localhost:6333/dashboard
- **Storybook**: http://localhost:6006 (see below for setup)

### 5. Verify Hybrid Retrieval is Active

**Check that semantic search is working (not just BM25 fallback):**

```bash
# Test retrieval endpoint
curl -X POST http://localhost:8000/api/v1/retrieval/search \
  -H "Content-Type: application/json" \
  -d '{"requirements": {"component_type": "Button"}}' \
  | jq '.retrieval_metadata'
```

**Expected output (SUCCESS):**

```json
{
  "methods_used": ["bm25", "semantic"],
  "weights": { "bm25": 0.3, "semantic": 0.7 }
}
```

**Failure output (degraded mode):**

```json
{
  "methods_used": ["bm25"],
  "weights": { "bm25": 1.0, "semantic": 0.0 }
}
```

**If you see BM25-only mode:**

1. Verify Qdrant is running: `curl http://localhost:6333/health`
2. Check pattern collection exists: `curl http://localhost:6333/collections/patterns`
3. Re-run seeding: `make seed-patterns`
4. Restart backend: Kill and restart `uvicorn src.main:app --reload`

## 📚 Documentation

Comprehensive documentation is available in the [`docs/`](./docs) directory:

- **[Getting Started](./docs/getting-started/README.md)** - Installation, FAQ, and contributing guide
- **[Architecture](./docs/architecture/overview.md)** - System design and technical decisions
- **[API Reference](./docs/api/overview.md)** - Endpoints, authentication, and error codes
- **[Features](./docs/features/README.md)** - Token extraction, Figma integration, observability
- **[Testing](./docs/testing/README.md)** - Integration tests, manual testing, and test reference
- **[Deployment](./docs/deployment/README.md)** - Production deployment and security guidelines
- **[Development](./docs/development/README.md)** - Setup guides and best practices
- **[Backend Docs](./backend/docs/README.md)** - Backend-specific documentation

## 🏗️ AI Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                              ComponentForge AI Pipeline                                     │
├─────────────────┬──────────────────────────────────┬─────────────────┬─────────────────────────┤
│  📷 Input       │  🤖 Multi-Agent System (6 Agents)│  📐 Retrieval   │  ✨ Generation         │
│                 │                                  │                 │                         │
│ • Screenshots   │ 1. Token Extractor (GPT-4V)      │ • BM25 Keyword  │ • TypeScript Component  │
│ • Figma Files   │ 2. Component Classifier          │   Search        │ • Storybook Stories     │
│ • Design Specs  │ ──────────────────────────────   │ • Semantic      │ • Accessibility Tests   │
│                 │ Orchestrator → Parallel (4):     │   Similarity    │ • Design Tokens JSON   │
│                 │ 3. Props Proposer     ┐          │ • Weighted      │                         │
│                 │ 4. Events Proposer    │ Async    │   Fusion        │                         │
│                 │ 5. States Proposer    │ Parallel │ • Explainability│                         │
│                 │ 6. A11y Proposer      ┘          │                 │                         │
└─────────────────┴──────────────────────────────────┴─────────────────┴─────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Services      │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   (Docker)      │
│                 │    │                 │    │                 │
│ • Next.js 15    │    │ • LangGraph     │    │ • PostgreSQL    │
│ • shadcn/ui     │    │ • LangSmith     │    │ • Qdrant Vector │
│ • Zustand       │    │ • GPT-4V        │    │ • Redis Cache   │
│ • TanStack      │    │ • Pillow        │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Tech Stack

**Frontend (`/app`)**

- **Next.js 15.5.4** with App Router and React 19
- **shadcn/ui + Radix UI** for accessible component library
- **Tailwind CSS v4** with CSS variables for theming
- **Zustand** for client state management
- **TanStack Query** for server state and caching
- **TypeScript 5.9.3** for strict type safety
- **axe-core** for accessibility testing
- **Playwright** for E2E testing

**Backend (`/backend`)**

- **FastAPI** for high-performance async API
- **LangGraph** for multi-agent AI orchestration
- **LangSmith** for AI observability and monitoring
- **LangChain** for AI workflow composition
- **GPT-4V** for vision and screenshot processing
- **Pillow** for image preprocessing
- **SQLAlchemy** with async PostgreSQL
- **Pydantic** for data validation

**Services (`docker-compose.yml`)**

- **PostgreSQL 16** - Primary database (Port 5432)
- **Qdrant** - Vector database for AI (Ports 6333/6334)
- **Redis 7** - Cache and sessions (Port 6379)

## 🛠️ Development Commands

```bash
# Install all dependencies
make install

# Start development environment
make dev

# Run all tests
make test

# Prepare demo environment
make demo

# Clean up containers and dependencies
make clean

# Show help
make help
```

### Component Development with Storybook

```bash
# Start Storybook development server
cd app && npm run storybook

# Build static Storybook for deployment
cd app && npm run build-storybook
```

Storybook runs on http://localhost:6006 and provides:

- **Interactive component development** - Build and test components in isolation
- **Visual documentation** - Auto-generated docs for all component variants
- **Accessibility testing** - Built-in a11y addon for WCAG compliance checks
- **Component testing** - Integrated Vitest for component unit tests

## 📁 Project Structure

```
component-forge/
├── app/                                    # Next.js 15 Frontend (React 19)
│   ├── src/
│   │   ├── app/                           # App Router pages and routes
│   │   │   ├── demo/                      # Demo page for testing
│   │   │   ├── extract/                   # Token extraction flow
│   │   │   ├── patterns/                  # Pattern library browsing
│   │   │   ├── preview/                   # Component preview page
│   │   │   ├── requirements/              # Requirements management
│   │   │   ├── layout.tsx                 # Root layout with providers
│   │   │   ├── page.tsx                   # Home page
│   │   │   ├── error.tsx                  # Error boundary
│   │   │   ├── providers.tsx              # React Query, Zustand providers
│   │   │   └── globals.css                # Global styles and CSS variables
│   │   ├── components/
│   │   │   ├── ui/                        # shadcn/ui base components (Button, Card, etc.)
│   │   │   ├── composite/                 # Composed business components
│   │   │   ├── extract/                   # Token extraction components
│   │   │   ├── patterns/                  # Pattern display components
│   │   │   ├── preview/                   # Code preview and editor
│   │   │   ├── requirements/              # Requirements form components
│   │   │   ├── tokens/                    # Design token components
│   │   │   ├── layout/                    # Layout components (Header, Footer)
│   │   │   └── onboarding/                # User onboarding flow
│   │   ├── hooks/                         # Custom React hooks
│   │   ├── lib/                           # Utilities and helpers
│   │   ├── services/                      # API client services
│   │   ├── store/                         # Zustand store (global state)
│   │   ├── stores/                        # Individual feature stores
│   │   ├── stories/                       # Storybook stories for components
│   │   └── types/                         # TypeScript type definitions
│   ├── e2e/                               # Playwright E2E tests
│   ├── public/                            # Static assets (images, fonts)
│   ├── components.json                    # shadcn/ui configuration
│   ├── eslint.config.mjs                  # ESLint configuration
│   ├── next.config.ts                     # Next.js configuration
│   ├── playwright.config.ts               # Playwright test configuration
│   ├── postcss.config.mjs                 # PostCSS configuration
│   ├── tsconfig.json                      # TypeScript configuration
│   ├── vitest.config.ts                   # Vitest test configuration
│   ├── .env.local.example                 # Frontend environment template
│   ├── package.json                       # Dependencies (React 19, Next.js 15.5.4)
│   └── README.md                          # Frontend documentation
│
├── backend/                                # FastAPI Backend
│   ├── src/
│   │   ├── agents/                        # 6 AI agents (LangGraph)
│   │   │   ├── token_extractor.py         # GPT-4V token extraction
│   │   │   ├── component_classifier.py    # Component type classification
│   │   │   ├── props_proposer.py          # Props inference
│   │   │   ├── events_proposer.py         # Event handlers inference
│   │   │   ├── states_proposer.py         # State management inference
│   │   │   ├── a11y_proposer.py           # Accessibility requirements
│   │   │   └── requirement_orchestrator.py # Parallel agent orchestration
│   │   ├── api/                           # API routes and endpoints
│   │   ├── cache/                         # Redis caching layer
│   │   ├── core/                          # Core utilities and database
│   │   ├── generation/                    # Code generation and validation
│   │   │   ├── generator_service.py       # TypeScript generation
│   │   │   ├── code_validator.py          # ESLint, TypeScript validation
│   │   │   └── storybook_generator.py     # Storybook story generation
│   │   ├── monitoring/                    # LangSmith observability and metrics
│   │   ├── prompts/                       # AI prompt templates
│   │   ├── retrieval/                     # Pattern retrieval system
│   │   │   ├── bm25_retriever.py          # Keyword-based search
│   │   │   ├── semantic_retriever.py      # Vector similarity search
│   │   │   ├── weighted_fusion.py         # Hybrid retrieval (0.3/0.7)
│   │   │   └── explainer.py               # Confidence scoring
│   │   ├── services/                      # Business logic services
│   │   ├── types/                         # Pydantic models and schemas
│   │   ├── validation/                    # Input validation and sanitization
│   │   └── main.py                        # FastAPI application entry point
│   ├── docs/                              # Backend technical documentation
│   ├── tests/                             # Unit and integration tests
│   │   ├── unit/                          # Unit tests for individual modules
│   │   └── integration/                   # Integration tests for workflows
│   ├── scripts/                           # Utility scripts (seed data, etc.)
│   ├── alembic/                           # Database migrations
│   ├── .env.example                       # Backend environment template
│   ├── requirements.txt                   # Python dependencies (LangGraph, etc.)
│   ├── pyproject.toml                     # Python project configuration
│   └── venv/                              # Python virtual environment
│
├── docs/                                   # Comprehensive Documentation
│   ├── getting-started/                   # Installation, setup, FAQ
│   ├── architecture/                      # System design and architecture decisions
│   ├── api/                               # API reference and examples
│   ├── features/                          # Feature documentation
│   ├── testing/                           # Testing guides and strategies
│   ├── deployment/                        # Production deployment guides
│   ├── development/                       # Development workflow and guides
│   ├── project-history/                   # Epic completion reports
│   ├── coursework/                        # Academic coursework documentation
│   ├── adr/                               # Architecture Decision Records
│   ├── backend/                           # Backend-specific documentation
│   ├── screenshots/                       # Documentation screenshots
│   ├── slides/                            # Presentation materials
│   └── README.md                          # Documentation index
│
├── scripts/                                # Utility Scripts
│   ├── seed_patterns.py                   # Seed pattern library to Qdrant
│   └── setup_dev.sh                       # Development environment setup
│
├── notebooks/                              # Jupyter Notebooks
│   └── (research and experimentation)
│
├── .claude/                                # Claude Code Configuration
│   └── BASE-COMPONENTS.md                 # Component library specification
│
├── docker-compose.yml                      # Services (PostgreSQL, Qdrant, Redis)
├── Makefile                                # Development commands (install, dev, test)
├── CLAUDE.md                               # Claude Code project instructions
├── LICENSE                                 # MIT License
├── RAG_Fusion.ipynb                        # RAG-Fusion evaluation notebook
├── pyproject.toml                          # Python project metadata
└── README.md                               # This file
```

## 🔧 Configuration

### Environment Variables

**Frontend (`.env.local`)**

```bash
# Authentication (Auth.js v5)
AUTH_SECRET=your-32-char-secret-key
NEXTAUTH_URL=http://localhost:3000

# API Connection
NEXT_PUBLIC_API_URL=http://localhost:8000
API_URL=http://localhost:8000

# AI Configuration
NEXT_PUBLIC_OPENAI_MODEL=gpt-4o
NEXT_PUBLIC_VISION_MODEL=gpt-4o

# Feature Flags
NEXT_PUBLIC_ENABLE_FIGMA_INTEGRATION=true
NEXT_PUBLIC_ENABLE_SCREENSHOT_UPLOAD=true
NEXT_PUBLIC_ENABLE_ACCESSIBILITY_TESTING=true
```

**Backend (`.env`)**

```bash
# Database Configuration
DATABASE_URL=postgresql+asyncpg://demo_user:demo_pass@localhost:5432/demo_db

# Vector Database (Qdrant)
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your-qdrant-api-key

# Cache (Redis)
REDIS_URL=redis://localhost:6379

# AI Services - Required for ComponentForge
OPENAI_API_KEY=your-openai-api-key
LANGCHAIN_API_KEY=your-langchain-api-key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
LANGCHAIN_PROJECT=component-forge

# Authentication
AUTH_SECRET=your-auth-secret-key-here
```

## 🧪 Testing

```bash
# Backend tests (AI agents, API endpoints)
cd backend && source venv/bin/activate && pytest tests/ -v

# Frontend unit tests (components, utilities)
cd app && npm test

# Component tests with Storybook + Vitest
cd app && npx vitest

# Accessibility testing (axe-core)
cd app && npm run test:a11y

# E2E tests with Playwright (full component generation flow)
cd app && npm run test:e2e
```

## 📊 AI Pipeline Monitoring

### Health Checks & APIs

- **ComponentForge Health**: http://localhost:8000/health
- **API Documentation**: http://localhost:8000/docs (FastAPI Swagger)
- **Metrics**: http://localhost:8000/metrics (Prometheus format)
- **Storybook**: http://localhost:6006 (Component library & testing)

### AI Observability

- **LangSmith Traces**: Monitor agent performance and costs
- **Token Extraction Confidence**: Track vision model accuracy
- **Pattern Retrieval Scores**: Semantic search effectiveness
- **Generation Quality**: TypeScript compilation and accessibility scores

### Infrastructure

- **Qdrant Dashboard**: http://localhost:6333/dashboard (Vector operations)
- **PostgreSQL**: Database performance and query logs
- **Redis**: Cache hit rates and performance

## 🐳 Docker Services

The project includes three essential services:

```yaml
# PostgreSQL Database
postgres:5432
  - User: demo_user
  - Password: demo_pass
  - Database: demo_db

# Qdrant Vector Database
qdrant:6333/6334
  - Dashboard: :6333/dashboard
  - API: :6333

# Redis Cache
redis:6379
  - Memory limit: 256MB
  - Policy: allkeys-lru
```

## 🚨 Troubleshooting

### Common Issues

**Docker not starting:**

```bash
# Ensure Docker Desktop is running
open -a Docker

# Check Docker status
docker --version
docker-compose ps
```

**Python environment issues:**

```bash
# Recreate virtual environment
rm -rf backend/venv
cd backend && python -m venv venv
source venv/bin/activate && pip install -r requirements.txt
```

**Node.js dependency issues:**

```bash
# Clean install
cd app && rm -rf node_modules package-lock.json
npm install
```

**Port conflicts:**

- Frontend (3000), Backend (8000), PostgreSQL (5432), Qdrant (6333), Redis (6379)
- Check for other services using these ports: `lsof -i :3000`

**Qdrant/Semantic Search Issues:**

**Symptom: "Semantic retriever unavailable" in backend logs**

This means the system is running in BM25-only fallback mode (degraded accuracy).

**Solution:**

```bash
# 1. Verify Qdrant is running
curl http://localhost:6333/health

# 2. Check if patterns collection exists
curl http://localhost:6333/collections/patterns

# 3. If collection missing, seed it
cd backend
source venv/bin/activate
python scripts/seed_patterns.py

# 4. Restart backend to reinitialize semantic retriever
# (Kill uvicorn and restart)
```

**Symptom: "Architecture mismatch (arm64 vs x86_64)" when seeding**

Your Python venv was created with wrong architecture.

**Solution:**

```bash
# Recreate venv with correct architecture
cd backend
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Retry seeding
python scripts/seed_patterns.py
```

**Symptom: OpenAI API errors during seeding**

Seeding requires OpenAI API to generate embeddings.

**Solution:**

```bash
# Check API key is set
echo $OPENAI_API_KEY

# If empty, add to backend/.env
echo "OPENAI_API_KEY=your-key-here" >> backend/.env

# Export it
export OPENAI_API_KEY="your-key-here"

# Retry seeding
cd backend && source venv/bin/activate
python scripts/seed_patterns.py
```

## 🎯 ComponentForge Workflow

### 1. Design Input

- **Screenshot Upload**: Drag & drop any UI design screenshot
- **Figma Integration**: Connect with Personal Access Token
- **Design Analysis**: GPT-4V extracts visual design patterns

### 2. AI Processing Pipeline

- **Token Extraction**: Colors, typography, spacing with confidence scores
- **Requirement Proposal**: Inferred props, states, behaviors, accessibility needs
- **Pattern Retrieval**: Semantic search through shadcn/ui component patterns
- **Quality Validation**: TypeScript, ESLint, axe-core accessibility checks

### 3. Generated Output

- **TypeScript Component**: Production-ready React component with proper types
- **Storybook Stories**: Interactive documentation and testing
- **Accessibility**: WCAG-compliant with proper ARIA attributes
- **Design Tokens**: JSON file with extracted design system values

## 📝 Development Notes

- **AI-First Architecture**: Every component uses LangSmith for observability
- **Hot Reloading**: Both frontend and backend support instant updates
- **Type Safety**: Strict TypeScript across the entire stack
- **Accessibility**: Built-in axe-core testing prevents WCAG violations
- **Production Ready**: Docker containerization for easy deployment

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Transform designs into code with AI!** 🧩✨

Built with ❤️ for developers who want to focus on logic, not repetitive UI coding.
