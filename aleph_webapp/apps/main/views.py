from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from aleph_webapp.common.redirect_to_login import redirect_to_login, redirect_to_after
from aleph_webapp.common.get_context import get_context
from django.conf import settings
from .error_handler import ErrorHandler

APP = getattr(settings, "APP", None)


# =======================================================================================================
# Home
# =======================================================================================================
def Home(request):
    if not request.user.is_authenticated: return redirect_to_login(request)
    authorizer = APP.AUTHORIZER

    G = []
    R = []
    for r in APP.RESOURCES:
        if not authorizer.user_can_read(request.user.username, r.key): continue
        if r.group not in G: G.append(r.group)
        R.append(r)

    # G.sort()

    return render(request, "main/home.html", get_context(resources=R, groups=G))


# =======================================================================================================
# Login
# =======================================================================================================
def Login(request):
    # Check if user is logged in
    if request.user.is_authenticated: return redirect(Home)

    # POST: log in user
    if request.method == "POST":

        # Check if request has credentials
        if "username" not in request.POST or "password" not in request.POST:
            return render(request, 'main/login.html', get_context())

        # Authenticate
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if user is None:
            msg = "Incorrect username or password"
            return render(request, 'main/login.html', get_context(msg=msg))

        login(request, user)

        # Get namespace token
        authorizer = APP.AUTHORIZER
        token = authorizer.token_get(user.username)

        # Return response
        response = redirect_to_after(request)
        session_duration = APP.SUPER_SESSION_DURATION if user.is_superuser else APP.SESSION_DURATION
        response.set_cookie("nstoken", token, max_age=session_duration)
        request.session.set_expiry(session_duration)
        return response

    # GET: return login page
    elif request.method == "GET":
        return render(request, 'main/login.html', get_context())

    return ErrorHandler.make(405)


# =======================================================================================================
# Logout
# =======================================================================================================
def Logout(request):
    # Check that method is GET and user is logged in
    if not request.user.is_authenticated: redirect(Login)

    # Logout and delete cookies
    logout(request)
    response = redirect(Login)
    response.delete_cookie("nstoken")
    return response


# =======================================================================================================
# Password Change
# =======================================================================================================
def ChangePassword(request):
    # Check if user is logged in
    if not request.user.is_authenticated: return redirect_to_login(request)

    # POST: check form and redirect to login if ok
    if request.method == "POST":

        if "password" not in request.POST or "new_password" not in request.POST:
            msg = ""

        else:
            user = authenticate(username=request.user.username, password=request.POST["password"])
            if user is None:
                msg = "Incorrect password"
            else:
                msg = "Password changed"
                user.set_password(request.POST["new_password"])
                user.save()
                login(request, user)

    # GET: return form
    elif request.method == "GET":
        msg = ""

    return render(request, 'main/pwchange.html', get_context(msg=msg))
