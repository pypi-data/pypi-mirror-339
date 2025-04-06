#!/usr/bin/env python
# coding=utf-8
"""
Author: Liu Kun && 16031215@qq.com
Date: 2025-04-04 20:17:42
LastEditors: Liu Kun && 16031215@qq.com
LastEditTime: 2025-04-04 20:17:45
FilePath: \\Python\\My_Funcs\\OAFuncs\\oafuncs\\oa_tool.py
Description:
EditPlatform: vscode
ComputerInfo: XPS 15 9510
SystemInfo: Windows 11
Python Version: 3.12
"""
from typing import Iterable

__all__ = ["PEx", "email", "pbar"]

class PEx:
    """
    PEx 封装了 ParallelExecutor，
    并将其方法全部委托，使得直接调用 PEx 的方法能够达到与 ParallelExecutor 相同的效果。

    示例:
        # 创建 PEx 实例
        executor = PEx(max_workers=4)

        # 使用 run 方法执行并行任务
        result = executor.run(lambda x: x * x, [(i,) for i in range(5)])
        print(result)  # 输出: [0, 1, 4, 9, 16]
    """

    try:
        from ._script.parallel import ParallelExecutor
    except ImportError:
        raise ImportError("ParallelExecutor could not be imported. Ensure the module '_script.parallel' exists and is accessible.")

    def __init__(self, *args, **kwargs):
        """
        初始化 PEx 实例，内部创建一个 ParallelExecutor 实例。

        参数:
            *args: 传递给 ParallelExecutor 的位置参数。
            **kwargs: 传递给 ParallelExecutor 的关键字参数。
        """
        self.executor = self.ParallelExecutor(*args, **kwargs)

    def __getattr__(self, attr):
        """
        将所有未定义的属性访问委托给内部的 ParallelExecutor 实例。

        参数:
            attr (str): 要访问的属性名称。

        返回:
            对应属性的值。
        """
        return getattr(self.executor, attr)


def email(title="Title", content=None, send_to="16031215@qq.com"):
    from ._script.email import send
    send(title, content, send_to)


def pbar(iterable: Iterable, description: str = "Working ...", color: str = "cyan", cmap: str = None, lupdate_interval: float = 0.1, bar_length: int = None, **kwargs) -> Iterable:
    """
    快速创建进度条的封装函数
    :param iterable: 可迭代对象
    :param prefix: 进度条前缀
    :param color: 基础颜色
    :param cmap: 渐变色名称
    :param kwargs: 其他ColorProgressBar支持的参数

    example:
    from oafuncs.oa_data import pbar
    from time import sleep
    for i in pbar(range(100), prefix="Processing", color="green", cmap="viridis"):
        sleep(0.1)
    """
    from ._script.cprogressbar import ColorProgressBar

    return ColorProgressBar(iterable=iterable, description=description, color=color, cmap=cmap, update_interval=lupdate_interval, bar_length=bar_length, **kwargs)
