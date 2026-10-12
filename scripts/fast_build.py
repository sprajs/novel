#!/usr/bin/env python3
"""Build the pinned native runtime using the isolated fast-build tool lock."""
import argparse
import importlib.metadata
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from novel.artifacts import sha256_file
from novel.fast_runtime import backend_config, bounded_int, host_record, validate_lock, verify_build, verify_source, write_new


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=("cloud-cpu", "local-2080ti", "rental"), required=True)
    parser.add_argument("--source", type=Path, default=ROOT / ".cache/llama.cpp")
    parser.add_argument("--jobs", type=int, default=5)
    parser.add_argument("--nvcc-version", choices=("12.8.90", "12.8.93"), default="12.8.90",
                        help="Exact CUDA 12.8 Update 1 compiler component; 12.8.93 is in NVIDIA's redistributable manifest")
    args = parser.parse_args()
    os.chdir(ROOT)
    bounded_int(args.jobs, "jobs", 1, 32)
    for package, version in (("cmake", "4.1.3"), ("ninja", "1.13.0")):
        if importlib.metadata.version(package) != version:
            raise ValueError("Run with environments/fast-build/.venv/bin/python after uv sync --locked")
    config = backend_config()
    packages = validate_lock(ROOT / "environments/fast-build/uv.lock")
    profile = config["profiles"][args.profile]
    source = args.source.resolve()
    if not source.exists():
        source.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", "--depth", "1", "--branch", config["tag"], config["repository"], str(source)], check=True)
    verify_source(source)
    build = ROOT / ".cache/fast" / args.profile
    if (build / "receipt.json").exists():
        receipt = verify_build(build, args.profile)
        if profile["cuda_arch"] and not re.search(r"\bV" + re.escape(args.nvcc_version) + r"\b", receipt.get("nvcc") or ""):
            raise ValueError("Existing GPU build used a different NVCC version; select its exact --nvcc-version")
        print(f"Verified existing build: {build}")
        return
    tools = Path(sys.executable).parent
    env = {**os.environ, "PATH": str(tools) + os.pathsep + os.environ["PATH"]}
    flags = ["-DCMAKE_BUILD_TYPE=Release", "-DGGML_NATIVE=ON", "-DLLAMA_BUILD_IS_DEV=OFF",
             "-DLLAMA_BUILD_TESTS=OFF", "-DLLAMA_BUILD_EXAMPLES=OFF", "-DLLAMA_OPENSSL=OFF"]
    nvcc = None
    if profile["cuda_arch"]:
        nvcc = subprocess.check_output(["nvcc", "--version"], text=True)
        if not re.search(r"release 12\.8,", nvcc) or not re.search(r"\bV" + re.escape(args.nvcc_version) + r"\b", nvcc):
            raise ValueError(f"GPU recipe requires explicitly provisioned CUDA 12.8 Update 1 (nvcc V{args.nvcc_version}); no installer/fallback")
        flags += ["-DGGML_CUDA=ON", "-DCMAKE_CUDA_ARCHITECTURES=" + profile["cuda_arch"]]
    else:
        flags += ["-DGGML_CUDA=OFF"]
    configure = [str(tools / "cmake"), "-S", str(source), "-B", str(build), "-G", "Ninja", *flags]
    compile_cmd = [str(tools / "cmake"), "--build", str(build), "--target", "llama-server", "llama-bench", "llama-quantize", "-j", str(args.jobs)]
    build.mkdir(parents=True, exist_ok=True)
    # A failed build remains reviewable; reruns never overwrite a failed log.
    log = build / "recipe-build.log"
    with log.open("xb") as handle:
        for command in (configure, compile_cmd):
            subprocess.run(command, env=env, check=True, stdout=handle, stderr=handle)
    receipt = {"schema_version": 1, "commit": verify_source(source), "tag": config["tag"],
               "profile": args.profile, "commands": [configure, compile_cmd], "host": host_record(),
               "packages": packages,
               "compiler": subprocess.check_output([os.environ.get("CXX", "c++"), "--version"], text=True), "nvcc": nvcc,
               "expected_nvcc_version": args.nvcc_version if nvcc else None,
               "system_runtime_linkage": subprocess.check_output(["ldd", str(build / "bin/llama-server")], text=True),
               "build_tool_lock_sha256": sha256_file(ROOT / "environments/fast-build/uv.lock"),
               "cmake_cache_sha256": sha256_file(build / "CMakeCache.txt"),
               "runtime_hashes": {p.name: sha256_file(p) for p in sorted((build / "bin").iterdir()) if p.is_file()},
               "gpu_execution_tested": False}
    write_new(build / "receipt.json", receipt)
    print(build)


if __name__ == "__main__":
    main()
