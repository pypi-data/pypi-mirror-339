from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.view_auth_keys_response import ViewAuthKeysResponse
from ...types import Response


def _get_kwargs(
    auth_key_id: int,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/auth_keys/view/{auth_key_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ViewAuthKeysResponse]]:
    if response.status_code == 200:
        response_200 = ViewAuthKeysResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ViewAuthKeysResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    auth_key_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, ViewAuthKeysResponse]]:
    """View an AuthKey

     View an AuthKey by its ID.

    args:

    - the user's authentification status

    - the current database

    - the id of the authkey

    returns:

    - the authkey

    Args:
        auth_key_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ViewAuthKeysResponse]]
    """

    kwargs = _get_kwargs(
        auth_key_id=auth_key_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    auth_key_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, ViewAuthKeysResponse]]:
    """View an AuthKey

     View an AuthKey by its ID.

    args:

    - the user's authentification status

    - the current database

    - the id of the authkey

    returns:

    - the authkey

    Args:
        auth_key_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ViewAuthKeysResponse]
    """

    return sync_detailed(
        auth_key_id=auth_key_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    auth_key_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, ViewAuthKeysResponse]]:
    """View an AuthKey

     View an AuthKey by its ID.

    args:

    - the user's authentification status

    - the current database

    - the id of the authkey

    returns:

    - the authkey

    Args:
        auth_key_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ViewAuthKeysResponse]]
    """

    kwargs = _get_kwargs(
        auth_key_id=auth_key_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    auth_key_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, ViewAuthKeysResponse]]:
    """View an AuthKey

     View an AuthKey by its ID.

    args:

    - the user's authentification status

    - the current database

    - the id of the authkey

    returns:

    - the authkey

    Args:
        auth_key_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ViewAuthKeysResponse]
    """

    return (
        await asyncio_detailed(
            auth_key_id=auth_key_id,
            client=client,
        )
    ).parsed
