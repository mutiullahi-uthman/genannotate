from fastapi import APIRouter, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.core.config import settings
from app.core.project_context import get_active_project_membership
from app.core.rate_limit import limiter

from app.api.auth.router import (
    router as auth_router,
)

from app.api.projects.router import (
    router as projects_router,
)

from app.api.datasets.router import (
    router as datasets_router,
)

from app.api.uploads.router import (
    router as uploads_router,
)

from app.api.imports.router import (
    router as imports_router,
)

from app.api.queue.router import (
    router as queue_router,
)

from app.api.annotations.router import (
    router as annotations_router,
)

from app.api.review.router import (
    router as review_router,
)

from app.api.reports.router import (
    router as reports_router,
)

from app.api.exports.router import (
    router as exports_router,
)

from app.api.audits.router import (
    router as audits_router,
)

from app.api.codebooks.router import (
    router as codebooks_router,
)

from app.api.users.router import (
    router as users_router,
)

from app.api.assignments.router import (
    router as assignments_router,
)
from app.api.records.router import (
    router as records_router,
)


app = FastAPI(
    title="GenAnnotate API",
)

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


api_router = APIRouter(prefix=settings.API_V1_PREFIX)
api_router.include_router(auth_router)
api_router.include_router(projects_router)

for project_router in (
    queue_router,
    annotations_router,
    audits_router,
    exports_router,
    reports_router,
    review_router,
    datasets_router,
    uploads_router,
    imports_router,
    codebooks_router,
    users_router,
    assignments_router,
    records_router,
):
    api_router.include_router(
        project_router,
        dependencies=[Depends(get_active_project_membership)],
    )

app.include_router(api_router)
