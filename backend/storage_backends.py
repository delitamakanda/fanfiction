"""Storage backends used in production."""

from storages.backends.s3boto3 import S3Boto3Storage
from whitenoise.storage import CompressedManifestStaticFilesStorage


class MediaStorage(S3Boto3Storage):
    location = "media"
    file_overwrite = False


class LenientManifestStaticFilesStorage(CompressedManifestStaticFilesStorage):
    """Does not crash on a static file missing from the manifest or the disk."""

    manifest_strict = False

    def stored_name(self, name):
        try:
            return super().stored_name(name)
        except ValueError:
            return name
