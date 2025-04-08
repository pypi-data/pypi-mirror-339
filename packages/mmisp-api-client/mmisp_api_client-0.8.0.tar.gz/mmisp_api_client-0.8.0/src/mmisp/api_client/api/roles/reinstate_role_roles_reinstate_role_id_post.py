from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.reinstate_role_response import ReinstateRoleResponse
from ...types import Response


def _get_kwargs(
    role_id: int,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/roles/reinstate/{role_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ReinstateRoleResponse]]:
    if response.status_code == 200:
        response_200 = ReinstateRoleResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ReinstateRoleResponse]]:
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
) -> Response[Union[HTTPValidationError, ReinstateRoleResponse]]:
    """Reinstate a deleted standard role

     Reinstate a deleted standard role.

    args:
        auth: the user's authentication status
        db: the current database
        role_id: the role id of the to be reinstated role

    returns:
        the reinstated role

    raises:
        200: Successful Response
        422: Validation Error
        403: Forbidden Error
        404: Not Found Error

    Args:
        role_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ReinstateRoleResponse]]
    """

    kwargs = _get_kwargs(
        role_id=role_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    role_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, ReinstateRoleResponse]]:
    """Reinstate a deleted standard role

     Reinstate a deleted standard role.

    args:
        auth: the user's authentication status
        db: the current database
        role_id: the role id of the to be reinstated role

    returns:
        the reinstated role

    raises:
        200: Successful Response
        422: Validation Error
        403: Forbidden Error
        404: Not Found Error

    Args:
        role_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ReinstateRoleResponse]
    """

    return sync_detailed(
        role_id=role_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    role_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, ReinstateRoleResponse]]:
    """Reinstate a deleted standard role

     Reinstate a deleted standard role.

    args:
        auth: the user's authentication status
        db: the current database
        role_id: the role id of the to be reinstated role

    returns:
        the reinstated role

    raises:
        200: Successful Response
        422: Validation Error
        403: Forbidden Error
        404: Not Found Error

    Args:
        role_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ReinstateRoleResponse]]
    """

    kwargs = _get_kwargs(
        role_id=role_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    role_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, ReinstateRoleResponse]]:
    """Reinstate a deleted standard role

     Reinstate a deleted standard role.

    args:
        auth: the user's authentication status
        db: the current database
        role_id: the role id of the to be reinstated role

    returns:
        the reinstated role

    raises:
        200: Successful Response
        422: Validation Error
        403: Forbidden Error
        404: Not Found Error

    Args:
        role_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ReinstateRoleResponse]
    """

    return (
        await asyncio_detailed(
            role_id=role_id,
            client=client,
        )
    ).parsed
