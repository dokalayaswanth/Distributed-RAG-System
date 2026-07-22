from app.routers.health import router as health_router
from app.routers.documents import router as documents_router
from app.routers.jobs import router as jobs_router

__all__ = [
    'health_router',
    'documents_router',
    'jobs_router'
]