import traceback
from aleph_webapp.response import GenericResponse
from django.http import JsonResponse
from django.conf import settings

APP = getattr(settings, "APP", None)


# --------------------------------------------------------------------------------------------------------------
# Error Handler
# --------------------------------------------------------------------------------------------------------------
class ErrorHandler:

    @staticmethod
    def make(request, code, message=None):
        error_codes = {
            400: "Bad request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not found",
            405: "Method not allowed",
            408: "Request timeout",
            415: "Unsupported media type",
            500: "Server error",
            501: "Not implemented",
            502: "Bad gateway",
            503: "Service unavailable (overload)",
            504: "Gateway timeout",
        }

        if code == 500:
            print(traceback.format_exc())

        if message is None:
            message = error_codes[code] if code in error_codes else "unkown"

        return JsonResponse({"r": code, "error": message}, status=code)

    @staticmethod
    def do_safely(func):
        def inner(request, *args, **kwargs):
            try:
                return func(request, *args, **kwargs)
            except:
                return ErrorHandler.make(request, 500)

        return inner


# --------------------------------------------------------------------------------------------------------------
# All keys
# --------------------------------------------------------------------------------------------------------------
@ErrorHandler.do_safely
def ApiKeys(request):
    """
    Get a list of all keys available to the user
    """

    authorizer = APP.AUTHORIZER

    # Check if user is authenticated. If not, return 401
    if request.user.is_authenticated:
        username = request.user.username
    elif "token" in request.GET:
        username = authorizer.user_from_token(request.GET["token"])
    elif "token" in request.POST:
        username = authorizer.user_from_token(request.POST["token"])
    else:
        return ErrorHandler.make(request, 401)

    # Return keys available to the user
    if request.method == "GET":
        metadata = {"key1": [{"field": "Field", "description": "Description"}]}

        return JsonResponse(["key1", "key2"], safe=False)

    else:
        return ErrorHandler.make(request, 405)


# --------------------------------------------------------------------------------------------------------------
# Data (collection)
# --------------------------------------------------------------------------------------------------------------
@ErrorHandler.do_safely
def ApiData(request, key):
    """
    Get data using the connections defined in custom.config and return it in the format
    requested by the user. Post (create, update, delete) data.
    """

    authorizer = APP.AUTHORIZER

    # Check if user is authenticated. If not, return 401
    username = None
    if request.user.is_authenticated:
        username = request.user.username
    elif "token" in request.GET:
        username = authorizer.user_from_token(request.GET["token"])
    elif "token" in request.POST:
        username = authorizer.user_from_token(request.POST["token"])
    else:
        ErrorHandler.make(request, 401)

    # GET: Read from connections
    if request.method == "GET":

        # Check if user can read. If not, return 403
        if not authorizer.user_can_read(username, key): return ErrorHandler.make(request, 403)

        # Get response format
        response_format = request.GET["format"] if "format" in request.GET else "json"

        # Get data
        if key in APP.CONNECTIONS:
            conn = APP.CONNECTIONS[key]
        else:
            conn = APP.CONNECTIONS["#"]
        data = conn.safe_read(key, {x: request.GET[x] for x in request.GET})

        # Make response
        response = GenericResponse(request, key, response_format, {})
        response.add_content(data)
        return response.make()

    # POST: Write to connections
    elif request.method == "POST":

        # Check if user can read. If not, return 403
        if not authorizer.user_can_write(username, key):
            return ErrorHandler.make(request, 403, "User can't write to key")

        # Get connection
        if key in APP.CONNECTIONS:
            conn = APP.CONNECTIONS[key]
        else:
            conn = APP.CONNECTIONS["#"]

        # Get data from POST
        if "data" not in request.POST:
            return ErrorHandler.make(request, 400, "Missing data in POST request")

        # Write data
        conn.safe_write(key, request.POST["data"])

        # Return OK response
        return JsonResponse({"r": 200})

    else:
        return ErrorHandler.make(request, 402)


# --------------------------------------------------------------------------------------------------------------
# Record (single record)
# --------------------------------------------------------------------------------------------------------------
@ErrorHandler.do_safely
def ApiRecord(request, key, id_):
    pass

