from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.change_login_info_response import ChangeLoginInfoResponse
from ...models.http_validation_error import HTTPValidationError
from ...models.identity_provider_edit_body import IdentityProviderEditBody
from ...types import Response


def _get_kwargs(
    open_id_connect_provider: str,
    *,
    body: IdentityProviderEditBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/auth/openID/editOpenIDConnectProvider/{open_id_connect_provider}",
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
    open_id_connect_provider: str,
    *,
    client: AuthenticatedClient,
    body: IdentityProviderEditBody,
) -> Response[Union[ChangeLoginInfoResponse, HTTPValidationError]]:
    """Edit Openid Connect Provider

     Edits an OpenID Connect provider

    args:

    - OpenID Connect provider

    - The current database

    returns:

    - updated OpenID Connect provider

    Args:
        open_id_connect_provider (str):
        body (IdentityProviderEditBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ChangeLoginInfoResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        open_id_connect_provider=open_id_connect_provider,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    open_id_connect_provider: str,
    *,
    client: AuthenticatedClient,
    body: IdentityProviderEditBody,
) -> Optional[Union[ChangeLoginInfoResponse, HTTPValidationError]]:
    """Edit Openid Connect Provider

     Edits an OpenID Connect provider

    args:

    - OpenID Connect provider

    - The current database

    returns:

    - updated OpenID Connect provider

    Args:
        open_id_connect_provider (str):
        body (IdentityProviderEditBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ChangeLoginInfoResponse, HTTPValidationError]
    """

    return sync_detailed(
        open_id_connect_provider=open_id_connect_provider,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    open_id_connect_provider: str,
    *,
    client: AuthenticatedClient,
    body: IdentityProviderEditBody,
) -> Response[Union[ChangeLoginInfoResponse, HTTPValidationError]]:
    """Edit Openid Connect Provider

     Edits an OpenID Connect provider

    args:

    - OpenID Connect provider

    - The current database

    returns:

    - updated OpenID Connect provider

    Args:
        open_id_connect_provider (str):
        body (IdentityProviderEditBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ChangeLoginInfoResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        open_id_connect_provider=open_id_connect_provider,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    open_id_connect_provider: str,
    *,
    client: AuthenticatedClient,
    body: IdentityProviderEditBody,
) -> Optional[Union[ChangeLoginInfoResponse, HTTPValidationError]]:
    """Edit Openid Connect Provider

     Edits an OpenID Connect provider

    args:

    - OpenID Connect provider

    - The current database

    returns:

    - updated OpenID Connect provider

    Args:
        open_id_connect_provider (str):
        body (IdentityProviderEditBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ChangeLoginInfoResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            open_id_connect_provider=open_id_connect_provider,
            client=client,
            body=body,
        )
    ).parsed
