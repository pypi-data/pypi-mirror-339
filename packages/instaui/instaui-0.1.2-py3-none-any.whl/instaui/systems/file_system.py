import uuid
from pathlib import Path


def generate_hash_name_from_path(file_path: Path):
    path_str = str(file_path)
    unique_id = uuid.uuid5(uuid.NAMESPACE_URL, path_str)
    return str(unique_id)
