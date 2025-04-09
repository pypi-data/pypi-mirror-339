import os
import json
import requests
from typing import Dict, List, Optional, Any, Union
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


class BlaskAPIAgent:
    """Agent for interacting with Blask API based on Swagger spec."""

    def __init__(
        self,
        swagger_url: str = None,
        login_url: str = None,
        base_url: str = None,
        username: str = None,
        password: str = None,
        llm: Optional[Any] = None,
    ):
        """Initialize the BlaskAPIAgent.

        Args:
            swagger_url: URL for the Swagger JSON specification
            login_url: URL for API authentication
            base_url: Base URL for API requests
            username: Username for API authentication
            password: Password for API authentication
            llm: Language model to use for agent operations
        """

        self.swagger_url = swagger_url or os.getenv(
            "SWAGGER_JSON_URL", "https://app.stage.blask.com/api/swagger-json"
        )
        self.login_url = login_url or os.getenv(
            "LOGIN_URL", "https://app.stage.blask.com/api/auth/sign-in"
        )
        self.base_url = base_url or os.getenv(
            "BASE_URL", "https://app.stage.blask.com/api"
        )
        self.username = username or os.getenv("BLASK_USERNAME")
        self.password = password or os.getenv("BLASK_PASSWORD")

        self.session = requests.Session()
        self.is_authenticated = False

        self.llm = llm or ChatOpenAI(
            model="perplexity/r1-1776",
            temperature=0.1,
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )

        self.swagger_data = None

    def authenticate(self) -> bool:
        """Authenticate with the Blask API.

        Returns:
            bool: True if authentication was successful, False otherwise
        """
        if self.is_authenticated:
            return True

        payload = {"identifier": self.username, "password": self.password}

        try:
            response = self.session.post(self.login_url, json=payload)

            if response.status_code in [200, 201]:
                self.is_authenticated = True
                return True
            else:
                print(f"Authentication error: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            print(f"Authentication error: {str(e)}")
            return False

    def load_swagger_spec(self) -> Dict:
        """Load the Swagger specification.

        Returns:
            Dict: The Swagger specification as a dictionary
        """
        if self.swagger_data:
            return self.swagger_data

        try:
            response = self.session.get(self.swagger_url)
            if response.status_code == 200:
                self.swagger_data = response.json()
                return self.swagger_data
            else:
                print(
                    f"Error loading Swagger spec: {response.status_code} - {response.text}"
                )
                return {}
        except Exception as e:
            print(f"Error loading Swagger spec: {str(e)}")
            return {}

    def get_endpoint_summary(self) -> Dict[str, List[Dict[str, str]]]:
        """Get a summary of available API endpoints.

        Returns:
            Dict[str, List[Dict[str, str]]]: A dictionary of endpoint categories
                with endpoint names and descriptions
        """
        if not self.swagger_data:
            self.load_swagger_spec()

        if not self.swagger_data:
            return {}

        summary = {}

        for path, path_info in self.swagger_data.get("paths", {}).items():
            for method, method_info in path_info.items():
                if method.lower() not in ["get", "post", "put", "delete", "patch"]:
                    continue

                tag = method_info.get("tags", ["Other"])[0]

                if tag not in summary:
                    summary[tag] = []

                summary[tag].append(
                    {
                        "method": method.upper(),
                        "path": path,
                        "summary": method_info.get("summary", "No description"),
                        "operationId": method_info.get(
                            "operationId", f"{method}_{path}"
                        ),
                    }
                )

        return summary

    def get_endpoint_details(self, path: str, method: str) -> Dict:
        """Get detailed information about a specific endpoint.

        Args:
            path: The API path
            method: The HTTP method (GET, POST, etc.)

        Returns:
            Dict: Detailed information about the endpoint
        """
        if not self.swagger_data:
            self.load_swagger_spec()

        if not self.swagger_data:
            return {}

        path_info = self.swagger_data.get("paths", {}).get(path, {})
        method_info = path_info.get(method.lower(), {})

        if not method_info:
            return {}

        parameters = method_info.get("parameters", [])

        request_body = {}
        if "requestBody" in method_info:
            content = method_info["requestBody"].get("content", {})
            if "application/json" in content:
                schema = content["application/json"].get("schema", {})
                request_body = self._resolve_schema_ref(schema)

        responses = {}
        for status, response_info in method_info.get("responses", {}).items():
            content = response_info.get("content", {})
            if "application/json" in content:
                schema = content["application/json"].get("schema", {})
                responses[status] = {
                    "description": response_info.get("description", ""),
                    "schema": self._resolve_schema_ref(schema),
                }
            else:
                responses[status] = {
                    "description": response_info.get("description", ""),
                }

        return {
            "method": method.upper(),
            "path": path,
            "summary": method_info.get("summary", ""),
            "description": method_info.get("description", ""),
            "parameters": parameters,
            "requestBody": request_body,
            "responses": responses,
        }

    def _resolve_schema_ref(self, schema: Dict) -> Dict:
        """Resolve schema references.

        Args:
            schema: Schema with potentially nested references

        Returns:
            Dict: Resolved schema
        """
        if not schema:
            return {}

        if "$ref" in schema:
            ref = schema["$ref"]
            if ref.startswith("#/components/schemas/"):
                schema_name = ref.split("/")[-1]
                return (
                    self.swagger_data.get("components", {})
                    .get("schemas", {})
                    .get(schema_name, {})
                )

        return schema

    def execute_api_call(
        self,
        path: str,
        method: str,
        path_params: Dict[str, Any] = None,
        query_params: Dict[str, Any] = None,
        body: Dict[str, Any] = None,
    ) -> Dict:
        """Execute an API call.

        Args:
            path: The API path
            method: The HTTP method (GET, POST, etc.)
            path_params: Parameters to substitute in the path
            query_params: Query parameters
            body: Request body for POST/PUT operations

        Returns:
            Dict: API response
        """
        if not self.is_authenticated:
            if not self.authenticate():
                return {"error": "Authentication failed"}

        actual_path = path
        if path_params:
            for param, value in path_params.items():
                actual_path = actual_path.replace(f"{{{param}}}", str(value))

        url = f"{self.base_url}{actual_path}"

        try:
            method = method.lower()
            if method == "get":
                response = self.session.get(url, params=query_params)
            elif method == "post":
                response = self.session.post(url, params=query_params, json=body)
            elif method == "put":
                response = self.session.put(url, params=query_params, json=body)
            elif method == "delete":
                response = self.session.delete(url, params=query_params, json=body)
            elif method == "patch":
                response = self.session.patch(url, params=query_params, json=body)
            else:
                return {"error": f"Unsupported HTTP method: {method}"}

            if response.status_code in [200, 201]:
                try:
                    return response.json()
                except:
                    return {"content": response.text}
            else:
                return {
                    "error": f"API call failed with status {response.status_code}",
                    "details": response.text,
                }

        except Exception as e:
            return {"error": f"Exception during API call: {str(e)}"}
