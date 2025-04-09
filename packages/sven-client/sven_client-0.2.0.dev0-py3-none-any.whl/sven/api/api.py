import logging
import os
from typing import Any, Dict, List, Optional

from httpx import AsyncClient, Client

# Configure logging to suppress httpx logs
logging.getLogger("httpx").setLevel(logging.ERROR)


class Api:
    def __init__(self, api_url: str | None = None, api_key: str | None = None):
        """
        Initialize the SvenApi.

        Args:
            api_url: Base URL of the API server
            api_key: API key for authentication
            debug: Enable debug mode for detailed error information
        """
        self.api_url: str | None = api_url
        self.api_key: str | None = api_key
        self.headers: Dict[str, str] = {
            "user-agent": "Sven",
            "Content-Type": "application/json",
        }

    def client(self) -> Client:
        return Client(base_url=self.api_url, headers=self.headers, timeout=120.0)

    async def async_client(self) -> AsyncClient:
        return AsyncClient(base_url=self.api_url, headers=self.headers, timeout=120.0)

    def authenticated_client(self) -> Client:
        headers: Dict[str, str] = self.headers

        if not self.api_key:
            raise ValueError("Sven API key is not set")

        headers["X-API-Key"] = self.api_key

        return Client(base_url=self.api_url, headers=headers, timeout=120.0)

    def authenticated_async_client(self) -> AsyncClient:
        headers: Dict[str, str] = self.headers

        if not self.api_key:
            raise ValueError("Sven API key is not set")

        headers["X-API-Key"] = self.api_key

        return AsyncClient(base_url=self.api_url, headers=headers, timeout=120.0)

    def add_knowledge_from_text(
        self, content: str, name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Add knowledge to the database from text content.

        Args:
            content: The text content to add
            name: Optional name/title for the document

        Returns:
            The API response as a dictionary
        """
        # Create the source data according to KnowledgeTextSource schema
        source_data = {"type": "text", "content": content}
        if name:
            source_data["name"] = name

        try:
            # Send as JSON directly
            response = self.client.post("/api/v1/knowledge", json=source_data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self._handle_request_error("POST", "/api/v1/knowledge", e)
            return {}

    def add_knowledge_from_url(
        self, url: str, name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Add knowledge to the database from a URL.

        Args:
            url: The URL to fetch content from
            name: Optional name/title for the document

        Returns:
            The API response as a dictionary
        """
        # Create the source data according to KnowledgeUrlSource schema
        source_data = {"type": "url", "source": url}
        if name:
            source_data["name"] = name

        try:
            # Send as JSON directly
            response = self.client.post("/api/v1/knowledge", json=source_data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self._handle_request_error("POST", "/api/v1/knowledge", e)
            return {}

    def add_knowledge_from_file(
        self, file_path: str, name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Add knowledge to the database from a file (PDF or Markdown).

        Args:
            file_path: Path to the file to upload
            name: Optional name/title for the document

        Returns:
            The API response as a dictionary
        """
        try:
            # Get file name and extension
            file_name = os.path.basename(file_path)
            file_ext = file_name.split(".")[-1].lower()

            # Read file content
            with open(file_path, "rb") as f:
                file_content = f.read()

            # FastAPI can handle file upload through Form + UploadFile
            # Create a proper multipart/form-data request

            # Add file with appropriate content type
            content_type = "application/pdf" if file_ext == "pdf" else "text/markdown"
            files = {"file": (file_name, file_content, content_type)}

            # Form data fields - need to include the type
            data = {"type": "file"}

            # Add name if provided
            if name:
                data["name"] = name

            response = self.client.post("/api/v1/knowledge", files=files, data=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self._handle_request_error("POST", "/api/v1/knowledge", e)
            return {}

    def search_knowledge(self, query: str, max_results: int = 3) -> Dict[str, Any]:
        """
        Search the knowledge database for relevant information.

        Args:
            query: The search query
            max_results: Maximum number of results to return

        Returns:
            The API response as a dictionary
        """
        params = {"q": query, "max_results": max_results}
        response = self.client.get("/api/v1/knowledge/search", params=params)
        response.raise_for_status()
        return response.json()

    def list_knowledge(self) -> List[Dict[str, Any]]:
        """
        List all knowledge documents.

        Returns:
            List of knowledge documents
        """
        url = "/api/v1/knowledge"
        try:
            response = self.client.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self._handle_request_error("GET", url, e)
            return []

    def delete_knowledge(self, document_id: str) -> bool:
        """
        Delete a knowledge document.

        Args:
            document_id: ID of the document to delete

        Returns:
            True if the document was deleted successfully
        """
        url = f"/api/v1/knowledge/{document_id}"
        try:
            response = self.client.delete(url)
            response.raise_for_status()
            return response.status_code == 204
        except Exception as e:
            self._handle_request_error("DELETE", url, e)
            return False

    def update_knowledge(
        self,
        document_id: str,
        title: Optional[str] = None,
        meta_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Update a knowledge document's metadata.

        Args:
            document_id: ID of the document to update
            title: New title for the document
            meta_data: New metadata for the document

        Returns:
            The updated document
        """
        url = f"/api/v1/knowledge/{document_id}"
        params = {}
        if title:
            params["title"] = title

        try:
            response = self.client.put(url, params=params, json=meta_data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self._handle_request_error("PUT", url, e)
            return {}

    def qa_store(self, categories: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Store question-answer pairs in the knowledge database.

        Args:
            categories: A list of category dictionaries containing question-answer pairs.
                Each category should have:
                - name: The name of the category
                - description: Optional description
                - qa: A list of question-answer pairs, each with 'q', 'a', and optional 'meta_data'

        Returns:
            The API response as a dictionary
        """
        try:
            # Send as JSON directly
            request_data = {"categories": categories}
            # Use an extended timeout of 300 seconds (5 minutes) for this specific operation
            response = self.client.post("/qa/store", json=request_data, timeout=300.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self._handle_request_error("POST", "/qa/store", e)
            return {}

    def qa_query(self, queries: List[str], limit: int = 3) -> Dict[str, Any]:
        """
        Query the QA database for answers to questions.

        Args:
            queries: List of questions to ask
            limit: Maximum number of results per query

        Returns:
            The API response containing answers to the queries
        """
        response = self.client.post(
            "/api/v1/qa/query", json={"queries": queries, "limit": limit}
        )
        response.raise_for_status()
        return response.json()

    def list_models(self) -> List[Dict[str, Any]]:
        """
        List all available models on the server.

        Returns:
            A list of available models and their details
        """
        try:
            response = self.client.get("/v1/models")
            response.raise_for_status()
            result = response.json()

            # Handle standard OpenAI format response
            if (
                isinstance(result, dict)
                and "data" in result
                and isinstance(result["data"], list)
            ):
                return result["data"]

            # Handle other response formats
            if isinstance(result, list):
                return result
            elif isinstance(result, dict):
                # If it's a dictionary with a models key
                if "models" in result:
                    models = result["models"]
                    if isinstance(models, list):
                        return models
                    else:
                        # Convert single model to list if needed
                        return [{"id": models, "description": "Available model"}]
                # If it has model names as keys
                else:
                    return [
                        {
                            "id": k,
                            "description": (
                                v.get("description", "") if isinstance(v, dict) else ""
                            ),
                        }
                        for k, v in result.items()
                    ]
            elif isinstance(result, str):
                # Handle case where the response is just a string
                return [{"id": result, "description": "Available model"}]
            else:
                # For any other format, create a generic representation
                return [{"id": str(result), "description": "Available model"}]
        except Exception as e:
            self._handle_request_error("GET", "/v1/models", e)
            return []
