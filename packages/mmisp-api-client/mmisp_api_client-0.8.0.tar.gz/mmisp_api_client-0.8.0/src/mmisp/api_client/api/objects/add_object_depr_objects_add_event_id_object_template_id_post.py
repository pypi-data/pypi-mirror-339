from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.object_create_body import ObjectCreateBody
from ...models.object_response import ObjectResponse
from ...types import Response


def _get_kwargs(
    event_id: int,
    object_template_id: int,
    *,
    body: ObjectCreateBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/objects/add/{event_id}/{object_template_id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ObjectResponse]]:
    if response.status_code == 201:
        response_201 = ObjectResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ObjectResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    event_id: int,
    object_template_id: int,
    *,
    client: AuthenticatedClient,
    body: ObjectCreateBody,
) -> Response[Union[HTTPValidationError, ObjectResponse]]:
    """Add object to event (Deprecated)

     Deprecated. Add an object to an event using the old route.

    args:

    - the user's authentification status

    - the current database

    - the event id

    - the object template id

    - the request body

    returns:

    - the added object

    Args:
        event_id (int):
        object_template_id (int):
        body (ObjectCreateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ObjectResponse]]
    """

    kwargs = _get_kwargs(
        event_id=event_id,
        object_template_id=object_template_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    event_id: int,
    object_template_id: int,
    *,
    client: AuthenticatedClient,
    body: ObjectCreateBody,
) -> Optional[Union[HTTPValidationError, ObjectResponse]]:
    """Add object to event (Deprecated)

     Deprecated. Add an object to an event using the old route.

    args:

    - the user's authentification status

    - the current database

    - the event id

    - the object template id

    - the request body

    returns:

    - the added object

    Args:
        event_id (int):
        object_template_id (int):
        body (ObjectCreateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ObjectResponse]
    """

    return sync_detailed(
        event_id=event_id,
        object_template_id=object_template_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    event_id: int,
    object_template_id: int,
    *,
    client: AuthenticatedClient,
    body: ObjectCreateBody,
) -> Response[Union[HTTPValidationError, ObjectResponse]]:
    """Add object to event (Deprecated)

     Deprecated. Add an object to an event using the old route.

    args:

    - the user's authentification status

    - the current database

    - the event id

    - the object template id

    - the request body

    returns:

    - the added object

    Args:
        event_id (int):
        object_template_id (int):
        body (ObjectCreateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ObjectResponse]]
    """

    kwargs = _get_kwargs(
        event_id=event_id,
        object_template_id=object_template_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    event_id: int,
    object_template_id: int,
    *,
    client: AuthenticatedClient,
    body: ObjectCreateBody,
) -> Optional[Union[HTTPValidationError, ObjectResponse]]:
    """Add object to event (Deprecated)

     Deprecated. Add an object to an event using the old route.

    args:

    - the user's authentification status

    - the current database

    - the event id

    - the object template id

    - the request body

    returns:

    - the added object

    Args:
        event_id (int):
        object_template_id (int):
        body (ObjectCreateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ObjectResponse]
    """

    return (
        await asyncio_detailed(
            event_id=event_id,
            object_template_id=object_template_id,
            client=client,
            body=body,
        )
    ).parsed
