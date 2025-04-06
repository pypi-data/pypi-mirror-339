#!/usr/bin/env python
# coding=utf-8
"""
Author: Liu Kun && 16031215@qq.com
Date: 2025-03-27 16:56:57
LastEditors: Liu Kun && 16031215@qq.com
LastEditTime: 2025-04-04 12:58:15
FilePath: \\Python\\My_Funcs\\OAFuncs\\oafuncs\\oa_date.py
Description:
EditPlatform: vscode
ComputerInfo: XPS 15 9510
SystemInfo: Windows 11
Python Version: 3.12
"""

import calendar
import datetime
from typing import List, Optional

__all__ = ["month_days", "hour_range", "adjust_time", "timeit"]


def month_days(year: int, month: int) -> int:
    return calendar.monthrange(year, month)[1]


def hour_range(start: str, end: str, interval: int = 6) -> List[str]:
    """
    Generate a list of datetime strings with a specified interval in hours.

    Args:
        start (str): Start date in the format "%Y%m%d%H".
        end (str): End date in the format "%Y%m%d%H".
        interval (int): Interval in hours between each datetime.

    Returns:
        list: List of datetime strings in the format "%Y%m%d%H".
    """
    date_s = datetime.datetime.strptime(start, "%Y%m%d%H")
    date_e = datetime.datetime.strptime(end, "%Y%m%d%H")
    date_list = []
    while date_s <= date_e:
        date_list.append(date_s.strftime("%Y%m%d%H"))
        date_s += datetime.timedelta(hours=interval)
    return date_list


def adjust_time(initial_time: str, amount: int, time_unit: str = "hours", output_format: Optional[str] = None) -> str:
    """
    Adjust a given initial time by adding a specified amount of time.

    Args:
        initial_time (str): Initial time in the format "yyyymmdd" to "yyyymmddHHMMSS".
                            Missing parts are assumed to be "0".
        amount (int): The amount of time to add.
        time_unit (str): The unit of time to add ("seconds", "minutes", "hours", "days").
        output_format (str, optional): Custom output format for the adjusted time. Defaults to None.

    Returns:
        str: The adjusted time as a string, formatted according to the output_format or time unit.
    """
    # Normalize the input time to "yyyymmddHHMMSS" format
    time_format = "%Y%m%d%H%M%S"
    initial_time = initial_time.ljust(14, "0")
    time_obj = datetime.datetime.strptime(initial_time, time_format)

    # Add the specified amount of time
    if time_unit == "seconds":
        time_obj += datetime.timedelta(seconds=amount)
    elif time_unit == "minutes":
        time_obj += datetime.timedelta(minutes=amount)
    elif time_unit == "hours":
        time_obj += datetime.timedelta(hours=amount)
    elif time_unit == "days":
        time_obj += datetime.timedelta(days=amount)
    else:
        raise ValueError("Invalid time unit. Use 'seconds', 'minutes', 'hours', or 'days'.")

    # Determine the output format
    if output_format:
        return time_obj.strftime(output_format)
    else:
        if time_unit == "seconds":
            default_format = "%Y%m%d%H%M%S"
        elif time_unit == "minutes":
            default_format = "%Y%m%d%H%M"
        elif time_unit == "hours":
            default_format = "%Y%m%d%H"
        elif time_unit == "days":
            default_format = "%Y%m%d"
        return time_obj.strftime(default_format)


class timeit:
    """
    A decorator to measure the execution time of a function.

    Usage:
        @timeit(log=True, print_time=True)
        def my_function():
            # Function code here

    Args:
        log (bool): Whether to log the execution time to a file. Defaults to False.
        print_time (bool): Whether to print the execution time to the console. Defaults to True.
    """

    def __init__(self, func, log: bool = False, print_time: bool = True):
        self.func = func
        self.log = log
        self.print_time = print_time

    def __call__(self, *args, **kwargs):
        start_time = datetime.datetime.now()
        result = self.func(*args, **kwargs)
        end_time = datetime.datetime.now()
        elapsed_time = (end_time - start_time).total_seconds()

        if self.print_time:
            print(f"Function '{self.func.__name__}' executed in {elapsed_time:.2f} seconds.")

        if self.log:
            with open("execution_time.log", "a") as log_file:
                log_file.write(f"{datetime.datetime.now()} - Function '{self.func.__name__}' executed in {elapsed_time:.2f} seconds.\n")

        return result
