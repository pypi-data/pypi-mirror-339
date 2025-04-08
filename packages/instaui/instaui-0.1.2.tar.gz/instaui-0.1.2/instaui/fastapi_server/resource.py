from pathlib import Path
from typing import Dict
from urllib.parse import quote as urllib_quote
from instaui.systems import file_system
from instaui.version import __version__ as _INSTA_VERSION

URL = f"/_instaui_{_INSTA_VERSION}/resource"
_THashPart = str
_HASH_PART_MAP: Dict[_THashPart, Path] = {}
_FILE_URL_MAP: Dict[Path, _THashPart] = {}


def get_by_hash(hash_part: str) -> Path:
    return _HASH_PART_MAP[hash_part]


def record_resource(path: Path):
    if path in _FILE_URL_MAP:
        return _FILE_URL_MAP[path]

    hash_part = _generate_hash_part(path)
    _HASH_PART_MAP[hash_part] = path
    url = f"{URL}/{hash_part}"
    _FILE_URL_MAP[path] = url
    return url


def generate_static_url(file_path: Path):
    return urllib_quote(f"{URL}/{_generate_hash_part(file_path)}")


def _generate_hash_part(file_path: Path):
    file_path = Path(file_path).resolve()
    hash_name = file_system.generate_hash_name_from_path(file_path)
    return f"{hash_name}/{file_path.name}"
