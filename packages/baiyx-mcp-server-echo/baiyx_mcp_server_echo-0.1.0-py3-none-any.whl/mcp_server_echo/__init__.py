"""
FastMCP Echo Server
"""
from typing import Optional
import uvicorn
from mcp.server.fastmcp import FastMCP

# Create server
mcp = FastMCP("Echo Server")


@mcp.tool()
def echo_tool(text: str) -> str:
    """Echo the input text"""
    return text


@mcp.resource("echo://static")
def echo_resource() -> str:
    return "Echo!"


@mcp.resource("echo://{text}")
def echo_template(text: str) -> str:
    """Echo the input text"""
    return f"Echo: {text}"


@mcp.prompt("echo")
def echo_prompt(text: str) -> str:
    return text


def main(host: str = "127.0.0.1", port: int = 8000) -> None:
    """Start the MCP Echo Server"""
    uvicorn.run(mcp.app, host=host, port=port) 