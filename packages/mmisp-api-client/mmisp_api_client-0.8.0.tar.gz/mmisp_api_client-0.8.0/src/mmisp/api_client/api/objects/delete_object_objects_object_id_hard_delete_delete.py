from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.standard_status_response import StandardStatusResponse
from ...types import Response


def _get_kwargs(
    object_id: int,
    hard_delete: bool,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": f"/objects/{object_id}/{hard_delete}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, StandardStatusResponse]]:
    if response.status_code == 200:
        response_200 = StandardStatusResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, StandardStatusResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    object_id: int,
    hard_delete: bool,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, StandardStatusResponse]]:
    """Delete object

     Delete a specific object. The hardDelete parameter determines if it's a hard or soft delete.

    args:

    - the user's authentification status

    - the current database

    - the object id

    - hard delete

    returns:

    - the deleted object

    Args:
        object_id (int):
        hard_delete (bool):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, StandardStatusResponse]]
    """

    kwargs = _get_kwargs(
        object_id=object_id,
        hard_delete=hard_delete,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    object_id: int,
    hard_delete: bool,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, StandardStatusResponse]]:
    """Delete object

     Delete a specific object. The hardDelete parameter determines if it's a hard or soft delete.

    args:

    - the user's authentification status

    - the current database

    - the object id

    - hard delete

    returns:

    - the deleted object

    Args:
        object_id (int):
        hard_delete (bool):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, StandardStatusResponse]
    """

    return sync_detailed(
        object_id=object_id,
        hard_delete=hard_delete,
        client=client,
    ).parsed


async def asyncio_detailed(
    object_id: int,
    hard_delete: bool,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, StandardStatusResponse]]:
    """Delete object

     Delete a specific object. The hardDelete parameter determines if it's a hard or soft delete.

    args:

    - the user's authentification status

    - the current database

    - the object id

    - hard delete

    returns:

    - the deleted object

    Args:
        object_id (int):
        hard_delete (bool):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, StandardStatusResponse]]
    """

    kwargs = _get_kwargs(
        object_id=object_id,
        hard_delete=hard_delete,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    object_id: int,
    hard_delete: bool,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, StandardStatusResponse]]:
    """Delete object

     Delete a specific object. The hardDelete parameter determines if it's a hard or soft delete.

    args:

    - the user's authentification status

    - the current database

    - the object id

    - hard delete

    returns:

    - the deleted object

    Args:
        object_id (int):
        hard_delete (bool):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, StandardStatusResponse]
    """

    return (
        await asyncio_detailed(
            object_id=object_id,
            hard_delete=hard_delete,
            client=client,
        )
    ).parsed
