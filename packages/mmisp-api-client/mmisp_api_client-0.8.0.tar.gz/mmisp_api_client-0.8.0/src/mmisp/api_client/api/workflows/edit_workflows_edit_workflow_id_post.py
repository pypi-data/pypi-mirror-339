from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.edit_workflows_edit_workflow_id_post_response_edit_workflows_edit_workflowid_post import (
    EditWorkflowsEditWorkflowIdPostResponseEditWorkflowsEditWorkflowidPost,
)
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    workflow_id: int,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/workflows/edit/{workflow_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[EditWorkflowsEditWorkflowIdPostResponseEditWorkflowsEditWorkflowidPost, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = EditWorkflowsEditWorkflowIdPostResponseEditWorkflowsEditWorkflowidPost.from_dict(response.json())

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
) -> Response[Union[EditWorkflowsEditWorkflowIdPostResponseEditWorkflowsEditWorkflowidPost, HTTPValidationError]]:
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
) -> Response[Union[EditWorkflowsEditWorkflowIdPostResponseEditWorkflowsEditWorkflowidPost, HTTPValidationError]]:
    """Edits a workflow

     Edits a workflow.

    When a change it made this endpoints overrwrites the outdated workflow in the database.
    It is also used to add new workflows. The response is the edited workflow.

    - **workflow_id** The ID of the workflow to edit.
    - **workflow_name** The new name.
    - **workflow_description** The new description.
    - **workflow_graph** The new workflow graph.

    Args:
        workflow_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[EditWorkflowsEditWorkflowIdPostResponseEditWorkflowsEditWorkflowidPost, HTTPValidationError]]
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
) -> Optional[Union[EditWorkflowsEditWorkflowIdPostResponseEditWorkflowsEditWorkflowidPost, HTTPValidationError]]:
    """Edits a workflow

     Edits a workflow.

    When a change it made this endpoints overrwrites the outdated workflow in the database.
    It is also used to add new workflows. The response is the edited workflow.

    - **workflow_id** The ID of the workflow to edit.
    - **workflow_name** The new name.
    - **workflow_description** The new description.
    - **workflow_graph** The new workflow graph.

    Args:
        workflow_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[EditWorkflowsEditWorkflowIdPostResponseEditWorkflowsEditWorkflowidPost, HTTPValidationError]
    """

    return sync_detailed(
        workflow_id=workflow_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    workflow_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[EditWorkflowsEditWorkflowIdPostResponseEditWorkflowsEditWorkflowidPost, HTTPValidationError]]:
    """Edits a workflow

     Edits a workflow.

    When a change it made this endpoints overrwrites the outdated workflow in the database.
    It is also used to add new workflows. The response is the edited workflow.

    - **workflow_id** The ID of the workflow to edit.
    - **workflow_name** The new name.
    - **workflow_description** The new description.
    - **workflow_graph** The new workflow graph.

    Args:
        workflow_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[EditWorkflowsEditWorkflowIdPostResponseEditWorkflowsEditWorkflowidPost, HTTPValidationError]]
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
) -> Optional[Union[EditWorkflowsEditWorkflowIdPostResponseEditWorkflowsEditWorkflowidPost, HTTPValidationError]]:
    """Edits a workflow

     Edits a workflow.

    When a change it made this endpoints overrwrites the outdated workflow in the database.
    It is also used to add new workflows. The response is the edited workflow.

    - **workflow_id** The ID of the workflow to edit.
    - **workflow_name** The new name.
    - **workflow_description** The new description.
    - **workflow_graph** The new workflow graph.

    Args:
        workflow_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[EditWorkflowsEditWorkflowIdPostResponseEditWorkflowsEditWorkflowidPost, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            workflow_id=workflow_id,
            client=client,
        )
    ).parsed
