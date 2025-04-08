from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_sharing_group_sharing_groups_id_get_response_get_sharing_group_sharing_groups_id_get import (
    GetSharingGroupSharingGroupsIdGetResponseGetSharingGroupSharingGroupsIdGet,
)
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    id: Union[UUID, int],
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/sharing_groups/{id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetSharingGroupSharingGroupsIdGetResponseGetSharingGroupSharingGroupsIdGet, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = GetSharingGroupSharingGroupsIdGetResponseGetSharingGroupSharingGroupsIdGet.from_dict(
            response.json()
        )

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
) -> Response[Union[GetSharingGroupSharingGroupsIdGetResponseGetSharingGroupSharingGroupsIdGet, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: Union[UUID, int],
    *,
    client: AuthenticatedClient,
) -> Response[Union[GetSharingGroupSharingGroupsIdGetResponseGetSharingGroupSharingGroupsIdGet, HTTPValidationError]]:
    """Get sharing group details

     Retrieve details of a specific sharing group.

    Args:
      auth: Authentication details
      db: Database session
      id: ID of the sharing group to retrieve

    Returns:
      Representation of the sharing group details

    Args:
        id (Union[UUID, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetSharingGroupSharingGroupsIdGetResponseGetSharingGroupSharingGroupsIdGet, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: Union[UUID, int],
    *,
    client: AuthenticatedClient,
) -> Optional[Union[GetSharingGroupSharingGroupsIdGetResponseGetSharingGroupSharingGroupsIdGet, HTTPValidationError]]:
    """Get sharing group details

     Retrieve details of a specific sharing group.

    Args:
      auth: Authentication details
      db: Database session
      id: ID of the sharing group to retrieve

    Returns:
      Representation of the sharing group details

    Args:
        id (Union[UUID, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetSharingGroupSharingGroupsIdGetResponseGetSharingGroupSharingGroupsIdGet, HTTPValidationError]
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: Union[UUID, int],
    *,
    client: AuthenticatedClient,
) -> Response[Union[GetSharingGroupSharingGroupsIdGetResponseGetSharingGroupSharingGroupsIdGet, HTTPValidationError]]:
    """Get sharing group details

     Retrieve details of a specific sharing group.

    Args:
      auth: Authentication details
      db: Database session
      id: ID of the sharing group to retrieve

    Returns:
      Representation of the sharing group details

    Args:
        id (Union[UUID, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetSharingGroupSharingGroupsIdGetResponseGetSharingGroupSharingGroupsIdGet, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: Union[UUID, int],
    *,
    client: AuthenticatedClient,
) -> Optional[Union[GetSharingGroupSharingGroupsIdGetResponseGetSharingGroupSharingGroupsIdGet, HTTPValidationError]]:
    """Get sharing group details

     Retrieve details of a specific sharing group.

    Args:
      auth: Authentication details
      db: Database session
      id: ID of the sharing group to retrieve

    Returns:
      Representation of the sharing group details

    Args:
        id (Union[UUID, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetSharingGroupSharingGroupsIdGetResponseGetSharingGroupSharingGroupsIdGet, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
