#!/usr/bin/env python
# coding=utf-8
"""
Author: Liu Kun && 16031215@qq.com
Date: 2024-09-17 17:26:11
LastEditors: Liu Kun && 16031215@qq.com
LastEditTime: 2024-11-21 13:10:47
FilePath: \\Python\\My_Funcs\\OAFuncs\\oafuncs\\oa_draw.py
Description:
EditPlatform: vscode
ComputerInfo: XPS 15 9510
SystemInfo: Windows 11
Python Version: 3.11
"""

import warnings

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from cartopy.mpl.ticker import LatitudeFormatter, LongitudeFormatter
from rich import print

__all__ = ["fig_minus", "gif", "add_cartopy", "add_gridlines", "MidpointNormalize", "add_lonlat_unit"]

warnings.filterwarnings("ignore")


def fig_minus(ax_x: plt.Axes = None, ax_y: plt.Axes = None, cbar: mpl.colorbar.Colorbar = None, decimal: int = None, add_space: bool = False) -> plt.Axes | mpl.colorbar.Colorbar | None:
    """
    Description: 将坐标轴刻度中的负号替换为减号

    param {*} ax_x : x轴
    param {*} ax_y : y轴
    param {*} cbar : colorbar
    param {*} decimal : 小数位数
    param {*} add_space : 是否在非负数前面加空格

    return {*} ax_x or ax_y or cbar
    """
    if ax_x is not None:
        current_ticks = ax_x.get_xticks()
    if ax_y is not None:
        current_ticks = ax_y.get_yticks()
    if cbar is not None:
        current_ticks = cbar.get_ticks()
    # 先判断是否需要加空格，如果要，先获取需要加的索引
    if add_space:
        index = 0
        for _, tick in enumerate(current_ticks):
            if tick >= 0:
                index = _
                break
    if decimal is not None:
        # my_ticks = [(round(float(iii), decimal)) for iii in my_ticks]
        current_ticks = [f"{val:.{decimal}f}" if val != 0 else "0" for val in current_ticks]

    out_ticks = [f"{val}".replace("-", "\u2212") for val in current_ticks]
    if add_space:
        # 在非负数前面加两个空格
        out_ticks[index:] = ["  " + m for m in out_ticks[index:]]

    if ax_x is not None:
        ax_x.set_xticklabels(out_ticks)
        return ax_x
    if ax_y is not None:
        ax_y.set_yticklabels(out_ticks)
        return ax_y
    if cbar is not None:
        cbar.set_ticklabels(out_ticks)
        return cbar


# ** 将生成图片/已有图片制作成动图
def gif(image_list: list[str], gif_name: str, duration: float = 200, resize: tuple[int, int] = None) -> None:  # 制作动图，默认间隔0.2
    """
    Description
        Make gif from images
    Parameters
        image_list : list, list of images
        gif_name : str, name of gif
        duration : float, duration of each frame, units: ms
        resize : tuple, (width, height) to resize images, if None, use first image size
    Returns
        None
    Example
        gif(["1.png", "2.png"], "test.gif", duration=0.2)
    """
    import imageio.v2 as imageio
    import numpy as np
    from PIL import Image

    frames = []

    # 获取目标尺寸
    if resize is None and image_list:
        # 使用第一张图片的尺寸作为标准
        with Image.open(image_list[0]) as img:
            resize = img.size

    # 读取并调整所有图片的尺寸
    for image_name in image_list:
        with Image.open(image_name) as img:
            if resize:
                img = img.resize(resize, Image.LANCZOS)
            frames.append(np.array(img))

    # 修改此处：明确使用 duration 值，并将其作为每帧的持续时间（以秒为单位）
    # 某些版本的 imageio 可能需要以毫秒为单位，或者使用 fps 参数
    try:
        # 先尝试直接使用 duration 参数（以秒为单位）
        imageio.mimsave(gif_name, frames, format="GIF", duration=duration)
    except Exception as e:
        print(f"尝试使用fps参数替代duration: {e}")
        # 如果失败，尝试使用 fps 参数（fps = 1/duration）
        fps = 1.0 / duration if duration > 0 else 5.0
        imageio.mimsave(gif_name, frames, format="GIF", fps=fps)

    print(f"Gif制作完成！尺寸: {resize}, 帧间隔: {duration}毫秒")
    return


# ** 转化经/纬度刻度
def add_lonlat_unit(lon: list[float] = None, lat: list[float] = None, decimal: int = 2) -> tuple[list[str], list[str]] | list[str]:
    """
    param        {*} lon : 经度列表
    param        {*} lat : 纬度列表
    param        {*} decimal : 小数位数
    return       {*} 转化后的经/纬度列表
    example     : add_lonlat_unit(lon=lon, lat=lat, decimal=2)
    """

    def _format_longitude(x_list):
        out_list = []
        for x in x_list:
            if x > 180:
                x -= 360
            # degrees = int(abs(x))
            degrees = round(abs(x), decimal)
            direction = "E" if x >= 0 else "W"
            out_list.append(f"{degrees:.{decimal}f}°{direction}" if x != 0 and x != 180 else f"{degrees}°")
        return out_list if len(out_list) > 1 else out_list[0]

    def _format_latitude(y_list):
        out_list = []
        for y in y_list:
            if y > 90:
                y -= 180
            # degrees = int(abs(y))
            degrees = round(abs(y), decimal)
            direction = "N" if y >= 0 else "S"
            out_list.append(f"{degrees:.{decimal}f}°{direction}" if y != 0 else f"{degrees}°")
        return out_list if len(out_list) > 1 else out_list[0]

    if lon and lat:
        return _format_longitude(lon), _format_latitude(lat)
    elif lon:
        return _format_longitude(lon)
    elif lat:
        return _format_latitude(lat)


# ** 添加网格线
def add_gridlines(ax: plt.Axes, xline: list[float] = None, yline: list[float] = None, projection: ccrs.Projection = ccrs.PlateCarree(), color: str = "k", alpha: float = 0.5, linestyle: str = "--", linewidth: float = 0.5) -> tuple[plt.Axes, mpl.ticker.Locator]:
    from matplotlib import ticker as mticker

    # add gridlines
    gl = ax.gridlines(crs=projection, draw_labels=True, linewidth=linewidth, color=color, alpha=alpha, linestyle=linestyle)
    gl.right_labels = False
    gl.top_labels = False
    gl.xformatter = LongitudeFormatter(zero_direction_label=False)
    gl.yformatter = LatitudeFormatter()

    if xline is not None:
        gl.xlocator = mticker.FixedLocator(np.array(xline))
    if yline is not None:
        gl.ylocator = mticker.FixedLocator(np.array(yline))

    return ax, gl


# ** 添加地图
def add_cartopy(ax: plt.Axes, lon: np.ndarray = None, lat: np.ndarray = None, projection: ccrs.Projection = ccrs.PlateCarree(), gridlines: bool = True, landcolor: str = "lightgrey", oceancolor: str = "lightblue", cartopy_linewidth: float = 0.5) -> None:
    # add coastlines
    ax.add_feature(cfeature.LAND, facecolor=landcolor)
    ax.add_feature(cfeature.OCEAN, facecolor=oceancolor)
    ax.add_feature(cfeature.COASTLINE, linewidth=cartopy_linewidth)
    # ax.add_feature(cfeature.BORDERS, linewidth=cartopy_linewidth, linestyle=":")

    # add gridlines
    if gridlines:
        ax, gl = add_gridlines(ax, projection=projection)

    # set longitude and latitude format
    lon_formatter = LongitudeFormatter(zero_direction_label=False)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

    # set extent
    if lon is not None and lat is not None:
        lon_min, lon_max = np.nanmin(lon), np.nanmax(lon)
        lat_min, lat_max = np.nanmin(lat), np.nanmax(lat)
        ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=projection)


# ** 自定义归一化类，使得0值处为中心点
class MidpointNormalize(mpl.colors.Normalize):
    """
    Description: 自定义归一化类，使得0值处为中心点

    param {*} mpl.colors.Normalize : 继承Normalize类
    return {*}

    Example:
    nrom = MidpointNormalize(vmin=-2, vmax=1, vcenter=0)
    """

    def __init__(self, vmin: float = None, vmax: float = None, vcenter: float = None, clip: bool = False) -> None:
        self.vcenter = vcenter
        super().__init__(vmin, vmax, clip)

    def __call__(self, value: np.ndarray, clip: bool = None) -> np.ma.MaskedArray:
        x, y = [self.vmin, self.vcenter, self.vmax], [0, 0.5, 1.0]
        return np.ma.masked_array(np.interp(value, x, y, left=-np.inf, right=np.inf))

    def inverse(self, value: np.ndarray) -> np.ndarray:
        y, x = [self.vmin, self.vcenter, self.vmax], [0, 0.5, 1]
        return np.interp(value, x, y, left=-np.inf, right=np.inf)



if __name__ == "__main__":
    pass
