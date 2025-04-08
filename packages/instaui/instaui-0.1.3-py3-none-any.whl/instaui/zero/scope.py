from pathlib import Path
from typing import Union
from instaui.runtime import new_app_slot, reset_app_slot
from contextlib import contextmanager
from .func import to_html, to_html_str


@contextmanager
def scope():
    token = new_app_slot("zero")
    yield Wrapper()
    reset_app_slot(token)


class Wrapper:
    def to_html(self, file: Union[str, Path]):
        return to_html(file)

    def to_html_str(self):
        return to_html_str()
