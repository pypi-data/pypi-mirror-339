from typing import Any, Iterable, List, Optional, Union

from rich import print

__all__ = ["PEx", "email", "pbar"]


class PEx:
    """
    PEx wraps ParallelExecutor and delegates all its methods,
    allowing direct calls to PEx methods to achieve the same effect as ParallelExecutor.

    Example:
        # Create a PEx instance
        executor = PEx(max_workers=4)

        # Use the run method to execute parallel tasks
        result = executor.run(lambda x: x * x, [(i,) for i in range(5)])
        print(result)  # Output: [0, 1, 4, 9, 16]
    """

    try:
        from ._script.parallel import ParallelExecutor
    except ImportError:
        raise ImportError("[red]ParallelExecutor could not be imported. Ensure the module '_script.parallel' exists and is accessible.[/red]")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialize a PEx instance, internally creating a ParallelExecutor instance.

        Args:
            *args: Positional arguments passed to ParallelExecutor.
            **kwargs: Keyword arguments passed to ParallelExecutor.
        """
        self.executor = self.ParallelExecutor(*args, **kwargs)

    def __getattr__(self, attr: str) -> Any:
        """
        Delegate all undefined attribute access to the internal ParallelExecutor instance.

        Args:
            attr (str): The name of the attribute to access.

        Returns:
            Any: The value of the corresponding attribute.
        """
        return getattr(self.executor, attr)


def email(title: str = "Title", content: Optional[str] = None, send_to: str = "10001@qq.com") -> None:
    """
    Send an email using the specified title, content, and recipient.

    Args:
        title (str): The title of the email. Defaults to "Title".
        content (Optional[str]): The content of the email. Defaults to None.
        send_to (str): The recipient's email address. Defaults to "10001@qq.com".
    """
    from ._script.email import send

    print(f"[green]Sending email to {send_to} with title: {title}[/green]")
    send(title, content, send_to)


def pbar(
    iterable: Iterable = range(100),
    description: str = "Working...",
    total: Optional[float] = None,
    completed: float = 0,
    color: Any = "cyan",
    cmap: Union[str, List[str], None] = None,
    update_interval: float = 0.1,
    bar_length: Optional[int] = None,
    speed_estimate_period: float = 30.0,
    next_line: bool = False,
) -> Any:
    """
    Convenience function to return a ColorProgressBar object.

    Args:
        iterable (Iterable): The iterable to track progress for. Defaults to range(100).
        description (str): Description text for the progress bar. Defaults to "Working...".
        total (Optional[float]): Total number of iterations. Defaults to None.
        completed (float): Number of completed iterations. Defaults to 0.
        color (Any): Color of the progress bar. Defaults to "cyan".
        cmap (Union[str, List[str], None]): Color map for the progress bar. Defaults to None.
        update_interval (float): Interval for updating the progress bar. Defaults to 0.1.
        bar_length (Optional[int]): Length of the progress bar. Defaults to None.
        speed_estimate_period (float): Period for speed estimation. Defaults to 30.0.
        next_line (bool): Whether to move to the next line after completion. Defaults to False.

    Returns:
        Any: An instance of ColorProgressBar.
    
    Example:
        >>> for i in pbar(range(10), description="Processing"):
        ...     time.sleep(0.1)
        >>> for i in pbar(range(10), description="Processing", color="green"):
        ...     time.sleep(0.1)
        >>> for i in pbar(range(10), description="Processing", cmap=["red", "green"]):
        ...     time.sleep(0.1)
        >>> for i in pbar(range(10), description="Processing", cmap="viridis"):
        ...     time.sleep(0.1)
    """
    from ._script.cprogressbar import ColorProgressBar

    print(f"[blue]{description}[/blue]")
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
