from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .core.database import create_db_and_tables
from .api import (
    users, institutions, accounts, transactions, investments, investment_tax,
    payroll, retirement, retirement_forecast, taxes, plaid, import_export, websocket
)

app = FastAPI(
    title=settings.project_name,
    version=settings.version,
    openapi_url=f"{settings.api_prefix}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    """Initialize database on startup"""
    create_db_and_tables()


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "message": "Welcome to FinApp API",
        "version": settings.version,
        "docs": "/docs"
    }


@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "healthy"}


# Include routers
app.include_router(users.router, prefix=settings.api_prefix)
app.include_router(institutions.router, prefix=settings.api_prefix)
app.include_router(accounts.router, prefix=settings.api_prefix)
app.include_router(transactions.router, prefix=settings.api_prefix)
app.include_router(investments.router, prefix=settings.api_prefix)
app.include_router(investment_tax.router, prefix=settings.api_prefix)
app.include_router(payroll.router, prefix=settings.api_prefix)
app.include_router(retirement.router, prefix=settings.api_prefix)
app.include_router(retirement_forecast.router, prefix=settings.api_prefix)
app.include_router(taxes.router, prefix=settings.api_prefix)
app.include_router(plaid.router, prefix=settings.api_prefix)
app.include_router(import_export.router, prefix=settings.api_prefix)

# Include WebSocket router (no prefix needed for WebSocket)
app.include_router(websocket.router)
