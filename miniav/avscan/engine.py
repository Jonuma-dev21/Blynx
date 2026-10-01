import logging
import os
from dataclasses import dataclass, field
from pathlib import Path

from .detectors import Finding

log = logging.getLogger("avscan")


@dataclass
class Result:
    path: Path
    findings: list = field(default_factory=list)

    @property
    def score(self):
        return sum(f.score for f in self.findings)

    @property
    def verdict(self):
        if self.score >= 100:
            return "MALICIOUS"
        if self.score >= 50:
            return "SUSPICIOUS"
        return "CLEAN"


def iter_files(root: Path):
    if root.is_file():
        yield root
        return
    for dirpath, _, names in os.walk(root, followlinks=False):
        for name in names:
            p = Path(dirpath) / name
            if p.is_file() and not p.is_symlink():
                yield p


def scan_file(path: Path, detectors) -> Result:
    res = Result(path)
    for d in detectors:
        try:
            res.findings.extend(d.scan(path))
        except (OSError, Exception) as e:  # un détecteur en panne ne doit pas tout arrêter
            log.warning("%s a échoué sur %s: %s", d.name, path, e)
    return res


def scan_tree(root: Path, detectors):
    for p in iter_files(root):
        yield scan_file(p, detectors)