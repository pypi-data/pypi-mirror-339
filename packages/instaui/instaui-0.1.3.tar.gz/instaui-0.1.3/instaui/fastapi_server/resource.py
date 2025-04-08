from pathlib import Path
from typing import Dict
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


def _generate_hash_part(path: Path):
    path = Path(path).resolve()
    is_file = path.is_file()

    if is_file:
        return f"{file_system.generate_hash_name_from_path(path.parent)}/{path.name}"

    return file_system.generate_hash_name_from_path(path)
