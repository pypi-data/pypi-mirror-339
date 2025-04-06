from typing import Any, Iterable, List, Optional, Union

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
        初始化 PEx 实例，内部创建一个 ParallelExecutor 实例

        参数:
            *args: 传递给 ParallelExecutor 的位置参数。
            **kwargs: 传递给 ParallelExecutor 的关键字参数。
        """
        self.executor = self.ParallelExecutor(*args, **kwargs)

    def __getattr__(self, attr):
        """
        将所有未定义的属性访问委托给内部的 ParallelExecutor 实例

        参数:
            attr (str): 要访问的属性名称。

        返回:
            对应属性的值。
        """
        return getattr(self.executor, attr)


def email(title="Title", content=None, send_to="10001@qq.com"):
    from ._script.email import send

    send(title, content, send_to)


def pbar(
    iterable: Iterable=range(100),
    description: str = "Working...",
    total: Optional[float] = None,
    completed: float = 0,
    color: Any = "cyan",
    cmap: Union[str, List[str], None] = None,
    update_interval: float = 0.1,
    bar_length: Optional[int] = None,
    speed_estimate_period: float = 30.0,
    next_line: bool = False,
):
    from ._script.cprogressbar import ColorProgressBar

    """便捷函数，返回 ColorProgressBar 对象"""
    return ColorProgressBar(
        iterable=iterable,
        description=description,
        total=total,
        completed=completed,
        color=color,
        cmap=cmap,
        update_interval=update_interval,
        bar_length=bar_length,
        speed_estimate_period=speed_estimate_period,
        next_line=next_line,
    )
