from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.standard_status_identified_response import StandardStatusIdentifiedResponse
from ...types import Response


def _get_kwargs(
    workflow_id: int,
    enabled: bool,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/workflows/debugToggleField/{workflow_id}/{enabled}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, StandardStatusIdentifiedResponse]]:
    if response.status_code == 200:
        response_200 = StandardStatusIdentifiedResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, StandardStatusIdentifiedResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workflow_id: int,
    enabled: bool,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, StandardStatusIdentifiedResponse]]:
    """Status whether the workflow setting is globally enabled/ disabled

    Args:
        workflow_id (int):
        enabled (bool):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, StandardStatusIdentifiedResponse]]
    """

    kwargs = _get_kwargs(
        workflow_id=workflow_id,
        enabled=enabled,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workflow_id: int,
    enabled: bool,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, StandardStatusIdentifiedResponse]]:
    """Status whether the workflow setting is globally enabled/ disabled

    Args:
        workflow_id (int):
        enabled (bool):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, StandardStatusIdentifiedResponse]
    """

    return sync_detailed(
        workflow_id=workflow_id,
        enabled=enabled,
        client=client,
    ).parsed


async def asyncio_detailed(
    workflow_id: int,
    enabled: bool,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, StandardStatusIdentifiedResponse]]:
    """Status whether the workflow setting is globally enabled/ disabled

    Args:
        workflow_id (int):
        enabled (bool):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, StandardStatusIdentifiedResponse]]
    """

    kwargs = _get_kwargs(
        workflow_id=workflow_id,
        enabled=enabled,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workflow_id: int,
    enabled: bool,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, StandardStatusIdentifiedResponse]]:
    """Status whether the workflow setting is globally enabled/ disabled

    Args:
        workflow_id (int):
        enabled (bool):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, StandardStatusIdentifiedResponse]
    """

    return (
        await asyncio_detailed(
            workflow_id=workflow_id,
            enabled=enabled,
            client=client,
        )
    ).parsed
