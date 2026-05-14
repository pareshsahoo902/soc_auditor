from fastapi import Request
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

async def tenant_isolation_middleware(request: Request, call_next):
    # Mock tenant extraction from headers (e.g., X-Tenant-ID)
    tenant_id = request.headers.get("X-Tenant-ID")
    if not tenant_id and request.url.path.startswith("/api/v1/reports"):
        logger.warning("Missing tenant ID in request")
        return JSONResponse(status_code=403, content={"detail": "Missing Tenant ID"})

    request.state.tenant_id = tenant_id
    response = await call_next(request)
    return response

async def rbac_middleware(request: Request, call_next):
    # Mock role extraction
    user_role = request.headers.get("X-User-Role", "auditor")
    if request.method in ["POST", "PUT", "DELETE"] and user_role != "admin":
        return JSONResponse(status_code=403, content={"detail": "Forbidden: insufficient permissions"})

    response = await call_next(request)
    return response
