"""
FastMCP Echo Server
"""
import asyncio
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


async def serve() -> None:
    """Start the MCP Echo Server"""
    print("\n🔊 MCP Echo Server starting...")
    print("✨ Server is ready to handle requests!\n")
    await mcp.run_stdio_async()


def main() -> None:
    """Main entry point for the Echo Server"""
    asyncio.run(serve()) 