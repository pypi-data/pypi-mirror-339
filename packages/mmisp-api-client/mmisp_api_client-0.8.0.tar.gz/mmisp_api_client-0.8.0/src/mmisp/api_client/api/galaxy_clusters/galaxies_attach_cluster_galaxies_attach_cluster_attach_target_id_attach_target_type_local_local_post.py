from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.attach_cluster_galaxy_body import AttachClusterGalaxyBody
from ...models.attach_cluster_galaxy_response import AttachClusterGalaxyResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    attach_target_id: str,
    attach_target_type: str,
    local: str,
    *,
    body: AttachClusterGalaxyBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/galaxies/attachCluster/{attach_target_id}/{attach_target_type}/local:{local}",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[AttachClusterGalaxyResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = AttachClusterGalaxyResponse.from_dict(response.json())

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
) -> Response[Union[AttachClusterGalaxyResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    attach_target_id: str,
    attach_target_type: str,
    local: str,
    *,
    client: AuthenticatedClient,
    body: AttachClusterGalaxyBody,
) -> Response[Union[AttachClusterGalaxyResponse, HTTPValidationError]]:
    """Attach Cluster to Galaxy.

     Attach a Galaxy Cluster to given Galaxy.

    args:

    - the user's authentification status

    - the current database

    - the id of the attach target

    - the type of the attach target

    - the request body

    - local

    returns:

    - the attached galaxy cluster and the attach target

    Args:
        attach_target_id (str):
        attach_target_type (str):
        local (str):
        body (AttachClusterGalaxyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AttachClusterGalaxyResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        attach_target_id=attach_target_id,
        attach_target_type=attach_target_type,
        local=local,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    attach_target_id: str,
    attach_target_type: str,
    local: str,
    *,
    client: AuthenticatedClient,
    body: AttachClusterGalaxyBody,
) -> Optional[Union[AttachClusterGalaxyResponse, HTTPValidationError]]:
    """Attach Cluster to Galaxy.

     Attach a Galaxy Cluster to given Galaxy.

    args:

    - the user's authentification status

    - the current database

    - the id of the attach target

    - the type of the attach target

    - the request body

    - local

    returns:

    - the attached galaxy cluster and the attach target

    Args:
        attach_target_id (str):
        attach_target_type (str):
        local (str):
        body (AttachClusterGalaxyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AttachClusterGalaxyResponse, HTTPValidationError]
    """

    return sync_detailed(
        attach_target_id=attach_target_id,
        attach_target_type=attach_target_type,
        local=local,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    attach_target_id: str,
    attach_target_type: str,
    local: str,
    *,
    client: AuthenticatedClient,
    body: AttachClusterGalaxyBody,
) -> Response[Union[AttachClusterGalaxyResponse, HTTPValidationError]]:
    """Attach Cluster to Galaxy.

     Attach a Galaxy Cluster to given Galaxy.

    args:

    - the user's authentification status

    - the current database

    - the id of the attach target

    - the type of the attach target

    - the request body

    - local

    returns:

    - the attached galaxy cluster and the attach target

    Args:
        attach_target_id (str):
        attach_target_type (str):
        local (str):
        body (AttachClusterGalaxyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[AttachClusterGalaxyResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        attach_target_id=attach_target_id,
        attach_target_type=attach_target_type,
        local=local,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    attach_target_id: str,
    attach_target_type: str,
    local: str,
    *,
    client: AuthenticatedClient,
    body: AttachClusterGalaxyBody,
) -> Optional[Union[AttachClusterGalaxyResponse, HTTPValidationError]]:
    """Attach Cluster to Galaxy.

     Attach a Galaxy Cluster to given Galaxy.

    args:

    - the user's authentification status

    - the current database

    - the id of the attach target

    - the type of the attach target

    - the request body

    - local

    returns:

    - the attached galaxy cluster and the attach target

    Args:
        attach_target_id (str):
        attach_target_type (str):
        local (str):
        body (AttachClusterGalaxyBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[AttachClusterGalaxyResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            attach_target_id=attach_target_id,
            attach_target_type=attach_target_type,
            local=local,
            client=client,
            body=body,
        )
    ).parsed
