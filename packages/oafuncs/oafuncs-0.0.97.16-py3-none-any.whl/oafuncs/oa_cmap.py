from typing import List, Optional, Union

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from rich import print

__all__ = ["show", "to_color", "create", "get"]


# ** 将cmap用填色图可视化（官网摘抄函数）
def show(colormaps: Union[str, mpl.colors.Colormap, List[Union[str, mpl.colors.Colormap]]]) -> None:
    """
    Description:
        Helper function to plot data with associated colormap.
    Parameters:
        colormaps : list of colormaps, or a single colormap; can be a string or a colormap object.
    Example:
        cmap = ListedColormap(["darkorange", "gold", "lawngreen", "lightseagreen"])
        show([cmap]); show("viridis"); show(["viridis", "cividis"])
    """
    if not isinstance(colormaps, list):
        colormaps = [colormaps]
    np.random.seed(19680801)
    data = np.random.randn(30, 30)
    n = len(colormaps)
    fig, axs = plt.subplots(1, n, figsize=(n * 2 + 2, 3), constrained_layout=True, squeeze=False)
    for ax, cmap in zip(axs.flat, colormaps):
        psm = ax.pcolormesh(data, cmap=cmap, rasterized=True, vmin=-4, vmax=4)
        fig.colorbar(psm, ax=ax)
    plt.show()


# ** 将cmap转为list，即多个颜色的列表
def to_color(cmap_name: str, n: int = 256) -> List[tuple]:
    """
    Description:
        Convert a colormap to a list of colors
    Parameters:
        cmap_name : str; the name of the colormap
        n         : int, optional; the number of colors
    Return:
        out_colors : list of colors
    Example:
        out_colors = to_color('viridis', 256)
    """
    cmap = mpl.colormaps.get_cmap(cmap_name)
    return [cmap(i) for i in np.linspace(0, 1, n)]


# ** 自制cmap，多色，可带位置
def create(color_list: Optional[List[Union[str, tuple]]] = None, rgb_file_path: Optional[str] = None, positions: Optional[List[float]] = None, under_color: Optional[Union[str, tuple]] = None, over_color: Optional[Union[str, tuple]] = None, delimiter: str = ",") -> mpl.colors.Colormap:
    """
    Description:
        Create a custom colormap from a list of colors or an RGB txt document.
    Parameters:
        color_list  : list of colors (optional, required if rgb_file_path is None)
        rgb_file_path : str, the path of txt file (optional, required if color_list is None)
        positions   : list of positions (optional, for color_list)
        under_color : color (optional)
        over_color  : color (optional)
        delimiter   : str, optional, default is ','; the delimiter of RGB values in txt file
    Return:
        cmap : colormap
    Example:
        cmap = create(color_list=['#C2B7F3','#B3BBF2','#B0CBF1','#ACDCF0','#A8EEED'])
        cmap = create(color_list=['aliceblue','skyblue','deepskyblue'], positions=[0.0,0.5,1.0])
        cmap = create(rgb_file_path='path/to/file.txt', delimiter=',')
    """
    if rgb_file_path:
        with open(rgb_file_path) as fid:
            data = fid.readlines()
        n = len(data)
        rgb = np.zeros((n, 3))
        for i in np.arange(n):
            rgb[i][0] = data[i].split(delimiter)[0]
            rgb[i][1] = data[i].split(delimiter)[1]
            rgb[i][2] = data[i].split(delimiter)[2]
        max_rgb = np.max(rgb)
        if max_rgb > 2:  # if the value is greater than 2, it is normalized to 0-1
            rgb = rgb / 255.0
        cmap_color = mpl.colors.ListedColormap(rgb, name="my_color")
    elif color_list:
        if positions is None:  # 自动分配比例
            cmap_color = mpl.colors.LinearSegmentedColormap.from_list("mycmap", color_list)
        else:  # 按提供比例分配
            cmap_color = mpl.colors.LinearSegmentedColormap.from_list("mycmap", list(zip(positions, color_list)))
    else:
        raise ValueError("Either 'color_list' or 'rgb_file_path' must be provided.")

    if under_color is not None:
        cmap_color.set_under(under_color)
    if over_color is not None:
        cmap_color.set_over(over_color)
    return cmap_color


# ** 选择cmap
def get(cmap_name: Optional[str] = None, query: bool = False) -> Optional[mpl.colors.Colormap]:
    """
    Description:
        Choosing a colormap from the list of available colormaps or a custom colormap
    Parameters:
        cmap_name : str, optional; the name of the colormap
        query     : bool, optional; whether to query the available colormap names
    Return:
        cmap : colormap
    Example:
        cmap = get('viridis')
        cmap = get('diverging_1')
        cmap = get('cool_1')
        cmap = get('warm_1')
        cmap = get('colorful_1')
    """
    my_cmap_dict = {
        "diverging_1": create(["#4e00b3", "#0000FF", "#00c0ff", "#a1d3ff", "#DCDCDC", "#FFD39B", "#FF8247", "#FF0000", "#FF5F9E"]),
        "cool_1": create(["#4e00b3", "#0000FF", "#00c0ff", "#a1d3ff", "#DCDCDC"]),
        "warm_1": create(["#DCDCDC", "#FFD39B", "#FF8247", "#FF0000", "#FF5F9E"]),
        "colorful_1": create(["#6d00db", "#9800cb", "#F2003C", "#ff4500", "#ff7f00", "#FE28A2", "#FFC0CB", "#DDA0DD", "#40E0D0", "#1a66f2", "#00f7fb", "#8fff88", "#E3FF00"]),
    }

    if query:
        print("Available cmap names:")
        print("-" * 20)
        print("Defined by myself:")
        print("\n".join(my_cmap_dict.keys()))
        print("-" * 20)
        print("Matplotlib built-in:")
        print("\n".join(mpl.colormaps.keys()))
        print("-" * 20)
        return None

    if cmap_name is None:
        return None

    if cmap_name in my_cmap_dict:
        return my_cmap_dict[cmap_name]
    else:
        try:
            return mpl.colormaps.get_cmap(cmap_name)
        except ValueError:
            print(f"Unknown cmap name: {cmap_name}\nNow return 'rainbow' as default.")
            return mpl.colormaps.get_cmap("rainbow")  # 默认返回 'rainbow'


if __name__ == "__main__":
    # ** 测试自制cmap
    colors = ["#C2B7F3", "#B3BBF2", "#B0CBF1", "#ACDCF0", "#A8EEED"]
    nodes = [0.0, 0.2, 0.4, 0.6, 1.0]
    c_map = create(colors, nodes)
    show([c_map])

    # ** 测试自制diverging型cmap
    diverging_cmap = create(["#4e00b3", "#0000FF", "#00c0ff", "#a1d3ff", "#DCDCDC", "#FFD39B", "#FF8247", "#FF0000", "#FF5F9E"])
    show([diverging_cmap])

    # ** 测试根据RGB的txt文档制作色卡
    file_path = "E:/python/colorbar/test.txt"
    cmap_rgb = create(rgb_file_path=file_path)

    # ** 测试将cmap转为list
    out_colors = to_color("viridis", 256)
