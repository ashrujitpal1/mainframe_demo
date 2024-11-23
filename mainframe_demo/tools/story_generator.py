
from typing import Dict, Any
import requests
from langchain_core.tools import BaseTool
from mainframe_demo.config.settings import settings
import logging

class StoryGeneratorTool(BaseTool):
    name: str = "story_generator"
    description: str = "Generates Java user stories from mainframe business rules"

    def _run(self, business_rule: str) -> Dict[str, Any]:
        try:
            print(" Within the _run method of StoryGeneratorTool ::::: {business_rule}")
            response = requests.post(
                settings.STORY_GENERATOR_URL,
                json={"topic": business_rule},
                timeout=300
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"Error generating story: {str(e)}")
            return {"error": str(e)}