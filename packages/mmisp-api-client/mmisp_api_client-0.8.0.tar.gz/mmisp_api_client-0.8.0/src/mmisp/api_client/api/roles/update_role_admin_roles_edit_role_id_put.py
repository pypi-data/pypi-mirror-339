from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.edit_role_body import EditRoleBody
from ...models.edit_role_response import EditRoleResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    role_id: int,
    *,
    body: EditRoleBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/admin/roles/edit/{role_id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[EditRoleResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = EditRoleResponse.from_dict(response.json())

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
) -> Response[Union[EditRoleResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    role_id: int,
    *,
    client: AuthenticatedClient,
    body: EditRoleBody,
) -> Response[Union[EditRoleResponse, HTTPValidationError]]:
    """Edit a role

     Update an existing event either by its event ID or via its UUID.

    args:
        auth: the user's authentification status
        db: the current database
        role_id: the ID of the role
        body: the request body

    returns:
        the updated event

    Args:
        role_id (int):
        body (EditRoleBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[EditRoleResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        role_id=role_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    role_id: int,
    *,
    client: AuthenticatedClient,
    body: EditRoleBody,
) -> Optional[Union[EditRoleResponse, HTTPValidationError]]:
    """Edit a role

     Update an existing event either by its event ID or via its UUID.

    args:
        auth: the user's authentification status
        db: the current database
        role_id: the ID of the role
        body: the request body

    returns:
        the updated event

    Args:
        role_id (int):
        body (EditRoleBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[EditRoleResponse, HTTPValidationError]
    """

    return sync_detailed(
        role_id=role_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    role_id: int,
    *,
    client: AuthenticatedClient,
    body: EditRoleBody,
) -> Response[Union[EditRoleResponse, HTTPValidationError]]:
    """Edit a role

     Update an existing event either by its event ID or via its UUID.

    args:
        auth: the user's authentification status
        db: the current database
        role_id: the ID of the role
        body: the request body

    returns:
        the updated event

    Args:
        role_id (int):
        body (EditRoleBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[EditRoleResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        role_id=role_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    role_id: int,
    *,
    client: AuthenticatedClient,
    body: EditRoleBody,
) -> Optional[Union[EditRoleResponse, HTTPValidationError]]:
    """Edit a role

     Update an existing event either by its event ID or via its UUID.

    args:
        auth: the user's authentification status
        db: the current database
        role_id: the ID of the role
        body: the request body

    returns:
        the updated event

    Args:
        role_id (int):
        body (EditRoleBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[EditRoleResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            role_id=role_id,
            client=client,
            body=body,
        )
    ).parsed
