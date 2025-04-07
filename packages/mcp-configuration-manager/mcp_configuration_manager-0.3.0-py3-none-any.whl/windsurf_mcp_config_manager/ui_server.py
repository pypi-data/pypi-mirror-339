#!/usr/bin/env python3
"""
UI Server for MCP Config Manager
Serves the UI and provides API endpoints to interact with the CLI
"""

import os
import json
import subprocess
import threading
import webbrowser
import sys
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse
import shutil

# Import the API module
from . import api

# Get the directory of the current script
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
UI_ASSETS_DIR = os.path.join(CURRENT_DIR, "ui_assets")

# Create a simple HTTP request handler
class MCPConfigHandler(SimpleHTTPRequestHandler):
    # Override the default directory
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=UI_ASSETS_DIR, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)
        
        # Check if we're requesting Cursor config
        platform = query_params.get('platform', ['windsurf'])[0].lower()
        
        # Serve API endpoints
        if parsed_path.path == "/api/servers":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            try:
                # Use the API module to get the servers
                config = api.get_servers(platform)
                print(f"API response for platform {platform}: {json.dumps(config)}")
                
                # Ensure all servers have the platform property
                if "mcpServers" in config:
                    for server_name, server_config in config["mcpServers"].items():
                        server_config["platform"] = platform
                        
                        # Ensure URL format consistency
                        if platform == "cursor" and "url" in server_config and "serverUrl" not in server_config:
                            server_config["serverUrl"] = server_config["url"]
                        elif platform == "windsurf" and "serverUrl" in server_config and "url" not in server_config:
                            server_config["url"] = server_config["serverUrl"]
                
                self.wfile.write(json.dumps(config).encode())
            except Exception as e:
                print(f"Error getting servers: {e}")
                error_response = json.dumps({"error": str(e)})
                self.wfile.write(error_response.encode())
            return
        
        # For all other paths, let the parent class handle it
        return super().do_GET()
    
    def do_POST(self):
        """Handle POST requests"""
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8")
        
        # Parse the request data
        try:
            data = json.loads(post_data)
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
            return
        
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)
        
        # Check if we're using Cursor
        platform = query_params.get('platform', ['windsurf'])[0].lower()
        
        # Debug endpoint to log request data
        if parsed_path.path == "/api/debug":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            print("DEBUG REQUEST:")
            print(f"Path: {self.path}")
            print(f"Data: {json.dumps(data, indent=2)}")
            
            response = {"success": True, "message": "Debug data logged"}
            self.wfile.write(json.dumps(response).encode())
            return
        
        # API endpoint to add a new MCP server
        if parsed_path.path.startswith("/api/servers/"):
            server_name = parsed_path.path.split("/")[-1]
            
            # Handle POST request (add server)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            try:
                print(f"Adding server '{server_name}' with config: {json.dumps(data)}")
                
                # Build the CLI command directly
                cmd = ["mcm"]
                
                # Add platform flag if cursor
                if platform.lower() == "cursor":
                    cmd.append("--cursor")
                
                cmd.extend(["add", server_name])
                
                # Handle URL
                if "url" in data:
                    cmd.extend(["--server-url", data["url"]])
                    print(f"Using URL from config: {data['url']}")
                elif "serverUrl" in data:
                    cmd.extend(["--server-url", data["serverUrl"]])
                    print(f"Using serverUrl from config: {data['serverUrl']}")
                
                # Handle command and args for proxy mode
                if "command" in data:
                    cmd.extend(["--command", data["command"]])
                    print(f"Using command from config: {data['command']}")
                    
                    # Handle args
                    if "args" in data and isinstance(data["args"], list):
                        # Join all args into a single string for the --args parameter
                        args_str = " ".join(data["args"])
                        cmd.extend(["--args", args_str])
                        print(f"Using args from config: {args_str}")
                
                # Handle environment variables
                if "env" in data and isinstance(data["env"], dict):
                    for key, value in data["env"].items():
                        cmd.extend(["--env", f"{key}={value}"])
                    print(f"Using env vars from config: {data['env']}")
                
                # Handle package management
                if data.get("usePipx"):
                    cmd.append("--pipx")
                    if "package" in data:
                        cmd.extend(["--package", data["package"]])
                elif data.get("useNpx"):
                    cmd.append("--npx")
                    if "package" in data:
                        cmd.extend(["--package", data["package"]])
                
                print(f"Executing command: {' '.join(cmd)}")
                
                # Execute the command directly
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                print(f"Command output: {result.stdout}")
                if result.stderr:
                    print(f"Command stderr: {result.stderr}")
                
                # Get the updated servers
                updated_servers = api.get_servers(platform)
                
                response = {
                    "success": True,
                    "message": f"Added MCP server '{server_name}'",
                    "config": updated_servers
                }
                self.wfile.write(json.dumps(response).encode())
            except subprocess.CalledProcessError as e:
                print(f"Command failed with exit code {e.returncode}")
                print(f"Command stderr: {e.stderr}")
                print(f"Command stdout: {e.stdout}")
                error_response = {"success": False, "error": str(e.stderr)}
                self.wfile.write(json.dumps(error_response).encode())
            except Exception as e:
                error_response = {"success": False, "error": str(e)}
                self.wfile.write(json.dumps(error_response).encode())
            return
        
        self.send_error(404, "Not Found")
    
    def do_PUT(self):
        """Handle PUT requests (update server)"""
        content_length = int(self.headers.get("Content-Length", 0))
        put_data = self.rfile.read(content_length).decode("utf-8")
        
        # Parse the request data
        try:
            data = json.loads(put_data)
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
            return
        
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)
        
        # Check if we're using Cursor
        platform = query_params.get('platform', ['windsurf'])[0].lower()
        
        # API endpoint to update an MCP server
        if parsed_path.path.startswith("/api/servers/"):
            server_name = parsed_path.path.split("/")[-1]
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            try:
                print(f"Updating server '{server_name}' with config: {json.dumps(data)}")
                
                # Build the CLI command directly
                cmd = ["mcm"]
                
                # Add platform flag if cursor
                if platform.lower() == "cursor":
                    cmd.append("--cursor")
                
                cmd.extend(["update", server_name])
                
                # Handle URL
                if "url" in data:
                    cmd.extend(["--server-url", data["url"]])
                    print(f"Using URL from config: {data['url']}")
                elif "serverUrl" in data:
                    cmd.extend(["--server-url", data["serverUrl"]])
                    print(f"Using serverUrl from config: {data['serverUrl']}")
                
                # Handle command and args for proxy mode
                if "command" in data:
                    cmd.extend(["--command", data["command"]])
                    print(f"Using command from config: {data['command']}")
                    
                    # Handle args
                    if "args" in data and isinstance(data["args"], list):
                        # Join all args into a single string for the --args parameter
                        args_str = " ".join(data["args"])
                        cmd.extend(["--args", args_str])
                        print(f"Using args from config: {args_str}")
                
                # Handle environment variables
                if "env" in data and isinstance(data["env"], dict):
                    for key, value in data["env"].items():
                        cmd.extend(["--env", f"{key}={value}"])
                    print(f"Using env vars from config: {data['env']}")
                
                # Handle package management
                if data.get("usePipx"):
                    cmd.append("--pipx")
                    if "package" in data:
                        cmd.extend(["--package", data["package"]])
                elif data.get("useNpx"):
                    cmd.append("--npx")
                    if "package" in data:
                        cmd.extend(["--package", data["package"]])
                
                print(f"Executing command: {' '.join(cmd)}")
                
                # Execute the command directly
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                print(f"Command output: {result.stdout}")
                if result.stderr:
                    print(f"Command stderr: {result.stderr}")
                
                # Get the updated servers
                updated_servers = api.get_servers(platform)
                
                response = {
                    "success": True,
                    "message": f"Updated MCP server '{server_name}'",
                    "config": updated_servers
                }
                self.wfile.write(json.dumps(response).encode())
            except subprocess.CalledProcessError as e:
                print(f"Command failed with exit code {e.returncode}")
                print(f"Command stderr: {e.stderr}")
                print(f"Command stdout: {e.stdout}")
                error_response = {"success": False, "error": str(e.stderr)}
                self.wfile.write(json.dumps(error_response).encode())
            except Exception as e:
                error_response = {"success": False, "error": str(e)}
                self.wfile.write(json.dumps(error_response).encode())
            return
        
        self.send_error(404, "Not Found")
    
    def do_DELETE(self):
        """Handle DELETE requests"""
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)
        
        # Check if we're using Cursor
        platform = query_params.get('platform', ['windsurf'])[0].lower()
        
        # API endpoint to delete an MCP server
        if parsed_path.path.startswith("/api/servers/"):
            server_name = parsed_path.path.split("/")[-1]
            
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            try:
                print(f"Deleting server '{server_name}'")
                
                # Build the CLI command directly
                cmd = ["mcm"]
                
                # Add platform flag if cursor
                if platform.lower() == "cursor":
                    cmd.append("--cursor")
                
                cmd.extend(["delete", server_name])
                
                print(f"Executing command: {' '.join(cmd)}")
                
                # Execute the command directly
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                print(f"Command output: {result.stdout}")
                if result.stderr:
                    print(f"Command stderr: {result.stderr}")
                
                # Get the updated servers
                updated_servers = api.get_servers(platform)
                
                response = {
                    "success": True,
                    "message": f"Deleted MCP server '{server_name}'",
                    "config": updated_servers
                }
                self.wfile.write(json.dumps(response).encode())
            except subprocess.CalledProcessError as e:
                print(f"Command failed with exit code {e.returncode}")
                print(f"Command stderr: {e.stderr}")
                print(f"Command stdout: {e.stdout}")
                error_response = {"success": False, "error": str(e.stderr)}
                self.wfile.write(json.dumps(error_response).encode())
            except Exception as e:
                error_response = {"success": False, "error": str(e)}
                self.wfile.write(json.dumps(error_response).encode())
            return
        
        self.send_error(404, "Not Found")
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS preflight"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

def start_server(port=8000):
    """Start the UI server on the specified port"""
    # Create UI assets directory if it doesn't exist
    if not os.path.exists(UI_ASSETS_DIR):
        os.makedirs(UI_ASSETS_DIR)
    
    # Copy the UI assets from the windsurf-config-wizard
    wizard_dist_dir = os.path.expanduser("~/CascadeProjects/foobar/windsurf-config-wizard/dist")
    if os.path.exists(wizard_dist_dir):
        # Copy all files from the wizard dist directory to the UI assets directory
        for item in os.listdir(wizard_dist_dir):
            source = os.path.join(wizard_dist_dir, item)
            destination = os.path.join(UI_ASSETS_DIR, item)
            
            if os.path.isdir(source):
                if os.path.exists(destination):
                    shutil.rmtree(destination)
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)
    
    # Print the UI directory path for debugging
    print(f"Serving files from: {UI_ASSETS_DIR}")
    print(f"Files in directory: {os.listdir(UI_ASSETS_DIR)}")
    
    try:
        server = HTTPServer(("", port), MCPConfigHandler)
        print(f"Server started at http://localhost:{port}")
        print("Press Ctrl+C to stop the server")
        
        # Open the browser
        threading.Timer(1.0, lambda: webbrowser.open(f"http://localhost:{port}")).start()
        
        # Start the server
        server.serve_forever()
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"Port {port} is already in use. Trying port {port + 1}...")
            start_server(port + 1)
        else:
            raise

if __name__ == "__main__":
    start_server()
