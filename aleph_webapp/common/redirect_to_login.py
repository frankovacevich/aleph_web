from django.shortcuts import redirect
from urllib.parse import quote, unquote


def redirect_to_login(request):
    return redirect('/login?after=' + quote(request.get_full_path(), safe=""))


def redirect_to_after(request):
    if "after" in request.GET:
        return redirect(unquote(request.GET["after"]))
    else:
        return redirect("/")
