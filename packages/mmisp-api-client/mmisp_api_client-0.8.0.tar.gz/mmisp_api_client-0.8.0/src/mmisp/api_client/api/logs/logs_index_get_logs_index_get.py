from http import HTTPStatus
from typing import Any, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    model: Union[Unset, str] = UNSET,
    action: Union[Unset, str] = UNSET,
    model_id: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["page"] = page

    params["limit"] = limit

    params["model"] = model

    params["action"] = action

    params["model_id"] = model_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/logs/index",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, list[Any]]]:
    if response.status_code == 200:
        response_200 = cast(list[Any], response.json())

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
) -> Response[Union[HTTPValidationError, list[Any]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    model: Union[Unset, str] = UNSET,
    action: Union[Unset, str] = UNSET,
    model_id: Union[Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, list[Any]]]:
    """List logs

     List logs, filter can be applied.

    - **page** the page for pagination
    - **limit** the limit for pagination

    Args:
        page (Union[Unset, int]):
        limit (Union[Unset, int]):
        model (Union[Unset, str]):
        action (Union[Unset, str]):
        model_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list[Any]]]
    """

    kwargs = _get_kwargs(
        page=page,
        limit=limit,
        model=model,
        action=action,
        model_id=model_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    model: Union[Unset, str] = UNSET,
    action: Union[Unset, str] = UNSET,
    model_id: Union[Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, list[Any]]]:
    """List logs

     List logs, filter can be applied.

    - **page** the page for pagination
    - **limit** the limit for pagination

    Args:
        page (Union[Unset, int]):
        limit (Union[Unset, int]):
        model (Union[Unset, str]):
        action (Union[Unset, str]):
        model_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list[Any]]
    """

    return sync_detailed(
        client=client,
        page=page,
        limit=limit,
        model=model,
        action=action,
        model_id=model_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    model: Union[Unset, str] = UNSET,
    action: Union[Unset, str] = UNSET,
    model_id: Union[Unset, str] = UNSET,
) -> Response[Union[HTTPValidationError, list[Any]]]:
    """List logs

     List logs, filter can be applied.

    - **page** the page for pagination
    - **limit** the limit for pagination

    Args:
        page (Union[Unset, int]):
        limit (Union[Unset, int]):
        model (Union[Unset, str]):
        action (Union[Unset, str]):
        model_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list[Any]]]
    """

    kwargs = _get_kwargs(
        page=page,
        limit=limit,
        model=model,
        action=action,
        model_id=model_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    model: Union[Unset, str] = UNSET,
    action: Union[Unset, str] = UNSET,
    model_id: Union[Unset, str] = UNSET,
) -> Optional[Union[HTTPValidationError, list[Any]]]:
    """List logs

     List logs, filter can be applied.

    - **page** the page for pagination
    - **limit** the limit for pagination

    Args:
        page (Union[Unset, int]):
        limit (Union[Unset, int]):
        model (Union[Unset, str]):
        action (Union[Unset, str]):
        model_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list[Any]]
    """

    return (
        await asyncio_detailed(
            client=client,
            page=page,
            limit=limit,
            model=model,
            action=action,
            model_id=model_id,
        )
    ).parsed
