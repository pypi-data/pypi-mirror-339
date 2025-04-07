#!/usr/bin/env python3
"""
Tests for the Windsurf MCP Config Manager CLI.
"""

import os
import json
import tempfile
from click.testing import CliRunner
from windsurf_mcp_config_manager.cli import cli


def test_cli_help():
    """Test the CLI help output."""
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'Manage Windsurf MCP server configurations' in result.output


def test_add_list_delete():
    """Test adding, listing, and deleting a server configuration."""
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp_path = tmp.name
        
    try:
        # Add a server
        runner = CliRunner()
        result = runner.invoke(cli, [
            '--config', tmp_path,
            'add', 'test-server',
            '--command', 'python',
            '--args', 'server.py',
            '--env', 'DEBUG=true'
        ])
        assert result.exit_code == 0
        assert "Added MCP server 'test-server'" in result.output
        
        # Verify the config file was created with the correct content
        with open(tmp_path, 'r') as f:
            config = json.load(f)
        assert 'mcpServers' in config
        assert 'test-server' in config['mcpServers']
        assert config['mcpServers']['test-server']['command'] == 'python'
        assert config['mcpServers']['test-server']['args'] == ['server.py']
        assert config['mcpServers']['test-server']['env'] == {'DEBUG': 'true'}
        
        # List servers
        result = runner.invoke(cli, ['--config', tmp_path, 'list'])
        assert result.exit_code == 0
        assert 'test-server' in result.output
        assert 'Command: python' in result.output
        assert 'Args: server.py' in result.output
        assert 'DEBUG=true' in result.output
        
        # Delete the server
        result = runner.invoke(cli, ['--config', tmp_path, 'delete', 'test-server'])
        assert result.exit_code == 0
        assert "Deleted MCP server 'test-server'" in result.output
        
        # Verify the server was deleted
        with open(tmp_path, 'r') as f:
            config = json.load(f)
        assert 'test-server' not in config['mcpServers']
        
    finally:
        # Clean up
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
