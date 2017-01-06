"""Credentials parser

    credentials can either live in credentials.properties
      or as environment variables

    the file will have two fields:
        registry_username=username
        registry_password=password

    The environment variables are:
        REGISTRY_USERNAME
        REGISTRY_PASSWORD

    If either field is missing from the file, it will look for the
    environment variable
"""

import os

REGISTRY_USERNAME = "registry_username"
REGISTRY_PASSWORD = "registry_password"

try:
    with open("credentials.properties") as cred_file:
        data = cred_file.readline().split("=")
        if data[0] == REGISTRY_USERNAME:
            username = data[1]
        elif data[0] == REGISTRY_PASSWORD:
            password = data[1]
except FileNotFoundError:
    pass


try:
    username
except NameError:
    username = os.getenv(REGISTRY_USERNAME)

try:
    password
except NameError:
    password = os.getenv(REGISTRY_PASSWORD)
