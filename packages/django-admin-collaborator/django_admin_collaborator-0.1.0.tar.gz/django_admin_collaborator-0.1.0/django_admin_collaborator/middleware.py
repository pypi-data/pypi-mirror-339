"""Middleware for Django Admin Collaborator."""

from django.http import HttpRequest
from django.utils.deprecation import MiddlewareMixin


class AdminCollaboratorMiddleware(MiddlewareMixin):
    """
    Middleware for Django Admin Collaborator.

    This middleware is not required, but can be used to perform
    additional customization for the collaborative admin editing experience.

    Currently, it's mainly a placeholder for future enhancements.
    """

    def process_request(self, request: HttpRequest) -> None:
        """
        Process the incoming request.

        Args:
            request: The incoming HTTP request
        """
        pass