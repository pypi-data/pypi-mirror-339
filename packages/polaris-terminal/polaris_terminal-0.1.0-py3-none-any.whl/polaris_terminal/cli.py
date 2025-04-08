#!/usr/bin/env python
"""
Polaris Terminal CLI

Command-line interface for connecting to Polaris containers via terminal
"""

import argparse
import json
import os
import re
import subprocess
import sys

import requests

from .terminal import SCRIPT_PATH

# Default server URL - can be overridden with environment variable
DEFAULT_SERVER_URL = "https://polaris-test-server.onrender.com"

def load_config():
    """Load configuration from config file"""
    config_file = os.path.expanduser("~/.polaris/config.json")
    config = {
        "server_url": os.environ.get("POLARIS_SERVER_URL", DEFAULT_SERVER_URL),
        "miner_id": os.environ.get("POLARIS_MINER_ID", "WWmHlBdA9KmiNHt3Hz7x")
    }
    
    if os.path.exists(config_file):
        try:
            with open(config_file, "r") as f:
                loaded_config = json.load(f)
                config.update(loaded_config)
        except Exception as e:
            print(f"Warning: Could not load config file: {e}")
    
    # Ensure miner_id is not None
    if config["miner_id"] is None:
        config["miner_id"] = "WWmHlBdA9KmiNHt3Hz7x"
        print(f"Warning: No miner_id found, using default: {config['miner_id']}")
    
    return config

def save_config(config):
    """Save configuration to config file"""
    config_dir = os.path.expanduser("~/.polaris")
    os.makedirs(config_dir, exist_ok=True)
    config_file = os.path.join(config_dir, "config.json")
    
    try:
        with open(config_file, "w") as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        print(f"Warning: Could not save config file: {e}")
        return False

def get_server_url():
    """Get the server URL from config or environment variable"""
    config = load_config()
    return config.get("server_url")

def get_default_miner_id():
    """Get the default miner ID from config or environment variable"""
    config = load_config()
    return config.get("miner_id")

def get_terminal_connection(container_name, server_url=None, miner_id=None):
    """Get terminal connection details from the API"""
    if not server_url:
        server_url = get_server_url()
    
    # If miner_id not provided, try to get it from pod details
    if not miner_id:
        pod_details = get_pod_details(container_name, server_url)
        miner_id = None
        if pod_details:
            miner_id = pod_details.get("miner_id")
            if not miner_id and "pod_info" in pod_details:
                miner_id = pod_details.get("pod_info", {}).get("miner_id")
    
    # Use environment variable or default if miner_id wasn't found
    if not miner_id:
        miner_id = get_default_miner_id()
        print(f"Using default miner ID: {miner_id}")
    
    # Make sure container name has the correct format
    if not container_name.startswith("polaris-pod-") and re.match(r'^[0-9]+.*', container_name):
        container_name = f"polaris-pod-{container_name}"
        print(f"Using normalized container name: {container_name}")
    
    url = f"{server_url}/api/v1/containers/terminal-connection"
    payload = {
        "container_name": container_name,
        "miner_id": miner_id
    }
    
    try:
        print(f"Sending request to {url} with payload: {payload}")
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        
        if not data.get("success"):
            print(f"Error: {data.get('message', 'Unknown error')}")
            sys.exit(1)
            
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Polaris server: {e}")
        print(f"Request URL: {url}")
        print(f"Request payload: {payload}")
        sys.exit(1)

def connect_to_terminal(container_name, server_url=None, verbose=False):
    """Connect to a container terminal"""
    print(f"Connecting to container: {container_name}")
    
    if not server_url:
        server_url = get_server_url()
    
    # Try to get details about the container first
    pod_details = get_pod_details(container_name, server_url)
    miner_id = None
    
    if pod_details:
        # Extract the real container name and miner ID
        pod_info = pod_details.get('pod_info', {})
        if pod_info and pod_info.get('container_name'):
            container_name = pod_info.get('container_name')
            print(f"Using container name: {container_name}")
        
        miner_id = pod_details.get('miner_id')
        if not miner_id and pod_info:
            miner_id = pod_info.get('miner_id')
        
        if miner_id:
            print(f"Using miner ID: {miner_id}")
    else:
        miner_id = get_default_miner_id()
        print(f"Container details not found, using default miner ID: {miner_id}")
    
    # Get connection details from API
    connection_info = get_terminal_connection(container_name, server_url, miner_id)
    
    # Get WebSocket URL directly instead of using the command
    websocket_url = connection_info.get("websocket_url")
    if not websocket_url:
        print("Error: No WebSocket URL received from server")
        sys.exit(1)
    
    print(f"WebSocket URL: {websocket_url}")
    print("Establishing connection...")
    
    try:
        # Build a clean command with just the needed arguments
        # Create a command with just the required arguments in the right order
        python_cmd = [
            sys.executable,
            SCRIPT_PATH,
            container_name,
            "--server-url", 
            server_url
        ]
        
        if verbose:
            python_cmd.append("--verbose")
        
        # Execute the terminal connection with python
        subprocess.run(python_cmd)
    except Exception as e:
        print(f"Error connecting to terminal: {e}")
        sys.exit(1)

def get_pod_details(pod_name_or_id, server_url=None):
    """Get pod details including miner_id for a given pod name or ID"""
    if not server_url:
        server_url = get_server_url()
    
    # Print debug info
    print(f"Looking up details for: {pod_name_or_id}")
    
    try:
        # Handle different formats
        pod_id = None
        container_name = pod_name_or_id
        
        # Check if it's already a pod-ID format
        if pod_name_or_id.startswith("pod-"):
            pod_id = pod_name_or_id
            print(f"Detected pod ID format: {pod_id}")
        # Check if it's in the container name format
        elif pod_name_or_id.startswith("polaris-pod-"):
            # Extract the pod ID from the container name if possible
            parts = pod_name_or_id.split("-")
            if len(parts) >= 4:
                # The pod ID might be the last part
                pod_id = f"pod-{parts[-1]}"
                print(f"Extracted pod ID from container name: {pod_id}")
        
        # First try to get pod by ID if we have one
        if pod_id:
            url = f"{server_url}/api/v1/pods/{pod_id}"
            print(f"Trying to get pod by ID: {url}")
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
        
        # If we have a miner ID, try to look up containers
        miner_id = get_default_miner_id()
        if miner_id:
            # Check if we need to normalize the container name
            if not container_name.startswith("polaris-pod-"):
                # Only add prefix if it looks like a timestamp/ID
                if re.match(r'^[0-9]+.*', container_name):
                    container_name = f"polaris-pod-{container_name}"
                    print(f"Normalized container name to: {container_name}")
            
            url = f"{server_url}/api/v1/containers/{miner_id}"
            print(f"Looking up containers for miner: {url}")
            response = requests.get(url)
            if response.status_code == 200:
                containers = response.json()
                
                # Log the number of containers found
                print(f"Found {len(containers)} containers for miner {miner_id}")
                
                # Look for container with matching name
                for container in containers:
                    pod_info = container.get("pod_info", {})
                    container_name_from_api = pod_info.get("container_name", "")
                    
                    if container_name_from_api == container_name:
                        print(f"Found matching container: {container_name_from_api}")
                        return container
        
        # If we didn't find anything, let the user know
        print(f"Could not find container or pod matching: {pod_name_or_id}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error getting pod details: {e}")
        return None

def list_containers(server_url=None, specified_container=None):
    """List available containers"""
    if not server_url:
        server_url = get_server_url()
    
    try:
        # If a container is specified, get its miner_id
        miner_id = None
        if specified_container:
            pod_details = get_pod_details(specified_container, server_url)
            if pod_details:
                # Try to get miner_id from different places in the response
                miner_id = pod_details.get("miner_id")
                if not miner_id and "pod_info" in pod_details:
                    miner_id = pod_details.get("pod_info", {}).get("miner_id")
                
                if not miner_id:
                    print(f"Could not find miner_id for container {specified_container}")
                    # Use default as fallback
                    miner_id = get_default_miner_id()
            else:
                print(f"Could not find container {specified_container}")
                return
        
        # If no miner_id was found or no container was specified, use the default or environment value
        if not miner_id:
            miner_id = get_default_miner_id()
        
        url = f"{server_url}/api/v1/containers/{miner_id}"
        
        print(f"Fetching containers from: {url}")
        
        response = requests.get(url)
        response.raise_for_status()
        containers = response.json()
        
        if not containers:
            print("No containers found.")
            return
        
        print("\nAvailable containers:")
        print("-" * 80)
        print(f"{'Container ID':<50} {'Status':<15} {'Miner ID':<20}")
        print("-" * 80)
        
        for container in containers:
            container_name = container.get("pod_info", {}).get("container_name", "Unknown")
            status = container.get("status", "Unknown")
            container_miner_id = container.get("miner_id", "Unknown")
            print(f"{container_name:<50} {status:<15} {container_miner_id:<20}")
            
    except requests.exceptions.RequestException as e:
        print(f"Error listing containers: {e}")
        sys.exit(1)

def show_container_info(container_name, server_url=None):
    """Show detailed information about a specific container"""
    if not server_url:
        server_url = get_server_url()
    
    # Try to get pod details
    pod_details = get_pod_details(container_name, server_url)
    if not pod_details:
        print(f"Container '{container_name}' not found")
        return
    
    # Display container information nicely formatted
    print("\nContainer Information:")
    print("-" * 50)
    
    # Get pod_info if available
    pod_info = pod_details.get('pod_info', {})
    if not pod_info:
        pod_info = {}
    
    # Basic info - try multiple places for each value
    container_name = pod_info.get('container_name') or pod_details.get('pod_info', {}).get('container_name', 'Unknown')
    status = pod_details.get('status', 'Unknown')
    pod_id = pod_details.get('pod_id') or pod_info.get('pod_id') or pod_details.get('id', 'Unknown')
    miner_id = pod_details.get('miner_id') or pod_info.get('miner_id', 'Unknown')
    
    print(f"Container Name: {container_name}")
    print(f"Status: {status}")
    print(f"Pod ID: {pod_id}")
    print(f"Miner ID: {miner_id}")
    
    # Creation info
    created_at = pod_details.get('created_at') or pod_info.get('created_at', 'Unknown')
    started_at = pod_details.get('started_at', 'Unknown')
    print(f"Created At: {created_at}")
    print(f"Started At: {started_at}")
    
    # Container details
    if pod_info:
        print("\nContainer Details:")
        print(f"  Image: {pod_info.get('image', 'Unknown')}")
        print(f"  CPU Count: {pod_info.get('cpu_count', 'Unknown')}")
        print(f"  Memory: {pod_info.get('memory', 'Unknown')}")
        print(f"  Disk: {pod_info.get('disk', 'Unknown')}")
        
        # GPU info if available
        gpu_count = pod_info.get('gpu_count')
        if gpu_count:
            print(f"  GPU Count: {gpu_count}")
            print(f"  GPU Type: {pod_info.get('gpu_type', 'Unknown')}")
    
    # Access methods
    access = pod_details.get('access', {})
    if access:
        print("\nAccess Methods:")
        
        # SSH access
        ssh = access.get('ssh', {})
        if ssh:
            print(f"\n  SSH:")
            print(f"    Host: {ssh.get('host', 'Unknown')}")
            print(f"    Port: {ssh.get('port', 'Unknown')}")
            print(f"    Username: {ssh.get('username', 'Unknown')}")
            print(f"    Command: ssh {ssh.get('username', 'pod-user')}@{ssh.get('host', 'localhost')} -p {ssh.get('port', '22')}")
        
        # HTTP access
        http = access.get('http', {})
        if http:
            print(f"\n  HTTP:")
            print(f"    URL: {http.get('url', 'Unknown')}")
    
    # If there are no access methods found but we have a container name and miner_id,
    # suggest how to enable access
    if not access and container_name != 'Unknown' and miner_id != 'Unknown':
        print("\nNo access methods configured. To enable SSH access:")
        print(f"  polaris connect {container_name}")
        print("\nTo view the web terminal:")
        print(f"  Open http://localhost:8001/api/v1/containers/{container_name}/terminal in your browser")

def main():
    """Main entry point for the Polaris CLI"""
    parser = argparse.ArgumentParser(description="Polaris Terminal Connection Tool")
    
    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Connect command
    connect_parser = subparsers.add_parser("connect", help="Connect to a container terminal")
    connect_parser.add_argument("container", help="Container name to connect to")
    connect_parser.add_argument("--server-url", help="Polaris server URL (default: from config or localhost:8001)")
    connect_parser.add_argument("--verbose", "-v", action="store_true", help="Show verbose output")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List available containers")
    list_parser.add_argument("--server-url", help="Polaris server URL (default: from config or localhost:8001)")
    list_parser.add_argument("--container", help="Get container details for a specific container")
    
    # Info command
    info_parser = subparsers.add_parser("info", help="Show detailed information about a container")
    info_parser.add_argument("container", help="Container name to show information for")
    info_parser.add_argument("--server-url", help="Polaris server URL (default: from config or localhost:8001)")
    
    # Config command
    config_parser = subparsers.add_parser("config", help="Configure default settings")
    config_parser.add_argument("--server-url", help="Set the default server URL")
    config_parser.add_argument("--miner-id", help="Set the default miner ID")
    config_parser.add_argument("--show", action="store_true", help="Show current configuration")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Handle commands
    if args.command == "connect":
        connect_to_terminal(args.container, args.server_url, getattr(args, 'verbose', False))
    elif args.command == "list":
        list_containers(args.server_url, getattr(args, 'container', None))
    elif args.command == "info":
        show_container_info(args.container, args.server_url)
    elif args.command == "config":
        # Handle config command
        config = load_config()
        
        # Update config if new values are provided
        if args.server_url:
            config["server_url"] = args.server_url
        if args.miner_id:
            config["miner_id"] = args.miner_id
        
        # Save config if changes were made
        if args.server_url or args.miner_id:
            if save_config(config):
                print("Configuration saved.")
            else:
                print("Failed to save configuration.")
        
        # Show current config
        if args.show or not (args.server_url or args.miner_id):
            print("\nCurrent Configuration:")
            print(f"  Server URL: {config['server_url']}")
            print(f"  Miner ID: {config['miner_id']}")
    else:
        # Default action if no command specified
        parser.print_help()

if __name__ == "__main__":
    main() 