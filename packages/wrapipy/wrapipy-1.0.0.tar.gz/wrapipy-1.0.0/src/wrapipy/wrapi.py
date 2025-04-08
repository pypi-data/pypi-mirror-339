"""The definition of the WrAPI API wrapper and related objects."""

import re
import time
from enum import Enum, auto
from typing import Dict, List, Optional

import requests
from pydantic import BaseModel

from wrapipy.swagger import SwaggerDoc, SwaggerPath

__pdoc__ = {}

REQ_PATH_RE = re.compile("{.*?}")
"""Regular expression matching a path parameter placehodler."""
LOCALHOST = "127.0.0.1"
"""Default host of Swagger 2.0 specifications."""


class RequestType(Enum):
    """Swagger 2.0 supported request types."""

    GET = auto()
    __pdoc__["RequestType.GET"] = " "
    POST = auto()
    __pdoc__["RequestType.POST"] = " "
    DELETE = auto()
    __pdoc__["RequestType.DELETE"] = " "
    PUT = auto()
    __pdoc__["RequestType.PUT"] = " "
    HEAD = auto()
    __pdoc__["RequestType.HEAD"] = " "
    OPTIONS = auto()
    __pdoc__["RequestType.OPTIONS"] = " "
    PATCH = auto()
    __pdoc__["RequestType.PATCH"] = " "


class Endpoint(BaseModel):
    """A minimal specification of an API endpoint as its resource path and request type."""

    __pdoc__["Endpoint.__init__"] = (
        "A minimal specification of an API endpoint as its resource path and request type."
    )
    resource_path: str
    __pdoc__["Endpoint.resource_path"] = " "
    request_type: str
    __pdoc__["Endpoint.request_type"] = " "
    __pdoc__["Endpoint.model_config"] = False


class WrAPI(object):
    """A wrapper around a Swagger 2.0 API documentation allowing to conveniently send requests
    to the API and receive responses from it.

    Attributes:
        domain (str): the domain of the API, i.e., http or https (if supported) protocol designation followed by the host specification.
        base_path (str): the location of the API with respect to the domain.
        endpoints (Dict[str, Endpoint]): the dictionary of endpoints of this API as their name (resource path) and Endpoint object representing them.
        swagger (wrapi.swagger.SwaggerDoc): the Swagger 2.0 documentation object of this API.
    """

    def __init__(self, swagger: SwaggerDoc) -> None:
        """Initialise the API.

        Args:
            swagger (SwaggerDoc): the Swagger 2.0 documentation object of this API.
        """
        self.domain = f"{'https' if 'https' in swagger.schemes else 'http'}://{swagger.host if swagger.host else LOCALHOST}"
        self.base_path = swagger.base_path if swagger.base_path else ""
        self.endpoints = self._parse_endpoints(swagger.paths)
        self.swagger = swagger

    def _parse_endpoints(self, paths: Dict[str, SwaggerPath]) -> Dict[str, Endpoint]:
        """Parse endpoints from the `paths` object of a Swagger 2.0 documentation object.

        Args:
            paths (Dict[str, SwaggerPath]): the `paths` object of a Swagger 2.0 documentation object.

        Returns:
            Dict[str, Endpoint]: the dictionary of endpoints of this API as their name
            (resource path) and Endpoint object representing them.
        """
        request_types = RequestType.__members__.keys()
        endpoints = {}
        for resource_path, path_entry in paths.items():
            for request_type in request_types:
                if getattr(path_entry, request_type.lower()):
                    endpoints[resource_path] = Endpoint(
                        resource_path=resource_path, request_type=request_type
                    )
        return endpoints

    def _send_request(self, endpoint: Endpoint, params: Dict) -> Dict:
        """_send_request.

        Args:
            endpoint (Endpoint): endpoint
            params (Dict): params

        Returns:
            Dict:
        """
        url = f"{self.domain}{self.base_path}{re.sub(REQ_PATH_RE, params.get('path', ''), endpoint.resource_path)}"
        return requests.request(
            endpoint.request_type,
            url,
            params=params.get("query", {}),
            json=params.get("payload", {}),
        )

    def request(
        self,
        endpoint_name: str,
        params: Dict,
        max_attempts: int = 100,
        wait_time: float = 0.1,
        retry_responses: List[int] = [429],
    ) -> Optional[requests.Response]:
        """Send a request to the specified endpoint of this API with given parameters.

        If a response code of one of the codes in `retry_responses` is returned, wait `wait_time` seconds,
        and retry. Repeat until a response code outside of the `retry_responses` set is returned, but
        at most `max_attempt` times.

        Args:
            endpoint_name (str): The name of the endpoint, aka its resource path.
            params (Dict): The parameters of this request as a dictionary with keys `"query"` (for a dictionary of query parameters as key-value pairs), `"path"` (for the path parameter), and `"payload"` (for the dictionary of payload parameters as key-value pairs).
            max_attempts (int): The maximum number of attempts to perform in case a response from `retry_responses` is received.
            wait_time (float): The waiting time in seconds before a new attempt is performed in case a response from `retry_responses` is received.
            retry_responses (List[int]): The list of responses as their codes for which to re-attempt the request.

        Returns:
            Optional[requests.Response]: The response of the endpoint to the request if the endpoint name is found, else `None`.
        """
        endpoint = self.endpoints.get(endpoint_name)
        if endpoint:
            attempts = 1
            r = self._send_request(endpoint, params)

            while r.status_code in retry_responses and attempts < max_attempts:
                time.sleep(wait_time)
                r = self._send_request(endpoint, params)
                attempts += 1

            return r

    def __str__(self) -> str:
        """A string representation of the API."""
        string = (
            f"WrAPI(domain={self.domain}, base_path={self.base_path}) with endpoints:\n"
        )
        for endpoint in self.endpoints.values():
            string += f"\t{endpoint}\n"
        return string
