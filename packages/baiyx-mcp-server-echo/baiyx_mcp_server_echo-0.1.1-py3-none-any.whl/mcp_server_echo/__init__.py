"""
FastMCP Echo Server
"""
from typing import Optional
import uvicorn
from mcp.server.fastmcp import FastMCP

# Create server
app = FastMCP("Echo Server")


@app.tool()
def echo_tool(text: str) -> str:
    """Echo the input text"""
    return text


@app.resource("echo://static")
def echo_resource() -> str:
    return "Echo!"


@app.resource("echo://{text}")
def echo_template(text: str) -> str:
    """Echo the input text"""
    return f"Echo: {text}"


@app.prompt("echo")
def echo_prompt(text: str) -> str:
    return text


def main(host: str = "127.0.0.1", port: int = 8000) -> None:
    """Start the MCP Echo Server"""
    uvicorn.run(app, host=host, port=port) 