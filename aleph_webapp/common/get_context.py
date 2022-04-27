from django.conf import settings
APP = getattr(settings, "APP", None)


def get_context(**kwargs):
    my_context = APP.GLOBALS
    for k in kwargs:
        my_context[k] = kwargs[k]

    return my_context
