from django_oss_storage.backends import OssMediaStorage

class MediaStorage(OssMediaStorage):
    location = 'media'
    file_overwrite = False
