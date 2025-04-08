from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_sharing_group_info_sharing_groups_id_info_get_response_get_sharing_group_info_sharing_groups_id_info_get import (
    GetSharingGroupInfoSharingGroupsIdInfoGetResponseGetSharingGroupInfoSharingGroupsIdInfoGet,
)
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    id: int,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/sharing_groups/{id}/info",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        GetSharingGroupInfoSharingGroupsIdInfoGetResponseGetSharingGroupInfoSharingGroupsIdInfoGet, HTTPValidationError
    ]
]:
    if response.status_code == 200:
        response_200 = (
            GetSharingGroupInfoSharingGroupsIdInfoGetResponseGetSharingGroupInfoSharingGroupsIdInfoGet.from_dict(
                response.json()
            )
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
        GetSharingGroupInfoSharingGroupsIdInfoGetResponseGetSharingGroupInfoSharingGroupsIdInfoGet, HTTPValidationError
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
) -> Response[
    Union[
        GetSharingGroupInfoSharingGroupsIdInfoGetResponseGetSharingGroupInfoSharingGroupsIdInfoGet, HTTPValidationError
    ]
]:
    """Additional infos from a sharing group

     Details of a sharing group and org.count, user_count and created_by_email.

    Args:
      auth: Authentication details
      db: Database session
      id: ID of the sharing group to retrieve additional information

    Returns:
      Representation of the sharing group information

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetSharingGroupInfoSharingGroupsIdInfoGetResponseGetSharingGroupInfoSharingGroupsIdInfoGet, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[
        GetSharingGroupInfoSharingGroupsIdInfoGetResponseGetSharingGroupInfoSharingGroupsIdInfoGet, HTTPValidationError
    ]
]:
    """Additional infos from a sharing group

     Details of a sharing group and org.count, user_count and created_by_email.

    Args:
      auth: Authentication details
      db: Database session
      id: ID of the sharing group to retrieve additional information

    Returns:
      Representation of the sharing group information

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetSharingGroupInfoSharingGroupsIdInfoGetResponseGetSharingGroupInfoSharingGroupsIdInfoGet, HTTPValidationError]
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: int,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[
        GetSharingGroupInfoSharingGroupsIdInfoGetResponseGetSharingGroupInfoSharingGroupsIdInfoGet, HTTPValidationError
    ]
]:
    """Additional infos from a sharing group

     Details of a sharing group and org.count, user_count and created_by_email.

    Args:
      auth: Authentication details
      db: Database session
      id: ID of the sharing group to retrieve additional information

    Returns:
      Representation of the sharing group information

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetSharingGroupInfoSharingGroupsIdInfoGetResponseGetSharingGroupInfoSharingGroupsIdInfoGet, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        id=id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[
        GetSharingGroupInfoSharingGroupsIdInfoGetResponseGetSharingGroupInfoSharingGroupsIdInfoGet, HTTPValidationError
    ]
]:
    """Additional infos from a sharing group

     Details of a sharing group and org.count, user_count and created_by_email.

    Args:
      auth: Authentication details
      db: Database session
      id: ID of the sharing group to retrieve additional information

    Returns:
      Representation of the sharing group information

    Args:
        id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetSharingGroupInfoSharingGroupsIdInfoGetResponseGetSharingGroupInfoSharingGroupsIdInfoGet, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
