from .users import router as users_router
from .institutions import router as institutions_router
from .accounts import router as accounts_router
from .transactions import router as transactions_router
from .investments import router as investments_router
from .payroll import router as payroll_router
from .retirement import router as retirement_router
from .taxes import router as taxes_router

__all__ = [
    "users_router",
    "institutions_router",
    "accounts_router", 
    "transactions_router",
    "investments_router",
    "payroll_router",
    "retirement_router",
    "taxes_router",
]
