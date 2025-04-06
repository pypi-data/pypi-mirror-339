"""Client for the Unraid GraphQL API.

This module provides a synchronous client for the Unraid GraphQL API."""
import logging
from typing import Any, Dict, Optional

import httpx

from .exceptions import (
    APIError,
    AuthenticationError,
    ConnectionError,
    GraphQLError,
)
from .resources.array import ArrayResource
from .resources.disk import DiskResource
from .resources.docker import DockerResource
from .resources.vm import VMResource
from .resources.notification import NotificationResource
from .resources.user import UserResource
from .resources.info import InfoResource
from .resources.config import ConfigResource

logger = logging.getLogger(__name__)


class UnraidClient:
    """Client for the Unraid GraphQL API.

    This client provides a synchronous interface to the Unraid GraphQL API.
    """

    def __init__(
        self,
        host: str,
        api_key: str,
        port: int = 443,
        use_ssl: bool = True,
        timeout: float = 30.0,
        verify_ssl: bool = False,
    ):
        """Initialize the Unraid client.

        Args:
            host: The hostname or IP address of the Unraid server
            api_key: The API key for authentication
            port: The port to connect to (default: 443)
            use_ssl: Whether to use SSL (default: True)
            timeout: Timeout for HTTP requests in seconds (default: 30.0)
            verify_ssl: Whether to verify SSL certificates (default: False)
        """
        self.host = host
        self.port = port
        self.use_ssl = use_ssl
        self.timeout = timeout
        self.verify_ssl = verify_ssl
        self.api_key = api_key
        self._base_url = f"{'https' if use_ssl else 'http'}://{host}:{port}/graphql"
        self._followed_url = None

        # Set up headers with API key
        self._headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "x-api-key": api_key
        }

        # Follow initial redirect if needed
        self._discover_redirect_url()

        # Initialize resource clients
        self.array = ArrayResource(self)
        self.disk = DiskResource(self)
        self.docker = DockerResource(self)
        self.vm = VMResource(self)
        self.notification = NotificationResource(self)
        self.user = UserResource(self)
        self.info = InfoResource(self)
        self.config = ConfigResource(self)

    def _discover_redirect_url(self) -> None:
        """Discover and follow any redirects to the actual GraphQL endpoint.

        Some Unraid servers may redirect to an Unraid Connect domain.
        This method discovers that URL and updates the base URL accordingly.
        """
        try:
            response = httpx.get(
                self._base_url,
                headers=self._headers,
                verify=self.verify_ssl,
                follow_redirects=False,
                timeout=self.timeout,
            )

            # Check for redirect
            if response.status_code == 302 and 'Location' in response.headers:
                redirect_url = response.headers['Location']
                logger.debug(f"Discovered redirect URL: {redirect_url}")

                # Update our base URL
                self._followed_url = redirect_url

                # Extract domain for Host header if needed
                if '://' in redirect_url:
                    domain = redirect_url.split('/')[2]
                    self._headers["Host"] = domain

        except Exception as e:
            logger.warning(f"Could not discover redirect URL: {e}")

    def set_api_key(self, api_key: str) -> None:
        """Set the API key for authentication.

        Args:
            api_key: The API key to use
        """
        self.api_key = api_key
        self._headers["x-api-key"] = api_key

    def execute_query(
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

        # Use discovered URL if available
        url = self._followed_url or self._base_url

        try:
            with httpx.Client(verify=self.verify_ssl, follow_redirects=True) as client:
                response = client.post(
                    url,
                    json={"query": query, "variables": variables},
                    headers=self._headers,
                    timeout=self.timeout,
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

    def get_system_info(self) -> Dict[str, Any]:
        """Get system information.

        Returns:
            System information

        Raises:
            Various exceptions from execute_query
        """
        return self.info.get_system_info()

    # Convenience methods
    def start_array(self) -> Dict[str, Any]:
        """Start the array.

        Returns:
            The mutation response

        Raises:
            Various exceptions from execute_query
        """
        return self.array.start_array()

    def stop_array(self) -> Dict[str, Any]:
        """Stop the array.

        Returns:
            The mutation response

        Raises:
            Various exceptions from execute_query
        """
        return self.array.stop_array()

    def reboot(self) -> Dict[str, Any]:
        """Reboot the Unraid server.

        Returns:
            The mutation response

        Raises:
            Various exceptions from execute_query
        """
        return self.info.reboot()

    def shutdown(self) -> Dict[str, Any]:
        """Shutdown the Unraid server.

        Returns:
            The mutation response

        Raises:
            Various exceptions from execute_query
        """
        return self.info.shutdown()
