from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Union
from .dataclass import JsLink, VueAppUse, VueAppComponent


class HtmlResource:
    use_tailwind: Optional[bool] = None
    _title: str = ""

    def __init__(self) -> None:
        self._css_links: Dict[Union[str, Path], Any] = {}
        self._style_tags: List[str] = []
        self._js_links: List[JsLink] = []
        self._script_tags: List[str] = []
        self._vue_app_use: Set[VueAppUse] = set()
        self._vue_app_components: Set[VueAppComponent] = set()
        self._import_maps: Dict[str, str] = {}
        self.title: str = self._title
        self._appConfig = "{}"

    def add_css_link(self, link: Union[str, Path]):
        self._css_links[link] = None

    def add_style_tag(self, content: str):
        self._style_tags.append(content)

    def add_js_link(
        self,
        link: Union[str, Path],
        *,
        attrs: Optional[Dict[str, Any]] = None,
        insert_before: int = -1,
    ):
        if insert_before == -1:
            self._js_links.append(JsLink(link, attrs or {}))
            return
        self._js_links.insert(insert_before, JsLink(link, attrs or {}))

    def add_script_tag(
        self, content: str, script_attrs: Optional[Dict[str, Any]] = None
    ):
        self._script_tags.append(content)

    def add_vue_app_use(self, name: str):
        self._vue_app_use.add(VueAppUse(name))

    def add_vue_app_component(self, name: str, url: str):
        self._vue_app_components.add(VueAppComponent(name, url))

    def add_import_map(self, name: str, link: str):
        self._import_maps[name] = link
