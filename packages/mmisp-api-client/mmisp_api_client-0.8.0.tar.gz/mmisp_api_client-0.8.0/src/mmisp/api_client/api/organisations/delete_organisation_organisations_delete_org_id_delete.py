from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.delete_force_update_organisation_response import DeleteForceUpdateOrganisationResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    org_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": f"/organisations/delete/{org_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[DeleteForceUpdateOrganisationResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = DeleteForceUpdateOrganisationResponse.from_dict(response.json())

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
) -> Response[Union[DeleteForceUpdateOrganisationResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    org_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[DeleteForceUpdateOrganisationResponse, HTTPValidationError]]:
    """Deletes an organisation by its ID

     Deletes an organisation by its ID.

    args:

    - ID of the organisation to delete

    - The current database

    returns:

    - Response indicating success or failure

    Args:
        org_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeleteForceUpdateOrganisationResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    org_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[DeleteForceUpdateOrganisationResponse, HTTPValidationError]]:
    """Deletes an organisation by its ID

     Deletes an organisation by its ID.

    args:

    - ID of the organisation to delete

    - The current database

    returns:

    - Response indicating success or failure

    Args:
        org_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DeleteForceUpdateOrganisationResponse, HTTPValidationError]
    """

    return sync_detailed(
        org_id=org_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    org_id: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[DeleteForceUpdateOrganisationResponse, HTTPValidationError]]:
    """Deletes an organisation by its ID

     Deletes an organisation by its ID.

    args:

    - ID of the organisation to delete

    - The current database

    returns:

    - Response indicating success or failure

    Args:
        org_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DeleteForceUpdateOrganisationResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        org_id=org_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    org_id: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[DeleteForceUpdateOrganisationResponse, HTTPValidationError]]:
    """Deletes an organisation by its ID

     Deletes an organisation by its ID.

    args:

    - ID of the organisation to delete

    - The current database

    returns:

    - Response indicating success or failure

    Args:
        org_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DeleteForceUpdateOrganisationResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            org_id=org_id,
            client=client,
        )
    ).parsed
