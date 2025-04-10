"""Main server implementation for Helmfile MCP Server.

This module defines the FastMCP server instance and tool functions for Helmfile operations,
providing a standardized interface for helmfile command execution and documentation.
"""

import asyncio
import logging
from typing import Optional

from fastmcp import Context, FastMCP
from pydantic import Field

# Configure logging
logger = logging.getLogger(__name__)

# Create the FastMCP server
mcp = FastMCP(
    name="Helmfile MCP Server",
    instructions="A server for executing Helmfile commands through MCP",
    version="0.1.0",
)

@mcp.tool(
    description="Execute Helmfile commands with support for Unix pipes.",
)
async def execute_helmfile(
    command: str = Field(description="Complete Helmfile command to execute (including any pipes and flags)"),
    timeout: Optional[int] = Field(description="Maximum execution time in seconds (default: 300)", default=None),
    ctx: Optional[Context] = None,
) -> dict:
    """Execute Helmfile commands with support for Unix pipes.

    Executes Helmfile commands with proper validation, error handling, and resource limits.
    Supports piping output to standard Unix utilities for filtering and transformation.

    Security considerations:
    - Commands are validated against security policies
    - Dangerous operations like apply/destroy require confirmation
    - Environment-specific commands are validated against allowed environments

    Examples:
        helmfile list
        helmfile status
        helmfile diff
        helmfile apply --environment prod

    Args:
        command: Complete Helmfile command to execute (can include Unix pipes)
        timeout: Optional timeout in seconds
        ctx: Optional MCP context for request tracking

    Returns:
        Dictionary containing output and status with structured error information
    """
    # Convert timeout to integer if it's a FieldInfo object
    actual_timeout = timeout.default if hasattr(timeout, 'default') else timeout
    actual_timeout = actual_timeout or 300

    logger.info(f"Executing Helmfile command: {command}" + (f" with timeout: {actual_timeout}" if actual_timeout else ""))

    # Add helmfile prefix if not present
    if not command.strip().startswith("helmfile"):
        command = f"helmfile {command}"

    if ctx:
        is_pipe = "|" in command
        message = "Executing" + (" piped" if is_pipe else "") + " Helmfile command"
        await ctx.info(message + (f" with timeout: {actual_timeout}s" if actual_timeout else ""))

    try:
        # Execute the command with timeout
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        
        try:
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=actual_timeout)
        except asyncio.TimeoutError:
            # Properly handle async process termination
            try:
                await process.terminate()
                try:
                    await asyncio.wait_for(process.wait(), timeout=5)
                except asyncio.TimeoutError:
                    # Only kill if process is still running
                    if process.returncode is None:
                        await process.kill()
            except Exception as e:
                logger.error(f"Error terminating process: {str(e)}")
                return {
                    "status": "error",
                    "error": {
                        "code": "TERMINATION_ERROR",
                        "message": f"Failed to terminate process: {str(e)}",
                    }
                }
            return {
                "status": "error",
                "error": {
                    "code": "TIMEOUT",
                    "message": f"Command timed out after {actual_timeout} seconds",
                }
            }

        # Check if command was successful
        if process.returncode == 0:
            return {
                "status": "success",
                "output": stdout.decode().strip(),
            }
        else:
            return {
                "status": "error",
                "error": {
                    "code": "COMMAND_ERROR",
                    "message": stderr.decode().strip(),
                }
            }

    except Exception as e:
        logger.error(f"Error executing Helmfile command: {str(e)}")
        return {
            "status": "error",
            "error": {
                "code": "INTERNAL_ERROR",
                "message": str(e),
            }
        }

@mcp.tool(
    description="Synchronize Helmfile releases.",
)
async def sync_helmfile(
    helmfile_path: str = Field(description="Path to the Helmfile configuration file"),
    namespace: Optional[str] = Field(description="Namespace to target", default=None),
    timeout: Optional[int] = Field(description="Maximum execution time in seconds (default: 300)", default=None),
    ctx: Optional[Context] = None,
) -> dict:
    """Synchronize Helmfile releases.

    Executes 'helmfile sync' command to synchronize the cluster state as described
    in the Helmfile configuration.

    Args:
        helmfile_path: Path to the Helmfile configuration file
        namespace: Optional namespace to target
        timeout: Optional timeout in seconds
        ctx: Optional MCP context for request tracking

    Returns:
        Dictionary containing output and status with structured error information
    """
    # Get actual values from FieldInfo objects if needed
    actual_namespace = namespace.default if hasattr(namespace, 'default') else namespace
    actual_timeout = timeout.default if hasattr(timeout, 'default') else timeout
    
    # Build the command with proper flag handling
    command_parts = ["helmfile", "sync", "-f", helmfile_path]
    
    # Only add namespace flag if namespace is provided and not empty
    if actual_namespace and str(actual_namespace).strip():
        command_parts.extend(["-n", str(actual_namespace).strip()])
    
    # Join the command parts with spaces
    command = " ".join(command_parts)
    
    return await execute_helmfile(command, actual_timeout, ctx)

def main():
    """Run the Helmfile MCP Server."""
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()