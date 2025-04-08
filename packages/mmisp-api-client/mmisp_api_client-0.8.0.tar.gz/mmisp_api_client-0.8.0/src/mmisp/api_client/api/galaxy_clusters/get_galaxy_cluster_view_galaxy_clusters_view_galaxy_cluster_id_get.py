from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    galaxy_cluster_id: int,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/galaxy_clusters/view/{galaxy_cluster_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[HTTPValidationError]:
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    galaxy_cluster_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError]:
    """Gets information from a galaxy cluster

     Deprecated
    Returns information from a galaxy cluster selected by its id.

    args:

    - the user's authentification status

    - the current database

    - the galaxy id

    returns:

    - the information of the galaxy cluster

    Args:
        galaxy_cluster_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError]
    """

    kwargs = _get_kwargs(
        galaxy_cluster_id=galaxy_cluster_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    galaxy_cluster_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[HTTPValidationError]:
    """Gets information from a galaxy cluster

     Deprecated
    Returns information from a galaxy cluster selected by its id.

    args:

    - the user's authentification status

    - the current database

    - the galaxy id

    returns:

    - the information of the galaxy cluster

    Args:
        galaxy_cluster_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError
    """

    return sync_detailed(
        galaxy_cluster_id=galaxy_cluster_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    galaxy_cluster_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[HTTPValidationError]:
    """Gets information from a galaxy cluster

     Deprecated
    Returns information from a galaxy cluster selected by its id.

    args:

    - the user's authentification status

    - the current database

    - the galaxy id

    returns:

    - the information of the galaxy cluster

    Args:
        galaxy_cluster_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[HTTPValidationError]
    """

    kwargs = _get_kwargs(
        galaxy_cluster_id=galaxy_cluster_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    galaxy_cluster_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[HTTPValidationError]:
    """Gets information from a galaxy cluster

     Deprecated
    Returns information from a galaxy cluster selected by its id.

    args:

    - the user's authentification status

    - the current database

    - the galaxy id

    returns:

    - the information of the galaxy cluster

    Args:
        galaxy_cluster_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        HTTPValidationError
    """

    return (
        await asyncio_detailed(
            galaxy_cluster_id=galaxy_cluster_id,
            client=client,
        )
    ).parsed
