from datetime import datetime, timezone
from decimal import Decimal
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session, select

from ..core.database import get_session
from ..models.account import Account, AccountType
from ..models.ledger import LedgerEntry, EntryType
from ..models.plaid import PlaidItem, PlaidAccount
from ..models.transaction import Transaction
from ..services.plaid_service import plaid_service

router = APIRouter(prefix="/plaid", tags=["plaid"])


class LinkTokenRequest(BaseModel):
    user_id: int
    username: str


class PublicTokenExchange(BaseModel):
    public_token: str
    user_id: int


class SyncRequest(BaseModel):
    plaid_item_id: int
    days: int = 30


@router.post("/link-token")
def create_link_token(request: LinkTokenRequest):
    """Create a Plaid Link token for connecting bank accounts"""
    try:
        result = plaid_service.create_link_token(request.user_id, request.username)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/exchange-token")
def exchange_public_token(request: PublicTokenExchange, session: Session = Depends(get_session)):
    """Exchange public token and save Plaid item"""
    try:
        # Exchange the public token for access token
        access_token = plaid_service.exchange_public_token(request.public_token)

        # Get accounts from Plaid
        plaid_accounts = plaid_service.get_accounts(access_token)

        # Create PlaidItem
        plaid_item = PlaidItem(
            user_id=request.user_id,
            plaid_item_id=plaid_accounts[0].get('item_id', ''),
            plaid_access_token=access_token,
            institution_id=plaid_accounts[0].get('institution_id', ''),
            institution_name=plaid_accounts[0].get('institution_name', 'Unknown'),
            last_synced=datetime.now(timezone.utc),
        )
        session.add(plaid_item)
        session.commit()
        session.refresh(plaid_item)

        # Create accounts and link to Plaid
        created_accounts = []
        for plaid_acc in plaid_accounts:
            # Create FinApp account
            account = Account(
                user_id=request.user_id,
                name=plaid_acc.get('name', 'Unknown Account'),
                account_type=AccountType.CHECKING if plaid_acc.get('type') == 'depository' else AccountType.CREDIT_CARD,
                account_number=plaid_acc.get('mask', ''),
                balance=Decimal(str(plaid_acc.get('balances', {}).get('current', 0.0))),
                currency='USD',
            )
            session.add(account)
            session.commit()
            session.refresh(account)

            # Create PlaidAccount link
            plaid_account = PlaidAccount(
                plaid_item_id=plaid_item.id,
                account_id=account.id,
                plaid_account_id=plaid_acc.get('account_id', ''),
                account_name=plaid_acc.get('name', 'Unknown'),
                account_mask=plaid_acc.get('mask'),
                account_type=plaid_acc.get('type', ''),
                account_subtype=plaid_acc.get('subtype'),
            )
            session.add(plaid_account)
            created_accounts.append(
                {
                    'account_id': account.id,
                    'plaid_account_id': plaid_acc.get('account_id'),
                    'name': account.name,
                    'balance': float(account.balance),
                },
            )

        session.commit()

        return {
            "message": "Accounts linked successfully",
            "plaid_item_id": plaid_item.id,
            "accounts": created_accounts,
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sync-transactions")
def sync_transactions(request: SyncRequest, session: Session = Depends(get_session)):
    """Sync transactions from Plaid for a specific item"""
    try:
        # Get PlaidItem
        plaid_item = session.get(PlaidItem, request.plaid_item_id)
        if not plaid_item:
            raise HTTPException(status_code=404, detail="Plaid item not found")

        # Get transactions from Plaid
        plaid_transactions = plaid_service.sync_transactions(
            plaid_item.plaid_access_token,
            days=request.days,
        )

        # Get PlaidAccount mappings
        plaid_accounts = session.exec(
            select(PlaidAccount).where(PlaidAccount.plaid_item_id == plaid_item.id),
        ).all()

        plaid_account_map = {pa.plaid_account_id: pa.account_id for pa in plaid_accounts}

        imported_count = 0
        for plaid_txn in plaid_transactions:
            plaid_account_id = plaid_txn.get('account_id')
            account_id = plaid_account_map.get(plaid_account_id)

            if not account_id:
                continue

            plaid_txn_id = plaid_txn.get('transaction_id')
            if not plaid_txn_id:
                continue

            # Check if transaction already exists using Plaid transaction ID
            existing = session.exec(
                select(Transaction).where(
                    Transaction.plaid_transaction_id == plaid_txn_id,
                ),
            ).first()

            if existing:
                continue

            # Get transaction date or skip if missing
            txn_date_str = plaid_txn.get('date')
            if not txn_date_str:
                continue  # Skip transactions without a date

            # Create transaction
            amount = Decimal(str(-plaid_txn.get('amount', 0.0)))  # Plaid uses negative for income
            transaction = Transaction(
                user_id=plaid_item.user_id,
                account_id=account_id,
                transaction_date=datetime.fromisoformat(txn_date_str),
                description=plaid_txn.get('name', 'Unknown'),
                amount=amount,
                category=', '.join(plaid_txn.get('category', [])),
                merchant=plaid_txn.get('merchant_name'),
                plaid_transaction_id=plaid_txn_id,
            )
            session.add(transaction)
            session.commit()
            session.refresh(transaction)

            # Create ledger entry
            ledger_entry = LedgerEntry(
                user_id=plaid_item.user_id,
                transaction_id=transaction.id,
                account_id=account_id,
                entry_type=EntryType.DEBIT if amount > 0 else EntryType.CREDIT,
                amount=abs(amount),
                entry_date=transaction.transaction_date,
                description=transaction.description,
            )
            session.add(ledger_entry)

            # Update account balance
            account = session.get(Account, account_id)
            if account:
                account.balance += amount
                account.updated_at = datetime.now(timezone.utc)
                session.add(account)

            imported_count += 1

        # Update last synced
        plaid_item.last_synced = datetime.now(timezone.utc)
        session.add(plaid_item)
        session.commit()

        return {
            "message": "Transactions synced successfully",
            "imported_count": imported_count,
            "total_transactions": len(plaid_transactions),
        }
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/items", response_model=List[PlaidItem])
def get_plaid_items(user_id: int, session: Session = Depends(get_session)):
    """Get all Plaid items for a user"""
    items = session.exec(select(PlaidItem).where(PlaidItem.user_id == user_id)).all()
    return items


@router.delete("/items/{item_id}")
def delete_plaid_item(item_id: int, session: Session = Depends(get_session)):
    """Delete a Plaid item and unlink accounts"""
    plaid_item = session.get(PlaidItem, item_id)
    if not plaid_item:
        raise HTTPException(status_code=404, detail="Plaid item not found")

    session.delete(plaid_item)
    session.commit()
    return {"message": "Plaid item deleted successfully"}
