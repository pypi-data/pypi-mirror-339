import asyncio
from mcp_server_time.server import TimeServer

server = TimeServer("Asia/Shanghai")
app = server.mcp

def main():
    """MCP Time Server - Time and timezone conversion functionality for MCP"""
    import argparse

    parser = argparse.ArgumentParser(
        description="give a model the ability to handle time queries and timezone conversions"
    )
    parser.add_argument("--local-timezone", type=str, help="Override local timezone")

    args = parser.parse_args()
    asyncio.run(server.mcp.run_stdio_async())


if __name__ == "__main__":
    main()
