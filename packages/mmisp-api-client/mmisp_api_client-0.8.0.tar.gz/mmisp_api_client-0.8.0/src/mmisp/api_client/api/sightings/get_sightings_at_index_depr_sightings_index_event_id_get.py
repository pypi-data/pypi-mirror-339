from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.sighting_attributes_response import SightingAttributesResponse
from ...types import Response


def _get_kwargs(
    event_id: int,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/sightings/index/{event_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, list["SightingAttributesResponse"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = SightingAttributesResponse.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[Union[HTTPValidationError, list["SightingAttributesResponse"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    event_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, list["SightingAttributesResponse"]]]:
    """Get sightings for event (Deprecated)

     Deprecated. Retrieve all sightings associated with a specific event ID using the old route.

    args:

    - auth: Authentication details

    - db: Database session

    - event_id: ID of the event

    returns:

    - Details of the sightings at index

    Args:
        event_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['SightingAttributesResponse']]]
    """

    kwargs = _get_kwargs(
        event_id=event_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    event_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, list["SightingAttributesResponse"]]]:
    """Get sightings for event (Deprecated)

     Deprecated. Retrieve all sightings associated with a specific event ID using the old route.

    args:

    - auth: Authentication details

    - db: Database session

    - event_id: ID of the event

    returns:

    - Details of the sightings at index

    Args:
        event_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['SightingAttributesResponse']]
    """

    return sync_detailed(
        event_id=event_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    event_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, list["SightingAttributesResponse"]]]:
    """Get sightings for event (Deprecated)

     Deprecated. Retrieve all sightings associated with a specific event ID using the old route.

    args:

    - auth: Authentication details

    - db: Database session

    - event_id: ID of the event

    returns:

    - Details of the sightings at index

    Args:
        event_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['SightingAttributesResponse']]]
    """

    kwargs = _get_kwargs(
        event_id=event_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    event_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, list["SightingAttributesResponse"]]]:
    """Get sightings for event (Deprecated)

     Deprecated. Retrieve all sightings associated with a specific event ID using the old route.

    args:

    - auth: Authentication details

    - db: Database session

    - event_id: ID of the event

    returns:

    - Details of the sightings at index

    Args:
        event_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['SightingAttributesResponse']]
    """

    return (
        await asyncio_detailed(
            event_id=event_id,
            client=client,
        )
    ).parsed
