import datetime
import hashlib
import hmac
import urllib
from typing import Any

import boto3


def sign(key: bytes, msg: str):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def get_signature_key(key: str, date_stamp: str, region_name: str, service_name: str):
    date = sign(("AWS4" + key).encode("utf-8"), date_stamp)
    region = sign(date, region_name)
    service = sign(region, service_name)
    signed = sign(service, "aws4_request")
    return signed


def aws_sig_v4_headers(
    session: boto3.Session,
    service: str,
    url: str,
    method: str,
    headers: dict[str, Any] = None,
    query: list[tuple[str, str]] = None,
    payload: str = None,
):
    if not headers:
        headers = {}
    parsed_url = urllib.parse.urlparse(url)
    t = datetime.datetime.utcnow()
    amz_date = t.strftime("%Y%m%dT%H%M%SZ")
    date_stamp = t.strftime("%Y%m%d")
    credentials = session.get_credentials()

    canonical_uri = parsed_url.path
    if not canonical_uri:
        canonical_uri = "/"
    canonical_querystring = ""
    if query:
        canonical_querystring = "&".join(
            [f"{query_[0]}={query_[1]}" for query_ in query]
        )
    canonical_headers = (
        f"content-type:{headers.get('Content-Type', 'application/json')}\n"
        f"host:{parsed_url.hostname}\n"
        f"x-amz-date:{amz_date}\n"
    )
    signed_headers = "content-type;host;x-amz-date"
    if payload is None:
        payload_hash = hashlib.sha256(b"").hexdigest()
    else:
        payload_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()

    canonical_request = "\n".join(
        [
            method,
            canonical_uri,
            canonical_querystring,
            canonical_headers,
            signed_headers,
            payload_hash,
        ]
    )

    algorithm = "AWS4-HMAC-SHA256"
    credential_scope = f"{date_stamp}/{session.region_name}/{service}/aws4_request"
    string_to_sign = "\n".join(
        [
            algorithm,
            amz_date,
            credential_scope,
            hashlib.sha256(canonical_request.encode("utf-8")).hexdigest(),
        ]
    )

    signing_key = get_signature_key(
        credentials.secret_key, date_stamp, session.region_name, service
    )
    signature = hmac.new(
        signing_key, (string_to_sign).encode("utf-8"), hashlib.sha256
    ).hexdigest()
    authorization_header = (
        f"{algorithm} Credential={credentials.access_key}/"
        f"{credential_scope}, SignedHeaders={signed_headers}, "
        f"Signature={signature}"
    )

    return {
        **headers,
        "x-amz-security-token": credentials.token,
        "X-Amz-Date": amz_date,
        "Authorization": authorization_header,
    }
