# server.py
from mcp.server.fastmcp import FastMCP
from typing import Any
import httpx
import urllib.parse


# Create an MCP server
mcp = FastMCP("Demo")

PORTAL_API_BASE = "http://portal-service.nimbus.test"
USER_AGENT = "portals-app/1.0"

async def make_portal_request(portal_domain: str, path: str) -> dict[str, Any] | None:
    """Make a request to the portals API with proper error handling."""
    headers = {
        "x-secret": "devsupersecret"
    }
    full_url = f"{PORTAL_API_BASE}/v1/contents?path={urllib.parse.quote(path)}&portalDomain={portal_domain}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(full_url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
async def get_portal_data(portal_domain: str = 'alfa.p.dev-thefusebase.com', path: str = '/') -> dict:
    """Get portal configuration data.

    Args:
        portal_domain: Optional domain of the portal to fetch data for
        path: Optional path within the portal to fetch data for
    """
    # Make request to portal service to get configuration
    portal_data = await make_portal_request(portal_domain=portal_domain, path=path)
    
    if not portal_data:
        return {
            "error": "Unable to fetch portal configuration"
        }
    
    return portal_data


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


if __name__ == "__main__":
    mcp.run()