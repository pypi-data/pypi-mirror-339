#!/usr/bin/env python
# -*- coding: utf-8 -*-
# test_mcp_server.py - Test client for YouTrack MCP Server via MCP Inspector

import requests
import json
import sys
import time
from typing import Dict, Any, Optional

# MCP Inspector configuration
INSPECTOR_URL = "http://127.0.0.1:6274"
API_ENDPOINT = f"{INSPECTOR_URL}/api"

def test_inspector_status():
    """Test MCP Inspector status"""
    print("Testing MCP Inspector status...")
    
    try:
        response = requests.get(f"{INSPECTOR_URL}/api/status")
        print(f"Response status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response data: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")

def test_inspector_servers():
    """Test MCP Inspector servers list"""
    print("\nTesting MCP Inspector servers list...")
    
    try:
        response = requests.get(f"{API_ENDPOINT}/servers")
        print(f"Response status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response data: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")

def test_youtrack_server_tools():
    """Test YouTrack MCP Server tools via MCP Inspector"""
    print("\nTesting YouTrack MCP Server tools...")
    
    # First, get the server ID for YouTrack MCP Server
    try:
        response = requests.get(f"{API_ENDPOINT}/servers")
        if response.status_code == 200:
            servers = response.json()
            youtrack_server = None
            
            # Find YouTrack MCP Server in the list
            for server in servers:
                if "YouTrack" in server.get("name", ""):
                    youtrack_server = server
                    break
            
            if youtrack_server:
                server_id = youtrack_server.get("id")
                print(f"Found YouTrack MCP Server with ID: {server_id}")
                
                # Now get the tools for this server
                tools_response = requests.get(f"{API_ENDPOINT}/servers/{server_id}/tools")
                if tools_response.status_code == 200:
                    tools = tools_response.json()
                    print(f"Found {len(tools)} tools:")
                    for tool in tools:
                        print(f"  - {tool.get('name', 'No name')}: {tool.get('description', 'No description')}")
                else:
                    print(f"Error getting tools: {tools_response.text}")
            else:
                print("YouTrack MCP Server not found in the list of servers")
        else:
            print(f"Error getting servers: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")

def main():
    """Run all tests"""
    print("Starting YouTrack MCP Server test client via MCP Inspector")
    
    # Test MCP Inspector status
    test_inspector_status()
    
    # Test MCP Inspector servers list
    test_inspector_servers()
    
    # Test YouTrack MCP Server tools
    test_youtrack_server_tools()

if __name__ == "__main__":
    main()
