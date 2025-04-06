"""Asynchronous client for the Unraid GraphQL API."""
import asyncio
import logging
from typing import Any, Dict, Optional

import httpx

from .exceptions import (
    APIError,
    AuthenticationError,
    ConnectionError,
    GraphQLError,
)

logger = logging.getLogger(__name__)


class AsyncAuthManager:
    """Handles authentication and token management for Unraid GraphQL API."""

    def __init__(
        self,
        host: str,
        api_key: str,
        port: int = 443,
        use_ssl: bool = True,
        token_persistence_path: Optional[str] = None,
    ):
        """Initialize the authentication manager.

        Args:
            host: The hostname or IP address of the Unraid server
            api_key: The API key for authentication
            port: The port to connect to (default: 443)
            use_ssl: Whether to use SSL (default: True)
            token_persistence_path: Path to save tokens for persistence (default: None)
        """
        self.host = host
        self.port = port
        self.use_ssl = use_ssl
        self.token_persistence_path = token_persistence_path
        self.api_key = api_key
        self._base_url = f"{'https' if use_ssl else 'http'}://{host}:{port}/graphql"
        self._lock = asyncio.Lock()

    # API key authentication doesn't require token management

    # Note: Username/password authentication has been removed as Unraid GraphQL API
    # now only supports API key authentication

    # Connect sign-in and token refresh methods have been removed as Unraid GraphQL API
    # now only supports API key authentication

    def is_authenticated(self) -> bool:
        """Check if the client is authenticated with a valid API key.

        Returns:
            True if API key is set, False otherwise
        """
        return bool(self.api_key)

    async def get_auth_headers(self) -> Dict[str, str]:
        """Get the authorization headers for API requests.

        Returns:
            Dict with authorization headers containing the API key
        """
        return {"x-api-key": self.api_key}


class AsyncUnraidClient:
    """Asynchronous client for the Unraid GraphQL API."""

    def __init__(
        self,
        host: str,
        api_key: str,
        port: int = 443,
        use_ssl: bool = True,
        token_persistence_path: Optional[str] = None,
        timeout: float = 30.0,
    ):
        """Initialize the Unraid client.

        Args:
            host: The hostname or IP address of the Unraid server
            api_key: The API key for authentication
            port: The port to connect to (default: 443)
            use_ssl: Whether to use SSL (default: True)
            token_persistence_path: Path to save tokens for persistence (default: None)
            timeout: Timeout for HTTP requests in seconds (default: 30.0)
        """
        self.host = host
        self.port = port
        self.use_ssl = use_ssl
        self.timeout = timeout
        self._base_url = f"{'https' if use_ssl else 'http'}://{host}:{port}/graphql"

        # Initialize authentication manager
        self.auth = AsyncAuthManager(host, api_key, port, use_ssl, token_persistence_path)

        # Resource clients will be initialized in the get_resource method
        self._resources = {}

    # Note: Username/password authentication has been removed as Unraid GraphQL API
    # now only supports API key authentication

    # Connect sign-in and logout methods have been removed as Unraid GraphQL API
    # now only supports API key authentication

    def is_authenticated(self) -> bool:
        """Check if the client is authenticated.

        Returns:
            True if authenticated, False otherwise
        """
        return self.auth.is_authenticated()

    async def execute_query(
        self, query: str, variables: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute a GraphQL query.

        Args:
            query: The GraphQL query or mutation
            variables: Variables for the query (default: None)

        Returns:
            The query response data

        Raises:
            AuthenticationError: If not authenticated
            GraphQLError: If a GraphQL error occurs
            ConnectionError: If the server cannot be reached
            APIError: If the API returns an error
        """
        if variables is None:
            variables = {}

        try:
            headers = await self.auth.get_auth_headers()
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self._base_url,
                    json={"query": query, "variables": variables},
                    headers=headers,
                    timeout=self.timeout
                )
                response.raise_for_status()
                data = response.json()

                if "errors" in data:
                    errors = data["errors"]
                    error_message = errors[0].get("message", "Unknown GraphQL error")
                    raise GraphQLError(error_message, errors)

                if "data" not in data:
                    raise APIError("Invalid response format: missing data field")

                return data["data"]

        except httpx.RequestError as e:
            raise ConnectionError(f"Failed to connect to Unraid server: {e}")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise AuthenticationError("Authentication required")
            raise APIError(f"HTTP error: {e}")
        except Exception as e:
            if isinstance(e, (GraphQLError, ConnectionError, AuthenticationError, APIError)):
                raise
            raise APIError(f"Unexpected error: {e}")

    def get_resource(self, resource_type: str):
        """Get a resource client.

        Args:
            resource_type: The type of resource to get

        Returns:
            The resource client
        """
        if resource_type not in self._resources:
            # Import the correct resource class on demand to avoid circular imports
            if resource_type == "array":
                from .resources.array import AsyncArrayResource
                self._resources[resource_type] = AsyncArrayResource(self)
            elif resource_type == "disk":
                from .resources.disk import AsyncDiskResource
                self._resources[resource_type] = AsyncDiskResource(self)
            elif resource_type == "docker":
                from .resources.docker import AsyncDockerResource
                self._resources[resource_type] = AsyncDockerResource(self)
            elif resource_type == "vm":
                from .resources.vm import AsyncVMResource
                self._resources[resource_type] = AsyncVMResource(self)
            elif resource_type == "notification":
                from .resources.notification import AsyncNotificationResource
                self._resources[resource_type] = AsyncNotificationResource(self)
            elif resource_type == "user":
                from .resources.user import AsyncUserResource
                self._resources[resource_type] = AsyncUserResource(self)
            elif resource_type == "info":
                from .resources.info import AsyncInfoResource
                self._resources[resource_type] = AsyncInfoResource(self)
            elif resource_type == "config":
                from .resources.config import AsyncConfigResource
                self._resources[resource_type] = AsyncConfigResource(self)
            else:
                raise ValueError(f"Unknown resource type: {resource_type}")

        return self._resources[resource_type]

    @property
    def array(self):
        """Get the array resource client."""
        return self.get_resource("array")

    @property
    def disk(self):
        """Get the disk resource client."""
        return self.get_resource("disk")

    @property
    def docker(self):
        """Get the docker resource client."""
        return self.get_resource("docker")

    @property
    def vm(self):
        """Get the VM resource client."""
        return self.get_resource("vm")

    @property
    def notification(self):
        """Get the notification resource client."""
        return self.get_resource("notification")

    @property
    def user(self):
        """Get the user resource client."""
        return self.get_resource("user")

    @property
    def info(self):
        """Get the info resource client."""
        return self.get_resource("info")

    @property
    def config(self):
        """Get the config resource client."""
        return self.get_resource("config")

    # Convenience methods
    async def get_system_info(self) -> Dict[str, Any]:
        """Get system information.

        Returns:
            System information

        Raises:
            Various exceptions from execute_query
        """
        return await self.info.get_system_info()

    async def start_array(self) -> Dict[str, Any]:
        """Start the array.

        Returns:
            The mutation response

        Raises:
            Various exceptions from execute_query
        """
        return await self.array.start_array()

    async def stop_array(self) -> Dict[str, Any]:
        """Stop the array.

        Returns:
            The mutation response

        Raises:
            Various exceptions from execute_query
        """
        return await self.array.stop_array()

    async def reboot(self) -> Dict[str, Any]:
        """Reboot the Unraid server.

        Returns:
            The mutation response

        Raises:
            Various exceptions from execute_query
        """
        return await self.info.reboot()

    async def shutdown(self) -> Dict[str, Any]:
        """Shutdown the Unraid server.

        Returns:
            The mutation response

        Raises:
            Various exceptions from execute_query
        """
        return await self.info.shutdown()
