from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.edit_auth_key_body import EditAuthKeyBody
from ...models.edit_auth_key_response_compl import EditAuthKeyResponseCompl
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    auth_key_id: int,
    *,
    body: EditAuthKeyBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/auth_keys/{auth_key_id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[EditAuthKeyResponseCompl, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = EditAuthKeyResponseCompl.from_dict(response.json())

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
) -> Response[Union[EditAuthKeyResponseCompl, HTTPValidationError]]:
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
    body: EditAuthKeyBody,
) -> Response[Union[EditAuthKeyResponseCompl, HTTPValidationError]]:
    """Edit an AuthKey.

     Edit an AuthKey by its ID.

    args:

    - the user's authentification status

    - the current database

    - the id of the authkey

    - the request body

    returns:

    - the updated authkey

    Args:
        auth_key_id (int):
        body (EditAuthKeyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[EditAuthKeyResponseCompl, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        auth_key_id=auth_key_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    auth_key_id: int,
    *,
    client: AuthenticatedClient,
    body: EditAuthKeyBody,
) -> Optional[Union[EditAuthKeyResponseCompl, HTTPValidationError]]:
    """Edit an AuthKey.

     Edit an AuthKey by its ID.

    args:

    - the user's authentification status

    - the current database

    - the id of the authkey

    - the request body

    returns:

    - the updated authkey

    Args:
        auth_key_id (int):
        body (EditAuthKeyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[EditAuthKeyResponseCompl, HTTPValidationError]
    """

    return sync_detailed(
        auth_key_id=auth_key_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    auth_key_id: int,
    *,
    client: AuthenticatedClient,
    body: EditAuthKeyBody,
) -> Response[Union[EditAuthKeyResponseCompl, HTTPValidationError]]:
    """Edit an AuthKey.

     Edit an AuthKey by its ID.

    args:

    - the user's authentification status

    - the current database

    - the id of the authkey

    - the request body

    returns:

    - the updated authkey

    Args:
        auth_key_id (int):
        body (EditAuthKeyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[EditAuthKeyResponseCompl, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        auth_key_id=auth_key_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    auth_key_id: int,
    *,
    client: AuthenticatedClient,
    body: EditAuthKeyBody,
) -> Optional[Union[EditAuthKeyResponseCompl, HTTPValidationError]]:
    """Edit an AuthKey.

     Edit an AuthKey by its ID.

    args:

    - the user's authentification status

    - the current database

    - the id of the authkey

    - the request body

    returns:

    - the updated authkey

    Args:
        auth_key_id (int):
        body (EditAuthKeyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[EditAuthKeyResponseCompl, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            auth_key_id=auth_key_id,
            client=client,
            body=body,
        )
    ).parsed
