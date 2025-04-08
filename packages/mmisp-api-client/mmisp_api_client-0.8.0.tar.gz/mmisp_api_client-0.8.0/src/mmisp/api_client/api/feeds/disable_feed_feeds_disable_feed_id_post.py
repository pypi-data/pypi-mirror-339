from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.feed_enable_disable_response import FeedEnableDisableResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    feed_id: int,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/feeds/disable/{feed_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[FeedEnableDisableResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = FeedEnableDisableResponse.from_dict(response.json())

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
) -> Response[Union[FeedEnableDisableResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    feed_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[FeedEnableDisableResponse, HTTPValidationError]]:
    """Disable Feed

     Deprecated. Disable a specific feed by its ID using the old route.

    Args:
      the user's authentification status
      the current database
      the feed id

    Returns:
      the disabled feed

    Args:
        feed_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[FeedEnableDisableResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        feed_id=feed_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    feed_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[FeedEnableDisableResponse, HTTPValidationError]]:
    """Disable Feed

     Deprecated. Disable a specific feed by its ID using the old route.

    Args:
      the user's authentification status
      the current database
      the feed id

    Returns:
      the disabled feed

    Args:
        feed_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[FeedEnableDisableResponse, HTTPValidationError]
    """

    return sync_detailed(
        feed_id=feed_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    feed_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[FeedEnableDisableResponse, HTTPValidationError]]:
    """Disable Feed

     Deprecated. Disable a specific feed by its ID using the old route.

    Args:
      the user's authentification status
      the current database
      the feed id

    Returns:
      the disabled feed

    Args:
        feed_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[FeedEnableDisableResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        feed_id=feed_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    feed_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[FeedEnableDisableResponse, HTTPValidationError]]:
    """Disable Feed

     Deprecated. Disable a specific feed by its ID using the old route.

    Args:
      the user's authentification status
      the current database
      the feed id

    Returns:
      the disabled feed

    Args:
        feed_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[FeedEnableDisableResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            feed_id=feed_id,
            client=client,
        )
    ).parsed
