from whitenoise.storage import CompressedManifestStaticFilesStorage
from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    location = 'media'
    file_overwrite = False


class LenientManifestStaticFilesStorage(CompressedManifestStaticFilesStorage):
    """Ne plante pas sur un fichier statique absent du manifeste."""
    manifest_strict = False
