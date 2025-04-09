import logging
from datetime import timedelta
from typing import override

from minio import Minio
from minio.error import S3Error

from archipy.adapters.minio.ports import MinioBucketType, MinioObjectType, MinioPolicyType, MinioPort
from archipy.configs.base_config import BaseConfig
from archipy.configs.config_template import MinioConfig
from archipy.helpers.decorators.cache import ttl_cache_decorator
from archipy.models.errors import (
    AlreadyExistsError,
    InternalError,
    InvalidArgumentError,
    NotFoundError,
    PermissionDeniedError,
)

logger = logging.getLogger(__name__)


class MinioAdapter(MinioPort):
    """Concrete implementation of the MinioPort interface using the minio library."""

    def __init__(self, minio_configs: MinioConfig | None = None) -> None:
        """Initialize MinioAdapter with configuration.

        Args:
            minio_configs: Optional MinIO configuration. If None, global config is used.
        """
        self.configs: MinioConfig = BaseConfig.global_config().MINIO if minio_configs is None else minio_configs
        self.client = Minio(
            self.configs.ENDPOINT,
            access_key=self.configs.ACCESS_KEY,
            secret_key=self.configs.SECRET_KEY,
            session_token=self.configs.SESSION_TOKEN,
            secure=self.configs.SECURE,
            region=self.configs.REGION,
        )

    def clear_all_caches(self) -> None:
        """Clear all cached values."""
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if hasattr(attr, "clear_cache"):
                attr.clear_cache()

    @override
    @ttl_cache_decorator(ttl_seconds=300, maxsize=100)  # Cache for 5 minutes
    def bucket_exists(self, bucket_name: str) -> bool:
        """Check if a bucket exists."""
        try:
            if not bucket_name:
                raise InvalidArgumentError(argument_name="bucket_name")
            return self.client.bucket_exists(bucket_name)
        except S3Error as e:
            logger.error(f"Failed to check bucket existence: {e}")
            if "NoSuchBucket" in str(e):
                return False
            raise InternalError(details=f"Failed to check bucket existence: {e}")

    @override
    def make_bucket(self, bucket_name: str) -> None:
        """Create a new bucket."""
        try:
            if not bucket_name:
                raise InvalidArgumentError(argument_name="bucket_name")
            self.client.make_bucket(bucket_name)
            self.clear_all_caches()  # Clear cache since bucket list changed
        except S3Error as e:
            logger.error(f"Failed to create bucket: {e}")
            if "BucketAlreadyOwnedByYou" in str(e) or "BucketAlreadyExists" in str(e):
                raise AlreadyExistsError(resource_type="bucket")
            if "AccessDenied" in str(e):
                raise PermissionDeniedError()
            raise InternalError(details=f"Failed to create bucket: {e}")

    @override
    def remove_bucket(self, bucket_name: str) -> None:
        """Remove a bucket."""
        try:
            if not bucket_name:
                raise InvalidArgumentError(argument_name="bucket_name")
            self.client.remove_bucket(bucket_name)
            self.clear_all_caches()  # Clear cache since bucket list changed
        except S3Error as e:
            logger.error(f"Failed to remove bucket: {e}")
            if "NoSuchBucket" in str(e):
                raise NotFoundError(resource_type="bucket")
            if "AccessDenied" in str(e):
                raise PermissionDeniedError()
            raise InternalError(details=f"Failed to remove bucket: {e}")

    @override
    @ttl_cache_decorator(ttl_seconds=300, maxsize=1)  # Cache for 5 minutes
    def list_buckets(self) -> list[MinioBucketType]:
        """List all buckets."""
        try:
            buckets = self.client.list_buckets()
            return [{"name": b.name, "creation_date": b.creation_date} for b in buckets]
        except S3Error as e:
            logger.error(f"Failed to list buckets: {e}")
            if "AccessDenied" in str(e):
                raise PermissionDeniedError()
            raise InternalError(details=f"Failed to list buckets: {e}")

    @override
    def put_object(self, bucket_name: str, object_name: str, file_path: str) -> None:
        """Upload a file to a bucket."""
        try:
            if not bucket_name or not object_name or not file_path:
                raise InvalidArgumentError(
                    argument_name=(
                        "bucket_name, object_name or file_path"
                        if not all([bucket_name, object_name, file_path])
                        else "bucket_name" if not bucket_name else "object_name" if not object_name else "file_path"
                    ),
                )
            self.client.fput_object(bucket_name, object_name, file_path)
            if hasattr(self.list_objects, "clear_cache"):
                self.list_objects.clear_cache()  # Clear object list cache
        except S3Error as e:
            logger.error(f"Failed to upload object: {e}")
            if "NoSuchBucket" in str(e):
                raise NotFoundError(resource_type="bucket")
            if "AccessDenied" in str(e):
                raise PermissionDeniedError()
            raise InternalError(details=f"Failed to upload object: {e}")

    @override
    def get_object(self, bucket_name: str, object_name: str, file_path: str) -> None:
        """Download an object to a file."""
        try:
            if not bucket_name or not object_name or not file_path:
                raise InvalidArgumentError(
                    argument_name=(
                        "bucket_name, object_name or file_path"
                        if not all([bucket_name, object_name, file_path])
                        else "bucket_name" if not bucket_name else "object_name" if not object_name else "file_path"
                    ),
                )
            self.client.fget_object(bucket_name, object_name, file_path)
        except S3Error as e:
            logger.error(f"Failed to download object: {e}")
            if "NoSuchBucket" in str(e) or "NoSuchKey" in str(e):
                raise NotFoundError(resource_type="object")
            if "AccessDenied" in str(e):
                raise PermissionDeniedError()
            raise InternalError(details=f"Failed to download object: {e}")

    @override
    def remove_object(self, bucket_name: str, object_name: str) -> None:
        """Remove an object from a bucket."""
        try:
            if not bucket_name or not object_name:
                raise InvalidArgumentError(
                    argument_name=(
                        "bucket_name or object_name"
                        if not all([bucket_name, object_name])
                        else "bucket_name" if not bucket_name else "object_name"
                    ),
                )
            self.client.remove_object(bucket_name, object_name)
            if hasattr(self.list_objects, "clear_cache"):
                self.list_objects.clear_cache()  # Clear object list cache
        except S3Error as e:
            logger.error(f"Failed to remove object: {e}")
            if "NoSuchBucket" in str(e) or "NoSuchKey" in str(e):
                raise NotFoundError(resource_type="object")
            if "AccessDenied" in str(e):
                raise PermissionDeniedError()
            raise InternalError(details=f"Failed to remove object: {e}")

    @override
    @ttl_cache_decorator(ttl_seconds=300, maxsize=100)  # Cache for 5 minutes
    def list_objects(self, bucket_name: str, prefix: str = "", recursive: bool = False) -> list[MinioObjectType]:
        """List objects in a bucket."""
        try:
            if not bucket_name:
                raise InvalidArgumentError(argument_name="bucket_name")
            objects = self.client.list_objects(bucket_name, prefix=prefix, recursive=recursive)
            return [
                {"object_name": obj.object_name, "size": obj.size, "last_modified": obj.last_modified}
                for obj in objects
            ]
        except S3Error as e:
            logger.error(f"Failed to list objects: {e}")
            if "NoSuchBucket" in str(e):
                raise NotFoundError(resource_type="bucket")
            if "AccessDenied" in str(e):
                raise PermissionDeniedError()
            raise InternalError(details=f"Failed to list objects: {e}")

    @override
    @ttl_cache_decorator(ttl_seconds=300, maxsize=100)  # Cache for 5 minutes
    def stat_object(self, bucket_name: str, object_name: str) -> MinioObjectType:
        """Get object metadata."""
        try:
            if not bucket_name or not object_name:
                raise InvalidArgumentError(
                    argument_name=(
                        "bucket_name or object_name"
                        if not all([bucket_name, object_name])
                        else "bucket_name" if not bucket_name else "object_name"
                    ),
                )
            obj = self.client.stat_object(bucket_name, object_name)
            return {
                "object_name": obj.object_name,
                "size": obj.size,
                "last_modified": obj.last_modified,
                "content_type": obj.content_type,
                "etag": obj.etag,
            }
        except S3Error as e:
            logger.error(f"Failed to get object stats: {e}")
            if "NoSuchBucket" in str(e) or "NoSuchKey" in str(e):
                raise NotFoundError(resource_type="object")
            if "AccessDenied" in str(e):
                raise PermissionDeniedError()
            raise InternalError(details=f"Failed to get object stats: {e}")

    @override
    def presigned_get_object(self, bucket_name: str, object_name: str, expires: int = 3600) -> str:
        """Generate a presigned URL for downloading an object."""
        try:
            if not bucket_name or not object_name:
                raise InvalidArgumentError(
                    argument_name=(
                        "bucket_name or object_name"
                        if not all([bucket_name, object_name])
                        else "bucket_name" if not bucket_name else "object_name"
                    ),
                )
            return self.client.presigned_get_object(bucket_name, object_name, expires=timedelta(seconds=expires))
        except S3Error as e:
            logger.error(f"Failed to generate presigned GET URL: {e}")
            if "NoSuchBucket" in str(e) or "NoSuchKey" in str(e):
                raise NotFoundError(resource_type="object")
            if "AccessDenied" in str(e):
                raise PermissionDeniedError()
            raise InternalError(details=f"Failed to generate presigned GET URL: {e}")

    @override
    def presigned_put_object(self, bucket_name: str, object_name: str, expires: int = 3600) -> str:
        """Generate a presigned URL for uploading an object."""
        try:
            if not bucket_name or not object_name:
                raise InvalidArgumentError(
                    argument_name=(
                        "bucket_name or object_name"
                        if not all([bucket_name, object_name])
                        else "bucket_name" if not bucket_name else "object_name"
                    ),
                )
            return self.client.presigned_put_object(bucket_name, object_name, expires=timedelta(seconds=expires))
        except S3Error as e:
            logger.error(f"Failed to generate presigned PUT URL: {e}")
            if "NoSuchBucket" in str(e):
                raise NotFoundError(resource_type="bucket")
            if "AccessDenied" in str(e):
                raise PermissionDeniedError()
            raise InternalError(details=f"Failed to generate presigned PUT URL: {e}")

    @override
    def set_bucket_policy(self, bucket_name: str, policy: str) -> None:
        """Set bucket policy."""
        try:
            if not bucket_name or not policy:
                raise InvalidArgumentError(
                    argument_name=(
                        "bucket_name or policy"
                        if not all([bucket_name, policy])
                        else "bucket_name" if not bucket_name else "policy"
                    ),
                )
            self.client.set_bucket_policy(bucket_name, policy)
        except S3Error as e:
            logger.error(f"Failed to set bucket policy: {e}")
            if "NoSuchBucket" in str(e):
                raise NotFoundError(resource_type="bucket")
            if "AccessDenied" in str(e):
                raise PermissionDeniedError()
            raise InternalError(details=f"Failed to set bucket policy: {e}")

    @override
    @ttl_cache_decorator(ttl_seconds=300, maxsize=100)  # Cache for 5 minutes
    def get_bucket_policy(self, bucket_name: str) -> MinioPolicyType:
        """Get bucket policy."""
        try:
            if not bucket_name:
                raise InvalidArgumentError(argument_name="bucket_name")
            policy = self.client.get_bucket_policy(bucket_name)
            return {"policy": policy}
        except S3Error as e:
            logger.error(f"Failed to get bucket policy: {e}")
            if "NoSuchBucket" in str(e):
                raise NotFoundError(resource_type="bucket")
            if "AccessDenied" in str(e):
                raise PermissionDeniedError()
            raise InternalError(details=f"Failed to get bucket policy: {e}")
