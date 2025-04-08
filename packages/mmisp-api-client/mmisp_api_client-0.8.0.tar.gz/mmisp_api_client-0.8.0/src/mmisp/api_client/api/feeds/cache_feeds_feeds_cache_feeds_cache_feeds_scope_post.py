from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.feed_cache_response import FeedCacheResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    cache_feeds_scope: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/feeds/cache_feeds/{cache_feeds_scope}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[FeedCacheResponse, HTTPValidationError]]:
    if response.status_code == 501:
        response_501 = FeedCacheResponse.from_dict(response.json())

        return response_501
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[FeedCacheResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    cache_feeds_scope: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[FeedCacheResponse, HTTPValidationError]]:
    """Cache Feeds

     Cache feeds based on a specific scope. NOT YET AVAILABLE!

    Args:
      auth: the user's authentification status
      db: the current database
      cache_feeds_scope: the cache feeds scope

    Returns:
      the cache feeds

    Args:
        cache_feeds_scope (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[FeedCacheResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        cache_feeds_scope=cache_feeds_scope,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    cache_feeds_scope: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[FeedCacheResponse, HTTPValidationError]]:
    """Cache Feeds

     Cache feeds based on a specific scope. NOT YET AVAILABLE!

    Args:
      auth: the user's authentification status
      db: the current database
      cache_feeds_scope: the cache feeds scope

    Returns:
      the cache feeds

    Args:
        cache_feeds_scope (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[FeedCacheResponse, HTTPValidationError]
    """

    return sync_detailed(
        cache_feeds_scope=cache_feeds_scope,
        client=client,
    ).parsed


async def asyncio_detailed(
    cache_feeds_scope: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[FeedCacheResponse, HTTPValidationError]]:
    """Cache Feeds

     Cache feeds based on a specific scope. NOT YET AVAILABLE!

    Args:
      auth: the user's authentification status
      db: the current database
      cache_feeds_scope: the cache feeds scope

    Returns:
      the cache feeds

    Args:
        cache_feeds_scope (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[FeedCacheResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        cache_feeds_scope=cache_feeds_scope,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    cache_feeds_scope: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[FeedCacheResponse, HTTPValidationError]]:
    """Cache Feeds

     Cache feeds based on a specific scope. NOT YET AVAILABLE!

    Args:
      auth: the user's authentification status
      db: the current database
      cache_feeds_scope: the cache feeds scope

    Returns:
      the cache feeds

    Args:
        cache_feeds_scope (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[FeedCacheResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            cache_feeds_scope=cache_feeds_scope,
            client=client,
        )
    ).parsed
