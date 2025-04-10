"""Tests for the Helmfile MCP server."""

import asyncio
import tempfile
from unittest.mock import AsyncMock, patch

import pytest
from fastmcp import Context

from mcp_helmfile.server import execute_helmfile, sync_helmfile

# Create a temporary Helmfile for testing
@pytest.fixture
def test_helmfile():
    with tempfile.NamedTemporaryFile(suffix='.yaml', delete=False) as f:
        f.write(b"""
releases:
  - name: test-release
    namespace: test-namespace
    chart: stable/nginx-ingress
""")
        return f.name

@pytest.fixture
def mock_process():
    """Create a mock process for testing."""
    process = AsyncMock()
    process.communicate.return_value = (b"helmfile version v0.156.0", b"")
    process.returncode = 0
    process.terminate = AsyncMock()
    process.kill = AsyncMock()
    process.wait = AsyncMock()
    return process

@pytest.mark.asyncio
async def test_execute_helmfile_version(mock_process):
    """Test executing helmfile version command."""
    with patch('asyncio.create_subprocess_shell', return_value=mock_process):
        result = await execute_helmfile("version")
        assert result["status"] == "success"
        assert "version" in result["output"].lower()

@pytest.mark.asyncio
async def test_execute_helmfile_list(mock_process):
    """Test executing helmfile list command."""
    with patch('asyncio.create_subprocess_shell', return_value=mock_process):
        result = await execute_helmfile("list")
        assert result["status"] == "success"

@pytest.mark.asyncio
async def test_sync_helmfile(test_helmfile, mock_process):
    """Test syncing a Helmfile configuration."""
    with patch('asyncio.create_subprocess_shell', return_value=mock_process):
        result = await sync_helmfile(
            helmfile_path=test_helmfile,
            namespace="test-namespace",
            timeout=60
        )
        assert result["status"] == "success"

@pytest.mark.asyncio
async def test_execute_helmfile_with_context(mock_process):
    """Test executing helmfile command with context."""
    class MockContext(Context):
        async def info(self, message: str):
            assert "Executing Helmfile command" in message

    ctx = MockContext()
    with patch('asyncio.create_subprocess_shell', return_value=mock_process):
        result = await execute_helmfile("version", ctx=ctx)
        assert result["status"] == "success"
        assert "version" in result["output"].lower()

@pytest.mark.asyncio
async def test_execute_helmfile_timeout():
    """Test command timeout handling."""
    process = AsyncMock()
    process.communicate.side_effect = asyncio.TimeoutError()
    process.terminate = AsyncMock()
    process.kill = AsyncMock()
    process.wait = AsyncMock()
    
    with patch('asyncio.create_subprocess_shell', return_value=process), \
         patch('asyncio.wait_for', side_effect=asyncio.TimeoutError()):
        result = await execute_helmfile("sleep 10", timeout=1)
        assert result["status"] == "error"
        assert result["error"]["code"] == "TIMEOUT"
        assert "timed out" in result["error"]["message"].lower()
        
        # Verify process termination was called
        process.terminate.assert_called_once()
        process.wait.assert_called_once()  # First wait call after terminate
        process.kill.assert_not_called()  # No kill since we're mocking a successful termination

def test_main():
    """Test that the main function can be imported and called."""
    from mcp_helmfile import main
    assert callable(main) 