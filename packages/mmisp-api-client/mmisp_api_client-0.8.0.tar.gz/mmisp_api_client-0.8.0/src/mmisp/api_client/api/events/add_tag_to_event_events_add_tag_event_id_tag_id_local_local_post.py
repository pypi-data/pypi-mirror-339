from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.add_remove_tag_events_response import AddRemoveTagEventsResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    event_id: Union[UUID, int],
    tag_id: str,
    local: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/events/addTag/{event_id}/{tag_id}/local:{local}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[AddRemoveTagEventsResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = AddRemoveTagEventsResponse.from_dict(response.json())

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
) -> Response[Union[AddRemoveTagEventsResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    event_id: Union[UUID, int],
    tag_id: str,
    local: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[AddRemoveTagEventsResponse, HTTPValidationError]]:
    r"""Add tag to event

     Add a tag to an event by their ids.

    args:
        auth: the user's authentification status
        db: the current database
        event_id: the event ID or UUID
        tag_id: the tag ID
        local: \"1\" if local

    returns:
        the result of adding the tag to the event given by the api

    Args:
        event_id (Union[UUID, int]):
        tag_id (str):
        local (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AddRemoveTagEventsResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        event_id=event_id,
        tag_id=tag_id,
        local=local,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    event_id: Union[UUID, int],
    tag_id: str,
    local: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[AddRemoveTagEventsResponse, HTTPValidationError]]:
    r"""Add tag to event

     Add a tag to an event by their ids.

    args:
        auth: the user's authentification status
        db: the current database
        event_id: the event ID or UUID
        tag_id: the tag ID
        local: \"1\" if local

    returns:
        the result of adding the tag to the event given by the api

    Args:
        event_id (Union[UUID, int]):
        tag_id (str):
        local (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AddRemoveTagEventsResponse, HTTPValidationError]
    """

    return sync_detailed(
        event_id=event_id,
        tag_id=tag_id,
        local=local,
        client=client,
    ).parsed


async def asyncio_detailed(
    event_id: Union[UUID, int],
    tag_id: str,
    local: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[AddRemoveTagEventsResponse, HTTPValidationError]]:
    r"""Add tag to event

     Add a tag to an event by their ids.

    args:
        auth: the user's authentification status
        db: the current database
        event_id: the event ID or UUID
        tag_id: the tag ID
        local: \"1\" if local

    returns:
        the result of adding the tag to the event given by the api

    Args:
        event_id (Union[UUID, int]):
        tag_id (str):
        local (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AddRemoveTagEventsResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        event_id=event_id,
        tag_id=tag_id,
        local=local,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    event_id: Union[UUID, int],
    tag_id: str,
    local: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[AddRemoveTagEventsResponse, HTTPValidationError]]:
    r"""Add tag to event

     Add a tag to an event by their ids.

    args:
        auth: the user's authentification status
        db: the current database
        event_id: the event ID or UUID
        tag_id: the tag ID
        local: \"1\" if local

    returns:
        the result of adding the tag to the event given by the api

    Args:
        event_id (Union[UUID, int]):
        tag_id (str):
        local (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AddRemoveTagEventsResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            event_id=event_id,
            tag_id=tag_id,
            local=local,
            client=client,
        )
    ).parsed
