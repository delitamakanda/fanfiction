import logging
import time

logger = logging.getLogger("apps.core.requests")


class RequestTimingMiddleware:
    """Log the duration of each request and expose it in ``Server-Timing``."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.perf_counter()
        response = self.get_response(request)
        duration_ms = (time.perf_counter() - start) * 1000
        response["Server-Timing"] = f"app;dur={duration_ms:.1f}"
        logger.debug(
            "%s %s -> %s in %.1f ms",
            request.method,
            request.path,
            response.status_code,
            duration_ms,
        )
        return response
