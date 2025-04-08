import logging

from django.contrib import auth
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger()


class AuthenticateSessionMiddleware(MiddlewareMixin):

    def process_request(self, request):
        logger.info(request.path_info.lower())
        if (hasattr(request, 'user') and request.user.is_authenticated) or \
                not request.path_info.lower().startswith("/admin"):
            return
        user = auth.authenticate(request)
        if hasattr(user, 'backend'):
            request._cached_user = user
            auth.login(
                request, user, user.backend)
