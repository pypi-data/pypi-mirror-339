from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, Literal, Optional, Union
from instaui.common.jsonable import dumps, dumps2dict
from instaui.runtime._app import get_app_slot


def add_css_link(href: Union[str, Path]):
    get_app_slot()._html_resource.add_css_link(href)


def add_js_link(
    link: Union[str, Path],
    *,
    type: Optional[Literal["module"]] = None,
):
    attrs = {
        "type": type,
    }

    get_app_slot()._html_resource.add_js_link(link, attrs=attrs)


def add_style(content: str):
    get_app_slot()._html_resource.add_style_tag(content)


def use_tailwind(value=True):
    get_app_slot()._html_resource.use_tailwind = value


def use_page_title(title: str):
    get_app_slot()._html_resource.title = title


def use_favicon(favicon: Path):
    get_app_slot()._html_resource.favicon = favicon


def add_js_code(code: str, *, script_attrs: Optional[Dict[str, Any]] = None):
    get_app_slot()._html_resource.add_script_tag(code, script_attrs=script_attrs)


def add_vue_app_use(name: str):
    get_app_slot()._html_resource.add_vue_app_use(name)


def to_config_data() -> Dict:
    return dumps2dict(get_app_slot())


def to_json(indent=False):
    return dumps(get_app_slot(), indent=indent)
