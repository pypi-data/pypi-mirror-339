#!/usr/bin/env python
# test_mock_server.py - Test client for mock MCP server

import requests
import json
import sys
import time
from typing import Dict, Any, Optional

# Server configuration
SERVER_URL = "http://localhost:8000"  # Real MCP server address
MCP_ENDPOINT = f"{SERVER_URL}/mcp"    # MCP endpoint

def test_tools_list() -> None:
    """Testing the tools/list endpoint via GET"""
    print("Testing tools/list endpoint via GET...")
    
    try:
        response = requests.get(f"{SERVER_URL}/tools/list")
        print(f"Response status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response data: {json.dumps(response.json(), indent=2)}")
            
            # Check if tools are in the response
            if "tools" in response.json():
                tools = response.json()["tools"]
                print(f"Found tools: {len(tools)}")
                for tool in tools:
                    print(f"  - {tool.get('name', 'No name')}: {tool.get('description', 'No description')}")
            else:
                print("Error: 'tools' field is missing in the response")
        else:
            print(f"Error: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")

def test_tools_list_mcp() -> None:
    """Testing the tools/list endpoint via MCP protocol"""
    print("\nTesting tools/list endpoint via MCP protocol...")
    
    try:
        response = requests.post(
            MCP_ENDPOINT,
            json={"type": "resource_request", "uri": "mcp://tools/list"}
        )
        
        print(f"Response status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response data: {json.dumps(response.json(), indent=2)}")
            
            # Check if tools are in the response
            if "tools" in response.json():
                tools = response.json()["tools"]
                print(f"Found tools: {len(tools)}")
                for tool in tools:
                    print(f"  - {tool.get('name', 'No name')}: {tool.get('description', 'No description')}")
            else:
                print("Error: 'tools' field is missing in the response")
        else:
            print(f"Error: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")

def test_server_info() -> None:
    """Testing the server://info resource"""
    print("\nTesting server://info resource...")
    
    try:
        response = requests.post(
            MCP_ENDPOINT,
            json={"type": "resource_request", "uri": "server://info"}
        )
        
        print(f"Response status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response data: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")

def test_tool_call(tool_name: str, params: Dict[str, Any]) -> None:
    """Testing a tool call"""
    print(f"\nTesting tool {tool_name}...")
    
    try:
        response = requests.post(
            MCP_ENDPOINT,
            json={
                "type": "tool_call",
                "name": tool_name,
                "parameters": params
            }
        )
        
        print(f"Response status: {response.status_code}")
        if response.status_code == 200:
            print(f"Response data: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"Error: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Connection error: {e}")

def main() -> None:
    """Run all tests"""
    print("Starting mock MCP server test client")
    
    # Test tools list via GET
    test_tools_list()
    
    # Test tools list via MCP protocol
    test_tools_list_mcp()
    
    # Test server info
    test_server_info()
    
    # Test search issues tool
    test_tool_call("youtrack_search_issues", {"query": "project: TEST", "top": 5})
    
    # Test get issue tool
    test_tool_call("youtrack_get_issue", {"issue_id": "TEST-1"})

if __name__ == "__main__":
    main()
