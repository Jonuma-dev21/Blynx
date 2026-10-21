"""Met à jour data/hashes.txt depuis l'API MalwareBazaar (abuse.ch).

Clé : variable d'environnement ABUSECH_KEY, ou fichier .env contenant
ABUSECH_KEY=ta_cle  (jamais dans le code, jamais dans git).

Exemples :
    python3 update_hashes.py --signature TrickBot --signature AgentTesla --limit 200
    python3 update_hashes.py --tag Mirai
    python3 update_hashes.py --recent 24
"""
import argparse
import os
import re
import sys
import time
from pathlib import Path

import requests

API = "https://mb-api.abuse.ch/api/v1/"
BASE = Path(__file__).parent
HASHES = BASE / "data" / "hashes.txt"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def load_key() -> str:
    key = os.environ.get("ABUSECH_KEY")
    env_file = BASE / ".env"
    if not key and env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.strip().startswith("ABUSECH_KEY="):
                key = line.split("=", 1)[1].strip().strip("'\"")
    if not key:
        sys.exit("Clé absente : définis ABUSECH_KEY (variable d'environnement ou fichier .env)")
    return key


def query(key: str, **params) -> dict:
    r = requests.post(API, headers={"Auth-Key": key}, data=params, timeout=30)
    r.raise_for_status()
    return r.json()


def existing_hashes() -> set:
    known = set()
    if HASHES.exists():
        for line in HASHES.read_text().splitlines():
            h = line.split("#")[0].strip().lower()
            if h:
                known.add(h)
    return known


def main():
    ap = argparse.ArgumentParser(description="Met à jour data/hashes.txt depuis MalwareBazaar")
    ap.add_argument("--signature", action="append", default=[], help="famille de malware (répétable)")
    ap.add_argument("--tag", action="append", default=[], help="tag MalwareBazaar (répétable)")
    ap.add_argument("--recent", type=int, metavar="HEURES", help="détections récentes (max 168 h)")
    ap.add_argument("--limit", type=int, default=100, help="max par requête (défaut 100, max 1000)")
    args = ap.parse_args()
    if not (args.signature or args.tag or args.recent):
        ap.error("donne au moins --signature, --tag ou --recent")

    key = load_key()
    jobs = [(f"signature:{s}", dict(query="get_siginfo", signature=s, limit=args.limit))
            for s in args.signature]
    jobs += [(f"tag:{t}", dict(query="get_taginfo", tag=t, limit=args.limit))
             for t in args.tag]
    if args.recent:
        jobs.append((f"recent:{args.recent}h", dict(query="recent_detections", hours=args.recent)))

    known = existing_hashes()
    new_lines = []
    for label, params in jobs:
        try:
            resp = query(key, **params)
        except requests.RequestException as e:
            print(f"[!] {label}: erreur réseau/HTTP : {e}", file=sys.stderr)
            continue
        status = resp.get("query_status")
        if status != "ok":
            print(f"[!] {label}: {status}")
            continue
        added = 0
        for item in resp.get("data", []):
            h = str(item.get("sha256_hash", "")).lower()
            if SHA256_RE.match(h) and h not in known:
                known.add(h)
                new_lines.append(f"{h}  # MalwareBazaar {label}")
                added += 1
        print(f"[+] {label}: {added} nouveau(x) hash(es)")
        time.sleep(1)  # politesse envers l'API

    if new_lines:
        prefix = ""
        if HASHES.exists() and not HASHES.read_text().endswith("\n"):
            prefix = "\n"
        with open(HASHES, "a") as f:
            f.write(prefix + "\n".join(new_lines) + "\n")
    print(f"\n{len(new_lines)} hash(es) ajouté(s) à {HASHES} (total : {len(known)})")


if __name__ == "__main__":
    main()