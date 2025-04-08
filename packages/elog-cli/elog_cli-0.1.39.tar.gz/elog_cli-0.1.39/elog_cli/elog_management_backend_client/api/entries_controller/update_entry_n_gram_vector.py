import datetime
from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.api_result_response_string import ApiResultResponseString
from ...types import Response


def _get_kwargs(
    event_at_start: datetime.datetime,
    event_at_end: datetime.datetime,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": f"/v1/entries/ngram-vector/update/{event_at_start}/{event_at_end}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ApiResultResponseString]:
    if response.status_code == 200:
        response_200 = ApiResultResponseString.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ApiResultResponseString]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    event_at_start: datetime.datetime,
    event_at_end: datetime.datetime,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ApiResultResponseString]:
    """Schedule the update of the ngram vector for all the entries in the data range, the api return the id
    of the job that has been scheduled

    Args:
        event_at_start (datetime.datetime):
        event_at_end (datetime.datetime):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseString]
    """

    kwargs = _get_kwargs(
        event_at_start=event_at_start,
        event_at_end=event_at_end,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    event_at_start: datetime.datetime,
    event_at_end: datetime.datetime,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ApiResultResponseString]:
    """Schedule the update of the ngram vector for all the entries in the data range, the api return the id
    of the job that has been scheduled

    Args:
        event_at_start (datetime.datetime):
        event_at_end (datetime.datetime):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseString
    """

    return sync_detailed(
        event_at_start=event_at_start,
        event_at_end=event_at_end,
        client=client,
    ).parsed


async def asyncio_detailed(
    event_at_start: datetime.datetime,
    event_at_end: datetime.datetime,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ApiResultResponseString]:
    """Schedule the update of the ngram vector for all the entries in the data range, the api return the id
    of the job that has been scheduled

    Args:
        event_at_start (datetime.datetime):
        event_at_end (datetime.datetime):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiResultResponseString]
    """

    kwargs = _get_kwargs(
        event_at_start=event_at_start,
        event_at_end=event_at_end,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    event_at_start: datetime.datetime,
    event_at_end: datetime.datetime,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ApiResultResponseString]:
    """Schedule the update of the ngram vector for all the entries in the data range, the api return the id
    of the job that has been scheduled

    Args:
        event_at_start (datetime.datetime):
        event_at_end (datetime.datetime):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiResultResponseString
    """

    return (
        await asyncio_detailed(
            event_at_start=event_at_start,
            event_at_end=event_at_end,
            client=client,
        )
    ).parsed
