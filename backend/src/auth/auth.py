import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = 'eccweizhi-fsnd.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'myFoobar'


class AuthError(Exception):
    """
    AuthError Exception
    A standardized way to communicate auth failure modes
    """

    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    :return: token part of header
    """
    if not request.headers:
        raise AuthError({
            "code": "missing_header",
            "description": "No header is present",
        }, 400)
    elif "Authorization" not in request.headers:
        raise AuthError({
            "code": "invalid_header",
            "description": "Authorization information not provided",
        }, 401)

    auth_header = request.headers["Authorization"]
    authorization_parts = auth_header.split(" ")

    if len(authorization_parts) != 2:
        raise AuthError({
            "code": "invalid_header",
            "description": "Authorization malformed",
        }, 401)
    elif authorization_parts[0].lower() != "bearer":
        raise AuthError({
            "code": "invalid_header",
            "description": "Authorization malformed",
        }, 401)

    return authorization_parts[1]


def check_permissions(permission, payload):
    """
    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
    :param permission: string permission (i.e. 'post:drink')
    :param payload: decoded jwt payload
    :return: true if no error is raised
    """
    if not payload:
        raise AuthError({
            "code": "token_malformed",
            "description": "Payload is missing",
        }, 401)
    elif "permissions" not in payload:
        raise AuthError({
            "code": "token_malformed",
            "description": "Permissions information missing from payload",
        }, 401)

    token_permissions = payload["permissions"]
    if permission not in token_permissions:
        raise AuthError({
            "code": "unauthorized",
            "description": f"Token lack permission: {permission}",
        }, 401)

    return True


def verify_decode_jwt(token):
    """
    @TODO implement verify_decode_jwt(token) method

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the

    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
    :param token: a json web token (string)
    :return: decoded payload
    """
    raise Exception('Not Implemented')


def requires_auth(permission=''):
    """
    @TODO implement @requires_auth(permission) decorator method
    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission

    :param permission: string permission (i.e. 'post:drink')
    :return: the decorator which passes the decoded payload to the decorated method
    """

    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
