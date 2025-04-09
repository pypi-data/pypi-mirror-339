import os
from unittest.mock import AsyncMock, patch

import pytest

from solscan_mcp_server.server import (
    WSOL_ADDRESS,
    BalanceFlow,
    get_balance_change,
    get_defi_activities,
    get_token_accounts,
    get_token_holders,
    get_token_markets,
    get_token_meta,
    get_token_price,
    get_transaction_actions,
    get_transaction_detail,
)

# Example responses for mocking
TOKEN_META_RESPONSE = {
    "success": True,
    "data": {
        "address": "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN",
        "name": "Jupiter",
        "symbol": "JUP",
        "decimals": 6,
        "price": 0.892218,
        "volume_24h": 404204318,
        "market_cap": 1499341479,
    },
}

TOKEN_MARKETS_RESPONSE = {
    "success": True,
    "data": [
        {
            "address": "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN",
            "name": "JUP/WSOL",
            "liquidity": 1000000,
            "volume_24h": 500000,
        }
    ],
}

# Mock responses for new test cases
MOCK_DEFI_ACTIVITIES = {
    "success": True,
    "data": [
        {
            "type": "swap",
            "timestamp": 1234567890,
            "address": "WaLLeTAddR3ss123",
            "amount": 1000.0,
            "token": "SOL",
        }
    ],
}

MOCK_TOKEN_ACCOUNTS = {
    "success": True,
    "data": [
        {
            "address": "TokenAccAddr3ss123",
            "balance": 5000.0,
            "mint": "TokenM1ntAddr3ss123",
        }
    ],
}

MOCK_TOKEN_HOLDERS = {
    "success": True,
    "data": [{"address": "HolderAddr3ss123", "amount": 10000.0, "rank": 1}],
}


@pytest.fixture
def api_key():
    """Provide a test API key"""
    return "test_api_key"


@pytest.mark.asyncio
async def test_get_token_meta(api_key):
    """Test token metadata endpoint"""
    with patch(
        "solscan_mcp_server.server.make_request", new_callable=AsyncMock
    ) as mock_request:
        mock_request.return_value = TOKEN_META_RESPONSE

        result = await get_token_meta(
            "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN", api_key
        )

        assert result["success"] is True
        assert result["data"]["name"] == "Jupiter"
        assert result["data"]["symbol"] == "JUP"

        # Verify API call
        mock_request.assert_called_once_with(
            "/token/meta",
            {"address": "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN"},
            api_key,
        )


@pytest.mark.asyncio
async def test_get_token_markets(api_key):
    """Test token markets endpoint"""
    with patch(
        "solscan_mcp_server.server.make_request", new_callable=AsyncMock
    ) as mock_request:
        mock_request.return_value = TOKEN_MARKETS_RESPONSE

        result = await get_token_markets(
            "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN", api_key=api_key
        )

        assert result["success"] is True
        assert len(result["data"]) == 1
        assert result["data"][0]["name"] == "JUP/WSOL"

        # Verify API call includes WSOL pairing
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        assert "/token/markets" == call_args[0][0]
        assert call_args[0][1]["token"] == [
            "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN",
            WSOL_ADDRESS,
        ]


@pytest.mark.asyncio
async def test_api_error_handling(api_key):
    """Test error handling for API calls"""
    with patch(
        "solscan_mcp_server.server.make_request", new_callable=AsyncMock
    ) as mock_request:
        mock_request.return_value = {"error": "HTTP 401 - Unauthorized"}

        result = await get_token_meta("invalid_token", api_key)

        assert "error" in result
        assert "401" in result["error"]


@pytest.mark.asyncio
async def test_pagination_parameters(api_key):
    """Test pagination parameter handling"""
    with patch(
        "solscan_mcp_server.server.make_request", new_callable=AsyncMock
    ) as mock_request:
        mock_request.return_value = {"success": True, "data": []}

        # Test with custom page size
        await get_token_holders("token123", page_size=30, page=2, api_key=api_key)

        call_args = mock_request.call_args
        assert call_args[0][1]["page_size"] == 30
        assert call_args[0][1]["page"] == 2

        # Test with invalid page size (should default to maximum)
        await get_token_holders("token123", page_size=999, api_key=api_key)

        call_args = mock_request.call_args
        assert call_args[0][1]["page_size"] == 40  # Should default to max allowed


@pytest.mark.asyncio
async def test_optional_parameters(api_key):
    """Test handling of optional parameters"""
    with patch(
        "solscan_mcp_server.server.make_request", new_callable=AsyncMock
    ) as mock_request:
        mock_request.return_value = {"success": True, "data": []}

        # Test with all optional parameters using YYYYMMDD format
        await get_balance_change(
            wallet_address="wallet123",
            token_account="account123",
            token="token123",
            from_time=20240101,  # January 1, 2024
            to_time=20240131,  # January 31, 2024
            remove_spam=True,
            flow=BalanceFlow.IN,  # Use enum instead of string
            api_key=api_key,
        )

        call_args = mock_request.call_args
        params = call_args[0][1]
        assert params["address"] == "wallet123"
        assert params["token_account"] == "account123"
        assert params["token"] == "token123"
        assert params["from_time"] == 20240101
        assert params["to_time"] == 20240131
        assert params["remove_spam"] == "true"
        assert params["flow"] == "in"


@pytest.mark.asyncio
async def test_get_token_price_with_dates(api_key):
    """Test token price endpoint with date parameters"""
    mock_response = {
        "success": True,
        "data": [
            {"time": "2024-01-01", "price": 1.0},
            {"time": "2024-01-31", "price": 1.1},
        ],
    }

    with patch(
        "solscan_mcp_server.server.make_request", new_callable=AsyncMock
    ) as mock_request:
        mock_request.return_value = mock_response

        # Test with both dates
        result = await get_token_price(
            token_address="token123",
            time_from=20240101,  # January 1, 2024
            time_to=20240131,  # January 31, 2024
            api_key=api_key,
        )

        call_args = mock_request.call_args
        params = call_args[0][1]
        assert params["address"] == "token123"
        assert params["from_time"] == 20240101
        assert params["to_time"] == 20240131
        assert result["success"] is True
        assert len(result["data"]) == 2

        # Test with optional dates (both None)
        await get_token_price(token_address="token123", api_key=api_key)
        call_args = mock_request.call_args
        params = call_args[0][1]
        assert "from_time" not in params
        assert "to_time" not in params

        # Test with only from_time
        await get_token_price(
            token_address="token123", time_from=20240101, api_key=api_key
        )
        call_args = mock_request.call_args
        params = call_args[0][1]
        assert params["from_time"] == 20240101
        assert "to_time" not in params


@pytest.mark.asyncio
async def test_transaction_endpoints(api_key):
    """Test transaction-related endpoints"""
    with patch(
        "solscan_mcp_server.server.make_request", new_callable=AsyncMock
    ) as mock_request:
        mock_request.return_value = {"success": True, "data": {}}

        tx_sig = "4h5iBF43gC88BKrjkuC8RytGtKeMzj7Z93go9tPa3GCgnjgw1sQUsV4N44LCTxDuQ9KL8Sut88Jt1EunXNqptzbZ"

        # Test transaction detail
        await get_transaction_detail(tx_sig, api_key)
        call_args = mock_request.call_args
        assert "/transaction/detail" == call_args[0][0]
        assert call_args[0][1]["tx"] == tx_sig

        # Test transaction actions
        await get_transaction_actions(tx_sig, api_key)
        call_args = mock_request.call_args
        assert "/transaction/actions" == call_args[0][0]
        assert call_args[0][1]["tx"] == tx_sig


@pytest.mark.asyncio
async def test_get_defi_activities(api_key):
    """Test DeFi activities endpoint with various parameters."""
    with patch(
        "solscan_mcp_server.server.make_request", new_callable=AsyncMock
    ) as mock_request:
        mock_request.return_value = MOCK_DEFI_ACTIVITIES

        # Test with wallet address
        result = await get_defi_activities(
            wallet_address="WaLLeTAddR3ss123", api_key=api_key
        )
        assert result["success"] is True
        assert len(result["data"]) > 0
        assert result["data"][0]["type"] == "swap"

        # Test with date range in YYYYMMDD format
        result = await get_defi_activities(
            wallet_address="WaLLeTAddR3ss123",
            from_time=20240101,  # January 1, 2024
            to_time=20240131,  # January 31, 2024
            api_key=api_key,
        )

        call_args = mock_request.call_args
        params = call_args[0][1]
        assert params["from_time"] == 20240101
        assert params["to_time"] == 20240131
        assert result["success"] is True

        # Test with only from_time
        result = await get_defi_activities(
            wallet_address="WaLLeTAddR3ss123",
            from_time=20240101,  # January 1, 2024
            api_key=api_key,
        )

        call_args = mock_request.call_args
        params = call_args[0][1]
        assert params["from_time"] == 20240101
        assert "to_time" not in params
        assert result["success"] is True


@pytest.mark.asyncio
async def test_get_token_accounts(api_key):
    """Test token accounts endpoint functionality."""
    with patch(
        "solscan_mcp_server.server.make_request", new_callable=AsyncMock
    ) as mock_request:
        mock_request.return_value = MOCK_TOKEN_ACCOUNTS

        # Test basic account lookup
        result = await get_token_accounts(
            wallet_address="WaLLeTAddR3ss123", api_key=api_key
        )
        assert result["success"] is True
        assert len(result["data"]) > 0
        assert result["data"][0]["balance"] == 5000.0

        # Test with all parameters
        result = await get_token_accounts(
            wallet_address="WaLLeTAddR3ss123",
            type="token",
            page=1,
            page_size=40,
            hide_zero=True,
            api_key=api_key,
        )
        assert result["success"] is True


@pytest.mark.asyncio
async def test_get_token_holders(api_key):
    """Test token holders endpoint with various parameters."""
    with patch(
        "solscan_mcp_server.server.make_request", new_callable=AsyncMock
    ) as mock_request:
        mock_request.return_value = MOCK_TOKEN_HOLDERS

        # Test basic holders lookup
        result = await get_token_holders(
            token_address="TokenM1ntAddr3ss123", api_key=api_key
        )
        assert result["success"] is True
        assert len(result["data"]) > 0
        assert result["data"][0]["amount"] == 10000.0

        # Test with all parameters
        result = await get_token_holders(
            token_address="TokenM1ntAddr3ss123",
            page=1,
            page_size=40,
            from_amount="1000",
            to_amount="100000",
            api_key=api_key,
        )
        assert result["success"] is True
