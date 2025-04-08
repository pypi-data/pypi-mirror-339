import httpx
import datetime
from typing import Optional, List, Dict, Any, Union

class UpdateServerClientError(Exception):
    """Custom exception for client errors."""
    pass

class UpdateServerClient:
    """
    Client for interacting with the Live Update Server (HTTP Polling version).
    """
    def __init__(self, base_url: str, timeout: float = 10.0):
        """
        Initializes the client.

        Args:
            base_url: The base URL of the live update server (e.g., "http://localhost:5000").
            timeout: Default request timeout in seconds.
        """
        if not base_url.endswith('/'):
            base_url += '/'
        self.base_url = base_url
        self.timeout = timeout
        self._client = httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout)

    async def close(self):
        """Closes the underlying httpx client. Recommended to call when done."""
        await self._client.aclose()

    async def send_update(
        self,
        scan_uuid: str,
        tool_name: str,
        content: Union[str, Dict, List],
        log_type: Optional[str] = None,
    ) -> int:
        """
        Sends a log or result update to the server.

        Args:
            scan_uuid: The UUID of the scan.
            tool_name: The name of the tool sending the update.
            content: The log message (str) or structured result (dict/list).
            log_type: The type of the log (e.g., 'stdout', 'stderr', 'result', 'status').

        Returns:
            The ID of the created update entry on the server.

        Raises:
            UpdateServerClientError: If the request fails or the server returns an error.
        """
        url_path = f"api/update/{scan_uuid}/{tool_name}"
        payload = {
            "log_type": log_type,
            "content": content, # httpx handles JSON encoding for dict/list
        }
        try:
            response = await self._client.post(url_path, json=payload)
            response.raise_for_status() # Raise exception for 4xx/5xx status codes
            response_data = response.json()
            if "id" not in response_data:
                 raise UpdateServerClientError(f"Server response missing 'id': {response_data}")
            return response_data["id"]
        except httpx.RequestError as e:
            raise UpdateServerClientError(f"Network error sending update to {e.request.url}: {e}") from e
        except httpx.HTTPStatusError as e:
            error_detail = e.response.text
            try:
                error_detail = e.response.json().get("error", error_detail)
            except Exception:
                pass
            raise UpdateServerClientError(
                f"Server error sending update ({e.response.status_code}) to {e.request.url}: {error_detail}"
            ) from e
        except Exception as e:
             raise UpdateServerClientError(f"An unexpected error occurred during send_update: {e}") from e


    async def get_updates(
        self,
        scan_uuid: str,
        since_id: Optional[int] = None,
        since_timestamp: Optional[Union[datetime.datetime, str]] = None,
        tool_name: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Fetches updates for a specific scan, optionally filtering for new ones.

        Args:
            scan_uuid: The UUID of the scan to fetch updates for.
            since_id: If provided, fetch updates with an ID greater than this.
            since_timestamp: If provided (as datetime or ISO string), fetch updates newer than this.
                               Note: Using since_id is generally preferred for polling consistency.
            tool_name: If provided, only fetch updates from this specific tool.

        Returns:
            A list of update dictionaries received from the server.

        Raises:
            UpdateServerClientError: If the request fails or the server returns an error.
        """
        url_path = f"api/updates/{scan_uuid}"
        params = {}
        if since_id is not None:
            params['since_id'] = since_id
        if since_timestamp is not None:
            if isinstance(since_timestamp, datetime.datetime):
                params['since_timestamp'] = since_timestamp.isoformat()
            else:
                params['since_timestamp'] = since_timestamp
        if tool_name is not None:
            params['tool_name'] = tool_name

        try:
            response = await self._client.get(url_path, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise UpdateServerClientError(f"Network error getting updates from {e.request.url}: {e}") from e
        except httpx.HTTPStatusError as e:
            error_detail = e.response.text
            try:
                error_detail = e.response.json().get("error", error_detail)
            except Exception:
                pass
            raise UpdateServerClientError(
                f"Server error getting updates ({e.response.status_code}) from {e.request.url}: {error_detail}"
            ) from e
        except Exception as e:
             raise UpdateServerClientError(f"An unexpected error occurred during get_updates: {e}") from e