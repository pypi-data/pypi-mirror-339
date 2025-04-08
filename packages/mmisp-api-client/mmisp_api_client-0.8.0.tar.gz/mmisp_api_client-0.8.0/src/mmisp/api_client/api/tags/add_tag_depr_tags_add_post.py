from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.tag_create_body import TagCreateBody
from ...models.tag_response import TagResponse
from ...types import Response


def _get_kwargs(
    *,
    body: TagCreateBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/tags/add",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, TagResponse]]:
    if response.status_code == 201:
        response_201 = TagResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, TagResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: TagCreateBody,
) -> Response[Union[HTTPValidationError, TagResponse]]:
    """Add new tag (Deprecated)

     Deprecated. Add a new tag using the old route.

    args:

    - auth: Authentication details

    - db: Database session

    - body: Tag creation details (TagCreateBody)

    returns:

    - TagResponse: Details of the created tag

    Args:
        body (TagCreateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, TagResponse]]
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
    body: TagCreateBody,
) -> Optional[Union[HTTPValidationError, TagResponse]]:
    """Add new tag (Deprecated)

     Deprecated. Add a new tag using the old route.

    args:

    - auth: Authentication details

    - db: Database session

    - body: Tag creation details (TagCreateBody)

    returns:

    - TagResponse: Details of the created tag

    Args:
        body (TagCreateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, TagResponse]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: TagCreateBody,
) -> Response[Union[HTTPValidationError, TagResponse]]:
    """Add new tag (Deprecated)

     Deprecated. Add a new tag using the old route.

    args:

    - auth: Authentication details

    - db: Database session

    - body: Tag creation details (TagCreateBody)

    returns:

    - TagResponse: Details of the created tag

    Args:
        body (TagCreateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, TagResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: TagCreateBody,
) -> Optional[Union[HTTPValidationError, TagResponse]]:
    """Add new tag (Deprecated)

     Deprecated. Add a new tag using the old route.

    args:

    - auth: Authentication details

    - db: Database session

    - body: Tag creation details (TagCreateBody)

    returns:

    - TagResponse: Details of the created tag

    Args:
        body (TagCreateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, TagResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
