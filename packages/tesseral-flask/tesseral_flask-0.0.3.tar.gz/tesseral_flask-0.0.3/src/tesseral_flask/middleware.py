from typing import Optional

from flask import Request, request, g
from flask.typing import BeforeRequestCallable
from httpx import Client
from tesseral.access_tokens import AccessTokenAuthenticator

from tesseral_flask.context import _AuthContext


def require_auth(
    *,
    publishable_key: str,
    config_api_hostname: str = "config.tesseral.com",
    jwks_refresh_interval_seconds: int = 3600,
    http_client: Optional[Client] = None,
) -> BeforeRequestCallable:
    authenticator = AccessTokenAuthenticator(
        publishable_key=publishable_key,
        config_api_hostname=config_api_hostname,
        jwks_refresh_interval_seconds=jwks_refresh_interval_seconds,
        http_client=http_client,
    )

    def before_request_require_auth():
        project_id = authenticator.project_id()
        access_token = _access_token(request, project_id)

        try:
            access_token_claims = authenticator.authenticate_access_token(
                access_token=access_token
            )
        except:  # noqa: E722
            return "Unauthorized", 401

        auth_context = _AuthContext()
        auth_context.access_token = access_token
        auth_context.access_token_claims = access_token_claims
        g._tesseral_auth = auth_context

    return before_request_require_auth


_PREFIX_BEARER = "Bearer "


def _access_token(request: Request, project_id: str) -> str:
    auth_header = request.headers.get("authorization")
    if auth_header and auth_header.startswith(_PREFIX_BEARER):
        return auth_header[len(_PREFIX_BEARER) :]

    cookie_name = f"tesseral_{project_id}_access_token"
    if cookie_name in request.cookies:
        return request.cookies[cookie_name]

    return ""
