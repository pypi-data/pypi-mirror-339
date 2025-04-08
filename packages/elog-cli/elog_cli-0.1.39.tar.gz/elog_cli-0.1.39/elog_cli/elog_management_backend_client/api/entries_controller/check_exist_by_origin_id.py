from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_result_response_boolean import ApiResultResponseBoolean
from ...types import Response


def _get_kwargs(
    origin_id: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/v1/entries/exists/by/originId/{origin_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ApiResultResponseBoolean]:
    if response.status_code == 200:
        response_200 = ApiResultResponseBoolean.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ApiResultResponseBoolean]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    origin_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ApiResultResponseBoolean]:
    """Check if an entry with the origin id exist

    Args:
        origin_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseBoolean]
    """

    kwargs = _get_kwargs(
        origin_id=origin_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    origin_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ApiResultResponseBoolean]:
    """Check if an entry with the origin id exist

    Args:
        origin_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseBoolean
    """

    return sync_detailed(
        origin_id=origin_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    origin_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ApiResultResponseBoolean]:
    """Check if an entry with the origin id exist

    Args:
        origin_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseBoolean]
    """

    kwargs = _get_kwargs(
        origin_id=origin_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    origin_id: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ApiResultResponseBoolean]:
    """Check if an entry with the origin id exist

    Args:
        origin_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseBoolean
    """

    return (
        await asyncio_detailed(
            origin_id=origin_id,
            client=client,
        )
    ).parsed
