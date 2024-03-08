# TODO - use this in a decorator directly on the routes
from src.utils.logging_config import log


def extract_bearer_token(request):
    authorization_header = request.headers.get('Authorization')

    out = None
    if authorization_header and authorization_header.startswith('Bearer '):
        # Extract the token by removing the 'Bearer ' prefix
        bearer_token = authorization_header[len('Bearer '):]

        # Now 'bearer_token' contains the Bearer token
        log.debug(f"Bearer Token: {bearer_token}")
        out = bearer_token
    else:
        log.error("No Bearer token found in the Authorization header")

    return out