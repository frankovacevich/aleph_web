import traceback
from django.shortcuts import render


class ErrorHandler:
    # HTTP Error codes:
    # 401 Unauthorized
    # 403 Forbidden
    # 404 Not found
    # 500 Server error

    def __init__(self, code, message=None):
        self.code = code
        self.on_error = None
        self.message = message

    def __call__(self, request, *args, **kwds):
        traceback_ = traceback.format_exc()
        context = {"error_code": self.code, "error_traceback": traceback_, "message": self.message}
        return render(request, 'main/error.html', status=self.code, context=context)

    @staticmethod
    def make(request, code, message=None):
        err = ErrorHandler(code)
        return err(request)

    @staticmethod
    def do_safely(func):
        def inner(request, *args, **kwargs):
            try:
                return func(request, *args, **kwargs)
            except:
                return ErrorHandler.make(request, 500)
        return inner
