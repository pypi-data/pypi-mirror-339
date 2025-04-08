from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.update_sharing_group_legacy_body import UpdateSharingGroupLegacyBody
from ...models.view_update_sharing_group_legacy_response import ViewUpdateSharingGroupLegacyResponse
from ...types import Response


def _get_kwargs(
    sharing_group_id: int,
    *,
    body: UpdateSharingGroupLegacyBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/sharing_groups/edit/{sharing_group_id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ViewUpdateSharingGroupLegacyResponse]]:
    if response.status_code == 200:
        response_200 = ViewUpdateSharingGroupLegacyResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ViewUpdateSharingGroupLegacyResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    sharing_group_id: int,
    *,
    client: AuthenticatedClient,
    body: UpdateSharingGroupLegacyBody,
) -> Response[Union[HTTPValidationError, ViewUpdateSharingGroupLegacyResponse]]:
    """Update sharing group

     Update an existing sharing group by its ID.

    Args:
      auth: Authentication details
      db: Database session
      id: ID of the sharing group to update
      body: Request body containing updated details for the sharing group

    Returns:
      ViewUpdateSharingGroupLegacyResponse: Representation of the updated sharing group.

    Args:
        sharing_group_id (int):
        body (UpdateSharingGroupLegacyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ViewUpdateSharingGroupLegacyResponse]]
    """

    kwargs = _get_kwargs(
        sharing_group_id=sharing_group_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sharing_group_id: int,
    *,
    client: AuthenticatedClient,
    body: UpdateSharingGroupLegacyBody,
) -> Optional[Union[HTTPValidationError, ViewUpdateSharingGroupLegacyResponse]]:
    """Update sharing group

     Update an existing sharing group by its ID.

    Args:
      auth: Authentication details
      db: Database session
      id: ID of the sharing group to update
      body: Request body containing updated details for the sharing group

    Returns:
      ViewUpdateSharingGroupLegacyResponse: Representation of the updated sharing group.

    Args:
        sharing_group_id (int):
        body (UpdateSharingGroupLegacyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ViewUpdateSharingGroupLegacyResponse]
    """

    return sync_detailed(
        sharing_group_id=sharing_group_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    sharing_group_id: int,
    *,
    client: AuthenticatedClient,
    body: UpdateSharingGroupLegacyBody,
) -> Response[Union[HTTPValidationError, ViewUpdateSharingGroupLegacyResponse]]:
    """Update sharing group

     Update an existing sharing group by its ID.

    Args:
      auth: Authentication details
      db: Database session
      id: ID of the sharing group to update
      body: Request body containing updated details for the sharing group

    Returns:
      ViewUpdateSharingGroupLegacyResponse: Representation of the updated sharing group.

    Args:
        sharing_group_id (int):
        body (UpdateSharingGroupLegacyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ViewUpdateSharingGroupLegacyResponse]]
    """

    kwargs = _get_kwargs(
        sharing_group_id=sharing_group_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sharing_group_id: int,
    *,
    client: AuthenticatedClient,
    body: UpdateSharingGroupLegacyBody,
) -> Optional[Union[HTTPValidationError, ViewUpdateSharingGroupLegacyResponse]]:
    """Update sharing group

     Update an existing sharing group by its ID.

    Args:
      auth: Authentication details
      db: Database session
      id: ID of the sharing group to update
      body: Request body containing updated details for the sharing group

    Returns:
      ViewUpdateSharingGroupLegacyResponse: Representation of the updated sharing group.

    Args:
        sharing_group_id (int):
        body (UpdateSharingGroupLegacyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ViewUpdateSharingGroupLegacyResponse]
    """

    return (
        await asyncio_detailed(
            sharing_group_id=sharing_group_id,
            client=client,
            body=body,
        )
    ).parsed
