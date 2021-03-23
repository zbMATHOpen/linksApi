# ------------------------------------------------------------------------------
# Header + Authentication
# ------------------------------------------------------------------------------

import os
from functools import wraps

from flask import request, url_for
from flask_restx import Api


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = None
        if not "ZBMATH_API_KEY" in os.environ:
            return {
                "message": "Authentication is not implemented on this server. "
                "Configure ZBMATH_API_KEY for write operations."
            }, 501

        if "X-API-KEY" in request.headers:
            token = request.headers["X-API-KEY"]

        if not token:
            return {"message": "Token is missing."}, 401

        if token != os.environ.get("ZBMATH_API_KEY"):
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
    version="0.1.0",
    title="zbMATH Links API",
    description="Links between zbMATH and selected partners API",
    authorizations=authorizations,
)
