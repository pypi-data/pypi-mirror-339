from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.identity_provider_callback_body import IdentityProviderCallbackBody
from ...models.token_response import TokenResponse
from ...types import Response


def _get_kwargs(
    identity_provider_name: str,
    *,
    body: IdentityProviderCallbackBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/auth/login/idp/{identity_provider_name}/callback",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, TokenResponse]]:
    if response.status_code == 200:
        response_200 = TokenResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, TokenResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    identity_provider_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: IdentityProviderCallbackBody,
) -> Response[Union[HTTPValidationError, TokenResponse]]:
    """Redirect To Frontend

     Redirects to the frontend.

    args:

    - the database

    - the identity provider id

    - the code

    returns:

    - the redirection

    Args:
        identity_provider_name (str):
        body (IdentityProviderCallbackBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, TokenResponse]]
    """

    kwargs = _get_kwargs(
        identity_provider_name=identity_provider_name,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    identity_provider_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: IdentityProviderCallbackBody,
) -> Optional[Union[HTTPValidationError, TokenResponse]]:
    """Redirect To Frontend

     Redirects to the frontend.

    args:

    - the database

    - the identity provider id

    - the code

    returns:

    - the redirection

    Args:
        identity_provider_name (str):
        body (IdentityProviderCallbackBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, TokenResponse]
    """

    return sync_detailed(
        identity_provider_name=identity_provider_name,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    identity_provider_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: IdentityProviderCallbackBody,
) -> Response[Union[HTTPValidationError, TokenResponse]]:
    """Redirect To Frontend

     Redirects to the frontend.

    args:

    - the database

    - the identity provider id

    - the code

    returns:

    - the redirection

    Args:
        identity_provider_name (str):
        body (IdentityProviderCallbackBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, TokenResponse]]
    """

    kwargs = _get_kwargs(
        identity_provider_name=identity_provider_name,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    identity_provider_name: str,
    *,
    client: Union[AuthenticatedClient, Client],
    body: IdentityProviderCallbackBody,
) -> Optional[Union[HTTPValidationError, TokenResponse]]:
    """Redirect To Frontend

     Redirects to the frontend.

    args:

    - the database

    - the identity provider id

    - the code

    returns:

    - the redirection

    Args:
        identity_provider_name (str):
        body (IdentityProviderCallbackBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, TokenResponse]
    """

    return (
        await asyncio_detailed(
            identity_provider_name=identity_provider_name,
            client=client,
            body=body,
        )
    ).parsed
