import json
from typing import Dict, Any
from langchain_core.tools import BaseTool
import requests

class UserStoryAPITool(BaseTool):
    name: str = "user_story_api"
    description: str = "Calls API endpoint to generate user stories"

    def _run(self, story_input: str) -> Dict[str, Any]:
        try:
            
            print(f"Within the UserStoryAPITool class story_input")
            
            response = requests.post(
                "http://localhost:5002/api/generate",
                json={"topic": story_input},
                headers={"Content-Type": "application/json"},
                timeout=300
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API call failed: {str(e)}")
