from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.view_user_setting_response import ViewUserSettingResponse
from ...types import Response


def _get_kwargs(
    user_setting_name: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/user_settings/me/{user_setting_name}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, ViewUserSettingResponse]]:
    if response.status_code == 200:
        response_200 = ViewUserSettingResponse.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, ViewUserSettingResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user_setting_name: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, ViewUserSettingResponse]]:
    """View UserSetting.

     Displays a UserSetting by given userID and UserSetting name.

    args:

    - userId: ID of the user for whom setting is to be viewed

    - userSettingName: Name of the user setting to view

    - auth: Authentication details

    - db: Database session

    returns:

    - ViewUserSettingResponse: Response with details of the viewed user setting

    Args:
        user_setting_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ViewUserSettingResponse]]
    """

    kwargs = _get_kwargs(
        user_setting_name=user_setting_name,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    user_setting_name: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, ViewUserSettingResponse]]:
    """View UserSetting.

     Displays a UserSetting by given userID and UserSetting name.

    args:

    - userId: ID of the user for whom setting is to be viewed

    - userSettingName: Name of the user setting to view

    - auth: Authentication details

    - db: Database session

    returns:

    - ViewUserSettingResponse: Response with details of the viewed user setting

    Args:
        user_setting_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ViewUserSettingResponse]
    """

    return sync_detailed(
        user_setting_name=user_setting_name,
        client=client,
    ).parsed


async def asyncio_detailed(
    user_setting_name: str,
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, ViewUserSettingResponse]]:
    """View UserSetting.

     Displays a UserSetting by given userID and UserSetting name.

    args:

    - userId: ID of the user for whom setting is to be viewed

    - userSettingName: Name of the user setting to view

    - auth: Authentication details

    - db: Database session

    returns:

    - ViewUserSettingResponse: Response with details of the viewed user setting

    Args:
        user_setting_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, ViewUserSettingResponse]]
    """

    kwargs = _get_kwargs(
        user_setting_name=user_setting_name,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_setting_name: str,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, ViewUserSettingResponse]]:
    """View UserSetting.

     Displays a UserSetting by given userID and UserSetting name.

    args:

    - userId: ID of the user for whom setting is to be viewed

    - userSettingName: Name of the user setting to view

    - auth: Authentication details

    - db: Database session

    returns:

    - ViewUserSettingResponse: Response with details of the viewed user setting

    Args:
        user_setting_name (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, ViewUserSettingResponse]
    """

    return (
        await asyncio_detailed(
            user_setting_name=user_setting_name,
            client=client,
        )
    ).parsed
