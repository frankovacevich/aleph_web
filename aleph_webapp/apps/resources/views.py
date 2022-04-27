from aleph_webapp.common.redirect_to_login import redirect_to_login
from aleph_webapp.apps.main.error_handler import ErrorHandler
from aleph_webapp.response import GenericResponse
from aleph_webapp.common.get_context import get_context
from django.shortcuts import render
from django.conf import settings

APP = getattr(settings, "APP", None)


class ResourceView:

    def __init__(self, resource):
        self.resource = resource()

    def __call__(self, request, **kwargs):

        # Check if user is logged in
        if not request.user.is_authenticated:
            return redirect_to_login(request)

        # Check if user can read
        authorizer = APP.AUTHORIZER
        if not authorizer.user_can_read(request.user.username, self.resource.key):
            return ErrorHandler.make(403)

        # Check format
        if "format" in request.GET:
            response_format = request.GET["format"]
            # if response_format not in self.resource.allowed_formats:
            #     return ErrorHandler.make(400)
        else:
            response_format = "json"

        # Get params
        params = {}
        for param in self.resource.params:
            p = param["name"]
            if p in request.GET:
                params[p] = request.GET[p]
            elif "default" in param:
                params[p] = param["default"]

        params.update(kwargs)

        # Return
        response = self.resource.make(request, **params)

        if response is None:
            raise Exception("Server error: empty response (possibly due to a reading timeout)")

        elif isinstance(response, dict) or isinstance(response, list):
            data = response
            response = GenericResponse(request, self.resource.label, response_format)
            response.add_content(data)
            response = response.make()

        elif isinstance(response, str):
            template = response
            response = render(request, template, get_context(**params))

        return response
