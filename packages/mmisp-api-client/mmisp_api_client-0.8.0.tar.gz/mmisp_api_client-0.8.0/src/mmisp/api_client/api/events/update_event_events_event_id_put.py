from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.add_edit_get_event_response import AddEditGetEventResponse
from ...models.edit_event_body import EditEventBody
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    event_id: Union[UUID, int],
    *,
    body: EditEventBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/events/{event_id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[AddEditGetEventResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = AddEditGetEventResponse.from_dict(response.json())

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
) -> Response[Union[AddEditGetEventResponse, HTTPValidationError]]:
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
    body: EditEventBody,
) -> Response[Union[AddEditGetEventResponse, HTTPValidationError]]:
    """Update an event

     Update an existing event either by its event ID or via its UUID.

    args:
        auth: the user's authentification status
        db: the current database
        event_id: the ID or UUID of the event
        body: the request body

    returns:
        the updated event

    Args:
        event_id (Union[UUID, int]):
        body (EditEventBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AddEditGetEventResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        event_id=event_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    event_id: Union[UUID, int],
    *,
    client: AuthenticatedClient,
    body: EditEventBody,
) -> Optional[Union[AddEditGetEventResponse, HTTPValidationError]]:
    """Update an event

     Update an existing event either by its event ID or via its UUID.

    args:
        auth: the user's authentification status
        db: the current database
        event_id: the ID or UUID of the event
        body: the request body

    returns:
        the updated event

    Args:
        event_id (Union[UUID, int]):
        body (EditEventBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AddEditGetEventResponse, HTTPValidationError]
    """

    return sync_detailed(
        event_id=event_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    event_id: Union[UUID, int],
    *,
    client: AuthenticatedClient,
    body: EditEventBody,
) -> Response[Union[AddEditGetEventResponse, HTTPValidationError]]:
    """Update an event

     Update an existing event either by its event ID or via its UUID.

    args:
        auth: the user's authentification status
        db: the current database
        event_id: the ID or UUID of the event
        body: the request body

    returns:
        the updated event

    Args:
        event_id (Union[UUID, int]):
        body (EditEventBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AddEditGetEventResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        event_id=event_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    event_id: Union[UUID, int],
    *,
    client: AuthenticatedClient,
    body: EditEventBody,
) -> Optional[Union[AddEditGetEventResponse, HTTPValidationError]]:
    """Update an event

     Update an existing event either by its event ID or via its UUID.

    args:
        auth: the user's authentification status
        db: the current database
        event_id: the ID or UUID of the event
        body: the request body

    returns:
        the updated event

    Args:
        event_id (Union[UUID, int]):
        body (EditEventBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AddEditGetEventResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            event_id=event_id,
            client=client,
            body=body,
        )
    ).parsed
