import os
from django.conf import settings


def get_cert_file_name():
    if not os.path.exists(settings.CERT_FILE):
        with open(settings.CERT_FILE, 'w') as file:
            file.write(settings.CLIENT_CERT)
    return settings.CERT_FILE


def get_key_file_name():
    if not os.path.exists(settings.KEY_FILE):
        with open(settings.KEY_FILE, 'w') as file:
            file.write(settings.CLIENT_KEY)
    return settings.KEY_FILE
