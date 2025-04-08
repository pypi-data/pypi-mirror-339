from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.module_index_workflows_module_index_type_type_get_response_200_item import (
    ModuleIndexWorkflowsModuleIndexTypeTypeGetResponse200Item,
)
from ...types import Response


def _get_kwargs(
    type_: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/workflows/moduleIndex/type:{type_}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, list["ModuleIndexWorkflowsModuleIndexTypeTypeGetResponse200Item"]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ModuleIndexWorkflowsModuleIndexTypeTypeGetResponse200Item.from_dict(
                response_200_item_data
            )

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
) -> Response[Union[HTTPValidationError, list["ModuleIndexWorkflowsModuleIndexTypeTypeGetResponse200Item"]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    type_: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, list["ModuleIndexWorkflowsModuleIndexTypeTypeGetResponse200Item"]]]:
    """Returns modules

     Retrieve modules with optional filtering.

    All filter parameters are optional. If no parameters are provided, no filtering will be applied.

    - **type**: Filter by type. Valid values are 'action', 'logic', 'custom', and 'all'.
    - **actiontype**: Filter by action type. Valid values are 'all', 'mispmodule', and 'blocking'.
    - **enabled**: If true, returns only enabled modules. If false, returns only disabled modules.
    - **limit**: The number of items to display per page (for pagination).
    - **page**: The page number to display (for pagination).

    Args:
        type_ (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['ModuleIndexWorkflowsModuleIndexTypeTypeGetResponse200Item']]]
    """

    kwargs = _get_kwargs(
        type_=type_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    type_: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, list["ModuleIndexWorkflowsModuleIndexTypeTypeGetResponse200Item"]]]:
    """Returns modules

     Retrieve modules with optional filtering.

    All filter parameters are optional. If no parameters are provided, no filtering will be applied.

    - **type**: Filter by type. Valid values are 'action', 'logic', 'custom', and 'all'.
    - **actiontype**: Filter by action type. Valid values are 'all', 'mispmodule', and 'blocking'.
    - **enabled**: If true, returns only enabled modules. If false, returns only disabled modules.
    - **limit**: The number of items to display per page (for pagination).
    - **page**: The page number to display (for pagination).

    Args:
        type_ (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['ModuleIndexWorkflowsModuleIndexTypeTypeGetResponse200Item']]
    """

    return sync_detailed(
        type_=type_,
        client=client,
    ).parsed


async def asyncio_detailed(
    type_: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, list["ModuleIndexWorkflowsModuleIndexTypeTypeGetResponse200Item"]]]:
    """Returns modules

     Retrieve modules with optional filtering.

    All filter parameters are optional. If no parameters are provided, no filtering will be applied.

    - **type**: Filter by type. Valid values are 'action', 'logic', 'custom', and 'all'.
    - **actiontype**: Filter by action type. Valid values are 'all', 'mispmodule', and 'blocking'.
    - **enabled**: If true, returns only enabled modules. If false, returns only disabled modules.
    - **limit**: The number of items to display per page (for pagination).
    - **page**: The page number to display (for pagination).

    Args:
        type_ (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, list['ModuleIndexWorkflowsModuleIndexTypeTypeGetResponse200Item']]]
    """

    kwargs = _get_kwargs(
        type_=type_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    type_: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, list["ModuleIndexWorkflowsModuleIndexTypeTypeGetResponse200Item"]]]:
    """Returns modules

     Retrieve modules with optional filtering.

    All filter parameters are optional. If no parameters are provided, no filtering will be applied.

    - **type**: Filter by type. Valid values are 'action', 'logic', 'custom', and 'all'.
    - **actiontype**: Filter by action type. Valid values are 'all', 'mispmodule', and 'blocking'.
    - **enabled**: If true, returns only enabled modules. If false, returns only disabled modules.
    - **limit**: The number of items to display per page (for pagination).
    - **page**: The page number to display (for pagination).

    Args:
        type_ (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, list['ModuleIndexWorkflowsModuleIndexTypeTypeGetResponse200Item']]
    """

    return (
        await asyncio_detailed(
            type_=type_,
            client=client,
        )
    ).parsed
