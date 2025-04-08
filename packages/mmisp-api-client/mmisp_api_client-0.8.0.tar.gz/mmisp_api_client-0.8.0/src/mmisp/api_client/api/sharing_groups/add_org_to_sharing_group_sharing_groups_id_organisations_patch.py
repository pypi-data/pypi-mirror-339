from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.add_org_to_sharing_group_body import AddOrgToSharingGroupBody
from ...models.http_validation_error import HTTPValidationError
from ...models.sharing_group_org import SharingGroupOrg
from ...types import Response


def _get_kwargs(
    id: int,
    *,
    body: AddOrgToSharingGroupBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": f"/sharing_groups/{id}/organisations",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, SharingGroupOrg]]:
    if response.status_code == 200:
        response_200 = SharingGroupOrg.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, SharingGroupOrg]]:
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
    body: AddOrgToSharingGroupBody,
) -> Response[Union[HTTPValidationError, SharingGroupOrg]]:
    """Add Org To Sharing Group

     Add an organisation to a sharing group.

    Args:
      auth: Authentication details
      db: Database session.
      id: ID of the sharing group to add the organisation
      body: Request body containing organisation details

    Returns:
      SharingGroupOrgSchema: Representation of the added organisation in the sharing group

    Args:
        id (int):
        body (AddOrgToSharingGroupBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, SharingGroupOrg]]
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
    body: AddOrgToSharingGroupBody,
) -> Optional[Union[HTTPValidationError, SharingGroupOrg]]:
    """Add Org To Sharing Group

     Add an organisation to a sharing group.

    Args:
      auth: Authentication details
      db: Database session.
      id: ID of the sharing group to add the organisation
      body: Request body containing organisation details

    Returns:
      SharingGroupOrgSchema: Representation of the added organisation in the sharing group

    Args:
        id (int):
        body (AddOrgToSharingGroupBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, SharingGroupOrg]
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
    body: AddOrgToSharingGroupBody,
) -> Response[Union[HTTPValidationError, SharingGroupOrg]]:
    """Add Org To Sharing Group

     Add an organisation to a sharing group.

    Args:
      auth: Authentication details
      db: Database session.
      id: ID of the sharing group to add the organisation
      body: Request body containing organisation details

    Returns:
      SharingGroupOrgSchema: Representation of the added organisation in the sharing group

    Args:
        id (int):
        body (AddOrgToSharingGroupBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, SharingGroupOrg]]
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
    body: AddOrgToSharingGroupBody,
) -> Optional[Union[HTTPValidationError, SharingGroupOrg]]:
    """Add Org To Sharing Group

     Add an organisation to a sharing group.

    Args:
      auth: Authentication details
      db: Database session.
      id: ID of the sharing group to add the organisation
      body: Request body containing organisation details

    Returns:
      SharingGroupOrgSchema: Representation of the added organisation in the sharing group

    Args:
        id (int):
        body (AddOrgToSharingGroupBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, SharingGroupOrg]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            body=body,
        )
    ).parsed
