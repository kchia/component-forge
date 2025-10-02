# 🧩 ComponentForge

**AI-powered design-to-code component generation** that transforms Figma designs and screenshots into production-ready, accessible React components using shadcn/ui patterns.

Transform design assets into high-quality TypeScript components in seconds, not hours.

[![Next.js](https://img.shields.io/badge/Next.js-15.5.4-black?style=flat-square&logo=next.js)](https://nextjs.org/)
[![shadcn/ui](https://img.shields.io/badge/shadcn%2Fui-Latest-black?style=flat-square)](https://ui.shadcn.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-0.6.8-blue?style=flat-square&logo=langchain)](https://github.com/langchain-ai/langgraph)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue?style=flat-square&logo=typescript)](https://www.typescriptlang.org/)
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

## 🏗️ AI Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ComponentForge AI Pipeline                         │
├─────────────────┬─────────────────┬─────────────────┬─────────────────────────┤
│  📷 Input       │  🤖 AI Agents   │  📐 Retrieval   │  ✨ Generation         │
│                 │                 │                 │                         │
│ • Screenshots   │ • Token         │ • Pattern       │ • TypeScript Component  │
│ • Figma Files   │   Extractor     │   Matcher       │ • Storybook Stories     │
│ • Design Specs  │ • Requirement   │ • Similarity    │ • Accessibility Tests   │
│                 │   Proposer      │   Search        │ • Design Tokens JSON   │
└─────────────────┴─────────────────┴─────────────────┴─────────────────────────┘

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
- **TypeScript 5** for strict type safety
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

## 📁 Project Structure

```
component-forge/
├── app/                          # Next.js frontend
│   ├── src/
│   │   ├── app/                 # App Router pages
│   │   ├── components/ui/       # shadcn/ui components
│   │   └── lib/                # Utilities and stores
│   ├── components.json         # shadcn/ui configuration
│   ├── .env.local.example      # Frontend environment template
│   └── package.json           # Dependencies (shadcn/ui, Zustand, etc.)
├── backend/                     # FastAPI backend
│   ├── src/
│   │   ├── agents/            # AI agents (LangGraph)
│   │   ├── api/v1/           # API routes
│   │   ├── rag/              # Retrieval and vector operations
│   │   ├── monitoring/       # LangSmith observability
│   │   └── main.py          # FastAPI application
│   ├── .env.example          # Backend environment template
│   ├── requirements.txt      # AI dependencies (LangGraph, LangSmith, Pillow)
│   └── venv/                # Python virtual environment
├── docs/                       # Architecture documentation
├── docker-compose.yml         # Services (PostgreSQL, Qdrant, Redis)
├── Makefile                   # Development commands
└── README.md                 # This file
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
