#!/usr/bin/env python
# mock_mcp_server.py - Simple mock MCP server for testing

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger('mock-mcp-server')

class MockMCPHandler(BaseHTTPRequestHandler):
    def _set_headers(self, content_type="application/json"):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests"""
        logger.info(f"GET request to {self.path}")
        
        if self.path == "/tools/list":
            self._handle_tools_list()
        else:
            self._handle_not_found()
    
    def do_POST(self):
        """Handle POST requests"""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            request_json = json.loads(post_data.decode('utf-8'))
            logger.info(f"POST request to {self.path} with data: {request_json}")
            
            if self.path == "/mcp":
                self._handle_mcp_request(request_json)
            else:
                self._handle_not_found()
        except json.JSONDecodeError:
            logger.error("Invalid JSON in request")
            self._handle_bad_request("Invalid JSON")
    
    def _handle_tools_list(self):
        """Handle tools/list request"""
        response = {
            "tools": [
                {
                    "name": "youtrack_search_issues",
                    "description": "Search for issues in YouTrack using a query"
                },
                {
                    "name": "youtrack_get_issue",
                    "description": "Get details for a specific YouTrack issue by its ID"
                },
                {
                    "name": "youtrack_update_issue",
                    "description": "Update an existing YouTrack issue by its ID"
                },
                {
                    "name": "youtrack_add_comment",
                    "description": "Add a comment to a YouTrack issue"
                }
            ]
        }
        
        self._set_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def _handle_mcp_request(self, request_json):
        """Handle MCP request"""
        if request_json.get("type") == "resource_request":
            uri = request_json.get("uri", "")
            
            if uri == "mcp://tools/list":
                self._handle_tools_list()
            elif uri == "server://info":
                self._handle_server_info()
            else:
                self._handle_not_found()
        
        elif request_json.get("type") == "tool_call":
            tool_name = request_json.get("name", "")
            parameters = request_json.get("parameters", {})
            
            if tool_name == "youtrack_search_issues":
                self._handle_search_issues(parameters)
            elif tool_name == "youtrack_get_issue":
                self._handle_get_issue(parameters)
            else:
                self._handle_not_found()
        
        else:
            self._handle_bad_request("Unknown request type")
    
    def _handle_server_info(self):
        """Handle server://info request"""
        response = {
            "status": "ok",
            "version": "0.2.0",
            "server": "YouTrack MCP Server",
            "youtrack_url": "https://example.youtrack.cloud"
        }
        
        self._set_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def _handle_search_issues(self, parameters):
        """Handle youtrack_search_issues tool call"""
        query = parameters.get("query", "")
        top = parameters.get("top", 10)
        
        response = {
            "status": "success",
            "result": [
                {
                    "idReadable": "TEST-1",
                    "summary": "Test issue 1",
                    "project": {"shortName": "TEST"}
                },
                {
                    "idReadable": "TEST-2",
                    "summary": "Test issue 2",
                    "project": {"shortName": "TEST"}
                }
            ]
        }
        
        self._set_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def _handle_get_issue(self, parameters):
        """Handle youtrack_get_issue tool call"""
        issue_id = parameters.get("issue_id", "")
        
        response = {
            "status": "success",
            "result": {
                "idReadable": issue_id,
                "summary": f"Test issue {issue_id}",
                "description": "This is a test issue",
                "project": {"shortName": "TEST"},
                "customFields": []
            }
        }
        
        self._set_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def _handle_not_found(self):
        """Handle 404 Not Found"""
        self.send_response(404)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {"error": "Not Found", "path": self.path}
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    def _handle_bad_request(self, message):
        """Handle 400 Bad Request"""
        self.send_response(400)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {"error": message}
        self.wfile.write(json.dumps(response).encode('utf-8'))

def run_server(port=8000):
    """Run the mock MCP server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, MockMCPHandler)
    logger.info(f"Starting mock MCP server on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    # Parse command line arguments
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"Invalid port number: {sys.argv[1]}")
            sys.exit(1)
    
    run_server(port)
