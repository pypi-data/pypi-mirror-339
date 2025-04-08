from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_remote_server import GetRemoteServer
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    server_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/servers/remote/{server_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetRemoteServer, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = GetRemoteServer.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[GetRemoteServer, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    server_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[GetRemoteServer, HTTPValidationError]]:
    """Requests information regarding a remote server

     Returns information for a specific remote server chosen by its id.

    args:

    - serverId: the server's ID

    - The current database

    returns:

    - server information regarding the chosen server

    Args:
        server_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetRemoteServer, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        server_id=server_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    server_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[GetRemoteServer, HTTPValidationError]]:
    """Requests information regarding a remote server

     Returns information for a specific remote server chosen by its id.

    args:

    - serverId: the server's ID

    - The current database

    returns:

    - server information regarding the chosen server

    Args:
        server_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetRemoteServer, HTTPValidationError]
    """

    return sync_detailed(
        server_id=server_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    server_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[GetRemoteServer, HTTPValidationError]]:
    """Requests information regarding a remote server

     Returns information for a specific remote server chosen by its id.

    args:

    - serverId: the server's ID

    - The current database

    returns:

    - server information regarding the chosen server

    Args:
        server_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetRemoteServer, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        server_id=server_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    server_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[GetRemoteServer, HTTPValidationError]]:
    """Requests information regarding a remote server

     Returns information for a specific remote server chosen by its id.

    args:

    - serverId: the server's ID

    - The current database

    returns:

    - server information regarding the chosen server

    Args:
        server_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetRemoteServer, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            server_id=server_id,
            client=client,
        )
    ).parsed
