from os import path

from django.core.exceptions import ValidationError


def _validate_extension(file, valid_extensions):
    extension = path.splitext(file.name)[-1]

    if extension.lower() not in valid_extensions:
        raise ValidationError("Unsupported file extension")


def validate_image_extension(file):
    valid_extensions = [".png", ".jpg", ".jpeg"]
    _validate_extension(file, valid_extensions)
