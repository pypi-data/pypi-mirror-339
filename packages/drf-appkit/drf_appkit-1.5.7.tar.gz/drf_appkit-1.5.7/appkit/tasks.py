import logging

from versatileimagefield.image_warmer import VersatileImageFieldWarmer

from .debug import log
from .models import MediaAttachment


def mediaattachment_warm_renditions(image_attachment_pk):
    try:
        media_attachment = MediaAttachment.objects.get(pk=image_attachment_pk)
    except MediaAttachment.DoesNotExist:
        log(f'MediaAttachment not found (PK: {image_attachment_pk}', level=logging.ERROR)
        return False

    if not (media_attachment.image and media_attachment.rendition_key):
        # This image does not support any renditions. Do nothing
        return True

    try:
        VersatileImageFieldWarmer(
            instance_or_queryset=media_attachment,
            rendition_key_set=media_attachment.rendition_key,
            image_attr='image'
        ).warm()
        media_attachment.warm = True
        media_attachment.save()
        return True
    except ValueError as e:
        log(f'Task `warm_image_attachment` failed with exception: {str(e)}')
        return False
