import logging
import os
from enum import Enum
from typing import Any, Dict, Optional

import aiohttp
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel, ConfigDict

SOLSCAN_API_BASE_URL = "https://pro-api.solscan.io/v2.0"
WSOL_ADDRESS = "So11111111111111111111111111111111111111112"

logger = logging.getLogger(__name__)


# Request models - keeping these simple with just the required fields
class TokenMetaRequest(BaseModel):
    token_address: str


class TokenMarketsRequest(BaseModel):
    token_address: str
    sort_by: Optional[str] = None
    program: Optional[list[str]] = None
    page: int = 1
    page_size: int = 10

    @property
    def token_pair(self) -> list[str]:
        """Returns the token pair array with WSOL as the second token"""
        return [self.token_address, WSOL_ADDRESS]

    model_config = ConfigDict(
        json_schema_extra={
            "properties": {"page_size": {"enum": [10, 20, 30, 40, 60, 100]}}
        }
    )


class TokenHoldersRequest(BaseModel):
    token_address: str
    page: int = 1
    page_size: int = 40
    from_amount: Optional[str] = None
    to_amount: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={"properties": {"page_size": {"enum": [10, 20, 30, 40]}}}
    )


class TokenPriceRequest(BaseModel):
    token_address: str
    from_time: Optional[int] = None  # Format: YYYYMMDD
    to_time: Optional[int] = None  # Format: YYYYMMDD


class TokenAccountsRequest(BaseModel):
    wallet_address: str
    type: str = "token"  # Default to fungible tokens
    page: int = 1
    page_size: int = 40
    hide_zero: bool = True

    model_config = ConfigDict(
        json_schema_extra={
            "properties": {
                "type": {"enum": ["token", "nft"]},
                "page_size": {"enum": [10, 20, 30, 40]},
            }
        }
    )


class ActivityType(str, Enum):
    TOKEN_SWAP = "ACTIVITY_TOKEN_SWAP"
    AGG_TOKEN_SWAP = "ACTIVITY_AGG_TOKEN_SWAP"
    TOKEN_ADD_LIQ = "ACTIVITY_TOKEN_ADD_LIQ"
    TOKEN_REMOVE_LIQ = "ACTIVITY_TOKEN_REMOVE_LIQ"
    SPL_TOKEN_STAKE = "ACTIVITY_SPL_TOKEN_STAKE"
    SPL_TOKEN_UNSTAKE = "ACTIVITY_SPL_TOKEN_UNSTAKE"
    TOKEN_DEPOSIT_VAULT = "ACTIVITY_TOKEN_DEPOSIT_VAULT"
    TOKEN_WITHDRAW_VAULT = "ACTIVITY_TOKEN_WITHDRAW_VAULT"
    SPL_INIT_MINT = "ACTIVITY_SPL_INIT_MINT"
    ORDERBOOK_ORDER_PLACE = "ACTIVITY_ORDERBOOK_ORDER_PLACE"


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"


class DefiActivitiesRequest(BaseModel):
    wallet_address: str
    activity_type: Optional[list[ActivityType]] = None
    from_address: Optional[str] = None
    platform: Optional[list[str]] = None
    source: Optional[list[str]] = None
    token: Optional[str] = None
    from_time: Optional[int] = None
    to_time: Optional[int] = None
    page: int = 1
    page_size: int = 100
    sort_by: str = "block_time"
    sort_order: SortOrder = SortOrder.DESC

    model_config = ConfigDict(
        json_schema_extra={
            "properties": {
                "page_size": {"enum": [10, 20, 30, 40, 60, 100]},
                "sort_by": {"enum": ["block_time"]},
            }
        }
    )


class BalanceFlow(str, Enum):
    IN = "in"
    OUT = "out"


class BalanceChangeRequest(BaseModel):
    wallet_address: str
    token_account: Optional[str] = None
    token: Optional[str] = None
    from_time: Optional[int] = None
    to_time: Optional[int] = None
    page_size: int = 100
    page: int = 1
    remove_spam: bool = True
    amount: Optional[list[float]] = None
    flow: Optional[BalanceFlow] = None
    sort_by: str = "block_time"
    sort_order: SortOrder = SortOrder.DESC

    model_config = ConfigDict(
        json_schema_extra={
            "properties": {
                "page_size": {"enum": [10, 20, 30, 40, 60, 100]},
                "sort_by": {"enum": ["block_time"]},
            }
        }
    )


class TransactionDetailRequest(BaseModel):
    tx: str  # Transaction signature/address


class TransactionActionsRequest(BaseModel):
    tx: str  # Transaction signature/address


class SolscanTools(str, Enum):
    TOKEN_META = "token_meta"
    TOKEN_MARKETS = "token_markets"
    TOKEN_HOLDERS = "token_holders"
    TOKEN_PRICE = "token_price"
    TOKEN_ACCOUNTS = "token_accounts"
    DEFI_ACTIVITIES = "defi_activities"
    BALANCE_CHANGE = "balance_change"
    TRANSACTION_DETAIL = "transaction_detail"
    TRANSACTION_ACTIONS = "transaction_actions"


async def make_request(
    endpoint: str, params: Dict[str, Any], api_key: str
) -> Dict[str, Any]:
    """Make a request to the Solscan API"""
    url = f"{SOLSCAN_API_BASE_URL}{endpoint}"
    headers = {"token": api_key}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=params) as response:
            if response.status != 200:
                error_text = await response.text()
                logger.error(f"Error from Solscan API: {error_text}")
                return {"error": f"HTTP {response.status} - {error_text}"}

            return await response.json()


async def get_token_meta(token_address: str, api_key: str) -> Dict[str, Any]:
    """Get token metadata from Solscan API"""
    logger.info(f"Fetching metadata for token {token_address}")
    return await make_request("/token/meta", {"address": token_address}, api_key)


async def get_token_markets(
    token_address: str,
    sort_by: Optional[str] = None,
    program: Optional[list[str]] = None,
    page: int = 1,
    page_size: int = 10,
    api_key: str = "",
) -> Dict[str, Any]:
    """Get token market data and liquidity pools"""
    logger.info(f"Fetching market data for token {token_address}")

    # Validate page_size
    if page_size not in [10, 20, 30, 40, 60, 100]:
        logger.warning(f"Invalid page_size {page_size}, defaulting to 10")
        page_size = 10

    # Build params
    params: Dict[str, Any] = {
        "token": [token_address, WSOL_ADDRESS],
        "page": page,
        "page_size": page_size,
    }

    # Add optional params if provided
    if sort_by:
        params["sort_by"] = sort_by
    if program:
        if len(program) > 5:
            logger.warning("Program list exceeds maximum of 5, truncating")
            program = program[:5]
        params["program"] = program

    return await make_request("/token/markets", params, api_key)


async def get_token_holders(
    token_address: str,
    page: int = 1,
    page_size: int = 40,
    from_amount: Optional[str] = None,
    to_amount: Optional[str] = None,
    api_key: str = "",
) -> Dict[str, Any]:
    """Get token holder distribution"""
    logger.info(f"Fetching holders for token {token_address}")

    # Validate page_size
    if page_size not in [10, 20, 30, 40]:
        logger.warning(f"Invalid page_size {page_size}, defaulting to 40")
        page_size = 40

    # Build params
    params: Dict[str, Any] = {
        "address": token_address,
        "page": page,
        "page_size": page_size,
    }

    # Add optional amount filters if provided
    if from_amount:
        params["from_amount"] = from_amount
    if to_amount:
        params["to_amount"] = to_amount

    return await make_request("/token/holders", params, api_key)


async def get_token_price(
    token_address: str,
    time_from: Optional[int] = None,
    time_to: Optional[int] = None,
    api_key: str = "",
) -> Dict[str, Any]:
    """Get historical token price data"""
    logger.info(f"Fetching price history for token {token_address}")

    # Build params
    params: Dict[str, Any] = {
        "address": token_address,
    }

    # Add optional time parameters
    if time_from is not None:
        params["from_time"] = time_from
    if time_to is not None:
        params["to_time"] = time_to

    return await make_request("/token/price", params, api_key)


async def get_token_accounts(
    wallet_address: str,
    type: str = "token",
    page: int = 1,
    page_size: int = 40,
    hide_zero: bool = True,
    api_key: str = "",
) -> Dict[str, Any]:
    """Get token holdings for a wallet"""
    logger.info(f"Fetching token accounts for wallet {wallet_address}")

    # Validate type
    if type not in ["token", "nft"]:
        logger.warning(f"Invalid type {type}, defaulting to 'token'")
        type = "token"

    # Validate page_size
    if page_size not in [10, 20, 30, 40]:
        logger.warning(f"Invalid page_size {page_size}, defaulting to 40")
        page_size = 40

    # Build params
    params: Dict[str, Any] = {
        "address": wallet_address,
        "type": type,
        "page": page,
        "page_size": page_size,
        "hide_zero": "true"
        if hide_zero
        else "false",  # API expects string 'true' or 'false'
    }

    return await make_request("/account/token-accounts", params, api_key)


async def get_defi_activities(
    wallet_address: str,
    activity_type: Optional[list[ActivityType]] = None,
    from_address: Optional[str] = None,
    platform: Optional[list[str]] = None,
    source: Optional[list[str]] = None,
    token: Optional[str] = None,
    from_time: Optional[int] = None,
    to_time: Optional[int] = None,
    page: int = 1,
    page_size: int = 100,
    sort_by: str = "block_time",
    sort_order: SortOrder = SortOrder.DESC,
    api_key: str = "",
) -> Dict[str, Any]:
    """Get DeFi activities for a wallet"""
    logger.info(f"Fetching DeFi activities for wallet {wallet_address}")

    # Validate page_size
    if page_size not in [10, 20, 30, 40, 60, 100]:
        logger.warning(f"Invalid page_size {page_size}, defaulting to 100")
        page_size = 100

    # Build base params
    params: Dict[str, Any] = {
        "address": wallet_address,
        "page": page,
        "page_size": page_size,
        "sort_by": sort_by,
        "sort_order": sort_order.value.lower(),
    }

    # Add optional filters
    if activity_type:
        params["activity_type"] = [t.value for t in activity_type]
    if from_address:
        params["from"] = from_address
    if platform:
        if len(platform) > 5:
            logger.warning("Platform list exceeds maximum of 5, truncating")
            platform = platform[:5]
        params["platform"] = platform
    if source:
        if len(source) > 5:
            logger.warning("Source list exceeds maximum of 5, truncating")
            source = source[:5]
        params["source"] = source
    if token:
        params["token"] = token
    if from_time:
        params["from_time"] = from_time
    if to_time:
        params["to_time"] = to_time

    return await make_request("/account/defi/activities", params, api_key)


async def get_balance_change(
    wallet_address: str,
    token_account: Optional[str] = None,
    token: Optional[str] = None,
    from_time: Optional[int] = None,
    to_time: Optional[int] = None,
    page_size: int = 100,
    page: int = 1,
    remove_spam: bool = True,
    amount: Optional[list[float]] = None,
    flow: Optional[BalanceFlow] = None,
    sort_by: str = "block_time",
    sort_order: SortOrder = SortOrder.DESC,
    api_key: str = "",
) -> Dict[str, Any]:
    """Get detailed balance change activities"""
    logger.info(f"Fetching balance changes for wallet {wallet_address}")

    # Validate page_size
    if page_size not in [10, 20, 30, 40, 60, 100]:
        logger.warning(f"Invalid page_size {page_size}, defaulting to 100")
        page_size = 100

    # Build base params
    params: Dict[str, Any] = {
        "address": wallet_address,
        "page": page,
        "page_size": page_size,
        "remove_spam": "true" if remove_spam else "false",
        "sort_by": sort_by,
        "sort_order": sort_order.value.lower(),
    }

    # Add optional filters
    if token_account:
        params["token_account"] = token_account
    if token:
        params["token"] = token
    if from_time:
        params["from_time"] = from_time
    if to_time:
        params["to_time"] = to_time
    if amount and len(amount) == 2:
        params["amount[]"] = amount
    if flow:
        params["flow"] = flow.value

    return await make_request("/account/balance_change", params, api_key)


async def get_transaction_detail(tx: str, api_key: str) -> Dict[str, Any]:
    """Get detailed transaction information including parsed data like token/SOL balance changes, IDL data, and DeFi activities"""
    logger.info(f"Fetching transaction details for {tx}")
    return await make_request("/transaction/detail", {"tx": tx}, api_key)


async def get_transaction_actions(tx: str, api_key: str) -> Dict[str, Any]:
    """Get transaction actions and token transfers"""
    logger.info(f"Fetching transaction actions for {tx}")
    return await make_request("/transaction/actions", {"tx": tx}, api_key)


async def serve(api_key: str) -> None:
    """Start the MCP server"""
    if not api_key:
        raise ValueError("Solscan API key is required")

    server = Server("mcp-solscan")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name=SolscanTools.TOKEN_META,
                description="Get token metadata",
                inputSchema=TokenMetaRequest.model_json_schema(),
            ),
            Tool(
                name=SolscanTools.TOKEN_MARKETS,
                description="Get token market data and liquidity pools",
                inputSchema=TokenMarketsRequest.model_json_schema(),
            ),
            Tool(
                name=SolscanTools.TOKEN_HOLDERS,
                description="Get token holder distribution",
                inputSchema=TokenHoldersRequest.model_json_schema(),
            ),
            Tool(
                name=SolscanTools.TOKEN_PRICE,
                description="Get historical token price data",
                inputSchema=TokenPriceRequest.model_json_schema(),
            ),
            Tool(
                name=SolscanTools.TOKEN_ACCOUNTS,
                description="Get token holdings for a wallet",
                inputSchema=TokenAccountsRequest.model_json_schema(),
            ),
            Tool(
                name=SolscanTools.DEFI_ACTIVITIES,
                description="Get DeFi activities for a wallet",
                inputSchema=DefiActivitiesRequest.model_json_schema(),
            ),
            Tool(
                name=SolscanTools.BALANCE_CHANGE,
                description="Get detailed balance change activities",
                inputSchema=BalanceChangeRequest.model_json_schema(),
            ),
            Tool(
                name=SolscanTools.TRANSACTION_DETAIL,
                description="Get detailed transaction information",
                inputSchema=TransactionDetailRequest.model_json_schema(),
            ),
            Tool(
                name=SolscanTools.TRANSACTION_ACTIONS,
                description="Get transaction actions and token transfers",
                inputSchema=TransactionActionsRequest.model_json_schema(),
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        try:
            match name:
                case SolscanTools.TOKEN_META:
                    result = await get_token_meta(arguments["token_address"], api_key)

                case SolscanTools.TOKEN_MARKETS:
                    result = await get_token_markets(
                        arguments["token_address"],
                        arguments.get("sort_by"),
                        arguments.get("program"),
                        arguments.get("page", 1),
                        arguments.get("page_size", 10),
                        api_key,
                    )

                case SolscanTools.TOKEN_HOLDERS:
                    result = await get_token_holders(
                        arguments["token_address"],
                        arguments.get("page", 1),
                        arguments.get("page_size", 40),
                        arguments.get("from_amount"),
                        arguments.get("to_amount"),
                        api_key,
                    )

                case SolscanTools.TOKEN_PRICE:
                    result = await get_token_price(
                        arguments["token_address"],
                        arguments.get("from_time"),
                        arguments.get("to_time"),
                        api_key,
                    )

                case SolscanTools.TOKEN_ACCOUNTS:
                    result = await get_token_accounts(
                        arguments["wallet_address"],
                        arguments.get("type", "token"),
                        arguments.get("page", 1),
                        arguments.get("page_size", 40),
                        arguments.get("hide_zero", True),
                        api_key,
                    )

                case SolscanTools.DEFI_ACTIVITIES:
                    # Convert activity_type strings to enum if provided
                    activity_types = None
                    if raw_types := arguments.get("activity_type"):
                        activity_types = [ActivityType(t) for t in raw_types]

                    result = await get_defi_activities(
                        arguments["wallet_address"],
                        activity_type=activity_types,
                        from_address=arguments.get("from_address"),
                        platform=arguments.get("platform"),
                        source=arguments.get("source"),
                        token=arguments.get("token"),
                        from_time=arguments.get("from_time"),
                        to_time=arguments.get("to_time"),
                        page=arguments.get("page", 1),
                        page_size=arguments.get("page_size", 100),
                        sort_by=arguments.get("sort_by", "block_time"),
                        sort_order=SortOrder(
                            arguments.get("sort_order", "desc").lower()
                        ),
                        api_key=api_key,
                    )

                case SolscanTools.BALANCE_CHANGE:
                    # Convert flow string to enum if provided
                    flow_enum = None
                    if flow_str := arguments.get("flow"):
                        flow_enum = BalanceFlow(flow_str.lower())

                    result = await get_balance_change(
                        arguments["wallet_address"],
                        token_account=arguments.get("token_account"),
                        token=arguments.get("token"),
                        from_time=arguments.get("from_time"),
                        to_time=arguments.get("to_time"),
                        page_size=arguments.get("page_size", 100),
                        page=arguments.get("page", 1),
                        remove_spam=arguments.get("remove_spam", True),
                        amount=arguments.get("amount"),
                        flow=flow_enum,
                        sort_by=arguments.get("sort_by", "block_time"),
                        sort_order=SortOrder(
                            arguments.get("sort_order", "desc").lower()
                        ),
                        api_key=api_key,
                    )

                case SolscanTools.TRANSACTION_DETAIL:
                    result = await get_transaction_detail(arguments["tx"], api_key)

                case SolscanTools.TRANSACTION_ACTIONS:
                    result = await get_transaction_actions(arguments["tx"], api_key)

                case _:
                    raise ValueError(f"Unknown tool: {name}")

            return [TextContent(type="text", text=str(result))]
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return [TextContent(type="text", text=str({"error": str(e)}))]

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)
