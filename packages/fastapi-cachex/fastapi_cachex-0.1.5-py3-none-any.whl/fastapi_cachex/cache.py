import hashlib
import inspect
from collections.abc import Awaitable
from collections.abc import Callable
from functools import update_wrapper
from functools import wraps
from inspect import Parameter
from inspect import Signature
from typing import TYPE_CHECKING
from typing import Any
from typing import Literal
from typing import Optional
from typing import TypeVar
from typing import Union

from fastapi import Request
from fastapi import Response
from fastapi.datastructures import DefaultPlaceholder
from starlette.status import HTTP_304_NOT_MODIFIED

from fastapi_cachex.backends import MemoryBackend
from fastapi_cachex.directives import DirectiveType
from fastapi_cachex.exceptions import BackendNotFoundError
from fastapi_cachex.exceptions import CacheXError
from fastapi_cachex.exceptions import RequestNotFoundError
from fastapi_cachex.proxy import BackendProxy
from fastapi_cachex.types import ETagContent

if TYPE_CHECKING:
    from fastapi.routing import APIRoute

T = TypeVar("T", bound=Response)
AsyncCallable = Callable[..., Awaitable[T]]
SyncCallable = Callable[..., T]
AnyCallable = Union[AsyncCallable[T], SyncCallable[T]]  # noqa: UP007


class CacheControl:
    def __init__(self) -> None:
        self.directives: list[str] = []

    def add(self, directive: DirectiveType, value: Optional[int] = None) -> None:
        if value is not None:
            self.directives.append(f"{directive.value}={value}")
        else:
            self.directives.append(directive.value)

    def __str__(self) -> str:
        return ", ".join(self.directives)


async def get_response(
    __func: AnyCallable[Response], __request: Request, *args: Any, **kwargs: Any
) -> Response:
    """Get the response from the function."""
    if inspect.iscoroutinefunction(__func):
        result = await __func(*args, **kwargs)
    else:
        result = __func(*args, **kwargs)

    # If already a Response object, return it directly
    if isinstance(result, Response):
        return result

    # Get response_class from route if available
    route: APIRoute | None = __request.scope.get("route")
    if route is None:  # pragma: no cover
        raise CacheXError("Route not found in request scope")

    if isinstance(route.response_class, DefaultPlaceholder):
        response_class: type[Response] = route.response_class.value

    else:
        response_class = route.response_class

    # Convert non-Response result to Response using appropriate response_class
    return response_class(content=result)


def cache(  # noqa: C901
    ttl: Optional[int] = None,
    stale_ttl: Optional[int] = None,
    stale: Literal["error", "revalidate"] | None = None,
    no_cache: bool = False,
    no_store: bool = False,
    public: bool = False,
    private: bool = False,
    immutable: bool = False,
    must_revalidate: bool = False,
) -> Callable[[AnyCallable[Response]], AsyncCallable[Response]]:
    def decorator(func: AnyCallable[Response]) -> AsyncCallable[Response]:  # noqa: C901
        try:
            cache_backend = BackendProxy.get_backend()
        except BackendNotFoundError:
            # Fallback to memory backend if no backend is set
            cache_backend = MemoryBackend()
            BackendProxy.set_backend(cache_backend)

        # Analyze the original function's signature
        sig: Signature = inspect.signature(func)
        params: list[Parameter] = list(sig.parameters.values())

        # Check if Request is already in the parameters
        found_request: Parameter | None = next(
            (param for param in params if param.annotation == Request), None
        )

        # Add Request parameter if it's not present
        if not found_request:
            request_name: str = "__cachex_request"

            request_param = inspect.Parameter(
                request_name,
                inspect.Parameter.KEYWORD_ONLY,
                annotation=Request,
            )

            sig = sig.replace(parameters=[*params, request_param])

        else:
            request_name = found_request.name

        async def get_cache_control(cache_control: CacheControl) -> str:  # noqa: C901
            # Set Cache-Control headers
            if no_cache:
                cache_control.add(DirectiveType.NO_CACHE)
                if must_revalidate:
                    cache_control.add(DirectiveType.MUST_REVALIDATE)
            else:
                # Handle normal cache control cases
                # 1. Access scope (public/private)
                if public:
                    cache_control.add(DirectiveType.PUBLIC)
                elif private:
                    cache_control.add(DirectiveType.PRIVATE)

                # 2. Cache time settings
                if ttl is not None:
                    cache_control.add(DirectiveType.MAX_AGE, ttl)

                # 3. Validation related
                if must_revalidate:
                    cache_control.add(DirectiveType.MUST_REVALIDATE)

                # 4. Stale response handling
                if stale is not None and stale_ttl is None:
                    raise CacheXError("stale_ttl must be set if stale is used")

                if stale == "revalidate":
                    cache_control.add(DirectiveType.STALE_WHILE_REVALIDATE, stale_ttl)
                elif stale == "error":
                    cache_control.add(DirectiveType.STALE_IF_ERROR, stale_ttl)

                # 5. Special flags
                if immutable:
                    cache_control.add(DirectiveType.IMMUTABLE)

            return str(cache_control)

        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Response:  # noqa: C901
            if found_request:
                req: Request | None = kwargs.get(request_name)
            else:
                req = kwargs.pop(request_name, None)

            if not req:  # pragma: no cover
                # Skip coverage for this case, as it should not happen
                raise RequestNotFoundError()

            # Only cache GET requests
            if req.method != "GET":
                return await get_response(func, req, *args, **kwargs)

            # Generate cache key and prepare headers
            cache_key = f"{req.url.path}:{req.query_params}"
            client_etag = req.headers.get("if-none-match")
            cache_control = await get_cache_control(CacheControl())

            # Handle special case: no-store (highest priority)
            if no_store:
                response = await get_response(func, req, *args, **kwargs)
                cc = CacheControl()
                cc.add(DirectiveType.NO_STORE)
                response.headers["Cache-Control"] = str(cc)
                return response

            # Check cache and handle ETag validation
            cached_data = await cache_backend.get(cache_key)

            current_response = None
            current_etag = None

            if client_etag:
                if no_cache:
                    # Get fresh response first if using no-cache
                    current_response = await get_response(func, req, *args, **kwargs)
                    current_etag = (
                        f'W/"{hashlib.md5(current_response.body).hexdigest()}"'  # noqa: S324
                    )

                    if client_etag == current_etag:
                        # For no-cache, compare fresh data with client's ETag
                        return Response(
                            status_code=HTTP_304_NOT_MODIFIED,
                            headers={
                                "ETag": current_etag,
                                "Cache-Control": cache_control,
                            },
                        )

                # Compare with cached ETag
                elif (
                    cached_data and client_etag == cached_data.etag
                ):  # pragma: no branch
                    return Response(
                        status_code=HTTP_304_NOT_MODIFIED,
                        headers={
                            "ETag": cached_data.etag,
                            "Cache-Control": cache_control,
                        },
                    )

            if not current_response or not current_etag:
                # Retrieve the current response if not already done
                current_response = await get_response(func, req, *args, **kwargs)
                current_etag = f'W/"{hashlib.md5(current_response.body).hexdigest()}"'  # noqa: S324

            # Set ETag header
            current_response.headers["ETag"] = current_etag

            # Update cache if needed
            if not cached_data or cached_data.etag != current_etag:
                # Store in cache if data changed
                await cache_backend.set(
                    cache_key, ETagContent(current_etag, current_response.body), ttl=ttl
                )

            current_response.headers["Cache-Control"] = cache_control
            return current_response

        # Update the wrapper with the new signature
        update_wrapper(wrapper, func)
        wrapper.__signature__ = sig  # type: ignore

        return wrapper

    return decorator
