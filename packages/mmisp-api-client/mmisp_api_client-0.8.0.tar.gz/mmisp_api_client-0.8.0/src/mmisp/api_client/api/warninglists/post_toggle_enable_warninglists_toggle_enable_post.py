from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.toggle_enable_warninglists_body import ToggleEnableWarninglistsBody
from ...models.toggle_enable_warninglists_response import ToggleEnableWarninglistsResponse
from ...types import Response


def _get_kwargs(
    *,
    body: ToggleEnableWarninglistsBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/warninglists/toggleEnable",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ToggleEnableWarninglistsResponse]]:
    if response.status_code == 200:
        response_200 = ToggleEnableWarninglistsResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ToggleEnableWarninglistsResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: ToggleEnableWarninglistsBody,
) -> Response[Union[HTTPValidationError, ToggleEnableWarninglistsResponse]]:
    """Disable/Enable warninglist

     Disable/Enable a specific warninglist by its ID or name.

    args:

    - auth: Authentication details

    - db:Database session

    - body: ToggleEnableWarninglistsBody, Data to toggle enable status of the warninglist

    returns:

    - ToggleEnableWarninglistsResponse: Response showing success or failure

    Args:
        body (ToggleEnableWarninglistsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ToggleEnableWarninglistsResponse]]
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
    body: ToggleEnableWarninglistsBody,
) -> Optional[Union[HTTPValidationError, ToggleEnableWarninglistsResponse]]:
    """Disable/Enable warninglist

     Disable/Enable a specific warninglist by its ID or name.

    args:

    - auth: Authentication details

    - db:Database session

    - body: ToggleEnableWarninglistsBody, Data to toggle enable status of the warninglist

    returns:

    - ToggleEnableWarninglistsResponse: Response showing success or failure

    Args:
        body (ToggleEnableWarninglistsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ToggleEnableWarninglistsResponse]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: ToggleEnableWarninglistsBody,
) -> Response[Union[HTTPValidationError, ToggleEnableWarninglistsResponse]]:
    """Disable/Enable warninglist

     Disable/Enable a specific warninglist by its ID or name.

    args:

    - auth: Authentication details

    - db:Database session

    - body: ToggleEnableWarninglistsBody, Data to toggle enable status of the warninglist

    returns:

    - ToggleEnableWarninglistsResponse: Response showing success or failure

    Args:
        body (ToggleEnableWarninglistsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ToggleEnableWarninglistsResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: ToggleEnableWarninglistsBody,
) -> Optional[Union[HTTPValidationError, ToggleEnableWarninglistsResponse]]:
    """Disable/Enable warninglist

     Disable/Enable a specific warninglist by its ID or name.

    args:

    - auth: Authentication details

    - db:Database session

    - body: ToggleEnableWarninglistsBody, Data to toggle enable status of the warninglist

    returns:

    - ToggleEnableWarninglistsResponse: Response showing success or failure

    Args:
        body (ToggleEnableWarninglistsBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ToggleEnableWarninglistsResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
