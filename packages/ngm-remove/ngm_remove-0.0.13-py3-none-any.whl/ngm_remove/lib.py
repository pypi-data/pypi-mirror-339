import os
import shutil

from pathlib import Path
from ngm_remove import log


def remove(entry: str, db):
    fullpath = os.path.abspath(entry)
    path = Path(fullpath)

    if path.is_file():
        try:
            path.unlink()
            print("file:", fullpath)
            log.loginfo("file: " + fullpath)
            db.insert("file", fullpath, "ok")
        except Exception as e:
            msg = str(e)
            print(msg)
            db.insert("file", fullpath, "err", msg)

    elif path.is_dir():
        try:
            shutil.rmtree(fullpath)
            print("dir:", fullpath)
            log.loginfo("dir: " + fullpath)
            db.insert("dir", fullpath, "ok")
        except Exception as e:
            msg = str(e)
            print(msg)
            db.insert("dir", fullpath, "err", msg)

    else:
        print("not found:", fullpath)
        log.loginfo("not found: " + fullpath)
        db.insert("none", fullpath, "error")
