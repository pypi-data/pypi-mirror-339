# solscan-mcp-server: A Solscan Pro API MCP Server

## Overview

A Model Context Protocol server for interacting with the Solscan Pro API. This server provides tools to query token information, account activities, and transaction details on the Solana blockchain via Large Language Models.

Please note that solscan-mcp-server requires a Solscan Pro API key to function. You can obtain one from [Solscan APIs](https://solscan.io/apis).

### Tools

1. `token_meta`

   - Get token metadata
   - Input:
     - `token_address` (string): A token address on Solana blockchain
   - Returns: Token metadata including name, symbol, price, market cap, etc.

2. `token_markets`

   - Get token market data and liquidity pools
   - Inputs:
     - `token_address` (string): Token address to query
     - `sort_by` (string, optional): Field to sort by
     - `program` (string[], optional): Filter by program addresses (max 5)
     - `page` (number, optional): Page number (default: 1)
     - `page_size` (number, optional): Items per page (10, 20, 30, 40, 60, 100)
   - Returns: Market data and liquidity pools for the token paired with WSOL

3. `token_holders`

   - Get token holder distribution
   - Inputs:
     - `token_address` (string): Token address to query
     - `page` (number, optional): Page number (default: 1)
     - `page_size` (number, optional): Items per page (10, 20, 30, 40)
     - `from_amount` (string, optional): Minimum token holding amount
     - `to_amount` (string, optional): Maximum token holding amount
   - Returns: List of token holders with their balances

4. `token_price`

   - Get historical token price data
   - Inputs:
     - `token_address` (string): Token address to query
     - `from_time` (number, optional): Start date in YYYYMMDD format (e.g., 20240701)
     - `to_time` (number, optional): End date in YYYYMMDD format (e.g., 20240715)
   - Returns: Historical price data for the specified date range

5. `token_accounts`

   - Get token holdings for a wallet
   - Inputs:
     - `wallet_address` (string): Wallet address to query
     - `type` (string, optional): Token type ("token" or "nft", default: "token")
     - `page` (number, optional): Page number (default: 1)
     - `page_size` (number, optional): Items per page (10, 20, 30, 40)
     - `hide_zero` (boolean, optional): Hide zero balance tokens (default: true)
   - Returns: List of token holdings for the wallet

6. `defi_activities`

   - Get DeFi activities for a wallet
   - Inputs:
     - `wallet_address` (string): Wallet address to query
     - `activity_type` (string[], optional): Types of activities to filter
     - `from_address` (string, optional): Filter activities from an address
     - `platform` (string[], optional): Filter by platform addresses (max 5)
     - `source` (string[], optional): Filter by source addresses (max 5)
     - `token` (string, optional): Filter by token address
     - `from_time` (number, optional): Start date in YYYYMMDD format (e.g., 20240701)
     - `to_time` (number, optional): End date in YYYYMMDD format (e.g., 20240715)
     - `page` (number, optional): Page number (default: 1)
     - `page_size` (number, optional): Items per page (10, 20, 30, 40, 60, 100)
     - `sort_by` (string, optional): Sort field (default: "block_time")
     - `sort_order` (string, optional): Sort order ("asc" or "desc", default: "desc")
   - Returns: List of DeFi activities

7. `balance_change`

   - Get detailed balance change activities
   - Inputs:
     - `wallet_address` (string): Wallet address to query
     - `token_account` (string, optional): Token account to filter
     - `token` (string, optional): Token address to filter
     - `from_time` (number, optional): Start date in YYYYMMDD format (e.g., 20240701)
     - `to_time` (number, optional): End date in YYYYMMDD format (e.g., 20240715)
     - `page_size` (number, optional): Items per page (10, 20, 30, 40, 60, 100)
     - `page` (number, optional): Page number (default: 1)
     - `remove_spam` (boolean, optional): Remove spam activities (default: true)
     - `amount` (number[], optional): Filter by amount range [min, max]
     - `flow` (string, optional): Filter by direction ("in" or "out")
     - `sort_by` (string, optional): Sort field (default: "block_time")
     - `sort_order` (string, optional): Sort order ("asc" or "desc", default: "desc")
   - Returns: List of balance change activities

8. `transaction_detail`

   - Get detailed transaction information
   - Input:
     - `tx` (string): Transaction signature/address
   - Returns: Detailed transaction data including parsed instructions

9. `transaction_actions`
   - Get transaction actions and token transfers
   - Input:
     - `tx` (string): Transaction signature/address
   - Returns: List of actions and token transfers in the transaction

## Installation

### Using uv (recommended)

When using [`uv`](https://docs.astral.sh/uv/) no specific installation is needed. We will
use [`uvx`](https://docs.astral.sh/uv/guides/tools/) to directly run _solscan-mcp-server_.

### Using PIP

Alternatively you can install `solscan-mcp-server` via pip:

```
pip install solscan-mcp-server
```

After installation, you can run it as a script using:

```
python -m solscan_mcp_server
```

## Configuration

The server requires a Solscan Pro API key to be set in the environment:

```bash
export SOLSCAN_API_KEY="your-api-key-here"
```

### Usage with Claude Desktop

Add this to your `claude_desktop_config.json`:

<details>
<summary>Using uvx</summary>

```json
"mcpServers": {
  "solscan": {
    "command": "uvx",
    "args": ["solscan-mcp-server"]
  }
}
```

</details>

<details>
<summary>Using pip installation</summary>

```json
"mcpServers": {
  "solscan": {
    "command": "python",
    "args": ["-m", "solscan_mcp_server"]
  }
}
```

</details>

### Usage with [Zed](https://github.com/zed-industries/zed)

Add to your Zed settings.json:

<details>
<summary>Using uvx</summary>

```json
"context_servers": [
  "solscan": {
    "command": {
      "path": "uvx",
      "args": ["solscan-mcp-server"]
    }
  }
],
```

</details>

<details>
<summary>Using pip installation</summary>

```json
"context_servers": {
  "solscan_mcp_server": {
    "command": {
      "path": "python",
      "args": ["-m", "solscan_mcp_server"]
    }
  }
},
```

</details>

## Debugging

You can use the MCP inspector to debug the server. For uvx installations:

```
npx @modelcontextprotocol/inspector uvx solscan-mcp-server
```

Or if you've installed the package in a specific directory or are developing on it:

```
cd path/to/servers/src/solscan
npx @modelcontextprotocol/inspector uv run solscan_mcp_server
```

Running `tail -n 20 -f ~/Library/Logs/Claude/mcp*.log` will show the logs from the server and may
help you debug any issues.

## Development

If you are doing local development, you can test your changes using the MCP inspector or the Claude desktop app.

For Claude desktop app, add the following to your `claude_desktop_config.json`:

### UVX

```json
{
"mcpServers": {
  "solscan": {
    "command": "uv",
    "args": [
      "--directory",
      "/<path to mcp-servers>/mcp-servers/src/solscan",
      "run",
      "solscan_mcp_server"
    ]
  }
}
```

## Docker Support

The MCP server can be run in a Docker container. This provides an isolated environment and makes deployment easier.

### Building the Docker Image

```bash
# Build the image
docker build -t solscan-mcp-server .
```

### Running with Docker

```bash
# Run the container with your Solscan Pro API key
docker run -e SOLSCAN_API_KEY=your_api_key_here solscan-mcp-server

# Run with custom verbosity level
docker run -e SOLSCAN_API_KEY=your_api_key_here solscan-mcp-server --verbose

# Run in detached mode
docker run -d -e SOLSCAN_API_KEY=your_api_key_here solscan-mcp-server
```

### Environment Variables

The Docker container accepts the following environment variables:

- `SOLSCAN_API_KEY` (required): Your Solscan Pro API key

### Docker Best Practices

1. Never commit your API key in the Dockerfile or docker-compose files
2. Use environment files or secure secrets management for the API key
3. Consider using Docker health checks in production
4. The container runs as a non-root user for security

## License

This MCP server is licensed under the MIT License. This means you are free to use, modify, and distribute the software, subject to the terms and conditions of the MIT License. For more details, please see the LICENSE file in the project repository.
