import asyncio

from kivymd.utils import asynckivy


def asyncio_run(function):
    def run(*args, **kwargs):
        asyncio.run(function(*args, **kwargs))

    return run


def asynckivy_start(function):
    def run(*args, **kwargs):
        asynckivy.start(function(*args, **kwargs))

    return run
