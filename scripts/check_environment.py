#!/usr/bin/env python3
"""Read-only capacity report; never installs drivers or changes credentials."""

import json
import os
from pathlib import Path
import platform
import shutil
import subprocess

import torch


def main():
    command = shutil.which("nvidia-smi")
    gpu_info = None
    if command:
        result = subprocess.run([command, "--query-gpu=name,driver_version,memory.total,memory.free", "--format=csv,noheader"],
                                capture_output=True, text=True, timeout=20, check=False)
        gpu_info = result.stdout.strip() if result.returncode == 0 else {"returncode": result.returncode}
    report = {
        "python": platform.python_version(), "cpu_count": os.cpu_count(),
        "torch": torch.__version__, "torch_cuda_build": torch.version.cuda,
        "cuda_available": torch.cuda.is_available(), "nvidia_smi": gpu_info,
        "free_disk_bytes": shutil.disk_usage(Path.cwd()).free,
        "ram_total_bytes": os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES"),
        "wheel_cuda_architectures": torch.cuda.get_arch_list() if torch.cuda.is_available() else [],
        "scope": "current cloud process; not the user's local RTX 2080 Ti",
    }
    if torch.cuda.is_available():
        report["gpu_capabilities"] = [torch.cuda.get_device_capability(i) for i in range(torch.cuda.device_count())]
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
