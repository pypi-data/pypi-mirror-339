from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.remove_server_from_sharing_group_sharing_groups_id_servers_server_id_delete_response_remove_server_from_sharing_group_sharing_groups_id_servers_serverid_delete import (
    RemoveServerFromSharingGroupSharingGroupsIdServersServerIdDeleteResponseRemoveServerFromSharingGroupSharingGroupsIdServersServeridDelete,
)
from ...types import Response


def _get_kwargs(
    id: int,
    server_id: int,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": f"/sharing_groups/{id}/servers/{server_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        HTTPValidationError,
        RemoveServerFromSharingGroupSharingGroupsIdServersServerIdDeleteResponseRemoveServerFromSharingGroupSharingGroupsIdServersServeridDelete,
    ]
]:
    if response.status_code == 200:
        response_200 = RemoveServerFromSharingGroupSharingGroupsIdServersServerIdDeleteResponseRemoveServerFromSharingGroupSharingGroupsIdServersServeridDelete.from_dict(
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
) -> Response[
    Union[
        HTTPValidationError,
        RemoveServerFromSharingGroupSharingGroupsIdServersServerIdDeleteResponseRemoveServerFromSharingGroupSharingGroupsIdServersServeridDelete,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    id: int,
    server_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[
        HTTPValidationError,
        RemoveServerFromSharingGroupSharingGroupsIdServersServerIdDeleteResponseRemoveServerFromSharingGroupSharingGroupsIdServersServeridDelete,
    ]
]:
    """Remove a server

     Remove a server from a sharing group.

    Args:
      auth: Authentication details
      db: Database session
      id: ID of the sharing group to remove the server
      server_id: ID of the server to remove

    Returns:
      Representation of the removed server from the sharing group

    Args:
        id (int):
        server_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, RemoveServerFromSharingGroupSharingGroupsIdServersServerIdDeleteResponseRemoveServerFromSharingGroupSharingGroupsIdServersServeridDelete]]
    """

    kwargs = _get_kwargs(
        id=id,
        server_id=server_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: int,
    server_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[
        HTTPValidationError,
        RemoveServerFromSharingGroupSharingGroupsIdServersServerIdDeleteResponseRemoveServerFromSharingGroupSharingGroupsIdServersServeridDelete,
    ]
]:
    """Remove a server

     Remove a server from a sharing group.

    Args:
      auth: Authentication details
      db: Database session
      id: ID of the sharing group to remove the server
      server_id: ID of the server to remove

    Returns:
      Representation of the removed server from the sharing group

    Args:
        id (int):
        server_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, RemoveServerFromSharingGroupSharingGroupsIdServersServerIdDeleteResponseRemoveServerFromSharingGroupSharingGroupsIdServersServeridDelete]
    """

    return sync_detailed(
        id=id,
        server_id=server_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: int,
    server_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[
        HTTPValidationError,
        RemoveServerFromSharingGroupSharingGroupsIdServersServerIdDeleteResponseRemoveServerFromSharingGroupSharingGroupsIdServersServeridDelete,
    ]
]:
    """Remove a server

     Remove a server from a sharing group.

    Args:
      auth: Authentication details
      db: Database session
      id: ID of the sharing group to remove the server
      server_id: ID of the server to remove

    Returns:
      Representation of the removed server from the sharing group

    Args:
        id (int):
        server_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, RemoveServerFromSharingGroupSharingGroupsIdServersServerIdDeleteResponseRemoveServerFromSharingGroupSharingGroupsIdServersServeridDelete]]
    """

    kwargs = _get_kwargs(
        id=id,
        server_id=server_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: int,
    server_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[
        HTTPValidationError,
        RemoveServerFromSharingGroupSharingGroupsIdServersServerIdDeleteResponseRemoveServerFromSharingGroupSharingGroupsIdServersServeridDelete,
    ]
]:
    """Remove a server

     Remove a server from a sharing group.

    Args:
      auth: Authentication details
      db: Database session
      id: ID of the sharing group to remove the server
      server_id: ID of the server to remove

    Returns:
      Representation of the removed server from the sharing group

    Args:
        id (int):
        server_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, RemoveServerFromSharingGroupSharingGroupsIdServersServerIdDeleteResponseRemoveServerFromSharingGroupSharingGroupsIdServersServeridDelete]
    """

    return (
        await asyncio_detailed(
            id=id,
            server_id=server_id,
            client=client,
        )
    ).parsed
