import secrets
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import BinaryIO, Optional

import boto3
from botocore.client import Config
from django.conf import settings

@dataclass
class S3UploadResult:
    url: str
    key: str

class S3Uploader:
    """환경 변수 설정을 기반으로 파일을 S3에 업로드한다."""

    def __init__(self) -> None:
        bucket = getattr(settings, "AWS_S3_UPLOAD_BUCKET", None)
        if not bucket:
            raise RuntimeError("AWS_S3_UPLOAD_BUCKET 설정이 필요합니다.")
        self.bucket_name = bucket
        self.region = getattr(settings, "AWS_S3_UPLOAD_REGION", None)
        self.prefix = getattr(settings, "AWS_S3_UPLOAD_PREFIX", "search_uploads")
        self.acl = getattr(settings, "AWS_S3_UPLOAD_ACL", "private")
        session = boto3.session.Session(
            aws_access_key_id=getattr(settings, "AWS_ACCESS_KEY_ID", None),
            aws_secret_access_key=getattr(settings, "AWS_SECRET_ACCESS_KEY", None),
            aws_session_token=getattr(settings, "AWS_SESSION_TOKEN", None),
            region_name=self.region,
        )
        config = Config(region_name=self.region) if self.region else None
        self.client = session.client("s3", config=config)

    def upload(self, file_obj: BinaryIO, filename: str, content_type: Optional[str] = None) -> S3UploadResult:
        key = self._build_key(filename)
        extra_args = {"ACL": self.acl}
        if content_type:
            extra_args["ContentType"] = content_type
        self.client.upload_fileobj(file_obj, self.bucket_name, key, ExtraArgs=extra_args)
        url = self._build_url(key)
        return S3UploadResult(url=url, key=key)

    def _build_key(self, filename: str) -> str:
        sanitized_prefix = self.prefix.strip("/")
        prefix = f"{sanitized_prefix}/" if sanitized_prefix else ""
        unique_part = self._generate_unique_id()
        return f"{prefix}{unique_part}-{filename}"

    def _generate_unique_id(self) -> str:
        """숫자형(정수 문자열)으로 된 고유 값을 생성한다."""
        epoch_ms = int(datetime.now(timezone.utc).timestamp() * 1000)
        random_suffix = secrets.randbelow(1_000_000)
        return f"{epoch_ms}{random_suffix:06d}"

    def _build_url(self, key: str) -> str:
        base_url = getattr(settings, "AWS_S3_UPLOAD_BASE_URL", None)
        if base_url:
            return f"{base_url.rstrip('/')}/{key}"
        region_part = f".{self.region}" if self.region else ""
        return f"https://{self.bucket_name}.s3{region_part}.amazonaws.com/{key}"
