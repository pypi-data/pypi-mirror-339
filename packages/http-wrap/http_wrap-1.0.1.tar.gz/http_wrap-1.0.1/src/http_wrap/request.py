from collections.abc import AsyncGenerator, Iterable, Mapping
from dataclasses import dataclass, field
from typing import Any, Literal, Optional, Protocol, Union, cast

from src.http_wrap.response import ResponseInterface

httpmethod = Literal["GET", "POST", "PUT", "PATCH", "DELETE", "HEAD"]


@dataclass
class HTTPRequestOptions:
    headers: Optional[Mapping[str, str]] = None
    params: Optional[Mapping[str, str]] = None
    body: Optional[dict[str, Any]] = None
    timeout: Optional[float] = None
    allow_redirects: Optional[bool] = None
    verify_ssl: Optional[bool] = None
    cookies: Optional[Mapping[str, str]] = None

    def __post_init__(self) -> None:
        if self.body is not None and not isinstance(self.body, dict):  # type: ignore # test espera dict
            raise TypeError("body must be a mapping")

        for attr_name in ("headers", "params", "cookies"):
            val = getattr(self, attr_name)
            if val is not None:
                if not isinstance(val, Mapping):
                    raise TypeError(
                        f"{attr_name} must be a mapping, got {type(val).__name__}"
                    )
                val = cast(Mapping[Any, Any], val)
                if not all(isinstance(k, str) for k in val.keys()):
                    raise TypeError(f"All keys in {attr_name} must be strings")

        if self.timeout is not None and self.timeout <= 0:
            raise ValueError("timeout must be a positive number")
        # if self.allow_redirects is not None:
        # warnings.warn("Check if the HTTP method supports 'allow_redirects' (e.g., aiohttp HEAD does not)")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "HTTPRequestOptions":
        """Creates an HTTPRequestOptions instance from a dictionary, validating keys."""
        known_fields = {f.name for f in cls.__dataclass_fields__.values()}
        unknown_keys = set(data) - known_fields
        if unknown_keys:
            raise ValueError(f"Unknown option keys: {unknown_keys}")
        return cls(**data)


@dataclass
class HTTPRequestConfig:
    method: httpmethod
    url: str
    options: HTTPRequestOptions = field(default_factory=HTTPRequestOptions)

    def __post_init__(self) -> None:
        if not isinstance(self.url, str) or not self.url:  # type: ignore
            raise ValueError("url must be a non-empty string")

        if not isinstance(self.options, HTTPRequestOptions):  # type: ignore
            raise TypeError("options must be of type HTTPRequestOptions")

        self.validate()

    def validate(self) -> None:
        method = self.method.upper()
        has_body = method in {"POST", "PUT", "PATCH"}
        has_params = method in {"GET", "DELETE", "HEAD"}

        if has_body and self.options.body is None:
            raise ValueError(f"{method} request requires a body in `options.body`")

        if not has_body and self.options.body is not None:
            raise ValueError(
                f"{method} request does not support a body (use `params` if needed)"
            )

        if has_params and self.options.params is not None:
            if not isinstance(self.options.params, dict):
                raise TypeError(f"{method} request expects params to be a dict")

        if method not in {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD"}:
            raise ValueError(f"Unsupported HTTP method: {method}")


class SyncHTTPRequest(Protocol):
    def request(self, config: HTTPRequestConfig) -> ResponseInterface: ...

    def requests(
        self, configs: list[HTTPRequestConfig], max: int
    ) -> Iterable[ResponseInterface]: ...


class AsyncHTTPRequest(Protocol):
    async def init_session(self) -> None: ...
    async def close_session(self) -> None: ...

    async def request(self, config: HTTPRequestConfig) -> ResponseInterface: ...

    async def requests(
        self, configs: list[HTTPRequestConfig], max: int
    ) -> AsyncGenerator[list[ResponseInterface], None]: ...


HTTPRequest = Union[SyncHTTPRequest, AsyncHTTPRequest]
