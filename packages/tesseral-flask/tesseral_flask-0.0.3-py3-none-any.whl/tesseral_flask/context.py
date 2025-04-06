from tesseral import AccessTokenClaims
from flask import g


class _AuthContext:
    access_token: str
    access_token_claims: AccessTokenClaims


def _extract_auth_context(name: str) -> _AuthContext:
    try:
        return g._tesseral_auth
    except Exception as e:
        raise RuntimeError(
            f"Called {name}() outside of an authenticated request. Did you forget to use RequireAuthMiddleware?"
        ) from e


def organization_id() -> str:
    return _extract_auth_context("organization_id").access_token_claims.organization.id  # type: ignore[union-attr,return-value]


def access_token_claims() -> AccessTokenClaims:
    return _extract_auth_context("access_token_claims").access_token_claims


def credentials() -> str:
    return _extract_auth_context("credentials").access_token
