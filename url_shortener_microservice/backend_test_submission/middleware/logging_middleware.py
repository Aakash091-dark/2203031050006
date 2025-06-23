import logging
import time
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class RequestLoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        duration = time.time() - getattr(request, 'start_time', time.time())
        method = request.method
        path = request.get_full_path()
        status = response.status_code
        ip = request.META.get('REMOTE_ADDR')
        log_message = f"{method} {path} {status} {ip} took {duration:.2f}s"
        logger.info(log_message)
        return response
