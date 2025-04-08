#!/usr/bin/env python3
"""
Terminal WebSocket Client for Polaris Containers

This script connects to the same WebSocket endpoint as the web terminal,
but runs in your local terminal instead of a browser.

Usage:
    python terminal.py <container_name> [options]

Example:
    python terminal.py polaris-pod-123456
"""

import argparse
import asyncio
import json
import os
import platform
import re
import signal
import sys
from pathlib import Path
from urllib.parse import urlparse

import requests
import websockets

# Path to this script when installed
SCRIPT_PATH = Path(__file__).resolve()

# Determine if we're on Windows
IS_WINDOWS = platform.system() == "Windows"

# Import platform-specific modules
if IS_WINDOWS:
    import msvcrt
else:
    import termios
    import tty


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Connect to a container via WebSocket terminal",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python terminal.py polaris-pod-12345
  
  # Specify server URL
  python terminal.py polaris-pod-12345 --server-url http://localhost:8001
  
  # Show debug information
  python terminal.py polaris-pod-12345 --verbose
"""
    )
    parser.add_argument(
        "container_name", 
        help="The name of the container to connect to"
    )
    parser.add_argument(
        "--server-url", 
        default="https://polaris-test-server.onrender.com",
        help="URL of the Polaris server (default: https://polaris-test-server.onrender.com)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show verbose debug output"
    )
    return parser.parse_args()


def normalize_container_name(container_name, verbose=False):
    """Normalize container name to include prefix if needed"""
    if not container_name.startswith("polaris-pod-"):
        # Check if it looks like a timestamp or other ID
        if re.match(r'^[0-9]+.*', container_name):
            # Prepend the prefix
            container_name = f"polaris-pod-{container_name}"
            if verbose:
                print(f"Normalized container name to: {container_name}")
    return container_name


def get_websocket_url(args):
    """Get WebSocket URL for the container terminal"""
    container_name = normalize_container_name(args.container_name, args.verbose)
    
    # First, check if the container terminal endpoint is available
    check_url = f"{args.server_url}/api/v1/containers/{container_name}/terminal"
    
    if args.verbose:
        print(f"Checking terminal endpoint: {check_url}")
    
    try:
        response = requests.get(check_url)
        
        if response.status_code == 200:
            # The response is an HTML page with a WebSocket URL embedded
            # We need to extract the WebSocket URL from the page
            html_content = response.text
            
            # Get the server base URL
            parsed_url = urlparse(args.server_url)
            server_base = f"{parsed_url.scheme}://{parsed_url.netloc}"
            
            # Replace http with ws (or https with wss)
            ws_proto = "wss" if parsed_url.scheme == "https" else "ws"
            ws_base = f"{ws_proto}://{parsed_url.netloc}"
            
            # Log the HTML content for debugging
            if args.verbose:
                print(f"Server responded with status 200")
                
            # Look for the WebSocket URL in the HTML
            ws_url_match = re.search(r'var\s+socket\s*=\s*new\s+WebSocket\s*\(\s*[\'"]([^\'"]+)[\'"]', html_content)
            
            if ws_url_match:
                ws_relative_url = ws_url_match.group(1)
                
                # Make sure the WebSocket URL is absolute
                if ws_relative_url.startswith('/'):
                    ws_url = f"{ws_base}{ws_relative_url}"
                else:
                    ws_url = ws_relative_url
                    
                if args.verbose:
                    print(f"Found WebSocket URL: {ws_url}")
                return ws_url
            
            # If we couldn't find the WebSocket URL through regex, use a default pattern
            ws_url = f"{ws_base}/api/v1/ws/terminal/{container_name}"
            if args.verbose:
                print(f"Using default WebSocket URL: {ws_url}")
            return ws_url
            
        else:
            print(f"Error: HTTP {response.status_code}")
            print(f"Server response: {response.text}")
            return None
            
    except Exception as e:
        print(f"Error connecting to server: {str(e)}")
        return None


class TerminalSettings:
    """Cross-platform terminal settings handler"""
    
    def __init__(self):
        self.old_settings = None
    
    def set_raw_mode(self):
        """Set terminal to raw mode"""
        if IS_WINDOWS:
            # Windows doesn't need special handling for raw mode
            pass
        else:
            # Unix systems need to save old settings and set raw mode
            self.old_settings = termios.tcgetattr(sys.stdin.fileno())
            tty.setraw(sys.stdin.fileno())
    
    def restore(self):
        """Restore original terminal settings"""
        if IS_WINDOWS:
            # Windows doesn't need special handling for restoring
            pass
        else:
            # Restore Unix terminal settings
            if self.old_settings:
                termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, self.old_settings)


async def read_stdin_char():
    """Cross-platform function to read a character from stdin"""
    loop = asyncio.get_event_loop()
    
    if IS_WINDOWS:
        # Windows input handling
        if msvcrt.kbhit():
            return msvcrt.getch().decode('utf-8', errors='ignore')
        else:
            # Sleep briefly to avoid high CPU usage
            await asyncio.sleep(0.01)
            return None
    else:
        # Unix input handling
        return await loop.run_in_executor(None, sys.stdin.read, 1)


async def handle_terminal_input(websocket, verbose=False):
    """Handle input from the terminal and send to the WebSocket"""
    while True:
        # Read a character from stdin
        if IS_WINDOWS:
            # Windows-specific input handling
            while True:
                char = await read_stdin_char()
                if char:
                    break
                await asyncio.sleep(0.01)
        else:
            # Unix input handling
            char = await read_stdin_char()
            
        # Skip if no character was read (Windows)
        if not char:
            continue
        
        # Send the character to the WebSocket
        if verbose:
            # Don't print control characters as they'll mess up the terminal
            if ord(char) >= 32:
                print(f"Sending: {char}")
            elif ord(char) == 3:  # Ctrl+C
                print("Sending: Ctrl+C")
        
        try:
            await websocket.send(char)
        except websockets.exceptions.ConnectionClosed:
            break


async def handle_websocket_output(websocket, verbose=False):
    """Handle output from the WebSocket and print to the terminal"""
    while True:
        try:
            # Receive message from WebSocket
            message = await websocket.recv()
            
            # Print the message to stdout
            sys.stdout.write(message)
            sys.stdout.flush()
            
        except websockets.exceptions.ConnectionClosed:
            break
        except Exception as e:
            if verbose:
                print(f"Error receiving message: {str(e)}")
            break


async def terminal_websocket_client(ws_url, verbose=False):
    """Connect to the terminal WebSocket and handle input/output"""
    # Set up terminal
    terminal = TerminalSettings()
    
    try:
        # Set terminal to raw mode
        terminal.set_raw_mode()
        
        # Connect to the WebSocket
        if verbose:
            print(f"Connecting to WebSocket: {ws_url}")
            
        async with websockets.connect(ws_url) as websocket:
            if verbose:
                print("WebSocket connection established")
                
            # Create bidirectional communication
            await asyncio.gather(
                handle_terminal_input(websocket, verbose),
                handle_websocket_output(websocket, verbose)
            )
            
    except websockets.exceptions.ConnectionClosed as e:
        if verbose:
            print(f"WebSocket connection closed: {e}")
    except Exception as e:
        print(f"Error in WebSocket client: {str(e)}")
    finally:
        # Restore terminal settings
        terminal.restore()
        if verbose:
            print("Terminal settings restored")


def main():
    """Main entry point for terminal WebSocket client"""
    # Parse command line arguments
    args = parse_args()
    
    if args.verbose:
        print(f"Connecting to container terminal: {args.container_name}")
        print(f"Server URL: {args.server_url}")
        print("(Press Ctrl+C to exit)")
    
    # Make sure container name is normalized
    args.container_name = normalize_container_name(args.container_name, args.verbose)
    
    # Get WebSocket URL
    ws_url = get_websocket_url(args)
    if not ws_url:
        print("Could not determine WebSocket URL")
        sys.exit(1)
    
    if args.verbose:
        print(f"Using WebSocket URL: {ws_url}")
        print("Establishing connection...")
    
    # Set up signal handler for clean exit
    def signal_handler(sig, frame):
        print("\nInterrupted by user. Exiting...")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Start the WebSocket client
    try:
        asyncio.run(terminal_websocket_client(ws_url, args.verbose))
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting...")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 