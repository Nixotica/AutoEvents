import os
import boto3

from lib.lambdas.src.nadeo_event_api.src.environment import (
    EVENT_NAME,
    STORAGE_BUCKET_NAME,
)

s3_client = boto3.client("s3")
s3_resouce = boto3.resource("s3")


def upload_event_id_to_s3(event_id: int) -> None:
    s3_client.put_object(
        Bucket=os.getenv(STORAGE_BUCKET_NAME),
        Key=os.getenv(EVENT_NAME),
        Body=event_id.to_bytes(32, "big"),
    )


def get_latest_event_id_from_s3() -> int:
    bucket = s3_resouce.Bucket(os.getenv(STORAGE_BUCKET_NAME))
    return int.from_bytes(
        bucket.Object(os.getenv(EVENT_NAME)).get()["Body"].read(), "big"
    )
