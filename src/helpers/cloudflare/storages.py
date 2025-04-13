from storages.backends.s3 import S3Storage

# import helpers.storages.mixins as mixins


class CloudflareStorage(S3Storage):
    pass


class StaticFileStorage(S3Storage):
    """
    For staticfiles
    """

    location = "staticfiles"
    default_acl = "public-read"


class MediaFileStorage(S3Storage):
    """
    For general uploads
    """

    location = "media"
    default_acl = "public-read"


# class ProtectedMediaStorage(mixins.DefaultACLMixin, CloudflareStorage):
#     """
#     For user private uploads
#     """

#     location = "protected"
#     default_acl = "private"
