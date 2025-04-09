from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass
import os
import httpx
from mcp.server.fastmcp import FastMCP, Context

# API endpoints and constants
ORCA_API_HOST = os.environ.get("ORCA_API_HOST", "https://api.orcasecurity.io")
ORCA_AUTH_TOKEN = os.environ.get("ORCA_AUTH_TOKEN", "")
ORCA_REQUEST_TIMEOUT = float(os.environ.get("ORCA_REQUEST_TIMEOUT", "30.0"))
COMMON_HEADERS = {"Content-Type": "application/json", "User-Agent": "orca"}


class TokenAuth(httpx.Auth):
    """Token authentication for httpx."""

    def __init__(self, token: str):
        """Initialize with the token."""
        if not token:
            raise ValueError("Authentication token cannot be empty")
        self.token = token

    def auth_flow(self, request):
        """Add the bearer token to the request with automatic refresh."""
        # Add the token to the request
        request.headers["Authorization"] = f"Token {self.token}"
        yield request


@dataclass
class AppContext:
    client: httpx.AsyncClient


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with type-safe context"""
    # Initialize on startup
    client = httpx.AsyncClient(
        headers=COMMON_HEADERS,
        auth=TokenAuth(ORCA_AUTH_TOKEN),
        timeout=ORCA_REQUEST_TIMEOUT,
    )
    try:
        yield AppContext(client=client)
    finally:
        # Cleanup on shutdown
        await client.aclose()


mcp = FastMCP("OrcaMCP", lifespan=app_lifespan)


@mcp.tool()
async def ask_orca(ctx: Context, question: str) -> dict:
    """
    Ask Orca Security a question in natural language and get results about security issues in the client's cloud environment.
    The tool can handle simple questions like 'Am I vulnerable to X?' or 'Show me which vms are exposed to the internet.'
    Don't overcomplicate and overuse this tool. Give it as much context as possible.
    """
    client = ctx.request_context.lifespan_context.client
    try:
        ai_sonar_resp = await client.post(
            f"{ORCA_API_HOST}/api/ai_sonar/sonar_schema/query",
            json={"search": question, "target_schema": "serving_layer"},
        )
        ai_sonar_resp.raise_for_status()
        ai_sonar_data = ai_sonar_resp.json()

        query = ai_sonar_data.get("sonar_optimized_payload", {}).get("query")
        if not query:
            return {
                "status": "error",
                "error": "Orca AI Sonar couldn't generate a query for your question.",
            }

        query_resp = await client.post(
            f"{ORCA_API_HOST}/api/serving-layer/query",
            json={"query": query, "start_at_index": 0, "limit": 10},
        )
        query_resp.raise_for_status()
        query_results = query_resp.json()

        if not query_results:
            return {"status": "error", "error": "No results found for your query."}

        return query_results
    except Exception as e:
        return {
            "status": "error",
            "error": f"Unable to get results from Orca Security: {e}",
        }


def main():
    mcp.run()
