#!/usr/bin/env python
# coding=utf-8
"""
Author: Liu Kun && 16031215@qq.com
Date: 2024-09-17 14:58:50
LastEditors: Liu Kun && 16031215@qq.com
LastEditTime: 2024-12-06 14:16:56
FilePath: \\Python\\My_Funcs\\OAFuncs\\oafuncs\\oa_nc.py
Description:
EditPlatform: vscode
ComputerInfo: XPS 15 9510
SystemInfo: Windows 11
Python Version: 3.11
"""

import os
from typing import List, Optional, Union, Tuple

import netCDF4 as nc
import numpy as np
import xarray as xr
from rich import print

__all__ = ["save", "merge", "modify", "rename", "check", "convert_longitude", "isel", "draw"]


def save(file: str, data: Union[np.ndarray, xr.DataArray], varname: Optional[str] = None, coords: Optional[dict] = None, mode: str = "w", scale_offset_switch: bool = True, compile_switch: bool = True) -> None:
    """
    Description:
        Write data to NetCDF file
    Parameters:
        file: str, file path
        data: np.ndarray or xr.DataArray, data to be written
        varname: Optional[str], variable name
        coords: Optional[dict], coordinates, key is the dimension name, value is the coordinate data
        mode: str, write mode, 'w' for write, 'a' for append
        scale_offset_switch: bool, whether to use scale_factor and add_offset, default is True
        compile_switch: bool, whether to use compression parameters, default is True
    Example:
        save(r'test.nc', data, 'u', {'time': np.linspace(0, 120, 100), 'lev': np.linspace(0, 120, 50)}, 'a')
    """
    from ._script.netcdf_write import save_to_nc

    save_to_nc(file, data, varname, coords, mode, scale_offset_switch, compile_switch)


def merge(file_list: Union[str, List[str]], var_name: Optional[Union[str, List[str]]] = None, dim_name: Optional[str] = None, target_filename: Optional[str] = None) -> None:
    """
    Description:
        Merge multiple NetCDF files into one.
    Parameters:
        file_list: Union[str, List[str]], list of file paths or a single file path
        var_name: Optional[Union[str, List[str]]], variable names to merge
        dim_name: Optional[str], dimension name to merge along
        target_filename: Optional[str], output file name
    """
    from ._script.netcdf_merge import merge_nc

    merge_nc(file_list, var_name, dim_name, target_filename)


def modify(nc_file: str, var_name: str, attr_name: Optional[str] = None, new_value: Optional[Union[str, float, int, np.ndarray]] = None) -> None:
    """
    Description:
        Modify the value of a variable or the value of an attribute in a NetCDF file.
    Parameters:
        nc_file: str, the path to the NetCDF file
        var_name: str, the name of the variable to be modified
        attr_name: Optional[str], the name of the attribute to be modified. If None, the variable value will be modified
        new_value: Optional[Union[str, float, int, np.ndarray]], the new value of the variable or attribute
    """
    from ._script.netcdf_modify import modify_nc

    modify_nc(nc_file, var_name, attr_name, new_value)


def rename(ncfile_path: str, old_name: str, new_name: str) -> None:
    """
    Description:
        Rename a variable and/or dimension in a NetCDF file.
    Parameters:
        ncfile_path: str, the path to the NetCDF file
        old_name: str, the current name of the variable or dimension
        new_name: str, the new name to assign to the variable or dimension
    """
    try:
        with nc.Dataset(ncfile_path, "r+") as dataset:
            # If the old name is not found as a variable or dimension, print a message
            if old_name not in dataset.variables and old_name not in dataset.dimensions:
                print(f"Variable or dimension {old_name} not found in the file.")

            # Attempt to rename the variable
            if old_name in dataset.variables:
                dataset.renameVariable(old_name, new_name)
                print(f"Successfully renamed variable {old_name} to {new_name}.")

            # Attempt to rename the dimension
            if old_name in dataset.dimensions:
                # Check if the new dimension name already exists
                if new_name in dataset.dimensions:
                    raise ValueError(f"Dimension name {new_name} already exists in the file.")
                dataset.renameDimension(old_name, new_name)
                print(f"Successfully renamed dimension {old_name} to {new_name}.")

    except Exception as e:
        print(f"An error occurred: {e}")


def check(ncfile: str, delete_switch: bool = False, print_switch: bool = True) -> bool:
    """
    Description:
        Check if a NetCDF file is corrupted with enhanced error handling.
    Parameters:
        ncfile: str, the path to the NetCDF file
        delete_switch: bool, whether to delete the file if it is corrupted
        print_switch: bool, whether to print messages during the check
    Returns:
        bool: True if the file is valid, False otherwise
    """
    is_valid = False

    if not os.path.exists(ncfile):
        if print_switch:
            print(f"[#ffeac5]Local file missing: [#009d88]{ncfile}")
            # 提示：提示文件缺失也许是正常的，这只是检查文件是否存在于本地
            print("[#d6d9fd]Note: File missing may be normal, this is just to check if the file exists locally.")
        return False

    try:
        # # 深度验证文件结构
        # with nc.Dataset(ncfile, "r") as ds:
        #     # 显式检查文件结构完整性
        #     ds.sync()  # 强制刷新缓冲区
        #     ds.close()  # 显式关闭后重新打开验证

        # 二次验证确保变量可访问
        with nc.Dataset(ncfile, "r") as ds_verify:
            if not ds_verify.variables:
                if print_switch:
                    print(f"[red]Empty variables: {ncfile}[/red]")
            else:
                # 尝试访问元数据
                _ = ds_verify.__dict__
                # 抽样检查第一个变量
                for var in ds_verify.variables.values():
                    _ = var.shape  # 触发实际数据访问
                    break
                is_valid = True

    except Exception as e:  # 捕获所有异常类型
        if print_switch:
            print(f"[red]HDF5 validation failed for {ncfile}: {str(e)}[/red]")
        error_type = type(e).__name__
        if "HDF5" in error_type or "h5" in error_type.lower():
            if print_switch:
                print(f"[red]Critical HDF5 structure error detected in {ncfile}[/red]")

    # 安全删除流程
    if not is_valid:
        if delete_switch:
            try:
                os.remove(ncfile)
                if print_switch:
                    print(f"[red]Removed corrupted file: {ncfile}[/red]")
            except Exception as del_error:
                if print_switch:
                    print(f"[red]Failed to delete corrupted file: {ncfile} - {str(del_error)}[/red]")
        return False

    return True


def convert_longitude(ds: xr.Dataset, lon_name: str = "longitude", convert: int = 180) -> xr.Dataset:
    """
    Description:
        Convert the longitude array to a specified range.
    Parameters:
        ds: xr.Dataset, the xarray dataset containing the longitude data
        lon_name: str, the name of the longitude variable, default is "longitude"
        convert: int, the target range to convert to, can be 180 or 360, default is 180
    Returns:
        xr.Dataset: The xarray dataset with the converted longitude
    """
    to_which = int(convert)
    if to_which not in [180, 360]:
        raise ValueError("convert value must be '180' or '360'")

    if to_which == 180:
        ds = ds.assign_coords({lon_name: (ds[lon_name] + 180) % 360 - 180})
    elif to_which == 360:
        ds = ds.assign_coords({lon_name: (ds[lon_name] + 360) % 360})

    return ds.sortby(lon_name)


def isel(ncfile: str, dim_name: str, slice_list: List[int]) -> xr.Dataset:
    """
    Description:
        Choose the data by the index of the dimension.
    Parameters:
        ncfile: str, the path of the netCDF file
        dim_name: str, the name of the dimension
        slice_list: List[int], the indices of the dimension
    Returns:
        xr.Dataset: The subset dataset
    """
    ds = xr.open_dataset(ncfile)
    slice_list = np.array(slice_list).flatten()
    slice_list = [int(i) for i in slice_list]
    ds_new = ds.isel(**{dim_name: slice_list})
    ds.close()
    return ds_new


def draw(output_dir: Optional[str] = None, dataset: Optional[xr.Dataset] = None, ncfile: Optional[str] = None, xyzt_dims: Union[List[str], Tuple[str, str, str, str]] = ("longitude", "latitude", "level", "time"), plot_type: str = "contourf", fixed_colorscale: bool = False) -> None:
    """
    Description:
        Draw the data in the netCDF file.
    Parameters:
        output_dir: Optional[str], the path of the output directory
        dataset: Optional[xr.Dataset], the xarray dataset to plot
        ncfile: Optional[str], the path of the netCDF file
        xyzt_dims: Union[List[str], Tuple[str, str, str, str]], the dimensions for plotting
        plot_type: str, the type of the plot, default is "contourf" (contourf, contour)
        fixed_colorscale: bool, whether to use fixed colorscale, default is False
    """
    from ._script.plot_dataset import func_plot_dataset

    if output_dir is None:
        output_dir = str(os.getcwd())
    if isinstance(xyzt_dims, (list, tuple)):
        xyzt_dims = tuple(xyzt_dims)
    else:
        raise ValueError("xyzt_dims must be a list or tuple")
    if dataset is not None:
        func_plot_dataset(dataset, output_dir, xyzt_dims, plot_type, fixed_colorscale)
    else:
        if ncfile is not None:
            if check(ncfile):
                ds = xr.open_dataset(ncfile)
                func_plot_dataset(ds, output_dir, xyzt_dims, plot_type, fixed_colorscale)
            else:
                print(f"Invalid file: {ncfile}")
        else:
            print("No dataset or file provided.")


if __name__ == "__main__":
    data = np.random.rand(100, 50)
    save(r"test.nc", data, "data", {"time": np.linspace(0, 120, 100), "lev": np.linspace(0, 120, 50)}, "a")
