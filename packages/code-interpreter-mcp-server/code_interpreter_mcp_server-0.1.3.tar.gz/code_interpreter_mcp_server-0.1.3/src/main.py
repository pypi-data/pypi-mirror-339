"""Main module for code-interpreter-mcp-server."""
from src.server import mcp
import pandas as pd
import openpyxl

def main():
    """Run the MCP Python Interpreter server."""
    mcp.run()


if __name__ == "__main__":
    main()