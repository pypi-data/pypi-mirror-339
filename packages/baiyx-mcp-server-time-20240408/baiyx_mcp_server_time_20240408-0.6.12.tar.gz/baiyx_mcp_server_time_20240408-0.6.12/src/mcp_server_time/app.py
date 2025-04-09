from .server import TimeServer

server = TimeServer("Asia/Shanghai")
app = server.mcp 