import numpy as np
import os
import netCDF4 as nc
import xarray as xr


def _numpy_to_nc_type(numpy_type):
    """将NumPy数据类型映射到NetCDF数据类型"""
    numpy_to_nc = {
        "float32": "f4",
        "float64": "f8",
        "int8": "i1",
        "int16": "i2",
        "int32": "i4",
        "int64": "i8",
        "uint8": "u1",
        "uint16": "u2",
        "uint32": "u4",
        "uint64": "u8",
    }
    # 确保传入的是字符串类型，如果不是，则转换为字符串
    numpy_type_str = str(numpy_type) if not isinstance(numpy_type, str) else numpy_type
    return numpy_to_nc.get(numpy_type_str, "f4")  # 默认使用 'float32'


def _calculate_scale_and_offset(data, n=16):
    if not isinstance(data, np.ndarray):
        raise ValueError("Input data must be a NumPy array.")

    # 使用 nan_to_num 来避免 NaN 值对 min 和 max 的影响
    data_min = np.nanmin(data)
    data_max = np.nanmax(data)

    if np.isnan(data_min) or np.isnan(data_max):
        raise ValueError("Input data contains NaN values, which are not allowed.")

    scale_factor = (data_max - data_min) / (2**n - 1)
    add_offset = data_min + 2 ** (n - 1) * scale_factor

    return scale_factor, add_offset


def save_to_nc(file, data, varname=None, coords=None, mode="w", scale_offset_switch=True, compile_switch=True):
    """
    Description:
        Write data to NetCDF file
    Parameters:
        file: str, file path
        data: data
        varname: str, variable name
        coords: dict, coordinates, key is the dimension name, value is the coordinate data
        mode: str, write mode, 'w' for write, 'a' for append
        scale_offset_switch: bool, whether to use scale_factor and add_offset, default is True
        compile_switch: bool, whether to use compression parameters, default is True
    Example:
        save(r'test.nc', data, 'u', {'time': np.linspace(0, 120, 100), 'lev': np.linspace(0, 120, 50)}, 'a')
    """
    # 设置压缩参数
    kwargs = {"zlib": True, "complevel": 4} if compile_switch else {}

    # 检查文件存在性并根据模式决定操作
    if mode == "w" and os.path.exists(file):
        os.remove(file)
    elif mode == "a" and not os.path.exists(file):
        mode = "w"

    # 打开 NetCDF 文件
    with nc.Dataset(file, mode, format="NETCDF4") as ncfile:
        # 如果 data 是 DataArray 并且没有提供 varname 和 coords
        if varname is None and coords is None and isinstance(data, xr.DataArray):
            encoding = {}
            for var in data.data_vars:
                scale_factor, add_offset = _calculate_scale_and_offset(data[var].values)
                encoding[var] = {
                    "zlib": True,
                    "complevel": 4,
                    "dtype": "int16",
                    "scale_factor": scale_factor,
                    "add_offset": add_offset,
                    "_FillValue": -32767,
                }
            data.to_netcdf(file, mode=mode, encoding=encoding)
            return

        # 添加坐标
        for dim, coord_data in coords.items():
            if dim in ncfile.dimensions:
                if len(coord_data) != len(ncfile.dimensions[dim]):
                    raise ValueError(f"Length of coordinate '{dim}' does not match the dimension length.")
                else:
                    ncfile.variables[dim][:] = np.array(coord_data)
            else:
                ncfile.createDimension(dim, len(coord_data))
                var = ncfile.createVariable(dim, _numpy_to_nc_type(coord_data.dtype), (dim,), **kwargs)
                var[:] = np.array(coord_data)

                # 如果坐标数据有属性，则添加到 NetCDF 变量
                if isinstance(coord_data, xr.DataArray) and coord_data.attrs:
                    for attr_name, attr_value in coord_data.attrs.items():
                        var.setncattr(attr_name, attr_value)

        # 添加或更新变量
        if varname in ncfile.variables:
            if data.shape != ncfile.variables[varname].shape:
                raise ValueError(f"Shape of data does not match the variable shape for '{varname}'.")
            ncfile.variables[varname][:] = np.array(data)
        else:
            # 创建变量
            dim_names = tuple(coords.keys())
            if scale_offset_switch:
                scale_factor, add_offset = _calculate_scale_and_offset(np.array(data))
                dtype = "i2"
                var = ncfile.createVariable(varname, dtype, dim_names, fill_value=-32767, **kwargs)
                var.setncattr("scale_factor", scale_factor)
                var.setncattr("add_offset", add_offset)
            else:
                dtype = _numpy_to_nc_type(data.dtype)
                var = ncfile.createVariable(varname, dtype, dim_names, **kwargs)
            var[:] = np.array(data)

        # 添加属性
        if isinstance(data, xr.DataArray) and data.attrs:
            for key, value in data.attrs.items():
                if key not in ["scale_factor", "add_offset", "_FillValue", "missing_value"] or not scale_offset_switch:
                    var.setncattr(key, value)