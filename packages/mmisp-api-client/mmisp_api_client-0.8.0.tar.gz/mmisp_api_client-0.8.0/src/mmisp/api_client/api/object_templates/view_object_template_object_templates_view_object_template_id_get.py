from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.resp_object_template_view import RespObjectTemplateView
from ...types import Response


def _get_kwargs(
    object_template_id: Union[UUID, int],
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/object_templates/view/{object_template_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[HTTPValidationError, RespObjectTemplateView]]:
    if response.status_code == 200:
        response_200 = RespObjectTemplateView.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, RespObjectTemplateView]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    object_template_id: Union[UUID, int],
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, RespObjectTemplateView]]:
    """View Object Template

     Retrieve all information about a given object template.

    Args:
      auth: The api authentication object
      db: The database session
      object_template_id: The ID of the object template information shall be retrieved

    Returns:
      All information about the object template

    Args:
        object_template_id (Union[UUID, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, RespObjectTemplateView]]
    """

    kwargs = _get_kwargs(
        object_template_id=object_template_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    object_template_id: Union[UUID, int],
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, RespObjectTemplateView]]:
    """View Object Template

     Retrieve all information about a given object template.

    Args:
      auth: The api authentication object
      db: The database session
      object_template_id: The ID of the object template information shall be retrieved

    Returns:
      All information about the object template

    Args:
        object_template_id (Union[UUID, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, RespObjectTemplateView]
    """

    return sync_detailed(
        object_template_id=object_template_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    object_template_id: Union[UUID, int],
    *,
    client: AuthenticatedClient,
) -> Response[Union[HTTPValidationError, RespObjectTemplateView]]:
    """View Object Template

     Retrieve all information about a given object template.

    Args:
      auth: The api authentication object
      db: The database session
      object_template_id: The ID of the object template information shall be retrieved

    Returns:
      All information about the object template

    Args:
        object_template_id (Union[UUID, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, RespObjectTemplateView]]
    """

    kwargs = _get_kwargs(
        object_template_id=object_template_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    object_template_id: Union[UUID, int],
    *,
    client: AuthenticatedClient,
) -> Optional[Union[HTTPValidationError, RespObjectTemplateView]]:
    """View Object Template

     Retrieve all information about a given object template.

    Args:
      auth: The api authentication object
      db: The database session
      object_template_id: The ID of the object template information shall be retrieved

    Returns:
      All information about the object template

    Args:
        object_template_id (Union[UUID, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, RespObjectTemplateView]
    """

    return (
        await asyncio_detailed(
            object_template_id=object_template_id,
            client=client,
        )
    ).parsed
