from fastapi import FastAPI
from fastapi.responses import FileResponse

from instaui.fastapi_server import resource


URL = f"{resource.URL}/{{hash_part:path}}"


def create_router(app: FastAPI):
    _dependency_handler(app)


def _dependency_handler(app: FastAPI):
    @app.get(URL)
    def _(hash_part: str) -> FileResponse:
        local_file = resource.get_by_hash(hash_part)

        return FileResponse(
            local_file, headers={"Cache-Control": "public, max-age=3600"}
        )
