import argparse
import logging
import sys
from pathlib import Path

from avscan.detectors import EntropyDetector, HashDetector, YaraDetector, sha256_of, yara
from avscan.engine import scan_tree
from avscan.quarantine import quarantine

BASE = Path(__file__).parent


def main():
    ap = argparse.ArgumentParser(description="Mini antivirus (scan à la demande)")
    ap.add_argument("path", type=Path)
    ap.add_argument("--quarantine", action="store_true", help="mettre en quarantaine les fichiers MALICIOUS")
    ap.add_argument("--qdir", type=Path, default=BASE / "quarantine")
    args = ap.parse_args()

    logging.basicConfig(level=logging.WARNING, format="%(levelname)s %(message)s")
    if yara is None:
        print("[!] yara-python absent : détecteur YARA désactivé", file=sys.stderr)

    detectors = [
        HashDetector(BASE / "data" / "hashes.txt"),
        YaraDetector(BASE / "rules"),
        EntropyDetector(),
    ]

    total = bad = 0
    for res in scan_tree(args.path, detectors):
        total += 1
        if res.verdict == "CLEAN":
            continue
        print(f"[{res.verdict}] {res.path} (score {res.score})")
        for f in res.findings:
            print(f"    - {f.detector}: {f.name}")
        if res.verdict == "MALICIOUS":
            bad += 1
            if args.quarantine:
                dest = quarantine(res.path, args.qdir, sha256_of(res.path),
                                  "; ".join(f.name for f in res.findings))
                print(f"    -> quarantaine : {dest}")

    print(f"\n{total} fichiers scannés, {bad} malveillant(s)")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()