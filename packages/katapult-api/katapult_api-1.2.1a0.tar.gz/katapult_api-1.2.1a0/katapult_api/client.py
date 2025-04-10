import asyncio
import logging.config
from time import time
from typing import Any, Literal, Optional

import aiohttp
from aiohttp.web_exceptions import HTTPException, HTTPTooManyRequests

from .structs import Response

logger = logging.getLogger(__name__)


class Client:
    def __init__(self, base_url: str, api_key: str, concurrent_rate_limit: int) -> None:
        self._base_url = base_url
        self._root_params = {"api_key": api_key}
        self._session: aiohttp.ClientSession | None = None
        self._semaphore = asyncio.Semaphore(value=concurrent_rate_limit)

        self._task_id = 0

    def _clean_params(self, params: dict[str, Any]) -> dict:
        # used to remove none items
        return {k: v for k, v in params.items() if v}

    async def request(
        self,
        method: Literal["GET", "POST", "PUT", "DEL", "PATCH"],
        url: str,
        *,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
        max_retries: int = 1,
    ) -> Response:
        if self._session:
            try:
                if params:
                    params = self._clean_params(params)
                else:
                    params = {}

                # add api key to params (according to the katapult pro docs it gets sent as a query param in each request)
                params.update(self._root_params)

                response = Response(self._task_id, time())
                self._task_id += 1

                logger.debug(f"Task ({response.id:0>6}): {method} {url}")

                async with self._semaphore:
                    try:
                        content, headers, status = await self._request(
                            method=method,
                            url=url,
                            params=params,
                            json=json,
                            max_retries=max_retries,
                        )
                    except HTTPException as exc:
                        if exc.status in [429, 500, 501, 502, 503]:
                            content, headers, status = exc.text, exc.headers, exc.status
                        else:
                            raise exc

                response.end = time()
                response.content = content
                response.url = url
                response.headers = headers
                response.method = method
                response.status = status

                logger.debug(
                    f"Task ({response.id:0>6}): {method} {url.split('?')[0]} returned {status} in {response.end - response.start:.2f}s"
                )

                return response
            except Exception as e:
                logger.critical("Uncaught error!", exc_info=True)
                raise e
        else:
            raise Exception("aiohttp session has not begun!")

    async def _request(
        self,
        method: Literal["GET", "POST", "PUT", "DEL", "PATCH"],
        url: str,
        *,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
        max_retries: int = 1,
    ) -> tuple[str, dict, int]:
        retries = 0

        while retries <= max_retries:
            async with self._session.request(
                method, url, params=params, json=json
            ) as client_response:
                if client_response.status == 429:
                    retries += 1

                    await asyncio.sleep(
                        int(client_response.headers.get("Retry-After", 10))
                    )
                    continue

                content = await client_response.text()

                return (
                    content,
                    dict(client_response.headers),
                    client_response.status,
                )
        raise HTTPTooManyRequests(
            headers=client_response.headers,
            reason=client_response.reason,
            text=await client_response.text(),
            content_type=client_response.content_type,
        )

    async def start_session(self, *args, **kwargs) -> None:
        self._session = aiohttp.ClientSession(*args, **kwargs)

    async def close_session(self):
        if self._session:
            await self._session.close()
            self._session = None
            self._task_id = 0

    async def __aenter__(self, *args, **kwargs) -> "Client":
        await self.start_session(*args, **kwargs)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close_session()

    def __repr__(self):
        return f"{self._base_url},{self._root_params}"
