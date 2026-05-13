from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
from pythonjsonlogger import jsonlogger

# Internal imports
from apps.api.connectors import router as connectors_router
from apps.api.reports import router as reports_router
from apps.api.middleware import tenant_isolation_middleware, rbac_middleware
from apps.api.metrics import router as metrics_router

# Setup JSON logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

app = FastAPI(
    title="Continuous Operational Governance Intelligence Platform",
    description="SOC2 Operational Intelligence API",
    version="0.1.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(tenant_isolation_middleware)
app.middleware("http")(rbac_middleware)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Outgoing response: {response.status_code}")
    return response

# Database init check
@app.on_event("startup")
def startup_event():
    logger.info("Initializing database schema...")
    from shared.models.database import Base, engine
    import shared.models.database
    import shared.models.auth
    Base.metadata.create_all(bind=engine)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/readiness")
def readiness_check():
    return {"status": "ready"}

app.include_router(connectors_router, prefix="/api/v1")
app.include_router(reports_router, prefix="/api/v1")
app.include_router(metrics_router, prefix="/api/v1")
