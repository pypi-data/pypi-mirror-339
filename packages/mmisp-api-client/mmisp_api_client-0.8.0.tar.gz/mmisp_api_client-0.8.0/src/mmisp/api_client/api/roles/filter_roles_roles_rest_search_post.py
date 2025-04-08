from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.filter_role_body import FilterRoleBody
from ...models.filter_role_response import FilterRoleResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    *,
    body: FilterRoleBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/roles/restSearch",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, list["FilterRoleResponse"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = FilterRoleResponse.from_dict(response_200_item_data)

            response_200.append(response_200_item)

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
) -> Response[Union[HTTPValidationError, list["FilterRoleResponse"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: FilterRoleBody,
) -> Response[Union[HTTPValidationError, list["FilterRoleResponse"]]]:
    """Search roles with filters

     Search roles based on filters.

    args:
        auth: the user's authentication status
        db: the current database
        body: the requested body containing the requested filter data

    returns:
        the searched and filtered roles

    raises:
        200: Successful Response
        422: Validation Error
        403: Forbidden Error
        404: Not Found Error

    Args:
        body (FilterRoleBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['FilterRoleResponse']]]
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
    body: FilterRoleBody,
) -> Optional[Union[HTTPValidationError, list["FilterRoleResponse"]]]:
    """Search roles with filters

     Search roles based on filters.

    args:
        auth: the user's authentication status
        db: the current database
        body: the requested body containing the requested filter data

    returns:
        the searched and filtered roles

    raises:
        200: Successful Response
        422: Validation Error
        403: Forbidden Error
        404: Not Found Error

    Args:
        body (FilterRoleBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['FilterRoleResponse']]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: FilterRoleBody,
) -> Response[Union[HTTPValidationError, list["FilterRoleResponse"]]]:
    """Search roles with filters

     Search roles based on filters.

    args:
        auth: the user's authentication status
        db: the current database
        body: the requested body containing the requested filter data

    returns:
        the searched and filtered roles

    raises:
        200: Successful Response
        422: Validation Error
        403: Forbidden Error
        404: Not Found Error

    Args:
        body (FilterRoleBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['FilterRoleResponse']]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: FilterRoleBody,
) -> Optional[Union[HTTPValidationError, list["FilterRoleResponse"]]]:
    """Search roles with filters

     Search roles based on filters.

    args:
        auth: the user's authentication status
        db: the current database
        body: the requested body containing the requested filter data

    returns:
        the searched and filtered roles

    raises:
        200: Successful Response
        422: Validation Error
        403: Forbidden Error
        404: Not Found Error

    Args:
        body (FilterRoleBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['FilterRoleResponse']]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
