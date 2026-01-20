from os import path
from uuid import uuid4


def path_and_rename_image(_, filename):
    upload_to = "images"
    # get filename
    ext = filename.split(".")[-1]

    # set filename as random string
    filename = f"{uuid4().hex}.{ext}"

    # return the whole path to the file
    return path.join(upload_to, filename)
