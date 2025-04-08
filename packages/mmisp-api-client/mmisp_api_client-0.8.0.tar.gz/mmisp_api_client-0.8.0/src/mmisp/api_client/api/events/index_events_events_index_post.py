from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_all_events_response import GetAllEventsResponse
from ...models.http_validation_error import HTTPValidationError
from ...models.index_events_body import IndexEventsBody
from ...types import Response


def _get_kwargs(
    *,
    body: IndexEventsBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/events/index",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, list["GetAllEventsResponse"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = GetAllEventsResponse.from_dict(response_200_item_data)

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
) -> Response[Union[HTTPValidationError, list["GetAllEventsResponse"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: IndexEventsBody,
) -> Response[Union[HTTPValidationError, list["GetAllEventsResponse"]]]:
    """Search events

     Search for events based on various filters, which are more general than the ones in 'rest search'.

    args:
        auth: the user's authentification status
        db: the current database
        body: the request body


    returns:
        the searched events

    Args:
        body (IndexEventsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['GetAllEventsResponse']]]
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
    body: IndexEventsBody,
) -> Optional[Union[HTTPValidationError, list["GetAllEventsResponse"]]]:
    """Search events

     Search for events based on various filters, which are more general than the ones in 'rest search'.

    args:
        auth: the user's authentification status
        db: the current database
        body: the request body


    returns:
        the searched events

    Args:
        body (IndexEventsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['GetAllEventsResponse']]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: IndexEventsBody,
) -> Response[Union[HTTPValidationError, list["GetAllEventsResponse"]]]:
    """Search events

     Search for events based on various filters, which are more general than the ones in 'rest search'.

    args:
        auth: the user's authentification status
        db: the current database
        body: the request body


    returns:
        the searched events

    Args:
        body (IndexEventsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['GetAllEventsResponse']]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: IndexEventsBody,
) -> Optional[Union[HTTPValidationError, list["GetAllEventsResponse"]]]:
    """Search events

     Search for events based on various filters, which are more general than the ones in 'rest search'.

    args:
        auth: the user's authentification status
        db: the current database
        body: the request body


    returns:
        the searched events

    Args:
        body (IndexEventsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['GetAllEventsResponse']]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
