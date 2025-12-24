# from django.conf import settings
# from storages.backends.s3boto3 import S3Boto3Storage

# class MediaStorage(S3Boto3Storage):
#     bucket_name = settings.AWS_STORAGE_BUCKET_NAME
#     region_name = settings.AWS_S3_REGION_NAME
#     location = ''  # root folder, atau bisa 'media' jika ingin subfolder
#     default_acl = 'public-read'
#     file_overwrite = False
#     custom_domain = settings.AWS_S3_CUSTOM_DOMAIN

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

class MediaStorage(S3Boto3Storage):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    region_name = settings.AWS_S3_REGION_NAME
    location = ''  # root folder, atau bisa 'media' jika ingin subfolder
    # HAPUS default_acl karena bucket tidak support ACL
    # default_acl = 'public-read'  # <- COMMENTED OUT
    file_overwrite = False
    custom_domain = settings.AWS_S3_CUSTOM_DOMAIN
    
    # Gunakan bucket policy untuk public access, bukan ACL
    object_parameters = {
        # Tidak pakai ACL
    }