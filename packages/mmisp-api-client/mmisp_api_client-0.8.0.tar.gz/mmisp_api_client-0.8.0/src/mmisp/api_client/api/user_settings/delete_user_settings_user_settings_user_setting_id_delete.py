from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.standard_status_identified_response import StandardStatusIdentifiedResponse
from ...types import Response


def _get_kwargs(
    user_setting_id: int,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "delete",
        "url": f"/user_settings/{user_setting_id}",
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
    user_setting_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, StandardStatusIdentifiedResponse]]:
    """Deletes a UserSetting.

     Deletes UserSetting by UserSetting ID.

    args:

    - userSettingId: ID of the user setting to delete

    - auth: Authentication details

    - db: Database session

    returns:

    - StandardStatusIdentifiedResponse: Response indicating success or failure

    Args:
        user_setting_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, StandardStatusIdentifiedResponse]]
    """

    kwargs = _get_kwargs(
        user_setting_id=user_setting_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    user_setting_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, StandardStatusIdentifiedResponse]]:
    """Deletes a UserSetting.

     Deletes UserSetting by UserSetting ID.

    args:

    - userSettingId: ID of the user setting to delete

    - auth: Authentication details

    - db: Database session

    returns:

    - StandardStatusIdentifiedResponse: Response indicating success or failure

    Args:
        user_setting_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, StandardStatusIdentifiedResponse]
    """

    return sync_detailed(
        user_setting_id=user_setting_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    user_setting_id: int,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, StandardStatusIdentifiedResponse]]:
    """Deletes a UserSetting.

     Deletes UserSetting by UserSetting ID.

    args:

    - userSettingId: ID of the user setting to delete

    - auth: Authentication details

    - db: Database session

    returns:

    - StandardStatusIdentifiedResponse: Response indicating success or failure

    Args:
        user_setting_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, StandardStatusIdentifiedResponse]]
    """

    kwargs = _get_kwargs(
        user_setting_id=user_setting_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_setting_id: int,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, StandardStatusIdentifiedResponse]]:
    """Deletes a UserSetting.

     Deletes UserSetting by UserSetting ID.

    args:

    - userSettingId: ID of the user setting to delete

    - auth: Authentication details

    - db: Database session

    returns:

    - StandardStatusIdentifiedResponse: Response indicating success or failure

    Args:
        user_setting_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, StandardStatusIdentifiedResponse]
    """

    return (
        await asyncio_detailed(
            user_setting_id=user_setting_id,
            client=client,
        )
    ).parsed
