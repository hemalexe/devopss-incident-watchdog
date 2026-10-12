"""
AWS Lambda WSGI Adapter for Flask Application
Allows running the Flask app directly inside AWS Lambda with API Gateway or Lambda Function URL.
Zero server cost, instant scaling, 100% AWS Free Tier compatible.
"""

import json
from io import BytesIO
from app.app import app


def lambda_handler(event, context):
    """
    Translates AWS API Gateway / Lambda Function URL event into WSGI format,
    invokes Flask app, and formats HTTP response for AWS.
    """
    # Handle direct event or API Gateway / Function URL event
    http_method = event.get("requestContext", {}).get("http", {}).get("method") or event.get("httpMethod", "GET")
    raw_path = event.get("rawPath") or event.get("path", "/")
    query_string = event.get("rawQueryString", "")

    # Headers
    headers = event.get("headers", {})

    # Body
    body = event.get("body", "")
    if body and event.get("isBase64Encoded", False):
        import base64
        body_bytes = base64.b64decode(body)
    else:
        body_bytes = (body or "").encode("utf-8")

    environ = {
        "REQUEST_METHOD": http_method,
        "PATH_INFO": raw_path,
        "QUERY_STRING": query_string,
        "SERVER_NAME": "lambda",
        "SERVER_PORT": "443",
        "wsgi.version": (1, 0),
        "wsgi.url_scheme": "https",
        "wsgi.input": BytesIO(body_bytes),
        "wsgi.errors": BytesIO(),
        "wsgi.multithread": False,
        "wsgi.multiprocess": False,
        "wsgi.run_once": False,
        "CONTENT_LENGTH": str(len(body_bytes)),
    }

    for key, value in headers.items():
        key_upper = key.upper().replace("-", "_")
        if key_upper in ("CONTENT_TYPE", "CONTENT_LENGTH"):
            environ[key_upper] = value
        else:
            environ[f"HTTP_{key_upper}"] = value

    response_headers = []
    status_code = [200]

    def start_response(status, response_headers_list, exc_info=None):
        status_code[0] = int(status.split(" ")[0])
        response_headers.extend(response_headers_list)

    response_body_iterable = app(environ, start_response)
    response_body = b"".join(response_body_iterable).decode("utf-8")

    header_dict = dict(response_headers)

    return {
        "statusCode": status_code[0],
        "headers": header_dict,
        "body": response_body
    }
