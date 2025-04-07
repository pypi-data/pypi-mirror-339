"""
API module for the MCP Config Manager.
This module provides functions to interact with the CLI commands.
"""

import subprocess
import json
import os
from pathlib import Path
import logging
from . import config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_servers(platform="windsurf"):
    """
    Get all MCP server configurations.
    
    Args:
        platform (str): The platform to use (windsurf or cursor)
        
    Returns:
        dict: The MCP server configurations
    """
    try:
        logger.info(f"Getting servers for platform: {platform}")
        config_file = config.get_config_file_path(platform)
        logger.info(f"Config file path: {config_file}")
        
        config_data = config.load_config(platform)
        logger.info(f"Loaded config: {json.dumps(config_data)}")
        
        # Extract the mcpServers section
        servers = {}
        if "mcpServers" in config_data:
            # Add platform info to each server
            for name, server_config in config_data["mcpServers"].items():
                # Add platform info
                server_config["platform"] = platform
                
                # Add URL field for compatibility
                if "serverUrl" in server_config and "url" not in server_config:
                    server_config["url"] = server_config["serverUrl"]
                
                servers[name] = server_config
            
            return servers
        else:
            # For backward compatibility, return the entire config
            return {"mcpServers": config_data}
    except Exception as e:
        logger.error(f"Error getting servers: {str(e)}")
        return {}

def add_server(name, server_config, platform="windsurf"):
    """
    Add a new MCP server to the configuration.
    
    Args:
        name (str): The name of the server
        server_config (dict): The server configuration
        platform (str): The platform to use (windsurf or cursor)
        
    Returns:
        dict: The updated MCP server configurations
    """
    try:
        logger.info(f"Adding server '{name}' with config: {json.dumps(server_config)} for platform: {platform}")
        
        # Prepare the command arguments
        cmd = ["mcm"]
        
        # Add platform flag if cursor
        if platform.lower() == "cursor":
            cmd.append("--cursor")
            
        cmd.extend(["add", name])
        
        # Add URL handling
        if "url" in server_config:
            cmd.extend(["--server-url", server_config["url"]])
            logger.info(f"Using URL from config: {server_config['url']}")
        elif "serverUrl" in server_config:
            cmd.extend(["--server-url", server_config["serverUrl"]])
            logger.info(f"Using serverUrl from config: {server_config['serverUrl']}")
        
        # Handle command and args for proxy mode
        if "command" in server_config:
            cmd.extend(["--command", server_config["command"]])
            logger.info(f"Using command from config: {server_config['command']}")
            
            # Handle args
            if "args" in server_config and isinstance(server_config["args"], list):
                # Join all args into a single string for the --args parameter
                args_str = " ".join(server_config["args"])
                cmd.extend(["--args", args_str])
                logger.info(f"Using args from config: {args_str}")
        
        # Handle environment variables
        if "env" in server_config and isinstance(server_config["env"], dict):
            for key, value in server_config["env"].items():
                cmd.extend(["--env", f"{key}={value}"])
            logger.info(f"Using env vars from config: {server_config['env']}")
        
        # Handle package management
        if server_config.get("usePipx"):
            cmd.append("--pipx")
            if "package" in server_config:
                cmd.extend(["--package", server_config["package"]])
        elif server_config.get("useNpx"):
            cmd.append("--npx")
            if "package" in server_config:
                cmd.extend(["--package", server_config["package"]])
        
        logger.info(f"Executing command: {' '.join(cmd)}")
        
        # Execute the command
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        if result.stdout:
            logger.info(f"Command output: {result.stdout}")
        if result.stderr:
            logger.warning(f"Command stderr: {result.stderr}")
        
        # Get the updated servers
        return get_servers(platform)
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {e.stderr}")
        raise
    except Exception as e:
        logger.error(f"Error adding server: {str(e)}")
        raise

def update_server(name, server_config, platform="windsurf"):
    """
    Update an existing MCP server configuration.
    
    Args:
        name (str): The name of the server
        server_config (dict): The updated server configuration
        platform (str): The platform to use (windsurf or cursor)
        
    Returns:
        dict: The updated MCP server configurations
    """
    try:
        logger.info(f"Updating server '{name}' with config: {json.dumps(server_config)} for platform: {platform}")
        
        # Prepare the command arguments
        cmd = ["mcm"]
        
        # Add platform flag if cursor
        if platform.lower() == "cursor":
            cmd.append("--cursor")
            
        cmd.extend(["update", name])
        
        # Handle type conversion flags
        if server_config.get("convertToProxy", False):
            cmd.append("--proxy")
            logger.info("Converting to proxy configuration")
        elif server_config.get("convertToServer", False):
            cmd.append("--server")
            logger.info("Converting to server configuration")
        
        # Add URL handling
        if "url" in server_config:
            cmd.extend(["--server-url", server_config["url"]])
            logger.info(f"Using URL from config: {server_config['url']}")
        elif "serverUrl" in server_config:
            cmd.extend(["--server-url", server_config["serverUrl"]])
            logger.info(f"Using serverUrl from config: {server_config['serverUrl']}")
        
        # Handle command and args for proxy mode
        if "command" in server_config:
            cmd.extend(["--command", server_config["command"]])
            logger.info(f"Using command from config: {server_config['command']}")
            
            # Handle args
            if "args" in server_config and isinstance(server_config["args"], list):
                # Join all args into a single string for the --args parameter
                args_str = " ".join(server_config["args"])
                cmd.extend(["--args", args_str])
                logger.info(f"Using args from config: {args_str}")
        
        # Handle environment variables
        if server_config.get("clearEnv", False):
            cmd.append("--clear-env")
            logger.info("Clearing all environment variables")
            
        if "env" in server_config and isinstance(server_config["env"], dict):
            # Combine all environment variables into a single comma-separated list
            env_list = []
            for key, value in server_config["env"].items():
                env_list.append(f"{key}={value}")
            
            if env_list:
                cmd.extend(["--env", ",".join(env_list)])
                logger.info(f"Using env vars from config: {server_config['env']}")
        
        # Handle package management
        if server_config.get("usePipx"):
            cmd.append("--pipx")
            if "package" in server_config:
                cmd.extend(["--package", server_config["package"]])
        elif server_config.get("useNpx"):
            cmd.append("--npx")
            if "package" in server_config:
                cmd.extend(["--package", server_config["package"]])
        
        logger.info(f"Executing command: {' '.join(cmd)}")
        
        # Execute the command
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        if result.stdout:
            logger.info(f"Command output: {result.stdout}")
        if result.stderr:
            logger.warning(f"Command stderr: {result.stderr}")
        
        # Get the updated servers
        return get_servers(platform)
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {e.stderr}")
        raise
    except Exception as e:
        logger.error(f"Error updating server: {str(e)}")
        raise

def delete_server(name, platform="windsurf"):
    """
    Delete an MCP server from the configuration.
    
    Args:
        name (str): The name of the server to delete
        platform (str): The platform to use (windsurf or cursor)
        
    Returns:
        dict: The updated MCP server configurations
    """
    try:
        logging.info(f"Deleting server '{name}' for platform: {platform}")
        
        # Prepare the command arguments
        cmd = ["mcm"]
        
        # Add platform flag if cursor
        if platform.lower() == "cursor":
            cmd.append("--cursor")
            
        cmd.extend(["delete", name])
        
        logging.info(f"Executing command: {' '.join(cmd)}")
        
        # Execute the command
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        if result.stdout:
            logging.info(f"Command output: {result.stdout}")
        if result.stderr:
            logging.warning(f"Command stderr: {result.stderr}")
        
        # Get the updated servers
        return get_servers(platform)
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed: {e.stderr}")
        raise
    except Exception as e:
        logging.error(f"Error deleting server: {str(e)}")
        raise
