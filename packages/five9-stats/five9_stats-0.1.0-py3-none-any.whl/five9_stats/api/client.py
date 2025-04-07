"""
Base client for Five9 Statistics APIs.

This module provides a base client class that handles authentication and common HTTP operations
for both the Interval Statistics API and the Real-time Stats Snapshot API.
"""

import asyncio
import json
import logging
import time
from typing import Dict, Any, Optional, List, Union, TypeVar, Type, Generic

import aiohttp
from pydantic import BaseModel

from five9_stats.models.common import TraceableHttpError

T = TypeVar('T', bound=BaseModel)

logger = logging.getLogger(__name__)


class Five9StatsClient:
    """Base client for Five9 Statistics APIs."""
    
    def __init__(
        self,
        username: str,
        password: str,
        base_url: str = "https://api.prod.us.five9.net",
        timeout: int = 30,
        max_retries: int = 3,
        retry_delay: int = 1,
    ):
        """
        Initialize the Five9 Stats client.
        
        Args:
            username: Five9 username
            password: Five9 password
            base_url: Base URL for the Five9 API
            timeout: Request timeout in seconds
            max_retries: Maximum number of retries for failed requests
            retry_delay: Delay between retries in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.username = username
        self.password = password
        
        # OAuth token data
        self._access_token = None
        self._refresh_token = None
        self._token_expiry = 0
        self._refresh_token_expiry = 0
        
        self._session = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.create_session()
        # Authenticate when entering the context
        await self.authenticate()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close_session()
    
    async def create_session(self):
        """Create an aiohttp session."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
                timeout=aiohttp.ClientTimeout(total=self.timeout),
            )
    
    async def close_session(self):
        """Close the aiohttp session."""
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None
    
    async def authenticate(self):
        """
        Authenticate with the Five9 API and obtain an access token.
        
        This method will obtain a new token if one doesn't exist or if the current token
        is expired. It will try to use the refresh token if available, otherwise it will
        perform a full authentication.
        
        Returns:
            str: The access token
        """
        current_time = time.time()
        
        # Check if we have a valid access token
        if self._access_token and current_time < self._token_expiry - 30:  # 30-second buffer
            return self._access_token
            
        # Check if we can use refresh token
        if self._refresh_token and current_time < self._refresh_token_expiry - 30:
            try:
                await self._refresh_access_token()
                return self._access_token
            except Exception as e:
                logger.warning(f"Failed to refresh token: {str(e)}. Trying full authentication.")
                
        # Perform full authentication
        await self._obtain_new_token()
        return self._access_token
    
    async def _obtain_new_token(self):
        """
        Obtain a new access token using username and password.
        """
        if self._session is None or self._session.closed:
            await self.create_session()
            
        auth_url = f"{self.base_url}/cloudauthsvcs/v1/admin/login"
        auth_data = {
            "userName": self.username,
            "password": self.password
        }
        
        logger.debug(f"Authenticating with Five9 API at {auth_url}")
        
        async with self._session.post(
            auth_url,
            json=auth_data,
            headers={"Content-Type": "application/json"}
        ) as response:
            if response.status != 200:
                response_text = await response.text()
                raise ValueError(f"Authentication failed: {response.status} - {response_text}")
                
            token_data = await response.json()
            
            # Store token data
            self._access_token = token_data.get("access_token")
            self._refresh_token = token_data.get("refresh_token")
            
            # Calculate expiry times
            current_time = time.time()
            self._token_expiry = current_time + token_data.get("expires_in", 600)
            self._refresh_token_expiry = current_time + token_data.get("refresh_token_expires_in", 1800)
            
            logger.debug("Successfully obtained new access token")
    
    async def _refresh_access_token(self):
        """
        Refresh the access token using the refresh token.
        """
        # Note: Implement this method if Five9 API supports token refresh
        # For now, we'll just obtain a new token
        await self._obtain_new_token()
    
    async def _request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        response_model: Optional[Type[T]] = None,
        auth_required: bool = True,
    ) -> Union[T, Dict[str, Any], List[Dict[str, Any]]]:
        """
        Make an HTTP request to the Five9 API.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            path: API path (without base URL)
            params: Query parameters
            json_data: JSON request body
            headers: Additional headers
            response_model: Pydantic model for response parsing
            auth_required: Whether authentication is required for this request
            
        Returns:
            Parsed response as a Pydantic model or dictionary
            
        Raises:
            aiohttp.ClientError: If the request fails
            ValueError: If the response cannot be parsed
        """
        if self._session is None or self._session.closed:
            await self.create_session()
            
        # Get authentication token if required
        if auth_required:
            await self.authenticate()
        
        url = f"{self.base_url}{path}"
        all_headers = {}
        if headers:
            all_headers.update(headers)
            
        # Add authorization header if required
        if auth_required and self._access_token:
            all_headers["Authorization"] = f"Bearer {self._access_token}"
        
        retries = 0
        while True:
            try:
                logger.debug(f"Making {method} request to {url}")
                if params:
                    logger.debug(f"Request params: {params}")
                if json_data:
                    logger.debug(f"Request body: {json_data}")
                if all_headers:
                    # Don't log Authorization header for security
                    safe_headers = {k: v for k, v in all_headers.items() if k.lower() != 'authorization'}
                    logger.debug(f"Request headers: {safe_headers}")
                
                async with self._session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=json_data,
                    headers=all_headers,
                ) as response:
                    logger.debug(f"Response status: {response.status}")
                    logger.debug(f"Response headers: {response.headers}")
                    
                    response_text = await response.text()
                    logger.debug(f"Response body: {response_text[:1000]}{'...' if len(response_text) > 1000 else ''}")
                    
                    # Check for error responses
                    if response.status >= 400:
                        try:
                            error_data = await response.json()
                            try:
                                # Use the new parse_error method for more flexible error parsing
                                error = TraceableHttpError.parse_error(error_data)
                                error_msg = f"API error: {error.message} (Code: {error.code}, Trace ID: {error.trace_id})"
                                
                                # Log additional details if available
                                if error.details:
                                    details_str = ", ".join([f"{d.code}: {d.message}" for d in error.details if d.code and d.message])
                                    logger.error(f"Error details: {details_str}")
                            except Exception as parse_err:
                                # If parsing as TraceableHttpError fails, log the raw error data
                                logger.error(f"Failed to parse error response: {str(parse_err)}")
                                logger.error(f"Raw error data: {error_data}")
                                error_msg = f"API error: {response.status} - {error_data}"
                        except Exception as json_err:
                            logger.error(f"Failed to parse error response as JSON: {str(json_err)}")
                            error_msg = f"API error: {response.status} - {response_text}"
                        
                        # Handle rate limiting (429)
                        if response.status == 429:
                            retry_after = response.headers.get("Retry-After")
                            if retry_after and retries < self.max_retries:
                                try:
                                    wait_time = int(retry_after)
                                except ValueError:
                                    wait_time = self.retry_delay
                                
                                logger.warning(f"Rate limited. Retrying after {wait_time} seconds...")
                                await asyncio.sleep(wait_time)
                                retries += 1
                                continue
                        
                        # Handle service unavailable (503)
                        if response.status == 503 and retries < self.max_retries:
                            retry_after = response.headers.get("Retry-After")
                            wait_time = int(retry_after) if retry_after else self.retry_delay
                            
                            logger.warning(f"Service unavailable. Retrying after {wait_time} seconds...")
                            await asyncio.sleep(wait_time)
                            retries += 1
                            continue
                        
                        raise ValueError(error_msg)
                    
                    # Parse successful response
                    if response_text:
                        try:
                            data = await response.json()
                            if response_model:
                                return response_model.parse_obj(data)
                            return data
                        except Exception as e:
                            raise ValueError(f"Failed to parse response: {str(e)}")
                    
                    return None
            
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                if retries < self.max_retries:
                    wait_time = self.retry_delay * (2 ** retries)  # Exponential backoff
                    logger.warning(f"Request failed: {str(e)}. Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                    retries += 1
                else:
                    raise
    
    async def get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        response_model: Optional[Type[T]] = None,
        auth_required: bool = True,
    ) -> Union[T, Dict[str, Any], List[Dict[str, Any]]]:
        """
        Make a GET request to the Five9 API.
        
        Args:
            path: API path (without base URL)
            params: Query parameters
            headers: Additional headers
            response_model: Pydantic model for response parsing
            auth_required: Whether authentication is required for this request
            
        Returns:
            Parsed response as a Pydantic model or dictionary
        """
        return await self._request("GET", path, params=params, headers=headers,
                                  response_model=response_model, auth_required=auth_required)
    
    async def post(
        self,
        path: str,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        response_model: Optional[Type[T]] = None,
        auth_required: bool = True,
    ) -> Union[T, Dict[str, Any], List[Dict[str, Any]]]:
        """
        Make a POST request to the Five9 API.
        
        Args:
            path: API path (without base URL)
            json_data: JSON request body
            params: Query parameters
            headers: Additional headers
            response_model: Pydantic model for response parsing
            auth_required: Whether authentication is required for this request
            
        Returns:
            Parsed response as a Pydantic model or dictionary
        """
        return await self._request(
            "POST", path, params=params, json_data=json_data, headers=headers,
            response_model=response_model, auth_required=auth_required
        )
    
    async def put(
        self,
        path: str,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        response_model: Optional[Type[T]] = None,
        auth_required: bool = True,
    ) -> Union[T, Dict[str, Any], List[Dict[str, Any]]]:
        """
        Make a PUT request to the Five9 API.
        
        Args:
            path: API path (without base URL)
            json_data: JSON request body
            params: Query parameters
            headers: Additional headers
            response_model: Pydantic model for response parsing
            auth_required: Whether authentication is required for this request
            
        Returns:
            Parsed response as a Pydantic model or dictionary
        """
        return await self._request(
            "PUT", path, params=params, json_data=json_data, headers=headers,
            response_model=response_model, auth_required=auth_required
        )
    
    async def delete(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        response_model: Optional[Type[T]] = None,
        auth_required: bool = True,
    ) -> Union[T, Dict[str, Any], List[Dict[str, Any]]]:
        """
        Make a DELETE request to the Five9 API.
        
        Args:
            path: API path (without base URL)
            params: Query parameters
            headers: Additional headers
            response_model: Pydantic model for response parsing
            auth_required: Whether authentication is required for this request
            
        Returns:
            Parsed response as a Pydantic model or dictionary
        """
        return await self._request("DELETE", path, params=params, headers=headers,
                                  response_model=response_model, auth_required=auth_required)