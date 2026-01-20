from django.conf import settings

OPTIMIZED_IMAGE_METHOD = getattr(settings, "OPTIMIZED_IMAGE_METHOD", "pillow")
