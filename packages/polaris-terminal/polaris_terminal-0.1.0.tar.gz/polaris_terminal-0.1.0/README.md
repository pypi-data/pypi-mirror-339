# Polaris Terminal

A command-line tool for connecting to Polaris containers via terminal.

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/BANADDA/polaris-terminal.git
cd polaris-terminal

# Install the package
pip install -e .
```

### Using pip

```bash
pip install polaris-terminal
```

### Using Installer Script

```bash
# Download and run the installer
python install_polaris_terminal.py
```

## Usage

### List Available Containers

List all containers for the default miner:
```bash
polaris list
```

### Show Container Details

View detailed information about a container. You can use either the container name or pod ID:
```bash
polaris info polaris-pod-1743999981-pod-1
```

Or using just the pod ID:
```bash
polaris info pod-1
```

Or using the timestamp part of the container name:
```bash
polaris info 1743999981-pod-1
```

### Connect to a Container

Connect to a container terminal. Multiple formats are supported:
```bash
# Using full container name
polaris connect polaris-pod-1743999981-pod-1

# Using pod ID
polaris connect pod-1

# Using timestamp part
polaris connect 1743999981-pod-1
```

### Configure Default Settings

View current configuration:
```bash
polaris config --show
```

Set default server URL:
```bash
polaris config --server-url http://148.76.188.132:8001
```

Set default miner ID:
```bash
polaris config --miner-id WWmHlBdA9KmiNHt3Hz7x
```

### Specify Server URL for a Single Command

```bash
polaris connect polaris-pod-1743999981-pod-1 --server-url http://148.76.188.132:8001
```

### Show Verbose Output

For detailed diagnostic information:
```bash
polaris connect polaris-pod-1743999981-pod-1 --verbose
```

## Features

- **Smart Container Name Handling**: Works with full container names, pod IDs, or partial names
- **Automatic Miner ID Detection**: Automatically detects the correct miner ID for each container
- **WebSocket Terminal**: Connect to container terminals via WebSocket
- **Detailed Container Information**: View complete details about containers
- **Configuration Management**: Persistent configuration stored in JSON file
- **Cross-Platform**: Works on Windows, Linux, and macOS
- **Robust Error Handling**: Helpful error messages and diagnostics

## Container Name Formats

The tool intelligently handles different formats for container identification:

- **Full Container Name**: `polaris-pod-1743999981-pod-1`
- **Pod ID**: `pod-1`
- **Timestamp Format**: `1743999981-pod-1`

All these formats will be automatically detected and handled correctly.

## Configuration

The tool stores its configuration in `~/.polaris/config.json`. You can edit this file directly or use the `polaris config` command to update settings.

Default configuration:
```json
{
  "server_url": "https://polaris-test-server.onrender.com",
  "miner_id": "WWmHlBdA9KmiNHt3Hz7x"
}
```

## Troubleshooting

If you encounter connection issues:

1. Check your server URL with `polaris config --show`
2. Ensure your container exists with `polaris list`
3. Try using the pod ID directly with `polaris connect pod-1`
4. Use the `--verbose` flag for detailed diagnostics
5. Try accessing the web terminal directly in your browser at `https://polaris-test-server.onrender.com/api/v1/containers/{container_name}/terminal`

## Requirements

- Python 3.7 or higher
- `requests` library
- `websockets` library "# polaris-terminal" 
