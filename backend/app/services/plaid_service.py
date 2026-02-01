"""
Plaid integration service for automatic bank account and transaction imports
"""
from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Dict, Any
import plaid
from plaid.api import plaid_api
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.accounts_get_request import AccountsGetRequest

from ..core.config import settings


class PlaidService:
    """Service for interacting with Plaid API"""
    
    def __init__(self):
        """Initialize Plaid client"""
        configuration = plaid.Configuration(
            host=self._get_plaid_environment(),
            api_key={
                'clientId': settings.plaid_client_id,
                'secret': settings.plaid_secret,
            }
        )
        api_client = plaid.ApiClient(configuration)
        self.client = plaid_api.PlaidApi(api_client)
    
    def _get_plaid_environment(self) -> str:
        """Get Plaid environment URL based on settings"""
        env_map = {
            'sandbox': plaid.Environment.Sandbox,
            'development': plaid.Environment.Development,
            'production': plaid.Environment.Production,
        }
        return env_map.get(settings.plaid_environment, plaid.Environment.Sandbox)
    
    def create_link_token(self, user_id: int, username: str) -> Dict[str, Any]:
        """
        Create a link token for Plaid Link initialization
        
        Args:
            user_id: User ID from the database
            username: Username for display
            
        Returns:
            Dictionary with link_token
        """
        try:
            request = LinkTokenCreateRequest(
                products=[Products("transactions"), Products("auth")],
                client_name="FinApp",
                country_codes=[CountryCode('US')],
                language='en',
                user=LinkTokenCreateRequestUser(client_user_id=str(user_id)),
                redirect_uri=settings.plaid_redirect_uri,
            )
            response = self.client.link_token_create(request)
            return response.to_dict()
        except plaid.ApiException as e:
            raise Exception(f"Error creating link token: {e}")
    
    def exchange_public_token(self, public_token: str) -> str:
        """
        Exchange a public token for an access token
        
        Args:
            public_token: Public token from Plaid Link
            
        Returns:
            Access token for future API calls
        """
        try:
            request = ItemPublicTokenExchangeRequest(public_token=public_token)
            response = self.client.item_public_token_exchange(request)
            return response.access_token
        except plaid.ApiException as e:
            raise Exception(f"Error exchanging public token: {e}")
    
    def get_accounts(self, access_token: str) -> List[Dict[str, Any]]:
        """
        Get accounts for a Plaid item
        
        Args:
            access_token: Plaid access token
            
        Returns:
            List of account dictionaries
        """
        try:
            request = AccountsGetRequest(access_token=access_token)
            response = self.client.accounts_get(request)
            return [account.to_dict() for account in response.accounts]
        except plaid.ApiException as e:
            raise Exception(f"Error fetching accounts: {e}")
    
    def get_transactions(
        self, 
        access_token: str, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[Dict[str, Any]]:
        """
        Get transactions for a Plaid item
        
        Args:
            access_token: Plaid access token
            start_date: Start date for transactions
            end_date: End date for transactions
            
        Returns:
            List of transaction dictionaries
        """
        try:
            request = TransactionsGetRequest(
                access_token=access_token,
                start_date=start_date.date(),
                end_date=end_date.date(),
            )
            response = self.client.transactions_get(request)
            transactions = response.transactions
            
            # Handle pagination
            while len(transactions) < response.total_transactions:
                request = TransactionsGetRequest(
                    access_token=access_token,
                    start_date=start_date.date(),
                    end_date=end_date.date(),
                    offset=len(transactions)
                )
                response = self.client.transactions_get(request)
                transactions.extend(response.transactions)
            
            return [txn.to_dict() for txn in transactions]
        except plaid.ApiException as e:
            raise Exception(f"Error fetching transactions: {e}")
    
    def sync_transactions(
        self, 
        access_token: str, 
        days: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Sync recent transactions from Plaid
        
        Args:
            access_token: Plaid access token
            days: Number of days to sync (default: 30)
            
        Returns:
            List of transaction dictionaries
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        return self.get_transactions(access_token, start_date, end_date)


# Create a singleton instance
plaid_service = PlaidService()
