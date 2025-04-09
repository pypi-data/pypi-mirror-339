import asyncio
from mcp_server_excel.server import ExcelServer, serve

server = ExcelServer()
app = server.mcp

def main():
    asyncio.run(serve()) 