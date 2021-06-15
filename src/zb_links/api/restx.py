# ------------------------------------------------------------------------------
# Header + Authentication
# ------------------------------------------------------------------------------

from functools import wraps

from flask import current_app, request, url_for
from flask_restx import Api


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        api_key = current_app.config["ZBMATH_API_KEY"]
        if api_key is None:
            return {
                "message": "Authentication is not implemented on this server. "
                "Configure ZBMATH_API_KEY for write operations."
            }, 501

        if "X-API-KEY" not in request.headers:
            return {"message": "Token is missing."}, 401
        token = request.headers["X-API-KEY"]

        if token != api_key:
            return {"message": "Token is wrong."}, 401

        return f(*args, **kwargs)

    return decorated


authorizations = {
    "apikey": {"type": "apiKey", "in": "header", "name": "X-API-KEY"}
}


# Fix for mixed content when deployed on https. Will be removed when resolved.
# https://github.com/python-restx/flask-restx/issues/188
class PatchedApi(Api):
    @property
    def specs_url(self):
        return url_for(self.endpoint("specs"))


api = PatchedApi(
    version="0.2.0",
    title="zbMATH Links API",
    description="Links between zbMATH and selected partners API",
    authorizations=authorizations,
)
