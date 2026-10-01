"""Détecteurs : chacun expose scan(path) -> list[Finding]."""
import hashlib
import math
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

try:
    import yara
except ImportError:
    yara = None


@dataclass
class Finding:
    detector: str
    name: str
    score: int  # 100+ = malveillant, 50+ = suspect


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


class HashDetector:
    name = "hash"

    def __init__(self, db_path):
        self.bad = set()
        for line in Path(db_path).read_text().splitlines():
            line = line.split("#")[0].strip().lower()
            if line:
                self.bad.add(line)

    def scan(self, path: Path):
        digest = sha256_of(path)
        if digest in self.bad:
            return [Finding(self.name, f"known-bad sha256 {digest[:12]}...", 100)]
        return []


class YaraDetector:
    name = "yara"

    def __init__(self, rules_dir):
        files = {p.stem: str(p) for p in Path(rules_dir).glob("*.yar")}
        self.rules = yara.compile(filepaths=files) if (yara and files) else None

    def scan(self, path: Path):
        if not self.rules:
            return []
        return [Finding(self.name, m.rule, 100) for m in self.rules.match(str(path))]


class EntropyDetector:
    """Entropie élevée = fichier chiffré/packé. Indice faible, jamais décisif seul."""
    name = "entropy"
    MAX_READ = 10 * 1024 * 1024
    MIN_SIZE = 4096

    def scan(self, path: Path):
        with open(path, "rb") as f:
            data = f.read(self.MAX_READ)
        if len(data) < self.MIN_SIZE:
            return []
        n = len(data)
        entropy = -sum((c / n) * math.log2(c / n) for c in Counter(data).values())
        if entropy > 7.5:
            return [Finding(self.name, f"entropie élevée ({entropy:.2f}/8)", 30)]
        return []