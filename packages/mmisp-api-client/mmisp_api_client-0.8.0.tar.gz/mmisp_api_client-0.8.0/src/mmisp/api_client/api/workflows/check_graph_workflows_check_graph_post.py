from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.check_graph_response import CheckGraphResponse
from ...types import Response


def _get_kwargs() -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/workflows/checkGraph",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[CheckGraphResponse]:
    if response.status_code == 200:
        response_200 = CheckGraphResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[CheckGraphResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[CheckGraphResponse]:
    """Checks if the given graph is correct

     Checks if the given graph is correct.

    This will check if the graph is acyclic, if any node has multiple output connections
    and if there are path warnings.

    - **graph** The workflow graph to check.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CheckGraphResponse]
    """

    kwargs = _get_kwargs()

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
) -> Optional[CheckGraphResponse]:
    """Checks if the given graph is correct

     Checks if the given graph is correct.

    This will check if the graph is acyclic, if any node has multiple output connections
    and if there are path warnings.

    - **graph** The workflow graph to check.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CheckGraphResponse
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
) -> Response[CheckGraphResponse]:
    """Checks if the given graph is correct

     Checks if the given graph is correct.

    This will check if the graph is acyclic, if any node has multiple output connections
    and if there are path warnings.

    - **graph** The workflow graph to check.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CheckGraphResponse]
    """

    kwargs = _get_kwargs()

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
) -> Optional[CheckGraphResponse]:
    """Checks if the given graph is correct

     Checks if the given graph is correct.

    This will check if the graph is acyclic, if any node has multiple output connections
    and if there are path warnings.

    - **graph** The workflow graph to check.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CheckGraphResponse
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
