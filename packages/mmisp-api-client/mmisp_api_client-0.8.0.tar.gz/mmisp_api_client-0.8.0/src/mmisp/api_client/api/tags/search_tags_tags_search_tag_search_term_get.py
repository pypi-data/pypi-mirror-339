from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.partial_tag_search_response import PartialTagSearchResponse
from ...types import Response


def _get_kwargs(
    tag_search_term: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/tags/search/{tag_search_term}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, PartialTagSearchResponse]]:
    if response.status_code == 200:
        response_200 = PartialTagSearchResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, PartialTagSearchResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    tag_search_term: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, PartialTagSearchResponse]]:
    """Search tags

     Search for tags using a specific search term.

    args:

    - auth: Authentication details

    - db: Database session

    - tag_search_term: Search term for finding tags

    returns:

    - dict: Dictionary containing search results

    Args:
        tag_search_term (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, PartialTagSearchResponse]]
    """

    kwargs = _get_kwargs(
        tag_search_term=tag_search_term,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    tag_search_term: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, PartialTagSearchResponse]]:
    """Search tags

     Search for tags using a specific search term.

    args:

    - auth: Authentication details

    - db: Database session

    - tag_search_term: Search term for finding tags

    returns:

    - dict: Dictionary containing search results

    Args:
        tag_search_term (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, PartialTagSearchResponse]
    """

    return sync_detailed(
        tag_search_term=tag_search_term,
        client=client,
    ).parsed


async def asyncio_detailed(
    tag_search_term: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, PartialTagSearchResponse]]:
    """Search tags

     Search for tags using a specific search term.

    args:

    - auth: Authentication details

    - db: Database session

    - tag_search_term: Search term for finding tags

    returns:

    - dict: Dictionary containing search results

    Args:
        tag_search_term (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, PartialTagSearchResponse]]
    """

    kwargs = _get_kwargs(
        tag_search_term=tag_search_term,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    tag_search_term: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, PartialTagSearchResponse]]:
    """Search tags

     Search for tags using a specific search term.

    args:

    - auth: Authentication details

    - db: Database session

    - tag_search_term: Search term for finding tags

    returns:

    - dict: Dictionary containing search results

    Args:
        tag_search_term (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, PartialTagSearchResponse]
    """

    return (
        await asyncio_detailed(
            tag_search_term=tag_search_term,
            client=client,
        )
    ).parsed
