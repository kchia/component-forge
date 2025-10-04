from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Initialize logging first
from .core.logging import init_logging_from_env, get_logger
from .api.middleware.logging import LoggingMiddleware

# Initialize logging configuration
init_logging_from_env()
logger = get_logger(__name__)

# Try to import optional packages with proper error handling
try:
    from fastapi.responses import PlainTextResponse
    from prometheus_client import Counter, Histogram, generate_latest

    METRICS_ENABLED = True
    logger.info("Prometheus metrics enabled")
except ImportError as e:
    METRICS_ENABLED = False
    logger.warning(f"Metrics disabled - prometheus_client not available: {e}")

try:
    from dotenv import load_dotenv

    load_dotenv()
    logger.info("Environment variables loaded from .env file")
except ImportError as e:
    logger.warning(f"Using system environment variables - python-dotenv not available: {e}")

# Initialize metrics only if available
if METRICS_ENABLED:
    request_counter = Counter(
        "requests_total", "Total requests", ["method", "endpoint"]
    )
    request_duration = Histogram("request_duration_seconds", "Request duration")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting FastAPI application", extra={"extra": {"event": "startup"}})
    
    # Validate OpenAI API key at startup
    import os
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.warning("OPENAI_API_KEY not set - token extraction will fail")
    else:
        logger.info("OpenAI API key configured")
    
    yield
    logger.info("Shutting down FastAPI application", extra={"extra": {"event": "shutdown"}})


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

# Add logging middleware
app.add_middleware(
    LoggingMiddleware,
    skip_paths=["/health", "/metrics", "/docs", "/redoc", "/openapi.json"],
    log_request_body=False,  # Set to True in development if needed
    log_response_body=False,  # Set to True in development if needed
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
from .api.v1.routes import tokens

app.include_router(tokens.router, prefix="/api/v1")
