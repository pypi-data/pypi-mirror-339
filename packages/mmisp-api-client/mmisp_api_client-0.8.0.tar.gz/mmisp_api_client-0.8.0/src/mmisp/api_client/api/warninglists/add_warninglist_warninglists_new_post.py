from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_warninglist_body import CreateWarninglistBody
from ...models.http_validation_error import HTTPValidationError
from ...models.warninglist_response import WarninglistResponse
from ...types import Response


def _get_kwargs(
    *,
    body: CreateWarninglistBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/warninglists/new",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, WarninglistResponse]]:
    if response.status_code == 201:
        response_201 = WarninglistResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, WarninglistResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateWarninglistBody,
) -> Response[Union[HTTPValidationError, WarninglistResponse]]:
    """Add a new warninglist

     Add a new warninglist with given details.

    args:

    - auth: Authentication details

    - db: Database session

    - body: CreateWarninglistBody, Data for creating the new warninglist

    returns:

    - WarninglistResponse: Response with details of the new warninglist

    Args:
        body (CreateWarninglistBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, WarninglistResponse]]
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
    body: CreateWarninglistBody,
) -> Optional[Union[HTTPValidationError, WarninglistResponse]]:
    """Add a new warninglist

     Add a new warninglist with given details.

    args:

    - auth: Authentication details

    - db: Database session

    - body: CreateWarninglistBody, Data for creating the new warninglist

    returns:

    - WarninglistResponse: Response with details of the new warninglist

    Args:
        body (CreateWarninglistBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, WarninglistResponse]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: CreateWarninglistBody,
) -> Response[Union[HTTPValidationError, WarninglistResponse]]:
    """Add a new warninglist

     Add a new warninglist with given details.

    args:

    - auth: Authentication details

    - db: Database session

    - body: CreateWarninglistBody, Data for creating the new warninglist

    returns:

    - WarninglistResponse: Response with details of the new warninglist

    Args:
        body (CreateWarninglistBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, WarninglistResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: CreateWarninglistBody,
) -> Optional[Union[HTTPValidationError, WarninglistResponse]]:
    """Add a new warninglist

     Add a new warninglist with given details.

    args:

    - auth: Authentication details

    - db: Database session

    - body: CreateWarninglistBody, Data for creating the new warninglist

    returns:

    - WarninglistResponse: Response with details of the new warninglist

    Args:
        body (CreateWarninglistBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, WarninglistResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
