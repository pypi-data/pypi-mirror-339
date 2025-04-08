from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.feed_enable_disable_response import FeedEnableDisableResponse
from ...models.feed_toggle_body import FeedToggleBody
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    feed_id: int,
    *,
    body: FeedToggleBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": f"/feeds/{feed_id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
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
    body: FeedToggleBody,
) -> Response[Union[FeedEnableDisableResponse, HTTPValidationError]]:
    """Toggle Feed

     Toggle the status of a feed between enabled and disabled.


    Args:
      auth: the user's authentification status
      db: the current database
      feed_id: the feed id
      body: the request body

    Returns:
      the new status of the feed

    Args:
        feed_id (int):
        body (FeedToggleBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[FeedEnableDisableResponse, HTTPValidationError]]
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
    body: FeedToggleBody,
) -> Optional[Union[FeedEnableDisableResponse, HTTPValidationError]]:
    """Toggle Feed

     Toggle the status of a feed between enabled and disabled.


    Args:
      auth: the user's authentification status
      db: the current database
      feed_id: the feed id
      body: the request body

    Returns:
      the new status of the feed

    Args:
        feed_id (int):
        body (FeedToggleBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[FeedEnableDisableResponse, HTTPValidationError]
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
    body: FeedToggleBody,
) -> Response[Union[FeedEnableDisableResponse, HTTPValidationError]]:
    """Toggle Feed

     Toggle the status of a feed between enabled and disabled.


    Args:
      auth: the user's authentification status
      db: the current database
      feed_id: the feed id
      body: the request body

    Returns:
      the new status of the feed

    Args:
        feed_id (int):
        body (FeedToggleBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[FeedEnableDisableResponse, HTTPValidationError]]
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
    body: FeedToggleBody,
) -> Optional[Union[FeedEnableDisableResponse, HTTPValidationError]]:
    """Toggle Feed

     Toggle the status of a feed between enabled and disabled.


    Args:
      auth: the user's authentification status
      db: the current database
      feed_id: the feed id
      body: the request body

    Returns:
      the new status of the feed

    Args:
        feed_id (int):
        body (FeedToggleBody):

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
            body=body,
        )
    ).parsed
