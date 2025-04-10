from datetime import timedelta, datetime
import requests_cache
import requests
from typing import TypedDict, Optional
import logging

logger = logging.getLogger(__name__)


def strip_headers_hook(response, *args, **kwargs):
    to_preserve = [
        "Content-Type",
        "Date",
        "Content-Encoding",
        "Content-Language",
        "Last-Modified",
    ]
    deleted = set()
    to_preserve_lower = [h.lower() for h in to_preserve]
    header_keys_to_check = response.headers.copy().keys()
    for header in header_keys_to_check:
        if header.lower() in to_preserve_lower:
            continue
        else:
            response.headers.pop(header, None)
            deleted.add(header)
    logger.debug("Deleted headers: %s", ", ".join(deleted))
    return response


class CacheOptions(TypedDict, total=False):
    """
    Options for configuring requests-cache.

    Attributes:
        cache_name (str, optional): The name of the cache. Defaults to 'nordigen'.  Can also be a path.
        backend (str, optional): The cache backend to use (e.g., 'sqlite', 'memory'). Defaults to 'sqlite'.
        expire_after (int, optional): The cache expiration time in seconds. Defaults to 86400 (24 hours).
        old_data_on_error (bool, optional): Whether to return old cached data on a request error. Defaults to False.
    """

    cache_name: requests_cache.StrOrPath
    backend: Optional[requests_cache.BackendSpecifier]
    expire_after: int
    old_data_on_error: bool


class HttpServiceException(Exception):
    """
    Exception raised for HTTP service errors.  This wraps HTTP errors from the underlying requests library.

    Attributes:
        error (str): The original error message.
        response_text (str, optional): The full response text from the server.
    """

    def __init__(self, error, response_text=None):
        self.error = error
        self.response_text = response_text
        super().__init__(f"{error}: {response_text}")


class BaseService:
    """
    Base class for HTTP services handling authentication and requests to the GoCardless Bank Account Data API.

    Attributes:
        BASE_URL (str): The base URL for the API.
        DEFAULT_CACHE_OPTIONS (CacheOptions): Default caching options.
        secret_id (str): Your GoCardless API secret ID.
        secret_key (str): Your GoCardless API secret key.
        token (str, optional): The current API access token.
        session (requests_cache.CachedSession): The cached requests session.
    """

    BASE_URL = "https://bankaccountdata.gocardless.com/api/v2"

    DEFAULT_CACHE_OPTIONS: CacheOptions = {
        "cache_name": "nordigen",
        "backend": "sqlite",
        "expire_after": 0,
        "old_data_on_error": True,
        "match_headers": False,
        "cache_control": False,
    }

    def __init__(
        self,
        secret_id: str,
        secret_key: str,
        cache_options: Optional[CacheOptions],
    ):
        """
        Initializes the BaseService.

        Args:
            secret_id (str): Your GoCardless API secret ID.
            secret_key (str): Your GoCardless API secret key.
            cache_options (CacheOptions, optional):  Custom cache options.  Merges with and overrides DEFAULT_CACHE_OPTIONS.
        """
        self.secret_id = secret_id
        self.secret_key = secret_key
        self._token = None
        merged_options = {**self.DEFAULT_CACHE_OPTIONS, **(cache_options or {})}
        self.session = requests_cache.CachedSession(**merged_options)
        self.session.hooks["response"].append(strip_headers_hook)

    def check_cache_status(self, method: str, url: str, params=None, data=None) -> dict:
        """
        Attempts to predict the cache status for a given request.

        NOTE: This is an approximation and relies on internal mechanisms
              that might change. It also performs I/O to check the cache.

        Args:
            method (str): HTTP method ("GET", "POST", etc.).
            endpoint (str): API endpoint.
            params (dict, optional): URL parameters.
            data (dict, optional): Request body data.

        Returns:
            dict: Information about the potential cache state:
                  {'key_exists': bool, 'is_expired': Optional[bool], 'cache_key': str}
                  'is_expired' is None if the key doesn't exist or expiration
                  cannot be reliably determined without full retrieval.
        """
        headers = {"Authorization": f"Bearer {self.token}"}

        req = requests.Request(method, url, params=params, data=data, headers=headers)
        prepared_request: requests.PreparedRequest = self.session.prepare_request(req)
        cache = self.session.cache
        cache_key = cache.create_key(prepared_request)
        key_exists = cache.contains(cache_key)
        is_expired = None

        if key_exists:
            try:
                # Try to get the response object without triggering expiration side effects
                # Note: This still reads from the cache backend (I/O)
                cached_response = cache.get_response(cache_key)
                if cached_response:
                    # is_expired is a property calculated on the CachedResponse
                    is_expired = cached_response.is_expired
                else:
                    # get_response might return None if item expired and configured to delete
                    # Or if backend consistency issue. Treat as expired/absent.
                    key_exists = False  # Correct the state if get_response fails
                    is_expired = True  # Assume expired if get_response returns None for existing key
            except Exception as e:
                logger.error(
                    f"Error checking expiration for cache key {cache_key}: {e}"
                )
                # Cannot determine expiration reliably
                is_expired = None  # Mark as unknown

        return {
            "key_exists": key_exists,
            "is_expired": is_expired,
            "cache_key": cache_key,
        }

    @property
    def token(self):
        """
        Ensure a token exists.  Gets a new token if one doesn't exist.
        Nordigen tokens don't currently have a refresh mechanism, so this just gets a new one if needed.
        """
        if not self._token:
            self.get_token()
        return self._token

    def get_token(self):
        """
        Fetch a new API access token using credentials. Sets the `self._token` attribute.

        Raises:
            HttpServiceException: If the API request fails.
        """
        response = requests.post(
            f"{self.BASE_URL}/token/new/",
            data={"secret_id": self.secret_id, "secret_key": self.secret_key},
        )
        self._handle_response(response)
        self._token = response.json()["access"]

    def _handle_response(self, response):
        """
        Check response status and handle errors.

        Args:
            response (requests.Response): The response object from the API request.

        Raises:
            HttpServiceException: If the API request returns an error status code.
        """
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise HttpServiceException(str(e), response.text)

    def _request(self, method, endpoint, params=None, data=None):
        """
        Execute an HTTP request with token handling and automatic retries.

        Args:
            method (str): The HTTP method (e.g., "GET", "POST", "DELETE").
            endpoint (str): The API endpoint (relative to BASE_URL).
            params (dict, optional): URL parameters for the request.
            data (dict, optional): Data to send in the request body (for POST requests).

        Returns:
            requests.Response: The response object from the API request.

        Raises:
            HttpServiceException: If the API request fails.
        """
        url = f"{self.BASE_URL}{endpoint}"
        headers = {"Authorization": f"Bearer {self.token}"}

        status = self.check_cache_status(method, url, params, data)
        logger.debug(f"{endpoint}: {'expired' if status["is_expired"] else 'cache ok'}")
        response = self.session.request(
            method, url, headers=headers, params=params, data=data
        )
        logger.info("Response headers", response.headers)

        # Retry once if token expired (401 Unauthorized)
        if response.status_code == 401:
            self.get_token()  # Get a new token
            headers = {"Authorization": f"Bearer {self.token}"}  # Update headers
            response = self.session.request(
                method, url, headers=headers, params=params, data=data
            )

        self._handle_response(response)
        return response

    def _get(self, endpoint, params=None):
        """
        Perform a GET request and return the JSON response.

        Args:
            endpoint (str): The API endpoint.
            params (dict, optional): URL parameters.

        Returns:
            dict: The JSON response from the API.
        """
        return self._request("GET", endpoint, params=params).json()

    def _post(self, endpoint, data=None):
        """
        Perform a POST request and return the JSON response.

        Args:
            endpoint (str): The API endpoint.
            data (dict, optional): Data to send in the request body.

        Returns:
            dict: The JSON response from the API.
        """
        return self._request("POST", endpoint, data=data).json()

    def _delete(self, endpoint):
        """
        Perform a DELETE request and return the JSON response.

        Args:
            endpoint (str): The API endpoint.

        Returns:
            dict: The JSON response from the API.
        """
        return self._request("DELETE", endpoint).json()


class NordigenClient(BaseService):
    """
    Client for interacting with the Nordigen API (GoCardless Bank Account Data).

    This class provides methods for listing banks, creating and managing requisitions (links),
    listing accounts, deleting links, and retrieving transactions. It inherits from `BaseService`
    to handle authentication and HTTP requests.
    """

    def list_banks(self, country="GB"):
        """
        List available institutions (banks) for a given country.

        Args:
            country (str, optional): The two-letter country code (ISO 3166). Defaults to "GB".

        Returns:
            list: A list of dictionaries, each containing the 'name' and 'id' of a bank.

        Example:
            ```python
            client = NordigenClient(...)
            banks = client.list_banks(country="US")
            for bank in banks:
                print(f"{bank['name']} (ID: {bank['id']})")
            ```
        """
        return [
            {"name": bank["name"], "id": bank["id"]}
            for bank in self._get("/institutions/", params={"country": country})
        ]

    def find_requisition_id(self, reference):
        """
        Find a requisition ID by its reference string.

        Args:
            reference (str): The unique reference string associated with the requisition.

        Returns:
            str or None: The requisition ID if found, otherwise None.
        """
        requisitions = self._get("/requisitions/")["results"]
        return next(
            (req["id"] for req in requisitions if req["reference"] == reference), None
        )

    def create_link(self, reference, bank_id, redirect_url="http://localhost"):
        """
        Create a new bank link requisition.

        Args:
            reference (str): A unique reference string for this link.
            bank_id (str): The ID of the institution (bank) to link to.
            redirect_url (str, optional): The URL to redirect the user to after authentication. Defaults to "http://localhost".

        Returns:
            dict: A dictionary with the status of the operation.  If successful, includes the link URL.
                - status: "exists" if a requisition with the given `reference` already exists, "created" otherwise
                - message: A descriptive message
                - link: (If status is "created") The URL to start the linking process.

        Example:
            ```python
            client = NordigenClient(...)
            result = client.create_link(reference="my-unique-ref", bank_id="SANDBOXFINANCE_SFIN0000")
            if result["status"] == "created":
                print(f"Redirect user to: {result['link']}")
            else:
                print(result["message"])
            ```
        """
        if self.find_requisition_id(reference):
            return {"status": "exists", "message": f"Link {reference} exists"}

        response = self._post(
            "/requisitions/",
            data={
                "redirect": redirect_url,
                "institution_id": bank_id,
                "reference": reference,
            },
        )
        return {
            "status": "created",
            "link": response["link"],
            "message": f"Complete linking at: {response['link']}",
        }

    def list_accounts(self):
        """
        List all connected accounts with details (ID, institution, reference, IBAN, currency, name).

        Returns:
            list: A list of dictionaries, each representing a connected account.
        """
        accounts = []
        for req in self._get("/requisitions/")["results"]:
            for account_id in req["accounts"]:
                account = self._get(f"/accounts/{account_id}")
                details = self._get(f"/accounts/{account_id}/details")["account"]

                accounts.append(
                    {
                        "id": account_id,
                        "institution_id": req.get("institution_id", ""),
                        "reference": req["reference"],
                        "iban": account.get("iban", ""),
                        "currency": details.get("currency", ""),
                        "name": details.get("name", "Unknown"),
                    }
                )
        return accounts

    def delete_link(self, reference):
        """
        Delete a bank link (requisition) by its reference.

        Args:
            reference (str): The unique reference string of the link to delete.

        Returns:
            dict: A dictionary with the status and a message.  Status can be "deleted" or "not_found".
        """
        req_id = self.find_requisition_id(reference)
        if not req_id:
            return {"status": "not_found", "message": f"Link {reference} not found"}

        self._delete(f"/requisitions/{req_id}")
        return {"status": "deleted", "message": f"Link {reference} removed"}

    def get_transactions(self, account_id, days_back=180):
        """
        Retrieve transactions for a given account.

        Args:
            account_id (str): The ID of the account.
            days_back (int, optional): The number of days back to retrieve transactions for. Defaults to 180.

        Returns:
            dict: The 'transactions' part of the API response, or an empty dict if no transactions are found.
              See the Nordigen API documentation for the structure of this data.
        """
        date_from = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        return self._get(
            f"/accounts/{account_id}/transactions/",
            params={
                "date_from": date_from,
                "date_to": datetime.now().strftime("%Y-%m-%d"),
            },
        ).get("transactions", [])
