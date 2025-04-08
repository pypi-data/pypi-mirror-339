from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_event_response import DeleteEventResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    event_id: Union[UUID, int],
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": f"/events/{event_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DeleteEventResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = DeleteEventResponse.from_dict(response.json())

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
) -> Response[Union[DeleteEventResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    event_id: Union[UUID, int],
    *,
    client: AuthenticatedClient,
) -> Response[Union[DeleteEventResponse, HTTPValidationError]]:
    """Delete an event

     Delete an event either by its event ID or via its UUID.

    args:
        auth: the user's authentification status
        db: the current database
        event_id: the ID or UUID of the event

    returns:
        the deleted event

    Args:
        event_id (Union[UUID, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeleteEventResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        event_id=event_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    event_id: Union[UUID, int],
    *,
    client: AuthenticatedClient,
) -> Optional[Union[DeleteEventResponse, HTTPValidationError]]:
    """Delete an event

     Delete an event either by its event ID or via its UUID.

    args:
        auth: the user's authentification status
        db: the current database
        event_id: the ID or UUID of the event

    returns:
        the deleted event

    Args:
        event_id (Union[UUID, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DeleteEventResponse, HTTPValidationError]
    """

    return sync_detailed(
        event_id=event_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    event_id: Union[UUID, int],
    *,
    client: AuthenticatedClient,
) -> Response[Union[DeleteEventResponse, HTTPValidationError]]:
    """Delete an event

     Delete an event either by its event ID or via its UUID.

    args:
        auth: the user's authentification status
        db: the current database
        event_id: the ID or UUID of the event

    returns:
        the deleted event

    Args:
        event_id (Union[UUID, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeleteEventResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        event_id=event_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    event_id: Union[UUID, int],
    *,
    client: AuthenticatedClient,
) -> Optional[Union[DeleteEventResponse, HTTPValidationError]]:
    """Delete an event

     Delete an event either by its event ID or via its UUID.

    args:
        auth: the user's authentification status
        db: the current database
        event_id: the ID or UUID of the event

    returns:
        the deleted event

    Args:
        event_id (Union[UUID, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DeleteEventResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            event_id=event_id,
            client=client,
        )
    ).parsed
