from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.view_workflows_view_workflow_id_get_response_view_workflows_view_workflowid_get import (
    ViewWorkflowsViewWorkflowIdGetResponseViewWorkflowsViewWorkflowidGet,
)
from ...types import Response


def _get_kwargs(
    workflow_id: int,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/workflows/view/{workflow_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ViewWorkflowsViewWorkflowIdGetResponseViewWorkflowsViewWorkflowidGet]]:
    if response.status_code == 200:
        response_200 = ViewWorkflowsViewWorkflowIdGetResponseViewWorkflowsViewWorkflowidGet.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ViewWorkflowsViewWorkflowIdGetResponseViewWorkflowsViewWorkflowidGet]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workflow_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, ViewWorkflowsViewWorkflowIdGetResponseViewWorkflowsViewWorkflowidGet]]:
    """Get a workflow

     Gets a workflow.

    Is called view because it is used to display the workflow in the visual editor
    but it just returns the data of a workflow.

    - **workflow_id** The ID of the workflow to view.

    Args:
        workflow_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ViewWorkflowsViewWorkflowIdGetResponseViewWorkflowsViewWorkflowidGet]]
    """

    kwargs = _get_kwargs(
        workflow_id=workflow_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workflow_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, ViewWorkflowsViewWorkflowIdGetResponseViewWorkflowsViewWorkflowidGet]]:
    """Get a workflow

     Gets a workflow.

    Is called view because it is used to display the workflow in the visual editor
    but it just returns the data of a workflow.

    - **workflow_id** The ID of the workflow to view.

    Args:
        workflow_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ViewWorkflowsViewWorkflowIdGetResponseViewWorkflowsViewWorkflowidGet]
    """

    return sync_detailed(
        workflow_id=workflow_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    workflow_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, ViewWorkflowsViewWorkflowIdGetResponseViewWorkflowsViewWorkflowidGet]]:
    """Get a workflow

     Gets a workflow.

    Is called view because it is used to display the workflow in the visual editor
    but it just returns the data of a workflow.

    - **workflow_id** The ID of the workflow to view.

    Args:
        workflow_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ViewWorkflowsViewWorkflowIdGetResponseViewWorkflowsViewWorkflowidGet]]
    """

    kwargs = _get_kwargs(
        workflow_id=workflow_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workflow_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, ViewWorkflowsViewWorkflowIdGetResponseViewWorkflowsViewWorkflowidGet]]:
    """Get a workflow

     Gets a workflow.

    Is called view because it is used to display the workflow in the visual editor
    but it just returns the data of a workflow.

    - **workflow_id** The ID of the workflow to view.

    Args:
        workflow_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ViewWorkflowsViewWorkflowIdGetResponseViewWorkflowsViewWorkflowidGet]
    """

    return (
        await asyncio_detailed(
            workflow_id=workflow_id,
            client=client,
        )
    ).parsed
