# youtrack_api.py - Functions for interacting with YouTrack API

import os
import logging
import requests
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class YouTrackAPI:
    def __init__(self, base_url: str, token: str):
        """
        Initialize YouTrack API client
        
        Args:
            base_url: YouTrack instance URL (e.g. https://your-instance.youtrack.cloud)
            token: Permanent token for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.token = token
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Accept': 'application/json'
        }

    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request to YouTrack API"""
        url = f"{self.base_url}/api/{endpoint}"
        response = requests.request(method, url, headers=self.headers, **kwargs)
        response.raise_for_status()
        return response.json() if response.text else {}

    def search_issues(
        self,
        query: str,
        fields: str = "idReadable,summary,project(shortName)",
        custom_fields: Optional[str] = None,
        top: int = 100,
        skip: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Search for issues using YouTrack query
        
        Args:
            query: YouTrack search query
            fields: Comma-separated list of fields to return
            custom_fields: Additional custom fields to include
            top: Maximum number of issues to return
            skip: Number of issues to skip
        """
        params = {
            'query': query,
            'fields': fields,
            '$top': top,
            '$skip': skip
        }
        if custom_fields:
            params['customFields'] = custom_fields
            
        return self._make_request('GET', 'issues', params=params)

    def get_issue(
        self,
        issue_id: str,
        fields: str = "idReadable,summary,description,project(shortName),customFields(projectCustomField(field(name)),value(name,login,fullName,text))",
        custom_fields: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get issue details by ID
        
        Args:
            issue_id: Issue ID (e.g. PROJECT-123)
            fields: Fields to return
            custom_fields: Additional custom fields
        """
        params = {'fields': fields}
        if custom_fields:
            params['customFields'] = custom_fields
            
        return self._make_request('GET', f'issues/{issue_id}', params=params)

    def update_issue(
        self,
        issue_id: str,
        data: Dict[str, Any],
        fields: str = "idReadable,summary"
    ) -> Dict[str, Any]:
        """
        Update issue fields
        
        Args:
            issue_id: Issue ID (e.g. PROJECT-123)
            data: Fields to update
            fields: Fields to return in response
        """
        params = {'fields': fields}
        return self._make_request('POST', f'issues/{issue_id}', json=data, params=params)

    def add_comment(
        self,
        issue_id: str,
        comment_text: str,
        fields: str = "id,text,author(login)"
    ) -> Dict[str, Any]:
        """
        Add comment to issue
        
        Args:
            issue_id: Issue ID (e.g. PROJECT-123)
            comment_text: Comment text
            fields: Fields to return in response
        """
        params = {'fields': fields}
        data = {'text': comment_text}
        return self._make_request('POST', f'issues/{issue_id}/comments', json=data, params=params)

def create_youtrack_api() -> YouTrackAPI:
    """Create YouTrack API client from environment variables"""
    url = os.getenv('YOUTRACK_URL')
    token = os.getenv('YOUTRACK_TOKEN')
    
    if not url or not token:
        raise ValueError(
            'YOUTRACK_URL and YOUTRACK_TOKEN environment variables must be set'
        )
        
    return YouTrackAPI(url, token)

# Example usage (for testing purposes)
if __name__ == "__main__":
    if os.getenv('YOUTRACK_URL') == "" or os.getenv('YOUTRACK_TOKEN') == "":
        print("Please set YOUTRACK_URL and YOUTRACK_TOKEN environment variables or update them in youtrack_api.py")
    else:
        # Example: Get details for a specific issue
        issue_id_to_test = "FXS-1673"
        print(f"\nAttempting to get details for issue: {issue_id_to_test}...")
        api = create_youtrack_api()
        issue_details = api.get_issue(issue_id_to_test)

        if isinstance(issue_details, dict) and 'error' not in issue_details:
            print(f"\n--- Details for {issue_details.get('idReadable', 'N/A')} ---")
            print(f"  Summary: {issue_details.get('summary', 'N/A')}")
            print(f"  Project: {issue_details.get('project', {}).get('shortName', 'N/A')}")
            # Optionally print description or other fields if needed
            # print(f"  Description: {issue_details.get('description', 'N/A')}")
            print("--- End Details ---")
        else:
            print(f"\nError getting issue details for {issue_id_to_test}: {issue_details}")

        # You can add calls to other functions like search_issues here for further testing
        # print("\nSearching for issues...")
        # search_results = api.search_issues("project: YourProject state: Open", top=5)
        # # ... (handle search results as before)
