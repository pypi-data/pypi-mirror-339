from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_sharing_group_legacy_body import CreateSharingGroupLegacyBody
from ...models.create_sharing_group_legacy_response import CreateSharingGroupLegacyResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    *,
    body: CreateSharingGroupLegacyBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/sharing_groups/add",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[CreateSharingGroupLegacyResponse, HTTPValidationError]]:
    if response.status_code == 201:
        response_201 = CreateSharingGroupLegacyResponse.from_dict(response.json())

        return response_201
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CreateSharingGroupLegacyResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateSharingGroupLegacyBody,
) -> Response[Union[CreateSharingGroupLegacyResponse, HTTPValidationError]]:
    """Create Sharing Group Legacy

     Add a new sharing group with given details.

    Args:
      auth: Authentication details
      db: Database session
      body: Request body containing details for creating the sharing group

    Returns:
      Representation of the created sharing group

    Args:
        body (CreateSharingGroupLegacyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateSharingGroupLegacyResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: CreateSharingGroupLegacyBody,
) -> Optional[Union[CreateSharingGroupLegacyResponse, HTTPValidationError]]:
    """Create Sharing Group Legacy

     Add a new sharing group with given details.

    Args:
      auth: Authentication details
      db: Database session
      body: Request body containing details for creating the sharing group

    Returns:
      Representation of the created sharing group

    Args:
        body (CreateSharingGroupLegacyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateSharingGroupLegacyResponse, HTTPValidationError]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateSharingGroupLegacyBody,
) -> Response[Union[CreateSharingGroupLegacyResponse, HTTPValidationError]]:
    """Create Sharing Group Legacy

     Add a new sharing group with given details.

    Args:
      auth: Authentication details
      db: Database session
      body: Request body containing details for creating the sharing group

    Returns:
      Representation of the created sharing group

    Args:
        body (CreateSharingGroupLegacyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateSharingGroupLegacyResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CreateSharingGroupLegacyBody,
) -> Optional[Union[CreateSharingGroupLegacyResponse, HTTPValidationError]]:
    """Create Sharing Group Legacy

     Add a new sharing group with given details.

    Args:
      auth: Authentication details
      db: Database session
      body: Request body containing details for creating the sharing group

    Returns:
      Representation of the created sharing group

    Args:
        body (CreateSharingGroupLegacyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateSharingGroupLegacyResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
