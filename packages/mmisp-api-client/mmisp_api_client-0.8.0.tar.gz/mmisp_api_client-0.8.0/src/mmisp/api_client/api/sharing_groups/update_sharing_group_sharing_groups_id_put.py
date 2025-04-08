from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.update_sharing_group_body import UpdateSharingGroupBody
from ...models.update_sharing_group_sharing_groups_id_put_response_update_sharing_group_sharing_groups_id_put import (
    UpdateSharingGroupSharingGroupsIdPutResponseUpdateSharingGroupSharingGroupsIdPut,
)
from ...types import Response


def _get_kwargs(
    id: int,
    *,
    body: UpdateSharingGroupBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/sharing_groups/{id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[HTTPValidationError, UpdateSharingGroupSharingGroupsIdPutResponseUpdateSharingGroupSharingGroupsIdPut]
]:
    if response.status_code == 200:
        response_200 = UpdateSharingGroupSharingGroupsIdPutResponseUpdateSharingGroupSharingGroupsIdPut.from_dict(
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
    Union[HTTPValidationError, UpdateSharingGroupSharingGroupsIdPutResponseUpdateSharingGroupSharingGroupsIdPut]
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
    body: UpdateSharingGroupBody,
) -> Response[
    Union[HTTPValidationError, UpdateSharingGroupSharingGroupsIdPutResponseUpdateSharingGroupSharingGroupsIdPut]
]:
    """Update sharing group

     Update an existing sharing group.

    Args:
      auth: Authentication details
      db: Database session
      id: ID of the sharing group to update
      body: Request body containing updated details for the sharing group

    Returns:
      Representation of the updated sharing group

    Args:
        id (int):
        body (UpdateSharingGroupBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, UpdateSharingGroupSharingGroupsIdPutResponseUpdateSharingGroupSharingGroupsIdPut]]
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
    body: UpdateSharingGroupBody,
) -> Optional[
    Union[HTTPValidationError, UpdateSharingGroupSharingGroupsIdPutResponseUpdateSharingGroupSharingGroupsIdPut]
]:
    """Update sharing group

     Update an existing sharing group.

    Args:
      auth: Authentication details
      db: Database session
      id: ID of the sharing group to update
      body: Request body containing updated details for the sharing group

    Returns:
      Representation of the updated sharing group

    Args:
        id (int):
        body (UpdateSharingGroupBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, UpdateSharingGroupSharingGroupsIdPutResponseUpdateSharingGroupSharingGroupsIdPut]
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
    body: UpdateSharingGroupBody,
) -> Response[
    Union[HTTPValidationError, UpdateSharingGroupSharingGroupsIdPutResponseUpdateSharingGroupSharingGroupsIdPut]
]:
    """Update sharing group

     Update an existing sharing group.

    Args:
      auth: Authentication details
      db: Database session
      id: ID of the sharing group to update
      body: Request body containing updated details for the sharing group

    Returns:
      Representation of the updated sharing group

    Args:
        id (int):
        body (UpdateSharingGroupBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, UpdateSharingGroupSharingGroupsIdPutResponseUpdateSharingGroupSharingGroupsIdPut]]
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
    body: UpdateSharingGroupBody,
) -> Optional[
    Union[HTTPValidationError, UpdateSharingGroupSharingGroupsIdPutResponseUpdateSharingGroupSharingGroupsIdPut]
]:
    """Update sharing group

     Update an existing sharing group.

    Args:
      auth: Authentication details
      db: Database session
      id: ID of the sharing group to update
      body: Request body containing updated details for the sharing group

    Returns:
      Representation of the updated sharing group

    Args:
        id (int):
        body (UpdateSharingGroupBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, UpdateSharingGroupSharingGroupsIdPutResponseUpdateSharingGroupSharingGroupsIdPut]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed
