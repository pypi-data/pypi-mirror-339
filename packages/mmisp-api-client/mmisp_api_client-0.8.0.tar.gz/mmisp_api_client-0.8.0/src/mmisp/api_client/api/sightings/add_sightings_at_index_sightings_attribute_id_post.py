from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.sighting_attributes_response import SightingAttributesResponse
from ...types import Response


def _get_kwargs(
    attribute_id: Union[UUID, int],
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/sightings/{attribute_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, SightingAttributesResponse]]:
    if response.status_code == 201:
        response_201 = SightingAttributesResponse.from_dict(response.json())

        return response_201
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[HTTPValidationError, SightingAttributesResponse]]:
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
) -> Response[Union[HTTPValidationError, SightingAttributesResponse]]:
    """Add sighting at index

     Add a new sighting for a specific attribute.

    args:
        auth: Authentication
        db: Database session
        attribute_id: ID or UUID of the attribute

    returns:
        details of new sightings

    Args:
        attribute_id (Union[UUID, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, SightingAttributesResponse]]
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
) -> Optional[Union[HTTPValidationError, SightingAttributesResponse]]:
    """Add sighting at index

     Add a new sighting for a specific attribute.

    args:
        auth: Authentication
        db: Database session
        attribute_id: ID or UUID of the attribute

    returns:
        details of new sightings

    Args:
        attribute_id (Union[UUID, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, SightingAttributesResponse]
    """

    return sync_detailed(
        attribute_id=attribute_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    attribute_id: Union[UUID, int],
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, SightingAttributesResponse]]:
    """Add sighting at index

     Add a new sighting for a specific attribute.

    args:
        auth: Authentication
        db: Database session
        attribute_id: ID or UUID of the attribute

    returns:
        details of new sightings

    Args:
        attribute_id (Union[UUID, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, SightingAttributesResponse]]
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
) -> Optional[Union[HTTPValidationError, SightingAttributesResponse]]:
    """Add sighting at index

     Add a new sighting for a specific attribute.

    args:
        auth: Authentication
        db: Database session
        attribute_id: ID or UUID of the attribute

    returns:
        details of new sightings

    Args:
        attribute_id (Union[UUID, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, SightingAttributesResponse]
    """

    return (
        await asyncio_detailed(
            attribute_id=attribute_id,
            client=client,
        )
    ).parsed
