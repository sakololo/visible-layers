import os
import shutil
import uuid
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def temporary_workspace():
    root = Path(os.environ.get("VISIBLE_LAYERS_TEST_TMP", ".test-tmp"))
    root.mkdir(parents=True, exist_ok=True)
    path = root / f"case-{uuid.uuid4().hex}"
    path.mkdir()
    try:
        yield str(path)
    finally:
        shutil.rmtree(path, ignore_errors=True)
