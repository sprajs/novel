#!/usr/bin/env python3
"""Use the selected interpreter and repository source; never sync the CPU project."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from novel.profile_runner import main  # noqa: E402

if __name__ == "__main__":
    main()
