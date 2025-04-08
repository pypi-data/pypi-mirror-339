import os

def handle_config(result):
    """
    Rounds the result if the MCP_ROUND environment variable is set to 'true'.
    """
    if os.getenv("MCP_ROUND") == "true":
        return round(result)
    return result