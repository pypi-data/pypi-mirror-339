import os
import json
from typing import Dict, List, Optional, Any, Tuple
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from datetime import datetime

from .agent import BlaskAPIAgent
from .prompts import planning_prompt

load_dotenv()


class APIAction(BaseModel):
    """An API action to take."""

    method: str = Field(description="HTTP method (GET, POST, PUT, DELETE, PATCH)")
    path: str = Field(description="API endpoint path")
    reason: str = Field(description="Reason for selecting this endpoint")
    priority: int = Field(description="Priority order (1 = highest)")
    dependencies: List[str] = Field(description="List of dependencies")


class APIPlan(BaseModel):
    """The API action plan."""

    actions: List[APIAction] = Field(description="List of API actions to take")
    explanation: str = Field(description="Overall explanation of the plan")


class PlannerTool:
    """Tool for planning API actions based on Swagger endpoints."""

    def __init__(
        self, api_agent: Optional[BlaskAPIAgent] = None, llm: Optional[Any] = None
    ):
        """Initialize the PlannerTool.

        Args:
            api_agent: BlaskAPIAgent instance
            llm: Language model to use for planning
        """
        self.api_agent = api_agent or BlaskAPIAgent()
        self.llm = llm or ChatOpenAI(
            model="perplexity/r1-1776",
            temperature=0.1,
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )

    def get_api_plan(self, query: str) -> Tuple[List[Dict], str]:
        """Generate an API action plan based on the query.

        Args:
            query: The user query to plan for

        Returns:
            Tuple[List[Dict], str]: A tuple of (actions list, explanation)
        """
        endpoints_summary = self._format_endpoints_summary()
        current_date = datetime.now().strftime("%Y-%m-%d")

        try:
            raw_response = self.llm.invoke(
                planning_prompt.format(
                    query=query,
                    endpoints_summary=endpoints_summary,
                    current_date=current_date,
                )
            )

            response_text = raw_response.content

            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "", 1)
                if response_text.endswith("```"):
                    response_text = response_text[:-3]
            elif response_text.startswith("```"):
                response_text = response_text.replace("```", "", 1)
                if response_text.endswith("```"):
                    response_text = response_text[:-3]

            try:
                parsed_response = json.loads(response_text.strip())
                actions = parsed_response.get("actions", [])
                explanation = parsed_response.get(
                    "explanation", "No explanation provided"
                )

                return actions, explanation
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON response: {str(e)}")
                print(f"Raw response text: {response_text}")
                return [], f"Error parsing response: {str(e)}"

        except Exception as e:
            print(f"Error generating API plan: {str(e)}")
            return [], f"Error generating plan: {str(e)}"

    def _format_endpoints_summary(self) -> str:
        """Format the endpoints summary for the prompt.

        Returns:
            str: Formatted endpoints summary
        """
        summary = self.api_agent.get_endpoint_summary()

        formatted_summary = ""
        for category, endpoints in summary.items():
            formatted_summary += f"CATEGORY: {category}\n"

            for endpoint in endpoints:
                formatted_summary += f"- {endpoint['method']} {endpoint['path']}: {endpoint['summary']}\n"

            formatted_summary += "\n"

        return formatted_summary
