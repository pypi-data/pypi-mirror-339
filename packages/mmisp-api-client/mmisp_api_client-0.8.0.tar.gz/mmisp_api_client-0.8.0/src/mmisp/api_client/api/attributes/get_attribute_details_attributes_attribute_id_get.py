from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_attribute_response import GetAttributeResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    attribute_id: Union[UUID, int],
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/attributes/{attribute_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetAttributeResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = GetAttributeResponse.from_dict(response.json())

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
) -> Response[Union[GetAttributeResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    attribute_id: Union[UUID, int],
    *,
    client: AuthenticatedClient,
) -> Response[Union[GetAttributeResponse, HTTPValidationError]]:
    """Get attribute details

     Retrieve details of a specific attribute by either by its ID or UUID.

    args:
        auth: the user's authentification status
        db: the current database
        attribute_id: the ID or UUID of the attribute

    returns:
        the attribute details

    Args:
        attribute_id (Union[UUID, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetAttributeResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        attribute_id=attribute_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    attribute_id: Union[UUID, int],
    *,
    client: AuthenticatedClient,
) -> Optional[Union[GetAttributeResponse, HTTPValidationError]]:
    """Get attribute details

     Retrieve details of a specific attribute by either by its ID or UUID.

    args:
        auth: the user's authentification status
        db: the current database
        attribute_id: the ID or UUID of the attribute

    returns:
        the attribute details

    Args:
        attribute_id (Union[UUID, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetAttributeResponse, HTTPValidationError]
    """

    return sync_detailed(
        attribute_id=attribute_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    attribute_id: Union[UUID, int],
    *,
    client: AuthenticatedClient,
) -> Response[Union[GetAttributeResponse, HTTPValidationError]]:
    """Get attribute details

     Retrieve details of a specific attribute by either by its ID or UUID.

    args:
        auth: the user's authentification status
        db: the current database
        attribute_id: the ID or UUID of the attribute

    returns:
        the attribute details

    Args:
        attribute_id (Union[UUID, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetAttributeResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        attribute_id=attribute_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    attribute_id: Union[UUID, int],
    *,
    client: AuthenticatedClient,
) -> Optional[Union[GetAttributeResponse, HTTPValidationError]]:
    """Get attribute details

     Retrieve details of a specific attribute by either by its ID or UUID.

    args:
        auth: the user's authentification status
        db: the current database
        attribute_id: the ID or UUID of the attribute

    returns:
        the attribute details

    Args:
        attribute_id (Union[UUID, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetAttributeResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            attribute_id=attribute_id,
            client=client,
        )
    ).parsed
