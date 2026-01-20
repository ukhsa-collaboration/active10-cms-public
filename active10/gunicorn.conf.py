from multiprocessing import cpu_count
from os import environ

bind = "0.0.0.0:" + environ.get("PORT", "8000")
workers = cpu_count()

env = {"DJANGO_SETTINGS_MODULE": "active10.settings"}

reload = True
name = "active10"
