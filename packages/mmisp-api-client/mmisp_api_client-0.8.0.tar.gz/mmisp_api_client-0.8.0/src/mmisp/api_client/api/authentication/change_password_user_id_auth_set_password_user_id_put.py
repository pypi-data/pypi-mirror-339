from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.change_login_info_response import ChangeLoginInfoResponse
from ...models.http_validation_error import HTTPValidationError
from ...models.set_password_body import SetPasswordBody
from ...types import Response


def _get_kwargs(
    user_id: int,
    *,
    body: SetPasswordBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": f"/auth/setPassword/{user_id}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ChangeLoginInfoResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = ChangeLoginInfoResponse.from_dict(response.json())

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
) -> Response[Union[ChangeLoginInfoResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user_id: int,
    *,
    client: AuthenticatedClient,
    body: SetPasswordBody,
) -> Response[Union[ChangeLoginInfoResponse, HTTPValidationError]]:
    """Admin sets the password of the user to a new password

     Set the password of the user to a new password

    args:

    - the request body

    - The current database

    returns:

    - the response from the api after the password change request

    Args:
        user_id (int):
        body (SetPasswordBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ChangeLoginInfoResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    user_id: int,
    *,
    client: AuthenticatedClient,
    body: SetPasswordBody,
) -> Optional[Union[ChangeLoginInfoResponse, HTTPValidationError]]:
    """Admin sets the password of the user to a new password

     Set the password of the user to a new password

    args:

    - the request body

    - The current database

    returns:

    - the response from the api after the password change request

    Args:
        user_id (int):
        body (SetPasswordBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ChangeLoginInfoResponse, HTTPValidationError]
    """

    return sync_detailed(
        user_id=user_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    user_id: int,
    *,
    client: AuthenticatedClient,
    body: SetPasswordBody,
) -> Response[Union[ChangeLoginInfoResponse, HTTPValidationError]]:
    """Admin sets the password of the user to a new password

     Set the password of the user to a new password

    args:

    - the request body

    - The current database

    returns:

    - the response from the api after the password change request

    Args:
        user_id (int):
        body (SetPasswordBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ChangeLoginInfoResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_id: int,
    *,
    client: AuthenticatedClient,
    body: SetPasswordBody,
) -> Optional[Union[ChangeLoginInfoResponse, HTTPValidationError]]:
    """Admin sets the password of the user to a new password

     Set the password of the user to a new password

    args:

    - the request body

    - The current database

    returns:

    - the response from the api after the password change request

    Args:
        user_id (int):
        body (SetPasswordBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ChangeLoginInfoResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            user_id=user_id,
            client=client,
            body=body,
        )
    ).parsed
