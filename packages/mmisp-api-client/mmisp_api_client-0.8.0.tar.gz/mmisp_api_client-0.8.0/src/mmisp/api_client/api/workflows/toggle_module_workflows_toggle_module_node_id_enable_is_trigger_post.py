from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.standart_response import StandartResponse
from ...types import Response


def _get_kwargs(
    node_id: str,
    enable: bool,
    is_trigger: bool,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/workflows/toggleModule/{node_id}/{enable}/{is_trigger}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, StandartResponse]]:
    if response.status_code == 200:
        response_200 = StandartResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, StandartResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    node_id: str,
    enable: bool,
    is_trigger: bool,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, StandartResponse]]:
    """Enables/ disables a module

     Enables/ disables a module. Respons with a success status.

    Disabled modules can't be used in the visual editor.

    Note that the legacy misp accepted all node ID's and never threw an error.

    - **module_id**: The ID of the module.
    - **enable**: Whether the module should be enabled or not.
    - **is_trigger**: Indicates if the module is a trigger module.
    Trigger modules have specific behaviors and usage within the system.

    Args:
        node_id (str):
        enable (bool):
        is_trigger (bool):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, StandartResponse]]
    """

    kwargs = _get_kwargs(
        node_id=node_id,
        enable=enable,
        is_trigger=is_trigger,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    node_id: str,
    enable: bool,
    is_trigger: bool,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, StandartResponse]]:
    """Enables/ disables a module

     Enables/ disables a module. Respons with a success status.

    Disabled modules can't be used in the visual editor.

    Note that the legacy misp accepted all node ID's and never threw an error.

    - **module_id**: The ID of the module.
    - **enable**: Whether the module should be enabled or not.
    - **is_trigger**: Indicates if the module is a trigger module.
    Trigger modules have specific behaviors and usage within the system.

    Args:
        node_id (str):
        enable (bool):
        is_trigger (bool):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, StandartResponse]
    """

    return sync_detailed(
        node_id=node_id,
        enable=enable,
        is_trigger=is_trigger,
        client=client,
    ).parsed


async def asyncio_detailed(
    node_id: str,
    enable: bool,
    is_trigger: bool,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, StandartResponse]]:
    """Enables/ disables a module

     Enables/ disables a module. Respons with a success status.

    Disabled modules can't be used in the visual editor.

    Note that the legacy misp accepted all node ID's and never threw an error.

    - **module_id**: The ID of the module.
    - **enable**: Whether the module should be enabled or not.
    - **is_trigger**: Indicates if the module is a trigger module.
    Trigger modules have specific behaviors and usage within the system.

    Args:
        node_id (str):
        enable (bool):
        is_trigger (bool):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, StandartResponse]]
    """

    kwargs = _get_kwargs(
        node_id=node_id,
        enable=enable,
        is_trigger=is_trigger,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    node_id: str,
    enable: bool,
    is_trigger: bool,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, StandartResponse]]:
    """Enables/ disables a module

     Enables/ disables a module. Respons with a success status.

    Disabled modules can't be used in the visual editor.

    Note that the legacy misp accepted all node ID's and never threw an error.

    - **module_id**: The ID of the module.
    - **enable**: Whether the module should be enabled or not.
    - **is_trigger**: Indicates if the module is a trigger module.
    Trigger modules have specific behaviors and usage within the system.

    Args:
        node_id (str):
        enable (bool):
        is_trigger (bool):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, StandartResponse]
    """

    return (
        await asyncio_detailed(
            node_id=node_id,
            enable=enable,
            is_trigger=is_trigger,
            client=client,
        )
    ).parsed
