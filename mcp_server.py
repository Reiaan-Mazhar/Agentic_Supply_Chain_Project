# Part B: Task 1 - Standalone MCP Server
import json

class ShippingMCPServer:
    def __init__(self):
        # Task 1: Structured Tool Definitions with JSON-Schema
        self._tools = {
            "calculate_freight": {
                "description": "Calculates air/sea freight costs based on weight and destination.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "weight_kg": {"type": "number", "description": "Weight of the package in kg"},
                        "destination": {"type": "string", "enum": ["Singapore", "Taiwan", "Karachi"]}
                    },
                    "required": ["weight_kg", "destination"]
                }
            },
            "verify_customs_id": {
                "description": "Checks if a Business Tax ID is valid for international logistics.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "tax_id": {"type": "string", "description": "The 9-digit alphanumeric tax ID"}
                    },
                    "required": ["tax_id"]
                }
            }
        }

    # --- PROTOCOL LAYER: Discovery ---
    # MCP Endpoint: tools/list
    def handle_discovery(self):
        """Standard MCP 'tools/list' endpoint simulation."""
        return {"tools": self._tools}

    # --- PROTOCOL LAYER: Execution ---
    # MCP Endpoint: tools/call
    def handle_call(self, tool_name, arguments):
        """Standard MCP 'tools/call' endpoint simulation."""
        print(f"[SERVER]: Executing tool '{tool_name}' with args: {arguments}")
        
        if tool_name == "calculate_freight":
            weight = arguments.get("weight_kg", 0)
            dest = arguments.get("destination", "Unknown")
            cost = weight * (25.0 if dest == "Singapore" else 15.0)
            return {"status": "success", "result": {"total_cost": cost, "currency": "USD"}}
        
        elif tool_name == "verify_customs_id":
            tax_id = arguments.get("tax_id", "")
            is_valid = len(tax_id) == 9
            return {"status": "success", "result": {"valid": is_valid, "clearance": "Standard"}}
        
        return {"status": "error", "message": "Tool not found"}

# Export the server instance
mcp_server = ShippingMCPServer()