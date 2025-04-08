import argparse
import os
import random
import sys
import json
import platform
import subprocess
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from .utils import handle_config

mcp = FastMCP("maths")


@mcp.tool(name="add", description="Add two numbers")
def add(a: float, b: float):
    return handle_config(float(a) + float(b))

@mcp.tool(name="sub", description="Subtract two numbers")
def sub(a: float, b: float):
    return handle_config(float(a) - float(b))

@mcp.tool(name="mul", description="Multiply two numbers")
def mul(a: float, b: float):
    return handle_config(float(a) * float(b))

@mcp.tool(name="div", description="Divide two numbers")
def div(a: float, b: float):
    return handle_config(float(a) / float(b))

@mcp.tool(name="random_number_generator", description="Get a random number")
def random_number(start=0, end=100):
    return random.randint(start, end)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run the Maths MCP server.")
    parser.add_argument(
        "--rounded",
        type=bool,
        help="Should the output be rounded to the nearest whole number?",
    )
    parser.add_argument(
        "--install",
        choices=["claude", "cursor"],
        help="Install method to use: 'claude' or 'cursor'."
    )
    return parser.parse_args()

def is_command_available(command: str) -> bool:
    return subprocess.call(["which" if platform.system() != "Windows" else "where", command],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

def get_user_rounded_choice():
    choice = input("Do you want to enable --rounded in Claude config? (y/n): ").strip().lower()
    return choice == "y"

def install_for_claude():
    if not is_command_available("maths-mcp"):
        print("`maths-mcp` not found globally. Installing with pip...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "maths-mcp"])
    else:
        print("`maths-mcp` found globally.")

    rounded = get_user_rounded_choice()

    if platform.system() == "Windows":
        config_path = Path(os.getenv("APPDATA")) / "Claude" / "claude_desktop_config.json"
    else:
        config_path = Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json"

    config_path.parent.mkdir(parents=True, exist_ok=True)
    if config_path.exists():
        with config_path.open("r", encoding="utf-8") as f:
            try:
                config_data = json.load(f)
            except json.JSONDecodeError:
                config_data = {}
    else:
        config_data = {}

    config_data.setdefault("mcpServers", {})
    config_data["mcpServers"]["maths"] = {
        "command": "pipx",
        "args": ["run", "maths-mcp" "--rounded=ROUNDED"] if rounded else ["run", "maths-mcp"]
    }

    with config_path.open("w", encoding="utf-8") as f:
        json.dump(config_data, f, indent=4)

    print(f"✅ Claude config updated at: {config_path}")
    print("🎉 You can now restart Claude Desktop to use maths-mcp.")

def main():
    args = parse_arguments()

    if args.install == "claude":
        install_for_claude()
        return

    if args.rounded:
        os.environ["MCP_ROUND"] = "true"

    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
