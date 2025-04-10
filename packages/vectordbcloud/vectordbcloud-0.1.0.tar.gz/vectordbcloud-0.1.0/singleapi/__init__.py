"""
SingleAPI Python SDK
~~~~~~~~~~~~~~~~~~~

The official Python SDK for SingleAPI, providing easy access to the SingleAPI platform
for vector database management, embeddings, and context management with ECP.
"""

import os
import json
import time
import uuid
import logging
import requests
from typing import List, Dict, Any, Optional, Union, Tuple, Generator, ContextManager
from contextlib import contextmanager

__version__ = "0.1.0"

logger = logging.getLogger("singleapi")


class SingleAPIError(Exception):
    """Base exception for SingleAPI SDK errors."""
    
    def __init__(self, message, status_code=None, response=None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class AuthenticationError(SingleAPIError):
    """Raised when authentication fails."""
    pass


class RateLimitError(SingleAPIError):
    """Raised when rate limit is exceeded."""
    pass


class ResourceNotFoundError(SingleAPIError):
    """Raised when a requested resource is not found."""
    pass


class ValidationError(SingleAPIError):
    """Raised when request validation fails."""
    pass


class Context:
    """Represents a context in the SingleAPI platform."""
    
    def __init__(self, id: str, metadata: Dict[str, Any] = None, client=None):
        self.id = id
        self.metadata = metadata or {}
        self._client = client
    
    def update(self, metadata: Dict[str, Any]) -> 'Context':
        """Update the context metadata."""
        if self._client:
            return self._client.update_context(self.id, metadata)
        raise SingleAPIError("Context is not associated with a client")
    
    def delete(self) -> bool:
        """Delete the context."""
        if self._client:
            return self._client.delete_context(self.id)
        raise SingleAPIError("Context is not associated with a client")


class QueryResult:
    """Represents a query result from the vector database."""
    
    def __init__(self, id: str, score: float, vector: List[float], metadata: Dict[str, Any]):
        self.id = id
        self.score = score
        self.vector = vector
        self.metadata = metadata


class Subscription:
    """Represents a subscription in the SingleAPI platform."""
    
    def __init__(self, subscription_id: str, plan_id: str, status: str, **kwargs):
        self.subscription_id = subscription_id
        self.plan_id = plan_id
        self.status = status
        self.trial_end = kwargs.get('trial_end')
        self.current_period_start = kwargs.get('current_period_start')
        self.current_period_end = kwargs.get('current_period_end')
        self.usage = kwargs.get('usage', {})


class Limits:
    """Represents usage limits in the SingleAPI platform."""
    
    def __init__(self, limits: Dict[str, Any]):
        self.limits = limits
        self.approaching_limit = limits.get('approaching_limit', False)
        self.approaching_limit_type = limits.get('approaching_limit_type')
        self.limits_exceeded = limits.get('limits_exceeded', False)
        self.exceeded_limit_types = limits.get('exceeded_limit_types', [])


class DeploymentResult:
    """Represents a deployment result in the SingleAPI platform."""
    
    def __init__(self, deployment_id: str, success: bool, resources: List[Dict[str, Any]], error: str = None):
        self.deployment_id = deployment_id
        self.success = success
        self.resources = resources
        self.error = error


class SingleAPI:
    """Client for the SingleAPI platform."""
    
    def __init__(
        self, 
        api_key: str = None, 
        base_url: str = "https://api.singleapi.com/v1",
        timeout: int = 30,
        max_retries: int = 3,
        retry_delay: int = 1
    ):
        self.api_key = api_key or os.environ.get("SINGLEAPI_API_KEY")
        if not self.api_key:
            raise AuthenticationError("API key is required")
        
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self._current_context_id = None
    
    def _request(
        self, 
        method: str, 
        path: str, 
        params: Dict[str, Any] = None, 
        data: Dict[str, Any] = None,
        context_id: str = None
    ) -> Dict[str, Any]:
        """Make a request to the SingleAPI API."""
        url = f"{self.base_url}{path}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": f"singleapi-python/{__version__}"
        }
        
        # Add context ID if provided or if there's a current context
        if context_id or self._current_context_id:
            headers["X-Context-ID"] = context_id or self._current_context_id
        
        retries = 0
        while retries <= self.max_retries:
            try:
                response = requests.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    json=data,
                    timeout=self.timeout
                )
                
                if response.status_code == 429:
                    # Rate limit exceeded, retry after delay
                    retry_after = int(response.headers.get("Retry-After", self.retry_delay))
                    logger.warning(f"Rate limit exceeded, retrying after {retry_after} seconds")
                    time.sleep(retry_after)
                    retries += 1
                    continue
                
                if response.status_code >= 400:
                    self._handle_error_response(response)
                
                return response.json()
            
            except requests.RequestException as e:
                if retries == self.max_retries:
                    raise SingleAPIError(f"Request failed: {str(e)}")
                
                logger.warning(f"Request failed, retrying ({retries+1}/{self.max_retries}): {str(e)}")
                time.sleep(self.retry_delay * (2 ** retries))  # Exponential backoff
                retries += 1
    
    def _handle_error_response(self, response: requests.Response) -> None:
        """Handle error responses from the API."""
        try:
            error_data = response.json()
            error_message = error_data.get("error", {}).get("message", "Unknown error")
        except ValueError:
            error_message = response.text or "Unknown error"
        
        if response.status_code == 401:
            raise AuthenticationError(error_message, response.status_code, response)
        elif response.status_code == 404:
            raise ResourceNotFoundError(error_message, response.status_code, response)
        elif response.status_code == 422:
            raise ValidationError(error_message, response.status_code, response)
        elif response.status_code == 429:
            raise RateLimitError(error_message, response.status_code, response)
        else:
            raise SingleAPIError(error_message, response.status_code, response)
    
    @contextmanager
    def context(self, metadata: Dict[str, Any] = None) -> Generator[Context, None, None]:
        """Create a context and use it for all requests within the block."""
        context = self.create_context(metadata)
        previous_context_id = self._current_context_id
        self._current_context_id = context.id
        
        try:
            yield context
        finally:
            self._current_context_id = previous_context_id
    
    def create_context(self, metadata: Dict[str, Any] = None) -> Context:
        """Create a new context."""
        data = {"metadata": metadata or {}}
        response = self._request("POST", "/contexts", data=data)
        return Context(
            id=response["context_id"],
            metadata=metadata,
            client=self
        )
    
    def get_context(self, context_id: str) -> Context:
        """Get a context by ID."""
        response = self._request("GET", f"/contexts/{context_id}")
        return Context(
            id=response["context_id"],
            metadata=response["metadata"],
            client=self
        )
    
    def update_context(self, context_id: str, metadata: Dict[str, Any]) -> Context:
        """Update a context's metadata."""
        data = {"metadata": metadata}
        response = self._request("PUT", f"/contexts/{context_id}", data=data)
        return Context(
            id=response["context_id"],
            metadata=response["metadata"],
            client=self
        )
    
    def delete_context(self, context_id: str) -> bool:
        """Delete a context."""
        self._request("DELETE", f"/contexts/{context_id}")
        return True
    
    def store_vectors(
        self, 
        vectors: List[List[float]], 
        metadata: List[Dict[str, Any]] = None,
        ids: List[str] = None,
        context_id: str = None
    ) -> List[str]:
        """Store vectors in the vector database."""
        if metadata and len(vectors) != len(metadata):
            raise ValidationError("Number of vectors and metadata must match")
        
        if ids and len(vectors) != len(ids):
            raise ValidationError("Number of vectors and IDs must match")
        
        data = {
            "vectors": vectors,
            "metadata": metadata or [{}] * len(vectors),
            "ids": ids or [str(uuid.uuid4()) for _ in range(len(vectors))]
        }
        
        response = self._request("POST", "/vectors", data=data, context_id=context_id)
        return response["ids"]
    
    def query_vectors(
        self, 
        query_vector: List[float], 
        top_k: int = 10,
        filter_metadata: Dict[str, Any] = None,
        include_vectors: bool = False,
        context_id: str = None
    ) -> List[QueryResult]:
        """Query vectors from the vector database."""
        data = {
            "query_vector": query_vector,
            "top_k": top_k,
            "filter": filter_metadata,
            "include_vectors": include_vectors
        }
        
        response = self._request("POST", "/vectors/query", data=data, context_id=context_id)
        
        results = []
        for result in response["results"]:
            results.append(QueryResult(
                id=result["id"],
                score=result["score"],
                vector=result.get("vector", []),
                metadata=result["metadata"]
            ))
        
        return results
    
    def delete_vectors(self, ids: List[str], context_id: str = None) -> bool:
        """Delete vectors from the vector database."""
        data = {"ids": ids}
        self._request("DELETE", "/vectors", data=data, context_id=context_id)
        return True
    
    def get_subscription(self) -> Subscription:
        """Get the current subscription."""
        response = self._request("GET", "/subscription")
        return Subscription(**response["subscription"])
    
    def check_limits(self) -> Limits:
        """Check usage limits."""
        response = self._request("GET", "/subscription/limits")
        return Limits(response)
    
    def deploy_to_aws(
        self, 
        account_id: str, 
        region: str, 
        resources: List[Dict[str, Any]]
    ) -> DeploymentResult:
        """Deploy resources to AWS."""
        data = {
            "cloud_provider": "aws",
            "account_id": account_id,
            "region": region,
            "resources": resources
        }
        
        response = self._request("POST", "/deployments", data=data)
        return DeploymentResult(
            deployment_id=response["deployment_id"],
            success=response["success"],
            resources=response["resources"],
            error=response.get("error")
        )
    
    def deploy_to_gcp(
        self, 
        project_id: str, 
        region: str, 
        resources: List[Dict[str, Any]]
    ) -> DeploymentResult:
        """Deploy resources to GCP."""
        data = {
            "cloud_provider": "gcp",
            "account_id": project_id,
            "region": region,
            "resources": resources
        }
        
        response = self._request("POST", "/deployments", data=data)
        return DeploymentResult(
            deployment_id=response["deployment_id"],
            success=response["success"],
            resources=response["resources"],
            error=response.get("error")
        )
    
    def deploy_to_azure(
        self, 
        subscription_id: str, 
        resource_group: str,
        location: str,
        resources: List[Dict[str, Any]]
    ) -> DeploymentResult:
        """Deploy resources to Azure."""
        data = {
            "cloud_provider": "azure",
            "account_id": subscription_id,
            "resource_group": resource_group,
            "location": location,
            "resources": resources
        }
        
        response = self._request("POST", "/deployments", data=data)
        return DeploymentResult(
            deployment_id=response["deployment_id"],
            success=response["success"],
            resources=response["resources"],
            error=response.get("error")
        )
    
    def get_deployments(self) -> List[Dict[str, Any]]:
        """Get all deployments."""
        response = self._request("GET", "/deployments")
        return response["deployments"]
    
    def delete_deployment(self, deployment_id: str) -> bool:
        """Delete a deployment."""
        self._request("DELETE", f"/deployments/{deployment_id}")
        return True
