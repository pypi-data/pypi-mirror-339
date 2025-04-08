from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_attribute_statistics_types_response import GetAttributeStatisticsTypesResponse
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    percentage: bool,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/attributes/attributeStatistics/type/{percentage}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[GetAttributeStatisticsTypesResponse, HTTPValidationError]]:
    if response.status_code == 200:
        response_200 = GetAttributeStatisticsTypesResponse.from_dict(response.json())

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
) -> Response[Union[GetAttributeStatisticsTypesResponse, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    percentage: bool,
    *,
    client: AuthenticatedClient,
) -> Response[Union[GetAttributeStatisticsTypesResponse, HTTPValidationError]]:
    """Get attribute statistics

     Get the count/percentage of attributes per category/type.

    args:
        auth: the user's authentification status
        db: the current database
        percentage: percentage request or not

    returns:
        the attributes statistics for one category/type

    Args:
        percentage (bool):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetAttributeStatisticsTypesResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        percentage=percentage,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    percentage: bool,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[GetAttributeStatisticsTypesResponse, HTTPValidationError]]:
    """Get attribute statistics

     Get the count/percentage of attributes per category/type.

    args:
        auth: the user's authentification status
        db: the current database
        percentage: percentage request or not

    returns:
        the attributes statistics for one category/type

    Args:
        percentage (bool):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetAttributeStatisticsTypesResponse, HTTPValidationError]
    """

    return sync_detailed(
        percentage=percentage,
        client=client,
    ).parsed


async def asyncio_detailed(
    percentage: bool,
    *,
    client: AuthenticatedClient,
) -> Response[Union[GetAttributeStatisticsTypesResponse, HTTPValidationError]]:
    """Get attribute statistics

     Get the count/percentage of attributes per category/type.

    args:
        auth: the user's authentification status
        db: the current database
        percentage: percentage request or not

    returns:
        the attributes statistics for one category/type

    Args:
        percentage (bool):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[GetAttributeStatisticsTypesResponse, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        percentage=percentage,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    percentage: bool,
    *,
    client: AuthenticatedClient,
) -> Optional[Union[GetAttributeStatisticsTypesResponse, HTTPValidationError]]:
    """Get attribute statistics

     Get the count/percentage of attributes per category/type.

    args:
        auth: the user's authentification status
        db: the current database
        percentage: percentage request or not

    returns:
        the attributes statistics for one category/type

    Args:
        percentage (bool):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[GetAttributeStatisticsTypesResponse, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            percentage=percentage,
            client=client,
        )
    ).parsed
