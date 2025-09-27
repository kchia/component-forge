from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Try to import optional packages with proper error handling
try:
    from fastapi.responses import PlainTextResponse
    from prometheus_client import Counter, Histogram, generate_latest

    METRICS_ENABLED = True
    print("✅ Prometheus metrics enabled")
except ImportError as e:
    METRICS_ENABLED = False
    print(f"⚠️ Metrics disabled - prometheus_client not available: {e}")

try:
    from dotenv import load_dotenv

    load_dotenv()
    print("✅ Environment variables loaded")
except ImportError as e:
    print(f"⚠️ Using system environment variables - python-dotenv not available: {e}")

# Initialize metrics only if available
if METRICS_ENABLED:
    request_counter = Counter(
        "requests_total", "Total requests", ["method", "endpoint"]
    )
    request_duration = Histogram("request_duration_seconds", "Request duration")


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting API...")
    yield
    print("👋 Shutting down...")


app = FastAPI(
    title="Demo Day API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "healthy"}


if METRICS_ENABLED:

    @app.get("/metrics", response_class=PlainTextResponse)
    async def metrics():
        return generate_latest()

else:

    @app.get("/metrics")
    async def metrics():
        return {"error": "Metrics not available - prometheus_client not installed"}


# Import and register routers
# from .api.v1.routes import chat, agents, documents
# app.include_router(chat.router, prefix="/api/v1")
