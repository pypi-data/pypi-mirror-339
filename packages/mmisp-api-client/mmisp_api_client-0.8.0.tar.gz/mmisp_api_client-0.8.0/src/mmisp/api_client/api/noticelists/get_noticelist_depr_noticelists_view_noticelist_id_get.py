from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.noticelist_response import NoticelistResponse
from ...types import Response


def _get_kwargs(
    noticelist_id: int,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/noticelists/view/{noticelist_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, NoticelistResponse]]:
    if response.status_code == 200:
        response_200 = NoticelistResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, NoticelistResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    noticelist_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, NoticelistResponse]]:
    """Get noticelist details (Deprecated)

     Deprecated. Retrieve details of a specific noticelist by its ID using the old route.

    args:

    - the user's authentification status

    - the current database

    - the id of the notice list

    returns:

    - the details of the notice list

    Args:
        noticelist_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, NoticelistResponse]]
    """

    kwargs = _get_kwargs(
        noticelist_id=noticelist_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    noticelist_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, NoticelistResponse]]:
    """Get noticelist details (Deprecated)

     Deprecated. Retrieve details of a specific noticelist by its ID using the old route.

    args:

    - the user's authentification status

    - the current database

    - the id of the notice list

    returns:

    - the details of the notice list

    Args:
        noticelist_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, NoticelistResponse]
    """

    return sync_detailed(
        noticelist_id=noticelist_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    noticelist_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, NoticelistResponse]]:
    """Get noticelist details (Deprecated)

     Deprecated. Retrieve details of a specific noticelist by its ID using the old route.

    args:

    - the user's authentification status

    - the current database

    - the id of the notice list

    returns:

    - the details of the notice list

    Args:
        noticelist_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, NoticelistResponse]]
    """

    kwargs = _get_kwargs(
        noticelist_id=noticelist_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    noticelist_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, NoticelistResponse]]:
    """Get noticelist details (Deprecated)

     Deprecated. Retrieve details of a specific noticelist by its ID using the old route.

    args:

    - the user's authentification status

    - the current database

    - the id of the notice list

    returns:

    - the details of the notice list

    Args:
        noticelist_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, NoticelistResponse]
    """

    return (
        await asyncio_detailed(
            noticelist_id=noticelist_id,
            client=client,
        )
    ).parsed
