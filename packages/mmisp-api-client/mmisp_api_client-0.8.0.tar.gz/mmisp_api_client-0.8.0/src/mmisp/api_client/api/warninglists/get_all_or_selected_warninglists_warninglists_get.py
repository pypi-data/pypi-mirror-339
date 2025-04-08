from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_selected_all_warninglists_response import GetSelectedAllWarninglistsResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    value: Union[Unset, str] = UNSET,
    enabled: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["value"] = value

    params["enabled"] = enabled

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/warninglists",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetSelectedAllWarninglistsResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = GetSelectedAllWarninglistsResponse.from_dict(response.json())

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
) -> Response[Union[GetSelectedAllWarninglistsResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    value: Union[Unset, str] = UNSET,
    enabled: Union[Unset, bool] = UNSET,
) -> Response[Union[GetSelectedAllWarninglistsResponse, HTTPValidationError]]:
    """Get all warninglists, or selected ones by value and status

     Receive a list of all warning lists, or when setting the path parameters value and enabled, receive
    a         list of warninglists for which the value matches either the name, description, or type and
    enabled matches         given parameter.

    args:

    - auth: Authentication details

    - db: Database session

    - value: str | None, Search term for filtering by value

    - enabled: bool | None, Status filter (enabled or disabled)

    returns:

    - GetSelectedAllWarninglistsResponse: Response containing filtered or all warninglists

    Args:
        value (Union[Unset, str]):
        enabled (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetSelectedAllWarninglistsResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        value=value,
        enabled=enabled,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    value: Union[Unset, str] = UNSET,
    enabled: Union[Unset, bool] = UNSET,
) -> Optional[Union[GetSelectedAllWarninglistsResponse, HTTPValidationError]]:
    """Get all warninglists, or selected ones by value and status

     Receive a list of all warning lists, or when setting the path parameters value and enabled, receive
    a         list of warninglists for which the value matches either the name, description, or type and
    enabled matches         given parameter.

    args:

    - auth: Authentication details

    - db: Database session

    - value: str | None, Search term for filtering by value

    - enabled: bool | None, Status filter (enabled or disabled)

    returns:

    - GetSelectedAllWarninglistsResponse: Response containing filtered or all warninglists

    Args:
        value (Union[Unset, str]):
        enabled (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetSelectedAllWarninglistsResponse, HTTPValidationError]
    """

    return sync_detailed(
        client=client,
        value=value,
        enabled=enabled,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    value: Union[Unset, str] = UNSET,
    enabled: Union[Unset, bool] = UNSET,
) -> Response[Union[GetSelectedAllWarninglistsResponse, HTTPValidationError]]:
    """Get all warninglists, or selected ones by value and status

     Receive a list of all warning lists, or when setting the path parameters value and enabled, receive
    a         list of warninglists for which the value matches either the name, description, or type and
    enabled matches         given parameter.

    args:

    - auth: Authentication details

    - db: Database session

    - value: str | None, Search term for filtering by value

    - enabled: bool | None, Status filter (enabled or disabled)

    returns:

    - GetSelectedAllWarninglistsResponse: Response containing filtered or all warninglists

    Args:
        value (Union[Unset, str]):
        enabled (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetSelectedAllWarninglistsResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        value=value,
        enabled=enabled,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    value: Union[Unset, str] = UNSET,
    enabled: Union[Unset, bool] = UNSET,
) -> Optional[Union[GetSelectedAllWarninglistsResponse, HTTPValidationError]]:
    """Get all warninglists, or selected ones by value and status

     Receive a list of all warning lists, or when setting the path parameters value and enabled, receive
    a         list of warninglists for which the value matches either the name, description, or type and
    enabled matches         given parameter.

    args:

    - auth: Authentication details

    - db: Database session

    - value: str | None, Search term for filtering by value

    - enabled: bool | None, Status filter (enabled or disabled)

    returns:

    - GetSelectedAllWarninglistsResponse: Response containing filtered or all warninglists

    Args:
        value (Union[Unset, str]):
        enabled (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetSelectedAllWarninglistsResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            client=client,
            value=value,
            enabled=enabled,
        )
    ).parsed
