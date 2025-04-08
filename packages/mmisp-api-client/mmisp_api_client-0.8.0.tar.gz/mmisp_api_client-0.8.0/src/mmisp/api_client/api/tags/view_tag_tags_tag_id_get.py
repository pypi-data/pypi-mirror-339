from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.tag_view_response import TagViewResponse
from ...types import Response


def _get_kwargs(
    tag_id: int,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/tags/{tag_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, TagViewResponse]]:
    if response.status_code == 200:
        response_200 = TagViewResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, TagViewResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    tag_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, TagViewResponse]]:
    """View tag details

     View details of a specific tag.

    args:

    - auth: Authentication details

    - db: Database session

    - tag_id: ID of the tag to view

    returns:

    - TagViewResponse: Detailed information of the specified tag

    Args:
        tag_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, TagViewResponse]]
    """

    kwargs = _get_kwargs(
        tag_id=tag_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    tag_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, TagViewResponse]]:
    """View tag details

     View details of a specific tag.

    args:

    - auth: Authentication details

    - db: Database session

    - tag_id: ID of the tag to view

    returns:

    - TagViewResponse: Detailed information of the specified tag

    Args:
        tag_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, TagViewResponse]
    """

    return sync_detailed(
        tag_id=tag_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    tag_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, TagViewResponse]]:
    """View tag details

     View details of a specific tag.

    args:

    - auth: Authentication details

    - db: Database session

    - tag_id: ID of the tag to view

    returns:

    - TagViewResponse: Detailed information of the specified tag

    Args:
        tag_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, TagViewResponse]]
    """

    kwargs = _get_kwargs(
        tag_id=tag_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    tag_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, TagViewResponse]]:
    """View tag details

     View details of a specific tag.

    args:

    - auth: Authentication details

    - db: Database session

    - tag_id: ID of the tag to view

    returns:

    - TagViewResponse: Detailed information of the specified tag

    Args:
        tag_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, TagViewResponse]
    """

    return (
        await asyncio_detailed(
            tag_id=tag_id,
            client=client,
        )
    ).parsed
