"""
.. module::  core.image_models
   :synopsis:  Django utils core image  models

Django utils core image models.
"""

import os
from django.conf import settings

from utils.image import encode_file
from core.models import app_table_name, db_table_name
from core.utils import current_site
from . import fields
from . import constants
from .models import NamedObject, NamedObjectManager

IMAGE_FORMAT_GIF = 'gif'
IMAGE_FORMAT_JPEG = 'jpeg'
IMAGE_FORMAT_PNG = 'png'
IMAGE_FORMATS = (IMAGE_FORMAT_GIF, IMAGE_FORMAT_JPEG,
                 IMAGE_FORMAT_PNG, constants.UNKNOWN)

ORIENTATION_PORTRAIT = 'Portrait'
ORIENTATION_LANDSCAPE = 'Landscape'
VISUAL_ORIENTATION = (ORIENTATION_PORTRAIT,
                      ORIENTATION_LANDSCAPE,
                      constants.UNKNOWN)

_app_label = 'core'


class ImageFormat(NamedObject):
    class Meta(NamedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name('ImageFormat'))


class DocumentOrientation(NamedObject):
    class Meta(NamedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label,
                                  db_table_name('DocumentOrientation'))


class ImageManager(NamedObjectManager):
    """
    Ad image manager class
    """
    context_explain = 'This transpired when fetching images for ad units {}'
    format_explain = 'Image of format "{}" has not been found. '

    def images(self, image_formats, ad_units):
        """
        Fetch images for ad units
        """
#         select = {'ad_unit_id': 'omas_ad_unit_2_ad_image.adunit_id'}
#         ad_unit_ids = [ad_unit.id for ad_unit in ad_units]
#         images = AdImage.objects.deferred_filter(
#             image_format__in=image_formats,
#             images__in=ad_unit_ids).extra(
#                 select=select).order_by()
#         if images.count() == 0:
#             formats = [image_format.name for image_format in image_formats]
#             context_explain = self.context_explain.format(ad_unit_ids)
#             format_explain = self.format_explain.format(formats)
#             raise AdServerError(explain_msg(
#                 object_type='images',
#                 context=context_explain,
#                 explanations=[format_explain]))
#         return images


def image_upload_path(instance, filename):
    domain_parts = current_site().domain.split('.')
    base_name = 'unknown'
    if settings.USE_MEDIA_ROOT:   # Used under AWS
        media = 'media'
    else:
        media = ''
    for part in domain_parts:
        if 'www' not in part and 'com' not in part:
            base_name = part
            break
    full_path = os.path.join(media, base_name, 'images', filename)
    return full_path


class Image(NamedObject):
    """
    Image class
    """
    class Meta(NamedObject.Meta):
        app_label = _app_label
        db_table = app_table_name(_app_label, db_table_name('Image'))

    objects = ImageManager()
    image = fields.image_field(upload_to=image_upload_path,
                               height_field='height',
                               width_field='width')

    image_format = fields.foreign_key_field(ImageFormat)
    image_orientation = fields.foreign_key_field(DocumentOrientation)
    width = fields.small_integer_field(default=0)
    height = fields.small_integer_field(default=0)

    def __init__(self, *args, **kwargs):
        super(Image, self).__init__(*args, **kwargs)
        # @TODO: revisit read only text fields
#         self._config_help(('width', 'height', 'image_format'),
#                              ad_image_help_texts)

    def __str__(self):
        return '{:s}({:s})'.format(self.full_name, self.image_type.full_name)

    def encode(self):
        """
        Encode the image
        Defaulting to base64 encoding
        """
        return encode_file(self.image.file)
