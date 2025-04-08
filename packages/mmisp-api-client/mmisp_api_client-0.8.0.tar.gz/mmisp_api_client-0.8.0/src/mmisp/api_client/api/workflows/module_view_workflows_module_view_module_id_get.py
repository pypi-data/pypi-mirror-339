from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.module_view_workflows_module_view_module_id_get_response_moduleview_workflows_moduleview_moduleid_get import (
    ModuleViewWorkflowsModuleViewModuleIdGetResponseModuleviewWorkflowsModuleviewModuleidGet,
)
from ...types import Response


def _get_kwargs(
    module_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/workflows/moduleView/{module_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[HTTPValidationError, ModuleViewWorkflowsModuleViewModuleIdGetResponseModuleviewWorkflowsModuleviewModuleidGet]
]:
    if response.status_code == 200:
        response_200 = (
            ModuleViewWorkflowsModuleViewModuleIdGetResponseModuleviewWorkflowsModuleviewModuleidGet.from_dict(
                response.json()
            )
        )

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
) -> Response[
    Union[HTTPValidationError, ModuleViewWorkflowsModuleViewModuleIdGetResponseModuleviewWorkflowsModuleviewModuleidGet]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    module_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[HTTPValidationError, ModuleViewWorkflowsModuleViewModuleIdGetResponseModuleviewWorkflowsModuleviewModuleidGet]
]:
    """Returns a singular module

     Returns a singular module.

    - **module_id** The ID of the module.

    Args:
        module_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ModuleViewWorkflowsModuleViewModuleIdGetResponseModuleviewWorkflowsModuleviewModuleidGet]]
    """

    kwargs = _get_kwargs(
        module_id=module_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    module_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[HTTPValidationError, ModuleViewWorkflowsModuleViewModuleIdGetResponseModuleviewWorkflowsModuleviewModuleidGet]
]:
    """Returns a singular module

     Returns a singular module.

    - **module_id** The ID of the module.

    Args:
        module_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ModuleViewWorkflowsModuleViewModuleIdGetResponseModuleviewWorkflowsModuleviewModuleidGet]
    """

    return sync_detailed(
        module_id=module_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    module_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[
    Union[HTTPValidationError, ModuleViewWorkflowsModuleViewModuleIdGetResponseModuleviewWorkflowsModuleviewModuleidGet]
]:
    """Returns a singular module

     Returns a singular module.

    - **module_id** The ID of the module.

    Args:
        module_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ModuleViewWorkflowsModuleViewModuleIdGetResponseModuleviewWorkflowsModuleviewModuleidGet]]
    """

    kwargs = _get_kwargs(
        module_id=module_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    module_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[
    Union[HTTPValidationError, ModuleViewWorkflowsModuleViewModuleIdGetResponseModuleviewWorkflowsModuleviewModuleidGet]
]:
    """Returns a singular module

     Returns a singular module.

    - **module_id** The ID of the module.

    Args:
        module_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ModuleViewWorkflowsModuleViewModuleIdGetResponseModuleviewWorkflowsModuleviewModuleidGet]
    """

    return (
        await asyncio_detailed(
            module_id=module_id,
            client=client,
        )
    ).parsed
