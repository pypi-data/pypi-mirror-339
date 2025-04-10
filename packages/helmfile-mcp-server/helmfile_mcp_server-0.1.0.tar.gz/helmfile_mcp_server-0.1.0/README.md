# Helmfile MCP Server

A FastMCP server for executing Helmfile commands through the Model Context Protocol (MCP). This server provides a standardized interface for managing Helmfile operations, allowing AI assistants to help with Helmfile deployments, configurations, and troubleshooting.

## Key Features

- **Command Execution**: Execute any Helmfile command with proper validation and error handling
- **Synchronization**: Specialized tool for synchronizing Helmfile releases
- **Async Operations**: Asynchronous command execution for better performance
- **Command Piping**: Support for Unix pipe operations to filter and transform command output
- **Progress Tracking**: Real-time progress updates through MCP context
- **Timeout Support**: Configurable command timeouts to prevent hanging operations
- **Structured Errors**: Detailed error responses with proper error codes and messages

## Installation

### Prerequisites

- Python 3.13 or higher
- Helmfile installed and available in PATH
- Access to a Kubernetes cluster

### Install from Source

1. Clone the repository:
```bash
git clone <repository-url>
cd mcp_helmfile
```

2. Install dependencies:
```bash
uv pip install -e .
```

## Configuration

The server can be configured through environment variables:

| Environment Variable | Description | Default |
|---------------------|-------------|---------|
| `HELMFILE_MCP_TIMEOUT` | Default timeout for commands (seconds) | `300` |
| `HELMFILE_MCP_TRANSPORT` | Transport protocol to use ("stdio" or "sse") | `stdio` |

## Usage

### Starting the Server

```bash
python -m mcp_helmfile
```

### Available Tools

#### 1. execute_helmfile

A general-purpose tool for executing any Helmfile command.

Parameters:
- `command`: Complete Helmfile command to execute (including any pipes and flags)
- `timeout`: Maximum execution time in seconds (default: 300)
- `ctx`: Optional MCP context for request tracking

Example:
```python
result = await execute_helmfile(
    command="list",
    timeout=60,
    ctx=context
)
```

#### 2. sync_helmfile

A specialized tool for synchronizing Helmfile releases.

Parameters:
- `helmfile_path`: Path to the Helmfile configuration file
- `namespace`: Optional namespace to target
- `timeout`: Maximum execution time in seconds (default: 300)
- `ctx`: Optional MCP context for request tracking

Example:
```python
result = await sync_helmfile(
    helmfile_path="/path/to/helmfile.yaml",
    namespace="production",
    timeout=300,
    ctx=context
)
```

### Response Format

All tools return a dictionary with the following structure:

```python
{
    "status": "success" | "error",
    "output": "Command output if successful",
    "error": {
        "code": "Error code",
        "message": "Error message"
    }  # Only present if status is "error"
}
```

## Development

### Running Tests

```bash
pytest
```

### Building and Publishing

1. Build the package:
```bash
uv build
```

2. Publish to PyPI:
```bash
uv publish
```

## Security Considerations

- Commands are executed with proper validation
- Dangerous operations like apply/destroy require confirmation
- Environment-specific commands are validated against allowed environments
- Command timeouts prevent resource exhaustion
- Proper error handling and reporting

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
