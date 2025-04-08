from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.single_sharing_group_response import SingleSharingGroupResponse
from ...types import Response


def _get_kwargs(
    sharing_group_id: Union[UUID, int],
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/sharing_groups/view/{sharing_group_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, SingleSharingGroupResponse]]:
    if response.status_code == 200:
        response_200 = SingleSharingGroupResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, SingleSharingGroupResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    sharing_group_id: Union[UUID, int],
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, SingleSharingGroupResponse]]:
    """Get sharing groups details

     Retrieve details of a specific sharing group by its ID.

    Args:
      auth: Authentication details
      db: Database session
      id: ID of the sharing group to retrieve

    Returns:
      Representation of the sharing group details

    Args:
        sharing_group_id (Union[UUID, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, SingleSharingGroupResponse]]
    """

    kwargs = _get_kwargs(
        sharing_group_id=sharing_group_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sharing_group_id: Union[UUID, int],
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, SingleSharingGroupResponse]]:
    """Get sharing groups details

     Retrieve details of a specific sharing group by its ID.

    Args:
      auth: Authentication details
      db: Database session
      id: ID of the sharing group to retrieve

    Returns:
      Representation of the sharing group details

    Args:
        sharing_group_id (Union[UUID, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, SingleSharingGroupResponse]
    """

    return sync_detailed(
        sharing_group_id=sharing_group_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    sharing_group_id: Union[UUID, int],
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, SingleSharingGroupResponse]]:
    """Get sharing groups details

     Retrieve details of a specific sharing group by its ID.

    Args:
      auth: Authentication details
      db: Database session
      id: ID of the sharing group to retrieve

    Returns:
      Representation of the sharing group details

    Args:
        sharing_group_id (Union[UUID, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, SingleSharingGroupResponse]]
    """

    kwargs = _get_kwargs(
        sharing_group_id=sharing_group_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sharing_group_id: Union[UUID, int],
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, SingleSharingGroupResponse]]:
    """Get sharing groups details

     Retrieve details of a specific sharing group by its ID.

    Args:
      auth: Authentication details
      db: Database session
      id: ID of the sharing group to retrieve

    Returns:
      Representation of the sharing group details

    Args:
        sharing_group_id (Union[UUID, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, SingleSharingGroupResponse]
    """

    return (
        await asyncio_detailed(
            sharing_group_id=sharing_group_id,
            client=client,
        )
    ).parsed
