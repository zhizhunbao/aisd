"""
CST8509 Lab 3: Gazebo Environment Check Script
Author: Peng Wang
Student Number: 041107730

Checks the WSL2 + Ubuntu 22.04 environment readiness for
Gazebo 11 + ROS 2 Humble + Create 3 Simulator setup.

Run from Windows: python check_env.py
"""

import subprocess
import sys
import re
import shutil


# ============================================================
# 辅助函数
# Helper Functions
# ============================================================

def run_cmd(cmd, shell=True, capture=True):
    """
    运行命令并返回输出
    Run a command and return its output
    """
    try:
        result = subprocess.run(
            cmd, shell=shell, capture_output=capture,
            text=True, timeout=30
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"
    except FileNotFoundError:
        return -1, "", "Command not found"


def run_wsl(cmd):
    """
    在 WSL 中运行命令
    Run a command inside WSL
    """
    return run_cmd(f'wsl -e bash -c "{cmd}"')


def print_check(name, passed, detail=""):
    """
    打印检查结果
    Print check result with status icon
    """
    icon = "✅" if passed else "❌"
    msg = f"  {icon} {name}"
    if detail:
        msg += f" — {detail}"
    print(msg)
    return passed


def print_header(title):
    """打印分隔标题 / Print section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


# ============================================================
# 检查项
# Check Items
# ============================================================

def check_wsl_installed():
    """
    检查 WSL 是否安装
    Check if WSL is installed
    """
    code, out, err = run_cmd("wsl --status")
    if code != 0:
        # wsl --status 在某些版本不支持，尝试 wsl --list
        code, out, err = run_cmd("wsl --list --verbose")
    return code == 0


def check_wsl_version():
    """
    检查 WSL 版本（需要 WSL2）
    Check WSL version (WSL2 required)
    """
    code, out, err = run_cmd("wsl --list --verbose")
    if code != 0:
        return False, "Cannot list WSL distributions"

    # 解析输出，查找 Ubuntu 和版本号
    # Parse output to find Ubuntu and version number
    lines = out.replace('\x00', '').split('\n')
    for line in lines:
        if 'Ubuntu' in line and '22.04' in line:
            if '2' in line.split()[-1]:
                return True, "Ubuntu 22.04 running on WSL2"
            else:
                return False, "Ubuntu 22.04 found but running WSL1 — need WSL2"
        elif 'Ubuntu' in line:
            parts = line.split()
            # 检查版本列
            # Check version column
            for p in parts:
                if p == '2':
                    return True, f"Ubuntu on WSL2 (check if 22.04)"
                elif p == '1':
                    return False, "Ubuntu found but running WSL1"
    return False, "No Ubuntu distribution found"


def check_ubuntu_version():
    """
    检查 Ubuntu 版本（需要 22.04）
    Check Ubuntu version (22.04 required)
    """
    code, out, err = run_wsl("cat /etc/os-release | grep VERSION_ID")
    if code != 0:
        return False, "Cannot read Ubuntu version"

    match = re.search(r'VERSION_ID="?(\d+\.\d+)"?', out)
    if match:
        version = match.group(1)
        if version == "22.04":
            return True, f"Ubuntu {version} (Jammy Jellyfish)"
        else:
            return False, f"Ubuntu {version} found — need 22.04"
    return False, "Cannot parse Ubuntu version"


def check_disk_space():
    """
    检查 WSL 可用磁盘空间（建议 >= 15GB）
    Check available disk space in WSL (recommend >= 15GB)
    """
    code, out, err = run_wsl("df -BG / | tail -1 | awk '{print $4}'")
    if code != 0:
        return False, "Cannot check disk space"

    match = re.search(r'(\d+)', out)
    if match:
        free_gb = int(match.group(1))
        if free_gb >= 15:
            return True, f"{free_gb} GB available (>= 15 GB recommended)"
        else:
            return False, f"Only {free_gb} GB available — need at least 15 GB"
    return False, "Cannot parse disk space"


def check_memory():
    """
    检查系统内存（建议 >= 8GB）
    Check system memory (recommend >= 8GB)
    """
    code, out, err = run_wsl("free -g | grep Mem | awk '{print $2}'")
    if code != 0:
        return False, "Cannot check memory"

    try:
        total_gb = int(out)
        if total_gb >= 7:  # WSL 通常分配系统内存的一半
            return True, f"{total_gb} GB total (>= 8 GB recommended)"
        else:
            return False, f"Only {total_gb} GB — may be insufficient"
    except ValueError:
        return False, f"Cannot parse memory: {out}"


def check_gpu():
    """
    检查 GPU 支持（Gazebo 需要 OpenGL）
    Check GPU support (Gazebo needs OpenGL)
    """
    # 检查 Windows 端的 GPU
    # Check GPU on Windows side
    code, out, err = run_cmd(
        'powershell -Command "Get-CimInstance -ClassName Win32_VideoController | Select-Object -ExpandProperty Name"'
    )

    gpu_info = out if code == 0 else "Unknown"

    # 检查 WSL 内是否能访问 GPU
    # Check if GPU is accessible in WSL
    code2, out2, err2 = run_wsl("ls /dev/dxg 2>/dev/null && echo GPU_OK || echo NO_GPU")

    has_gpu = "GPU_OK" in out2
    return has_gpu, f"GPU: {gpu_info.split(chr(10))[0] if gpu_info else 'Unknown'} | WSL GPU: {'Available' if has_gpu else 'Not detected'}"


def check_wslg():
    """
    检查 WSLg（GUI 支持）
    Check WSLg (GUI support for running Gazebo/RViz)
    """
    code, out, err = run_wsl("ls /mnt/wslg/ 2>/dev/null && echo WSLG_OK || echo NO_WSLG")
    has_wslg = "WSLG_OK" in out

    if has_wslg:
        return True, "WSLg detected — GUI apps supported"
    else:
        return False, "WSLg not found — may need X server (VcXsrv/X410)"


def check_ros2():
    """
    检查 ROS 2 是否已安装
    Check if ROS 2 is already installed
    """
    code, out, err = run_wsl("source /opt/ros/humble/setup.bash 2>/dev/null && ros2 --version")
    if code == 0 and out:
        return True, f"ROS 2 version: {out}"
    return False, "Not installed"


def check_gazebo():
    """
    检查 Gazebo 11 是否已安装
    Check if Gazebo 11 is already installed
    """
    code, out, err = run_wsl("gazebo --version 2>/dev/null | head -1")
    if code == 0 and "Gazebo" in out:
        return True, f"{out}"
    return False, "Not installed"


def check_create3_ws():
    """
    检查 create3_ws 工作空间是否存在
    Check if create3_ws workspace exists
    """
    code, out, err = run_wsl("test -d ~/create3_ws/src/create3_sim && echo EXISTS || echo MISSING")
    if "EXISTS" in out:
        # 检查分支
        # Check branch
        code2, out2, _ = run_wsl("cd ~/create3_ws/src/create3_sim && git branch --show-current 2>/dev/null")
        branch = out2 if code2 == 0 else "unknown"
        return True, f"Found (branch: {branch})"
    return False, "Not found"


# ============================================================
# 主程序
# Main Program
# ============================================================

def main():
    print("\n" + "=" * 60)
    print("  🔍 CST8509 Lab 3 — Gazebo Environment Check")
    print("  检查 WSL2 环境是否满足 Gazebo 仿真需求")
    print("=" * 60)

    all_passed = True
    results = {}

    # ---------- 第一部分：WSL 基础检查 ----------
    # ---------- Part 1: WSL Foundation ----------
    print_header("1. WSL 基础 (WSL Foundation)")

    # 检查 WSL 是否安装
    # Check if WSL is installed
    wsl_ok = check_wsl_installed()
    print_check("WSL installed / WSL 已安装", wsl_ok)
    results["wsl"] = wsl_ok

    if not wsl_ok:
        print("\n  ⚠️  WSL is not installed. Run: wsl --install")
        print("     WSL 未安装。运行: wsl --install")
        print("\n  After installation, restart your computer and re-run this script.")
        print("  安装后重启电脑再运行此脚本。")
        return

    # 检查 WSL 版本
    # Check WSL version
    ver_ok, ver_detail = check_wsl_version()
    print_check("WSL2 with Ubuntu / WSL2 + Ubuntu", ver_ok, ver_detail)
    results["wsl_version"] = ver_ok

    # 检查 Ubuntu 版本
    # Check Ubuntu version
    ubuntu_ok, ubuntu_detail = check_ubuntu_version()
    print_check("Ubuntu 22.04 / Ubuntu 版本", ubuntu_ok, ubuntu_detail)
    results["ubuntu"] = ubuntu_ok

    # ---------- 第二部分：硬件资源 ----------
    # ---------- Part 2: Hardware Resources ----------
    print_header("2. 硬件资源 (Hardware Resources)")

    disk_ok, disk_detail = check_disk_space()
    print_check("Disk space (>= 15GB) / 磁盘空间", disk_ok, disk_detail)
    results["disk"] = disk_ok

    mem_ok, mem_detail = check_memory()
    print_check("Memory (>= 8GB) / 内存", mem_ok, mem_detail)
    results["memory"] = mem_ok

    gpu_ok, gpu_detail = check_gpu()
    print_check("GPU access / GPU 支持", gpu_ok, gpu_detail)
    results["gpu"] = gpu_ok

    wslg_ok, wslg_detail = check_wslg()
    print_check("WSLg (GUI support) / GUI 支持", wslg_ok, wslg_detail)
    results["wslg"] = wslg_ok

    # ---------- 第三部分：已安装软件 ----------
    # ---------- Part 3: Installed Software ----------
    print_header("3. 已安装软件 (Installed Software)")

    ros_ok, ros_detail = check_ros2()
    print_check("ROS 2 Humble", ros_ok, ros_detail)
    results["ros2"] = ros_ok

    gz_ok, gz_detail = check_gazebo()
    print_check("Classic Gazebo 11", gz_ok, gz_detail)
    results["gazebo"] = gz_ok

    ws_ok, ws_detail = check_create3_ws()
    print_check("create3_ws workspace / 工作空间", ws_ok, ws_detail)
    results["workspace"] = ws_ok

    # ---------- 总结 ----------
    # ---------- Summary ----------
    print_header("📊 Summary / 总结")

    # 必需项
    # Required items
    required = ["wsl", "wsl_version", "ubuntu"]
    required_ok = all(results.get(k, False) for k in required)

    # 推荐项
    # Recommended items
    recommended = ["disk", "memory", "gpu", "wslg"]
    rec_count = sum(1 for k in recommended if results.get(k, False))

    # 软件项
    # Software items
    software = ["ros2", "gazebo", "workspace"]
    sw_count = sum(1 for k in software if results.get(k, False))

    if required_ok and rec_count >= 3 and sw_count == 3:
        print("  🎉 All checks passed! Environment is ready.")
        print("     所有检查通过！环境已就绪。")
        print("     You can proceed to run the Gazebo simulation.")
        print("     可以开始运行 Gazebo 仿真了。")
    elif required_ok and sw_count < 3:
        print("  ⚡ WSL2 environment is ready, but software needs to be installed.")
        print("     WSL2 环境已就绪，但需要安装软件。")
        print("     Run: python install_env.py")
        print("     运行: python install_env.py")
    elif not required_ok:
        print("  ⚠️  WSL2 + Ubuntu 22.04 is required but not ready.")
        print("     需要 WSL2 + Ubuntu 22.04 但尚未就绪。")
        if not results.get("wsl"):
            print("     → Install WSL: wsl --install / 安装 WSL: wsl --install")
        elif not results.get("ubuntu"):
            print("     → Install Ubuntu 22.04: wsl --install -d Ubuntu-22.04")
            print("       安装 Ubuntu 22.04: wsl --install -d Ubuntu-22.04")

    if not results.get("gpu", False):
        print("\n  💡 GPU not detected in WSL. Gazebo may run slowly.")
        print("     WSL 中未检测到 GPU。Gazebo 运行可能较慢。")
        print("     Update your GPU driver for WSL2 support.")

    if not results.get("wslg", False) and required_ok:
        print("\n  💡 WSLg not detected. You may need an X server (VcXsrv).")
        print("     未检测到 WSLg。可能需要 X server（VcXsrv）。")

    print()


if __name__ == "__main__":
    main()
