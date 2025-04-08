from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.sighting_attributes_response import SightingAttributesResponse
from ...models.sighting_create_body import SightingCreateBody
from ...types import Response


def _get_kwargs(
    *,
    body: SightingCreateBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/sightings/add",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, list["SightingAttributesResponse"]]]:
    if response.status_code == 201:
        response_201 = []
        _response_201 = response.json()
        for response_201_item_data in _response_201:
            response_201_item = SightingAttributesResponse.from_dict(response_201_item_data)

            response_201.append(response_201_item)

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
) -> Response[Union[HTTPValidationError, list["SightingAttributesResponse"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: SightingCreateBody,
) -> Response[Union[HTTPValidationError, list["SightingAttributesResponse"]]]:
    """Add sighting (Deprecated)

     Deprecated. Add a new sighting using the old route.

    args:

    - auth: Authentication details

    - db: Database session

    - body: Sighting creation data

    returns:

    - List of sighting attributes

    Args:
        body (SightingCreateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['SightingAttributesResponse']]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: SightingCreateBody,
) -> Optional[Union[HTTPValidationError, list["SightingAttributesResponse"]]]:
    """Add sighting (Deprecated)

     Deprecated. Add a new sighting using the old route.

    args:

    - auth: Authentication details

    - db: Database session

    - body: Sighting creation data

    returns:

    - List of sighting attributes

    Args:
        body (SightingCreateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['SightingAttributesResponse']]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: SightingCreateBody,
) -> Response[Union[HTTPValidationError, list["SightingAttributesResponse"]]]:
    """Add sighting (Deprecated)

     Deprecated. Add a new sighting using the old route.

    args:

    - auth: Authentication details

    - db: Database session

    - body: Sighting creation data

    returns:

    - List of sighting attributes

    Args:
        body (SightingCreateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['SightingAttributesResponse']]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: SightingCreateBody,
) -> Optional[Union[HTTPValidationError, list["SightingAttributesResponse"]]]:
    """Add sighting (Deprecated)

     Deprecated. Add a new sighting using the old route.

    args:

    - auth: Authentication details

    - db: Database session

    - body: Sighting creation data

    returns:

    - List of sighting attributes

    Args:
        body (SightingCreateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['SightingAttributesResponse']]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
