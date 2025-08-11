from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.exceptions import HTTPException
from .logging import setup_logging
from .middleware import RequestIDMiddleware, http_exception_handler, general_exception_handler
from .routers import routes_api, tts_api, health

setup_logging()

limiter = Limiter(key_func=get_remote_address, default_limits=["30/minute"])

app = FastAPI(title="City Guide")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app.include_router(routes_api.router)
app.include_router(tts_api.router)
app.include_router(health.router)
