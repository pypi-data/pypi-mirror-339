from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.add_server_to_sharing_group_body import AddServerToSharingGroupBody
from ...models.add_server_to_sharing_group_sharing_groups_id_servers_patch_response_add_server_to_sharing_group_sharing_groups_id_servers_patch import (
    AddServerToSharingGroupSharingGroupsIdServersPatchResponseAddServerToSharingGroupSharingGroupsIdServersPatch,
)
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    id: int,
    *,
    body: AddServerToSharingGroupBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": f"/sharing_groups/{id}/servers",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        AddServerToSharingGroupSharingGroupsIdServersPatchResponseAddServerToSharingGroupSharingGroupsIdServersPatch,
        HTTPValidationError,
    ]
]:
    if response.status_code == 200:
        response_200 = AddServerToSharingGroupSharingGroupsIdServersPatchResponseAddServerToSharingGroupSharingGroupsIdServersPatch.from_dict(
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
        AddServerToSharingGroupSharingGroupsIdServersPatchResponseAddServerToSharingGroupSharingGroupsIdServersPatch,
        HTTPValidationError,
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
    *,
    client: AuthenticatedClient,
    body: AddServerToSharingGroupBody,
) -> Response[
    Union[
        AddServerToSharingGroupSharingGroupsIdServersPatchResponseAddServerToSharingGroupSharingGroupsIdServersPatch,
        HTTPValidationError,
    ]
]:
    """Add a server

     Add a server to a sharing group.

    Args:
      auth: Authentication details
      db: Database session
      id: ID of the sharing group to add the server
      body: Request body containing server details

    Returns:
      Representation of the added server in the sharing group

    Args:
        id (int):
        body (AddServerToSharingGroupBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AddServerToSharingGroupSharingGroupsIdServersPatchResponseAddServerToSharingGroupSharingGroupsIdServersPatch, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: int,
    *,
    client: AuthenticatedClient,
    body: AddServerToSharingGroupBody,
) -> Optional[
    Union[
        AddServerToSharingGroupSharingGroupsIdServersPatchResponseAddServerToSharingGroupSharingGroupsIdServersPatch,
        HTTPValidationError,
    ]
]:
    """Add a server

     Add a server to a sharing group.

    Args:
      auth: Authentication details
      db: Database session
      id: ID of the sharing group to add the server
      body: Request body containing server details

    Returns:
      Representation of the added server in the sharing group

    Args:
        id (int):
        body (AddServerToSharingGroupBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AddServerToSharingGroupSharingGroupsIdServersPatchResponseAddServerToSharingGroupSharingGroupsIdServersPatch, HTTPValidationError]
    """

    return sync_detailed(
        id=id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    id: int,
    *,
    client: AuthenticatedClient,
    body: AddServerToSharingGroupBody,
) -> Response[
    Union[
        AddServerToSharingGroupSharingGroupsIdServersPatchResponseAddServerToSharingGroupSharingGroupsIdServersPatch,
        HTTPValidationError,
    ]
]:
    """Add a server

     Add a server to a sharing group.

    Args:
      auth: Authentication details
      db: Database session
      id: ID of the sharing group to add the server
      body: Request body containing server details

    Returns:
      Representation of the added server in the sharing group

    Args:
        id (int):
        body (AddServerToSharingGroupBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AddServerToSharingGroupSharingGroupsIdServersPatchResponseAddServerToSharingGroupSharingGroupsIdServersPatch, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        id=id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: int,
    *,
    client: AuthenticatedClient,
    body: AddServerToSharingGroupBody,
) -> Optional[
    Union[
        AddServerToSharingGroupSharingGroupsIdServersPatchResponseAddServerToSharingGroupSharingGroupsIdServersPatch,
        HTTPValidationError,
    ]
]:
    """Add a server

     Add a server to a sharing group.

    Args:
      auth: Authentication details
      db: Database session
      id: ID of the sharing group to add the server
      body: Request body containing server details

    Returns:
      Representation of the added server in the sharing group

    Args:
        id (int):
        body (AddServerToSharingGroupBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AddServerToSharingGroupSharingGroupsIdServersPatchResponseAddServerToSharingGroupSharingGroupsIdServersPatch, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed
