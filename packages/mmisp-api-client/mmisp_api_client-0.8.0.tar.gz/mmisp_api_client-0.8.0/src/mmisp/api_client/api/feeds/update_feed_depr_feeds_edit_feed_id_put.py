from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.feed_response import FeedResponse
from ...models.feed_update_body import FeedUpdateBody
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    feed_id: int,
    *,
    body: FeedUpdateBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/feeds/edit/{feed_id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[FeedResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = FeedResponse.from_dict(response.json())

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
) -> Response[Union[FeedResponse, HTTPValidationError]]:
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
    body: FeedUpdateBody,
) -> Response[Union[FeedResponse, HTTPValidationError]]:
    """Update Feed Depr

     Deprecated. Update an existing feed by its ID using the old route.


    Args:
      auth: the user's authentification status
      db: the current database
      feed_id: the feed id
      body: the request body

    Returns:
      the updated feed

    Args:
        feed_id (int):
        body (FeedUpdateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[FeedResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        feed_id=feed_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    feed_id: int,
    *,
    client: AuthenticatedClient,
    body: FeedUpdateBody,
) -> Optional[Union[FeedResponse, HTTPValidationError]]:
    """Update Feed Depr

     Deprecated. Update an existing feed by its ID using the old route.


    Args:
      auth: the user's authentification status
      db: the current database
      feed_id: the feed id
      body: the request body

    Returns:
      the updated feed

    Args:
        feed_id (int):
        body (FeedUpdateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[FeedResponse, HTTPValidationError]
    """

    return sync_detailed(
        feed_id=feed_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    feed_id: int,
    *,
    client: AuthenticatedClient,
    body: FeedUpdateBody,
) -> Response[Union[FeedResponse, HTTPValidationError]]:
    """Update Feed Depr

     Deprecated. Update an existing feed by its ID using the old route.


    Args:
      auth: the user's authentification status
      db: the current database
      feed_id: the feed id
      body: the request body

    Returns:
      the updated feed

    Args:
        feed_id (int):
        body (FeedUpdateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[FeedResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        feed_id=feed_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    feed_id: int,
    *,
    client: AuthenticatedClient,
    body: FeedUpdateBody,
) -> Optional[Union[FeedResponse, HTTPValidationError]]:
    """Update Feed Depr

     Deprecated. Update an existing feed by its ID using the old route.


    Args:
      auth: the user's authentification status
      db: the current database
      feed_id: the feed id
      body: the request body

    Returns:
      the updated feed

    Args:
        feed_id (int):
        body (FeedUpdateBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[FeedResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            feed_id=feed_id,
            client=client,
            body=body,
        )
    ).parsed
