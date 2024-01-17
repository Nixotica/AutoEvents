import json
import os
import boto3

from nadeo_event_api.environment import (
    EVENT_NAME,
    STORAGE_BUCKET_NAME,
    SECRETS_BUCKET_NAME,
)

from nadeo_event_api.constants import (
    SECRET_FILE,
    SECRET_UBI_AUTH,
)

s3_client = boto3.client("s3")
s3_resource = boto3.resource("s3")


def get_ubi_auth_from_secrets() -> str:
    """
    Accesses the encrypted secrets bucket to get the ubi auth string (not authorization token,
    you still need to call authenticate function with this string)

    :returns: Ubi Auth
    """
    json_content = (
        s3_client.get_object(Bucket=os.getenv(SECRETS_BUCKET_NAME), Key=SECRET_FILE)[
            "Body"
        ]
        .read()
        .decode("utf-8")
    )
    return json.loads(json_content)[SECRET_UBI_AUTH]


def upload_event_id_to_s3(event_id: int) -> None:
    s3_client.put_object(
        Bucket=os.getenv(STORAGE_BUCKET_NAME),
        Key=os.getenv(EVENT_NAME),
        Body=event_id.to_bytes(32, "big"),
    )


def get_latest_event_id_from_s3() -> int:
    bucket = s3_resource.Bucket(os.getenv(STORAGE_BUCKET_NAME))
    return int.from_bytes(
        bucket.Object(os.getenv(EVENT_NAME)).get()["Body"].read(), "big"
    )
