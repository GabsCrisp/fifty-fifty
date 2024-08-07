from flask import session, redirect
from functools import wraps
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

#si hay una sesión activa no puede ir a la página de login o registro
def session_activate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("id"):
            return redirect("/eventos")
        return f(*args, **kwargs)
    return decorated_function

#si hay una sesión activa no puede ir a la página de login o registro
def evento_finalizado(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("evento"):
            return redirect("/eventos")
        return f(*args, **kwargs)
    return decorated_function