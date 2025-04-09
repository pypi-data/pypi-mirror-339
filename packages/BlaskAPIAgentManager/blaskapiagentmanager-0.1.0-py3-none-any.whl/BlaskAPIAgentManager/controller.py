import os
import json
from typing import Dict, List, Optional, Any, Union
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from datetime import datetime

from .agent import BlaskAPIAgent
from .prompts import parameter_prompt, synthesis_prompt

load_dotenv()


class APIParam(BaseModel):
    """API parameter for API call."""

    name: str = Field(description="Parameter name")
    value: Any = Field(description="Parameter value")


class APIParams(BaseModel):
    """Parameters for API call."""

    path_params: Optional[List[APIParam]] = Field(
        default=None, description="Path parameters"
    )
    query_params: Optional[List[APIParam]] = Field(
        default=None, description="Query parameters"
    )
    body: Optional[Dict[str, Any]] = Field(default=None, description="Request body")


class ControllerTool:
    """Tool for executing API actions based on detailed endpoint information."""

    def __init__(
        self, api_agent: Optional[BlaskAPIAgent] = None, llm: Optional[Any] = None
    ):
        """Initialize the ControllerTool.

        Args:
            api_agent: BlaskAPIAgent instance
            llm: Language model to use for parameter generation
        """
        self.api_agent = api_agent or BlaskAPIAgent()
        self.llm = llm or ChatOpenAI(
            model="perplexity/r1-1776",
            temperature=0.1,
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )

        self.synthesis_chain = synthesis_prompt | self.llm | StrOutputParser()

    def execute_api_actions(self, query: str, actions: List[Dict]) -> Dict[str, Any]:
        """Execute API actions based on the provided plan.

        Args:
            query: The user query
            actions: List of API actions to execute

        Returns:
            Dict[str, Any]: Results of the API calls
        """
        sorted_actions = sorted(actions, key=lambda x: x.get("priority", 999))

        results = {}
        all_results = {}  # Track all results for data enrichment purposes
        enriched_data = {}  # Store enriched data from different calls

        for action in sorted_actions:
            method = action.get("method", "").upper()
            path = action.get("path", "")
            dependencies = action.get("dependencies", [])

            if not method or not path:
                continue

            endpoint_info = self.api_agent.get_endpoint_details(path, method)

            params = self._generate_parameters(query, endpoint_info, all_results)

            path_params = {}
            query_params = {}
            body = {}

            if params.path_params:
                for param in params.path_params:
                    path_params[param.name] = param.value

            if params.query_params:
                for param in params.query_params:
                    query_params[param.name] = param.value

            body = params.body if params.body else {}

            result = self.api_agent.execute_api_call(
                path=path,
                method=method,
                path_params=path_params,
                query_params=query_params,
                body=body,
            )

            result_key = f"{method} {path}"
            results[result_key] = result
            all_results[result_key] = result

            if dependencies and isinstance(result, dict):
                enriched_data[result_key] = self._enrich_result(
                    result, all_results, action
                )
                all_results[f"{result_key}_enriched"] = enriched_data[result_key]

        for key, data in enriched_data.items():
            if data:
                results[key] = data

        return results

    def _enrich_result(self, result: Dict, all_results: Dict, action: Dict) -> Dict:
        """Enrich a result with additional context from other API calls.

        Args:
            result: The API result to enrich
            all_results: All API results collected so far
            action: The current API action being processed

        Returns:
            Dict: Enriched result with additional context
        """
        enriched = result.copy()

        if "brandIds" in result or (
            "data" in result
            and isinstance(result["data"], list)
            and len(result["data"]) > 0
            and "brandId" in result["data"][0]
        ):
            brand_details = {}
            for key, res in all_results.items():
                if "brands" in key.lower() and isinstance(res, dict) and "data" in res:
                    if isinstance(res["data"], list):
                        for brand in res["data"]:
                            if "id" in brand and "name" in brand:
                                brand_details[brand["id"]] = brand
                    elif (
                        isinstance(res["data"], dict)
                        and "id" in res["data"]
                        and "name" in res["data"]
                    ):
                        brand_details[res["data"]["id"]] = res["data"]

            if "brandIds" in result and brand_details:
                enriched["brandNames"] = []
                for brand_id in result["brandIds"]:
                    brand_name = brand_details.get(brand_id, {}).get(
                        "name", f"Unknown Brand {brand_id}"
                    )
                    enriched["brandNames"].append({"id": brand_id, "name": brand_name})

            if "data" in result and isinstance(result["data"], list):
                for item in enriched["data"]:
                    if "brandId" in item and item["brandId"] in brand_details:
                        item["brandName"] = brand_details[item["brandId"]].get("name")

        if "countryIds" in result or (
            "data" in result
            and isinstance(result["data"], list)
            and len(result["data"]) > 0
            and "countryId" in result["data"][0]
        ):
            country_details = {}
            for key, res in all_results.items():
                if (
                    "countries" in key.lower()
                    and isinstance(res, dict)
                    and "data" in res
                ):
                    if isinstance(res["data"], list):
                        for country in res["data"]:
                            if "id" in country and "name" in country:
                                country_details[country["id"]] = country
                    elif (
                        isinstance(res["data"], dict)
                        and "id" in res["data"]
                        and "name" in res["data"]
                    ):
                        country_details[res["data"]["id"]] = res["data"]

            if "countryIds" in result and country_details:
                enriched["countryNames"] = []
                for country_id in result["countryIds"]:
                    country_name = country_details.get(country_id, {}).get(
                        "name", f"Unknown Country {country_id}"
                    )
                    enriched["countryNames"].append(
                        {"id": country_id, "name": country_name}
                    )

            if "data" in result and isinstance(result["data"], list):
                for item in enriched["data"]:
                    if "countryId" in item and item["countryId"] in country_details:
                        item["countryName"] = country_details[item["countryId"]].get(
                            "name"
                        )

        return enriched

    def _generate_parameters(
        self, query: str, endpoint_info: Dict, all_results: Dict = None
    ) -> APIParams:
        """Generate parameters for an API call.

        Args:
            query: The user query
            endpoint_info: Detailed information about the endpoint
            all_results: All API results collected so far

        Returns:
            APIParams: Parameters for the API call
        """
        try:
            endpoint_info_str = json.dumps(endpoint_info, indent=2)
            all_results_str = json.dumps(all_results or {}, indent=2)
            current_date = datetime.now().strftime("%Y-%m-%d")

            parameter_generation_prompt = parameter_prompt.format(
                query=query,
                endpoint_info=endpoint_info_str,
                current_date=current_date,
                previous_results=(
                    "No previous results available."
                    if not all_results
                    else f"Previous API results:\n{all_results_str}"
                ),
            )

            raw_response = self.llm.invoke(parameter_generation_prompt)

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

                params = APIParams()

                if "path_params" in parsed_response and parsed_response["path_params"]:
                    params.path_params = []
                    for param in parsed_response["path_params"]:
                        if (
                            isinstance(param, dict)
                            and "name" in param
                            and "value" in param
                        ):
                            params.path_params.append(
                                APIParam(name=param["name"], value=param["value"])
                            )

                if (
                    "query_params" in parsed_response
                    and parsed_response["query_params"]
                ):
                    params.query_params = []
                    for param in parsed_response["query_params"]:
                        if (
                            isinstance(param, dict)
                            and "name" in param
                            and "value" in param
                        ):
                            params.query_params.append(
                                APIParam(name=param["name"], value=param["value"])
                            )

                if "body" in parsed_response and parsed_response["body"]:
                    params.body = parsed_response["body"]

                return params
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON response: {str(e)}")
                print(f"Raw response text: {response_text}")
                return APIParams()

        except Exception as e:
            print(f"Error generating parameters: {str(e)}")
            return APIParams()

    def synthesize_results(
        self, query: str, api_results: Dict[str, Any], explanation: Optional[str] = None
    ) -> str:
        """Synthesize API results into a coherent summary.

        Args:
            query: The user query
            api_results: Results of the API calls
            explanation: Optional explanation of the API plan

        Returns:
            str: Synthesized summary of the API results
        """
        try:
            api_results_str = json.dumps(api_results, indent=2)

            response = self.llm.invoke(
                synthesis_prompt.format(
                    query=query,
                    api_results=api_results_str,
                    explanation=explanation or "No explanation provided",
                )
            )

            response_text = response.content

            if response_text.startswith("```"):
                response_text = response_text.replace("```", "", 1)
                if response_text.endswith("```"):
                    response_text = response_text[:-3]

            return response_text.strip()
        except Exception as e:
            print(f"Error synthesizing results: {str(e)}")
            return f"Failed to synthesize API results: {str(e)}"
