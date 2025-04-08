import os
import netCDF4 as nc
import numpy as np
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
    numpy_type_str = str(numpy_type) if not isinstance(numpy_type, str) else numpy_type
    return numpy_to_nc.get(numpy_type_str, "f4")


def _calculate_scale_and_offset(data, n=16):
    if not isinstance(data, np.ndarray):
        raise ValueError("Input data must be a NumPy array.")

    data_min = np.nanmin(data)
    data_max = np.nanmax(data)

    if np.isnan(data_min) or np.isnan(data_max):
        raise ValueError("Input data contains NaN values.")

    scale_factor = (data_max - data_min) / (2**n - 1)
    add_offset = data_min + 2 ** (n - 1) * scale_factor
    return scale_factor, add_offset


def save_to_nc(file, data, varname=None, coords=None, mode="w", scale_offset_switch=True, compile_switch=True):
    # 处理xarray对象的情况（当varname和coords都为None时）
    if varname is None and coords is None:
        if not isinstance(data, (xr.DataArray, xr.Dataset)):
            raise ValueError("When varname and coords are not provided, data must be an xarray object")

        encoding = {}
        if isinstance(data, xr.DataArray):
            if data.name is None:
                data = data.rename("data")
            varname = data.name
            encoding[varname] = {"zlib": compile_switch, "complevel": 4}
            if scale_offset_switch:
                scale, offset = _calculate_scale_and_offset(data.values)
                encoding[varname].update({"dtype": "int16", "scale_factor": scale, "add_offset": offset, "_FillValue": -32767})
            else:
                encoding[varname].update({"dtype": "float32", "_FillValue": np.nan})
        else:  # Dataset情况
            for var in data.data_vars:
                encoding[var] = {"zlib": compile_switch, "complevel": 4}
                if scale_offset_switch:
                    scale, offset = _calculate_scale_and_offset(data[var].values)
                    encoding[var].update({"dtype": "int16", "scale_factor": scale, "add_offset": offset, "_FillValue": -32767})
                else:
                    encoding[var].update({"dtype": "float32", "_FillValue": np.nan})

        try:
            data.to_netcdf(file, mode=mode, encoding=encoding)
            return
        except Exception as e:
            raise RuntimeError(f"Failed to save xarray object: {str(e)}") from e

    # 处理普通numpy数组的情况
    if mode == "w" and os.path.exists(file):
        os.remove(file)
    elif mode == "a" and not os.path.exists(file):
        mode = "w"

    try:
        with nc.Dataset(file, mode, format="NETCDF4") as ncfile:
            # 创建维度并写入坐标
            if coords is not None:
                for dim, values in coords.items():
                    if dim not in ncfile.dimensions:
                        ncfile.createDimension(dim, len(values))
                        var = ncfile.createVariable(dim, _numpy_to_nc_type(values.dtype), (dim,))
                        var[:] = values

            # 创建变量
            dims = list(coords.keys()) if coords else []
            if scale_offset_switch:
                scale, offset = _calculate_scale_and_offset(data)
                var = ncfile.createVariable(varname, "i2", dims, fill_value=-32767, zlib=compile_switch)
                var.scale_factor = scale
                var.add_offset = offset
            else:
                dtype = _numpy_to_nc_type(data.dtype)
                var = ncfile.createVariable(varname, dtype, dims, zlib=compile_switch)

            var[:] = data
    except Exception as e:
        raise RuntimeError(f"Failed to save netCDF4 file: {str(e)}") from e


if __name__ == "__main__":
    # Example usage
    data = xr.open_dataset(r"F:\roms_rst.nc")["u"]
    save_to_nc(r"F:\test.nc", data)

    # xarray测试
    data = xr.DataArray(np.random.rand(10, 20), dims=("x", "y"), name="temperature")
    save_to_nc(r"F:\test_xarray.nc", data)

    # numpy测试
    arr = np.random.rand(5, 3)
    coords = {"x": np.arange(5), "y": np.arange(3)}
    save_to_nc(r"F:\test_numpy.nc", arr, varname="data", coords=coords)
