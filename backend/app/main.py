from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from app.core.config import settings
from app.core.rate_limit import limiter

from app.api.auth.router import (
    router as auth_router,
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


app.include_router(queue_router)

app.include_router(annotations_router)

app.include_router(audits_router)

app.include_router(exports_router)

app.include_router(reports_router)

app.include_router(auth_router)

app.include_router(review_router)

app.include_router(datasets_router)

app.include_router(uploads_router)

app.include_router(imports_router)

app.include_router(codebooks_router)

app.include_router(users_router)
