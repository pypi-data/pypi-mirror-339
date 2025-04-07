#!/usr/bin/env python3
"""
MCP Config Manager CLI - A utility to manage MCP server configurations
for both Windsurf and Cursor platforms.
"""

import os
import sys
import json
import click
import requests
from pathlib import Path
from tabulate import tabulate
import re
from urllib.parse import urlparse
import shutil

# Constants
DEFAULT_CONFIG_DIR = os.path.expanduser("~/.codeium/windsurf")
DEFAULT_CONFIG_FILE = "mcp_config.json"
CURSOR_CONFIG_DIR = os.path.expanduser("~/.cursor")
CURSOR_CONFIG_FILE = "mcp.json"

def load_config(cursor=False):
    """Load the MCP configuration file."""
    if cursor:
        config_path = os.path.join(CURSOR_CONFIG_DIR, CURSOR_CONFIG_FILE)
    else:
        config_path = os.path.join(DEFAULT_CONFIG_DIR, DEFAULT_CONFIG_FILE)
    
    if not os.path.exists(config_path):
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        # Create a default config file
        default_config = {"mcpServers": {}}
        with open(config_path, "w") as f:
            json.dump(default_config, f, indent=2)
        return default_config
    
    # Load existing config
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        
        # Ensure the mcpServers key exists
        if "mcpServers" not in config:
            config["mcpServers"] = {}
            
        return config
    except json.JSONDecodeError:
        click.echo(f"Error: {config_path} is not a valid JSON file.")
        return {"mcpServers": {}}

def save_config(config, config_path, cursor=False):
    """Save the MCP server configuration."""
    # Create a backup of the existing config
    if os.path.exists(config_path):
        backup_path = f"{config_path}.bak"
        shutil.copy2(config_path, backup_path)
        click.echo(f"Backup created at {backup_path}")
    
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    
    # Save the config
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    
    click.echo(f"Configuration saved to {config_path}")

def check_pypi_package(package_name):
    """Check if a package exists on PyPI and get its latest version."""
    try:
        response = requests.get(f"https://pypi.org/pypi/{package_name}/json", timeout=5)
        if response.status_code == 200:
            data = response.json()
            version = data["info"]["version"]
            click.echo(f"Found package '{package_name}' on PyPI (version {version})")
            return True, version
        else:
            click.echo(f"Package '{package_name}' not found on PyPI")
            return False, None
    except Exception as e:
        click.echo(f"Error checking PyPI: {e}")
        return False, None

@click.group()
@click.option('--cursor', is_flag=True, help='Use Cursor configuration')
@click.pass_context
def cli(ctx, cursor):
    """Manage MCP server configurations."""
    ctx.ensure_object(dict)
    
    if cursor:
        ctx.obj["CONFIG_PATH"] = os.path.join(CURSOR_CONFIG_DIR, CURSOR_CONFIG_FILE)
        ctx.obj["CONFIG"] = load_config(cursor=True)
        ctx.obj["CURSOR"] = True
    else:
        ctx.obj["CONFIG_PATH"] = os.path.join(DEFAULT_CONFIG_DIR, DEFAULT_CONFIG_FILE)
        ctx.obj["CONFIG"] = load_config(cursor=False)
        ctx.obj["CURSOR"] = False

@cli.command()
@click.argument('name', required=True)
@click.option('--server-url', 'server_url', help='URL of the MCP server (for Windsurf)')
@click.option('--url', help='URL of the MCP server (for Cursor)')
@click.option('--package', help='Package name to use with pipx or npx')
@click.option('--pipx', is_flag=True, help='Use pipx to run the package')
@click.option('--npx', is_flag=True, help='Use npx to run the package')
@click.option('--cursor', is_flag=True, help='Configure for Cursor')
@click.option('--proxy', is_flag=True, help='Configure as a proxy with command and args (Windsurf only)')
@click.option('--command', help='Command to run for proxy servers (Windsurf only)')
@click.option('--args', help='Arguments for the command (Windsurf only)')
@click.option('--env', help='Environment variables in KEY=VALUE format (Windsurf only). For multiple variables, use a comma-separated list: KEY1=VALUE1,KEY2=VALUE2')
@click.pass_context
def add(ctx, name, server_url, url, package, pipx, npx, cursor, proxy, command, args, env):
    """Add a new MCP server configuration."""
    # Override cursor flag from context if provided
    cursor = cursor or ctx.obj.get("CURSOR", False)
    config = ctx.obj['CONFIG']
    config_path = ctx.obj['CONFIG_PATH']
    
    if pipx and npx:
        click.echo("Error: Cannot specify both --pipx and --npx")
        return
        
    if (pipx or npx) and not package:
        click.echo("Error: --package is required when using --pipx or --npx")
        return
    
    # Get the URL based on the platform
    if cursor:
        server_url = url or server_url
    
    # Check if the server already exists
    if name in config["mcpServers"]:
        click.echo(f"Error: MCP server '{name}' already exists")
        return
        
    # Handle different configurations based on platform
    if cursor:
        # Cursor doesn't support proxy configuration
        if proxy or command or args or env:
            click.echo("Error: Cursor does not support proxy configuration")
            return
            
        # Add the server configuration for Cursor
        if not server_url:
            click.echo("Error: --url is required for server configurations in Cursor")
            return
            
        config["mcpServers"][name] = {
            "url": server_url
        }
    else:
        # Determine if this is a proxy or a server for Windsurf
        is_proxy = proxy or pipx or npx or command
        
        if is_proxy:
            # This is a proxy configuration with command, args, env
            if pipx:
                cmd = "pipx"
                arg_list = ["run", package]
                
                # Check if the package exists on PyPI
                exists, _ = check_pypi_package(package)
                
                if server_url:
                    arg_list.append(server_url)
                    
            elif npx:
                cmd = "npx"
                arg_list = ["-y", package]
                
                if server_url:
                    arg_list.append(server_url)
            elif command:
                cmd = command
                arg_list = args.split() if args else []
            else:
                # Default to mcp-proxy for proxy servers without a specific command
                cmd = "mcp-proxy"
                arg_list = [server_url] if server_url else []
            
            # Add environment variables if provided
            env_vars = {}
            if env:
                for env_var in env.split(','):
                    env_var = env_var.strip()
                    if not env_var:
                        continue
                        
                    try:
                        key, value = env_var.split('=', 1)
                        env_vars[key.strip()] = value.strip()
                    except ValueError:
                        click.echo(f"Warning: Invalid environment variable format: {env_var}")
            
            # Add the proxy configuration for Windsurf
            config["mcpServers"][name] = {
                "command": cmd,
                "args": arg_list,
                "env": env_vars
            }
        else:
            # This is a server configuration with just serverUrl for Windsurf
            if not server_url:
                click.echo("Error: --server-url is required for server configurations")
                return
                
            # Add the server configuration
            config["mcpServers"][name] = {
                "serverUrl": server_url
            }
    
    save_config(config, config_path, cursor=cursor)
    click.echo(f"Added MCP server '{name}'")

@cli.command()
@click.argument('name')
@click.pass_context
def delete(ctx, name):
    """Delete an MCP server configuration."""
    config = ctx.obj['CONFIG']
    cursor = ctx.obj.get("CURSOR", False)
    
    if cursor:
        if name not in config["mcpServers"]:
            click.echo(f"Error: MCP server '{name}' not found")
            return
        
        del config["mcpServers"][name]
    else:
        if name not in config["mcpServers"]:
            click.echo(f"Error: MCP server '{name}' not found")
            return
        
        del config["mcpServers"][name]
    
    save_config(config, ctx.obj['CONFIG_PATH'], cursor=cursor)
    click.echo(f"Deleted MCP server '{name}'")

@cli.command()
@click.option('--json', is_flag=True, help='Output in JSON format')
@click.pass_context
def list(ctx, json):
    """List all MCP server configurations."""
    config = ctx.obj['CONFIG']
    cursor = ctx.obj.get("CURSOR", False)
    servers = config["mcpServers"]
    
    if not servers:
        if json:
            click.echo('{"mcpServers": {}}')
        else:
            click.echo("No MCP servers configured.")
        return
    
    if json:
        click.echo(json.dumps({"mcpServers": servers}, indent=2))
        return
        
    # Format for tabulate
    table_data = []
    for name, server_config in servers.items():
        if cursor:
            if "url" in server_config:
                table_data.append([name, "Server", server_config["url"], ""])
            elif "command" in server_config:
                args = ' '.join(server_config.get('args', []))
                table_data.append([name, "Proxy", server_config["command"], args])
        else:
            if "serverUrl" in server_config:
                table_data.append([name, "Server", server_config["serverUrl"], ""])
            elif "command" in server_config:
                args = ' '.join(server_config.get('args', []))
                table_data.append([name, "Proxy", server_config["command"], args])
    
    click.echo(tabulate(
        table_data,
        headers=['Name', 'Type', 'Command/Server URL', 'Arguments'],
        tablefmt='grid'
    ))

@cli.command()
@click.argument('name')
@click.option('--server-url', 'server_url', help='URL of the MCP server (for Windsurf)')
@click.option('--url', help='URL of the MCP server (for Cursor)')
@click.option('--command', help='Command to run for proxy servers (Windsurf only)')
@click.option('--args', help='Arguments for the command (Windsurf only)')
@click.option('--env', help='Environment variables in KEY=VALUE format (Windsurf only). Use KEY= to remove a variable. For multiple variables, use a comma-separated list: KEY1=VALUE1,KEY2=VALUE2,KEY3=')
@click.option('--clear-env', is_flag=True, help='Clear all environment variables (Windsurf only)')
@click.option('--proxy', is_flag=True, help='Convert to a proxy configuration (Windsurf only)')
@click.option('--server', 'convert_to_server', is_flag=True, help='Convert to a server configuration (Windsurf only)')
@click.option('--cursor', is_flag=True, help='Configure for Cursor')
@click.pass_context
def update(ctx, name, server_url, url, command, args, env, clear_env, proxy, convert_to_server, cursor):
    """Update an existing MCP server configuration."""
    # Override cursor flag from context if provided
    cursor = cursor or ctx.obj.get("CURSOR", False)
    config = ctx.obj['CONFIG']
    config_path = ctx.obj['CONFIG_PATH']
    
    if name not in config["mcpServers"]:
        click.echo(f"Error: MCP server '{name}' not found")
        return
    
    server = config["mcpServers"][name]
    
    # Get the URL based on the platform
    if cursor:
        server_url = url or server_url
    
    if cursor:
        # Cursor only supports URL updates, not proxy configurations
        if command or args or env or clear_env or proxy or convert_to_server:
            click.echo("Error: Cursor does not support proxy configuration")
            return
            
        # Update Cursor server URL
        if server_url:
            server["url"] = server_url
        else:
            click.echo("Error: --url is required for updating Cursor server configurations")
            return
    else:
        # Update Windsurf server
        is_server_type = "serverUrl" in server
        
        # Check for conflicting conversion flags
        if proxy and convert_to_server:
            click.echo("Error: Cannot specify both --proxy and --server")
            return
            
        # Handle type conversion
        if proxy and is_server_type:
            # Convert from server to proxy
            click.echo(f"Converting '{name}' from server to proxy configuration")
            
            # Create a new proxy configuration
            new_config = {
                "command": command or "mcp-proxy",
                "env": {}
            }
            
            # Handle args properly
            if args:
                new_config["args"] = args.split()
            else:
                server_url = server.get("serverUrl", "")
                if server_url:
                    new_config["args"] = [server_url]
                else:
                    new_config["args"] = []
            
            # Replace the server configuration
            config["mcpServers"][name] = new_config
            server = config["mcpServers"][name]
            is_server_type = False
            
        elif convert_to_server and not is_server_type:
            # Convert from proxy to server
            click.echo(f"Converting '{name}' from proxy to server configuration")
            
            # Create a new server configuration
            new_config = {
                "serverUrl": server_url or ""
            }
            
            if not server_url:
                # Try to extract URL from args if available
                if "args" in server and len(server["args"]) > 0:
                    possible_url = server["args"][0]
                    if possible_url.startswith("http"):
                        new_config["serverUrl"] = possible_url
                        click.echo(f"Extracted URL from args: {possible_url}")
            
            if not new_config["serverUrl"]:
                click.echo("Warning: No server URL provided for conversion. Please update with --server-url")
            
            # Replace the proxy configuration
            config["mcpServers"][name] = new_config
            server = config["mcpServers"][name]
            is_server_type = True
        
        # Now update the configuration based on its type
        if is_server_type:
            # This is a server configuration
            if server_url:
                server["serverUrl"] = server_url
        else:
            # This is a proxy configuration
            if command:
                server["command"] = command
            if args:
                server["args"] = args.split()
                
            # Handle environment variables
            if clear_env:
                server["env"] = {}
                click.echo("Cleared all environment variables")
            
            if env:
                if "env" not in server:
                    server["env"] = {}
                
                for env_var in env.split(','):
                    env_var = env_var.strip()
                    if not env_var:
                        continue
                    
                    try:
                        if '=' in env_var:
                            key, value = env_var.split('=', 1)
                            key = key.strip()
                            
                            # If the value is empty, remove the variable
                            if not value.strip():
                                if key in server["env"]:
                                    del server["env"][key]
                                    click.echo(f"Removed environment variable: {key}")
                            else:
                                # Otherwise, set the variable
                                server["env"][key] = value.strip()
                                click.echo(f"Set environment variable: {key}={value.strip()}")
                        else:
                            click.echo(f"Warning: Invalid environment variable format: {env_var}")
                    except ValueError:
                        click.echo(f"Warning: Invalid environment variable format: {env_var}")
    
    save_config(config, config_path, cursor=cursor)
    click.echo(f"Updated MCP server '{name}'")

@cli.command()
@click.pass_context
def ui(ctx):
    """Launch the web UI for managing MCP configurations."""
    try:
        from windsurf_mcp_config_manager.ui_server import start_server
        start_server()
    except ImportError as e:
        click.echo(f"Error: Could not load UI server. {e}")
        click.echo("Make sure all UI dependencies are installed.")

def main():
    """Entry point for the console script."""
    cli()

if __name__ == "__main__":
    main()
