import asyncio
from collections.abc import AsyncGenerator
from dataclasses import dataclass

import aiohttp

from src.http_wrap.request import (
    AsyncHTTPRequest,
    HTTPRequestConfig,
    HTTPRequestOptions,
)
from src.http_wrap.response import ResponseInterface


@dataclass
class AiohttpResponse(ResponseInterface):
    _code: int
    _text: str
    _content: bytes
    _url: str

    @property
    def status_code(self) -> int:
        return self._code

    @property
    def text(self) -> str:
        return self._text

    @property
    def content(self) -> bytes:
        return self._content

    @property
    def url(self) -> str:
        return self._url


async def make_reponse(resp: aiohttp.ClientResponse) -> ResponseInterface:
    text = await resp.text()
    content = await resp.read()
    return AiohttpResponse(
        _code=resp.status, _text=text, _content=content, _url=str(resp.url)
    )


@dataclass
class AioHttpAdapter(AsyncHTTPRequest):
    session: aiohttp.ClientSession | None = None

    async def init_session(self, verify_ssl: bool = True) -> None:
        if not self.session or self.session.closed:
            connector = aiohttp.TCPConnector(ssl=verify_ssl)
            self.session = aiohttp.ClientSession(connector=connector)

    async def close_session(self) -> None:
        if self.session and not self.session.closed:
            await self.session.close()
            self.session = None

    async def request(self, config: HTTPRequestConfig) -> ResponseInterface:
        method = config.method.lower()
        url = config.url
        opts: HTTPRequestOptions = config.options or HTTPRequestOptions()

        if not self.session or self.session.closed:
            raise Exception("Session is Closed")

        timeout = (
            aiohttp.ClientTimeout(total=opts.timeout)
            if opts.timeout is not None
            else None
        )

        async with self.session.request(
            method,
            url,
            headers=opts.headers,
            params=opts.params,
            json=opts.body,
            timeout=timeout,
            allow_redirects=(
                opts.allow_redirects if opts.allow_redirects is not None else True
            ),
            # verify=opts.verify_ssl if opts.verify_ssl is not None else True,
            cookies=dict(opts.cookies) if opts.cookies else None,
        ) as resp:
            return await make_reponse(resp)

    async def requests(
        self, configs: list[HTTPRequestConfig], max: int
    ) -> AsyncGenerator[list[ResponseInterface], None]:  # type: ignore
        for i in range(0, len(configs), max):
            chunk = configs[i : i + max]
            tasks = [self.request(cfg) for cfg in chunk]
            results = await asyncio.gather(*tasks)
            yield results
