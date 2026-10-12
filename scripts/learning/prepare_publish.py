#!/usr/bin/env python3
"""Mirror a validated static build into an ignored, separately owned Site checkout."""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkout", required=True)
    args = parser.parse_args()
    destination = Path(args.checkout)
    if not destination.is_absolute():
        destination = ROOT / destination
    allowed = (ROOT / ".local").resolve()
    try:
        destination.resolve().relative_to(allowed)
    except ValueError:
        parser.error("Site checkout must be inside this repo's ignored .local directory.")
    if any(p.is_symlink() for p in [destination, *destination.parents] if p != p.parent):
        parser.error("Site checkout must not traverse symlinks.")
    subprocess.run([sys.executable, str(ROOT / "scripts/learning/build.py")], cwd=ROOT, check=True)
    source = ROOT / "learning/site"
    destination.mkdir(parents=True, exist_ok=True)
    for name in ("index.html", "app.js", "style.css", "favicon.svg", ".openai/hosting.json"):
        target = destination / name
        if target.is_symlink():
            parser.error(f"Refusing symlink: {target}")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source / name, target)
    target = destination / "dist"
    if target.is_symlink():
        parser.error("Refusing symlinked dist")
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source / "dist", target)
    print(f"Prepared static Site checkout: {destination}")


if __name__ == "__main__":
    main()
