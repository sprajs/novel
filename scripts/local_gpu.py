#!/usr/bin/env python3
"""Run a local GPU command using provisioned user-space tools, without system changes."""
import argparse
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def prepend(env, key, path):
    env[key] = str(path) + (os.pathsep + env[key] if env.get(key) else "")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--toolchain", action="store_true", help="Use the provisioned .cache/toolchains/cuda128 compiler/sysroot")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        parser.error("Supply a command after --")
    env = os.environ.copy()
    probe = ["nvidia-smi", "--query-gpu=driver_version", "--format=csv,noheader"]
    result = subprocess.run(probe, env=env, capture_output=True, text=True, check=False)
    if result.returncode:
        version = re.search(r"Kernel Module.*?\s(\d+\.\d+\.\d+)", Path("/proc/driver/nvidia/version").read_text())
        if version is None:
            raise RuntimeError("Cannot identify loaded NVIDIA module")
        driver = ROOT / ".cache/host" / f"nvidia-{version[1]}" / "usr"
        if not (driver / "bin/nvidia-smi").is_file() or not (driver / "lib/libcuda.so.1").is_file():
            raise RuntimeError("System NVIDIA access failed and no matching local driver libraries are provisioned")
        prepend(env, "PATH", driver / "bin")
        prepend(env, "LD_LIBRARY_PATH", driver / "lib")
        verified = subprocess.run(probe, env=env, capture_output=True, text=True, check=True)
        if any(row.strip() != version[1] for row in verified.stdout.splitlines()) or not verified.stdout.strip():
            raise RuntimeError("Local NVIDIA library version differs from loaded module")
        print(f"Using isolated NVIDIA {version[1]} libraries for this command", file=sys.stderr, flush=True)
    if args.toolchain:
        toolkit = ROOT / ".cache/toolchains/cuda128"
        for name in ("nvcc", "x86_64-conda-linux-gnu-cc", "x86_64-conda-linux-gnu-c++"):
            if not (toolkit / "bin" / name).is_file():
                raise RuntimeError(f"Missing provisioned toolchain binary: {name}")
        prepend(env, "PATH", toolkit / "bin")
        env["CC"] = str(toolkit / "bin/x86_64-conda-linux-gnu-cc")
        env["CXX"] = str(toolkit / "bin/x86_64-conda-linux-gnu-c++")
        env["CUDAHOSTCXX"] = env["CXX"]
        env["CUDACXX"] = str(toolkit / "bin/nvcc")
        env["CUDAToolkit_ROOT"] = str(toolkit)
    os.chdir(ROOT)
    os.execvpe(command[0], command, env)


if __name__ == "__main__":
    main()
