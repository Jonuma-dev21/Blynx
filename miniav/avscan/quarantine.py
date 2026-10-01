import json
import os
import shutil
import time
from pathlib import Path


def quarantine(path: Path, qdir, sha: str = "", reason: str = "") -> Path:
    qdir = Path(qdir)
    qdir.mkdir(parents=True, exist_ok=True)
    dest = qdir / f"{int(time.time())}_{path.name}.quar"
    shutil.move(str(path), dest)
    os.chmod(dest, 0o000)  # rend le fichier non exécutable/lisible (POSIX)
    meta = {"original": str(path.resolve()), "sha256": sha, "reason": reason}
    Path(str(dest) + ".json").write_text(json.dumps(meta, indent=2))
    return dest