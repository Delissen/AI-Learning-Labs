# ============================================================================
# Lab004 - Local MCP Server
# ============================================================================
#
# Description
# -----------
# This file implements a local Model Context Protocol (MCP) server.
#
# The server exposes business functionality ("tools") that can be called
# dynamically by an AI Agent.
#
# In this example two inventory tools are published:
#
#   • get_inventory_levels()
#   • get_weekly_sales()
#
# The AI Agent does not call these functions directly.
# Instead it discovers them through the MCP protocol.
#
#
# Architecture
# ------------
#
#        Azure AI Agent
#               │
#               ▼
#          MCP Client
#               │
#               ▼
#          Local MCP Server
#               │
#      ┌────────┴────────┐
#      ▼                 ▼
# get_inventory()   get_weekly_sales()
#
# ============================================================================

# Add references
from fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP(name="Inventory")

# Add an inventory check mcp tool
@mcp.tool()
def get_inventory_levels() -> dict:
    """Returns current inventory for all products."""
    return {
        "Moisturizer": 6,
        "Shampoo": 8,
        "Body Spray": 28,
        "Hair Gel": 5, 
        "Lip Balm": 12,
        "Skin Serum": 9,
        "Cleanser": 30,
        "Conditioner": 3,
        "Setting Powder": 17,
        "Dry Shampoo": 45
    }

# Add a weekly sales mcp tool
@mcp.tool()
def get_weekly_sales() -> dict:
    """Returns number of units sold last week."""
    return {
        "Moisturizer": 22,
        "Shampoo": 18,
        "Body Spray": 3,
        "Hair Gel": 2,
        "Lip Balm": 14,
        "Skin Serum": 19,
        "Cleanser": 4,
        "Conditioner": 1,
        "Setting Powder": 13,
        "Dry Shampoo": 17
    }

# Run the MCP server
mcp.run(show_banner=False)