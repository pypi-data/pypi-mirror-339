#!/usr/bin/env python
# coding=utf-8
"""
Author: Liu Kun && 16031215@qq.com
Date: 2025-03-27 16:51:26
LastEditors: Liu Kun && 16031215@qq.com
LastEditTime: 2025-04-05 14:17:07
FilePath: \\Python\\My_Funcs\\OAFuncs\\oafuncs\\oa_python.py
Description:
EditPlatform: vscode
ComputerInfo: XPS 15 9510
SystemInfo: Windows 11
Python Version: 3.12
"""

import os

from rich import print

__all__ = ["install_packages", "upgrade_packages"]


def install_packages(packages=None, python_executable="python", package_manager="pip"):
    """
    packages: list, libraries to be installed
    python_executable: str, Python version; for example, on Windows, copy python.exe to python312.exe, then set python_executable='python312'
    package_manager: str, the package manager to use ('pip' or 'conda')
    """
    if not isinstance(packages, (list, type(None))):
        raise ValueError("The 'packages' parameter must be a list or None")

    if package_manager not in ["pip", "conda"]:
        raise ValueError("The 'package_manager' parameter must be either 'pip' or 'conda'")

    if package_manager == "conda":
        if not packages:
            return
        try:
            package_count = len(packages)
            for i, package in enumerate(packages):
                os.system(f"conda install -c conda-forge {package} -y")
                print("-" * 100)
                print(f"Successfully installed {package} ({i + 1}/{package_count})")
                print("-" * 100)
        except Exception as e:
            print(f"Installation failed: {str(e)}")
        return

    os.system(f"{python_executable} -m ensurepip")
    os.system(f"{python_executable} -m pip install --upgrade pip")
    if not packages:
        return
    try:
        installed_packages = os.popen(f"{python_executable} -m pip list --format=freeze").read().splitlines()
        installed_packages = {pkg.split("==")[0].lower() for pkg in installed_packages}
        package_count = len(packages)
        for i, package in enumerate(packages):
            # Check if the library is already installed, skip if installed
            if package.lower() in installed_packages:
                print(f"{package} is already installed")
                continue
            os.system(f"{python_executable} -m pip install {package}")
            print("-" * 100)
            print(f"Successfully installed {package} ({i + 1}/{package_count})")
            print("-" * 100)
    except Exception as e:
        print(f"Installation failed: {str(e)}")


def upgrade_packages(packages=None, python_executable="python", package_manager="pip"):
    """
    packages: list, libraries to be upgraded
    python_executable: str, Python version; for example, on Windows, copy python.exe to python312.exe, then set python_executable='python312'
    package_manager: str, the package manager to use ('pip' or 'conda')
    """
    if not isinstance(packages, (list, type(None))):
        raise ValueError("The 'packages' parameter must be a list or None")

    if package_manager not in ["pip", "conda"]:
        raise ValueError("The 'package_manager' parameter must be either 'pip' or 'conda'")

    try:
        if package_manager == "conda":
            if not packages:
                installed_packages = os.popen("conda list --export").read().splitlines()
                packages = [pkg.split("=")[0] for pkg in installed_packages if not pkg.startswith("#")]
            for package in packages:
                os.system(f"conda update -c conda-forge {package} -y")
            print("Upgrade successful")
        else:
            if not packages:
                installed_packages = os.popen(f"{python_executable} -m pip list --format=freeze").read().splitlines()
                packages = [pkg.split("==")[0] for pkg in installed_packages]
            for package in packages:
                os.system(f"{python_executable} -m pip install --upgrade {package}")
            print("Upgrade successful")
    except Exception as e:
        print(f"Upgrade failed: {str(e)}")
