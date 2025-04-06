#!/usr/bin/env python
# coding=utf-8
"""
Author: Liu Kun && 16031215@qq.com
Date: 2024-09-17 15:07:13
LastEditors: Liu Kun && 16031215@qq.com
LastEditTime: 2024-12-13 16:28:56
FilePath: \\Python\\My_Funcs\\OAFuncs\\oafuncs\\oa_file.py
Description:
EditPlatform: vscode
ComputerInfo: XPS 15 9510
SystemInfo: Windows 11
Python Version: 3.11
"""

import glob
import os
import re
import shutil


from rich import print

__all__ = ["find_file", "link_file", "copy_file", "rename_file", "move_file", "clear_folder", "remove_empty_folder", "remove", "file_size", "mean_size", "make_dir", "replace_content"]


# ** 查找文件，支持通配符
def find_file(parent_path, fname, mode="path"):
    """
    description:
    param {*} parent_path: The parent path where the files are located
    param {*} fname: The file name pattern to search for
    param {*} mode: 'path' to return the full path of the files, 'file' to return only the file names
    return {*} A list of file paths or file names if files are found, None otherwise
    """

    def natural_sort_key(s):
        """生成一个用于自然排序的键"""
        return [int(text) if text.isdigit() else text.lower() for text in re.split("([0-9]+)", s)]

    # 将parent_path和fname结合成完整的搜索路径
    search_pattern = os.path.join(str(parent_path), fname)

    # 使用glob模块查找所有匹配的文件
    matched_files = glob.glob(search_pattern)

    # 如果没有找到任何文件，则返回False
    if not matched_files:
        return None

    # 在find_files函数中替换natsorted调用
    matched_files = sorted(matched_files, key=natural_sort_key)

    # 根据mode参数决定返回的内容
    if mode == "file":
        # 只返回文件名
        result = [os.path.basename(file) for file in matched_files]
    else:  # 默认为'path'
        # 返回文件的绝对路径
        result = [os.path.abspath(file) for file in matched_files]

    return result


# ** 创建符号链接，支持通配符
def link_file(src_pattern, dst):
    """
    # 描述：创建符号链接，支持通配符
    # 使用示例
    # link_file(r'/data/hejx/liukun/era5/*', r'/data/hejx/liukun/Test/')
    # link_file(r'/data/hejx/liukun/era5/py.o*', r'/data/hejx/liukun/Test/py.o')
    # link_file(r'/data/hejx/liukun/era5/py.o*', r'/data/hejx/liukun/Test')
    param      {*} src_pattern # 源文件或目录
    param      {*} dst # 目标文件或目录
    """
    src_pattern = str(src_pattern)
    # 使用glob.glob来处理可能包含通配符的src
    src_files = glob.glob(src_pattern)
    if not src_files:
        raise FileNotFoundError("File does not exist: {}".format(src_pattern))

    # 判断dst是路径还是包含文件名的路径
    if os.path.isdir(dst):
        # 如果dst是路径，则保持源文件的文件名
        dst_dir = dst
        for src_file in src_files:
            src_file_basename = os.path.basename(src_file)
            dst_file = os.path.join(dst_dir, src_file_basename)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            os.symlink(src_file, dst_file)
            # print(f"创建符号链接: {src_file} -> {dst_file}")
            print(f"Create a symbolic link: {src_file} -> {dst_file}")
    else:
        # 如果dst包含文件名，则创建链接后重命名
        dst_dir = os.path.dirname(dst)
        os.makedirs(dst_dir, exist_ok=True)
        # 只处理第一个匹配的文件
        src_file = src_files[0]
        dst_file = dst
        if os.path.exists(dst_file):
            os.remove(dst_file)
        os.symlink(src_file, dst_file)
        # print(f"创建符号链接并重命名: {src_file} -> {dst_file}")
        print(f"Create a symbolic link and rename: {src_file} -> {dst_file}")


# ** 复制文件或目录，支持通配符
def copy_file(src_pattern, dst):
    """
    # 描述：复制文件或目录，支持通配符
    # 使用示例
    # copy_file(r'/data/hejx/liukun/era5/py.o*', r'/data/hejx/liukun/Test/py.o')
    # copy_file(r'/data/hejx/liukun/era5/py.o*', r'/data/hejx/liukun/Test')
    param      {*} src_pattern # 源文件或目录
    param      {*} dst # 目标文件或目录
    """
    src_pattern = str(src_pattern)
    # 使用glob.glob来处理可能包含通配符的src
    src_files = glob.glob(src_pattern)
    if not src_files:
        raise FileNotFoundError("File does not exist: {}".format(src_pattern))

    # 判断dst是路径还是包含文件名的路径
    if os.path.isdir(dst):
        # 如果dst是路径，则保持源文件的文件名
        dst_dir = dst
        for src_file in src_files:
            src_file_basename = os.path.basename(src_file)
            dst_file = os.path.join(dst_dir, src_file_basename)
            if os.path.exists(dst_file):
                if os.path.isdir(dst_file):
                    shutil.rmtree(dst_file)
                else:
                    os.remove(dst_file)
            if os.path.isdir(src_file):
                shutil.copytree(src_file, dst_file, symlinks=True)
            else:
                shutil.copy2(src_file, dst_file)
            print(f"Copy file or directory: {src_file} -> {dst_file}")
    else:
        # 如果dst包含文件名，则复制后重命名
        dst_dir = os.path.dirname(dst)
        os.makedirs(dst_dir, exist_ok=True)
        # 只处理第一个匹配的文件
        src_file = src_files[0]
        dst_file = dst
        if os.path.exists(dst_file):
            if os.path.isdir(dst_file):
                shutil.rmtree(dst_file)
            else:
                os.remove(dst_file)
        if os.path.isdir(src_file):
            shutil.copytree(src_file, dst_file, symlinks=True)
        else:
            shutil.copy2(src_file, dst_file)
        print(f"Copy and rename file or directory: {src_file} -> {dst_file}")


# ** 移动文件或目录，支持通配符
def move_file(src_pattern, dst):
    """
    # 描述：移动文件或目录，支持通配符
    # 使用示例
    # move_file(r'/data/hejx/liukun/era5/*', r'/data/hejx/liukun/Test/')
    # move_file(r'/data/hejx/liukun/era5/py.o*', r'/data/hejx/liukun/Test/py.o')
    # move_file(r'/data/hejx/liukun/era5/py.o*', r'/data/hejx/liukun/Test')
    param      {*} src_pattern # 源文件或目录
    param      {*} dst # 目标文件或目录
    """
    src_pattern = str(src_pattern)
    # 使用glob.glob来处理可能包含通配符的src
    src_files = glob.glob(src_pattern)
    if not src_files:
        raise FileNotFoundError("File does not exist: {}".format(src_pattern))

    # 判断dst是路径还是包含文件名的路径
    if os.path.isdir(dst):
        # 如果dst是路径，则保持源文件的文件名
        dst_dir = dst
        for src_file in src_files:
            src_file_basename = os.path.basename(src_file)
            dst_file = os.path.join(dst_dir, src_file_basename)
            if os.path.exists(dst_file):
                if os.path.isdir(dst_file):
                    shutil.rmtree(dst_file)
                else:
                    os.remove(dst_file)
            shutil.move(src_file, dst_file)
            print(f"Move file or directory: {src_file} -> {dst_file}")
    else:
        # 如果dst包含文件名，则移动后重命名
        dst_dir = os.path.dirname(dst)
        os.makedirs(dst_dir, exist_ok=True)
        # 只处理第一个匹配的文件
        src_file = src_files[0]
        dst_file = dst
        if os.path.exists(dst_file):
            if os.path.isdir(dst_file):
                shutil.rmtree(dst_file)
            else:
                os.remove(dst_file)
        shutil.move(src_file, dst_file)
        print(f"Move and rename file or directory: {src_file} -> {dst_file}")


# ** 重命名文件，支持通配符
def rename_file(directory, old_str, new_str):
    """
    # 描述：重命名目录下的文件，支持通配符
    # 使用示例
    directory_path = r"E:\\windfarm\\CROCO_FILES"
    old_str = "croco"
    new_str = "roms"
    rename_file(directory_path, old_str, new_str)
    param      {*} directory # 目录
    param      {*} old_str # 要替换的字符串
    param      {*} new_str # 新字符串
    """
    # 获取目录下的所有文件
    files = os.listdir(directory)

    # 构建正则表达式以匹配要替换的字符串
    pattern = re.compile(re.escape(old_str))

    # 遍历目录下的文件
    for filename in files:
        # 检查文件名中是否包含要替换的字符串
        if pattern.search(filename):
            # 构建新的文件名
            new_filename = pattern.sub(new_str, filename)

            # 构建旧文件的完整路径
            old_path = os.path.join(directory, filename)

            # 构建新文件的完整路径
            new_path = os.path.join(directory, new_filename)

            # 重命名文件
            os.rename(old_path, new_path)
            print(f"Rename file: {old_path} -> {new_path}")


# ** 创建路径
def make_dir(directory):
    """
    Description:
        Create a directory if it does not exist

    Parameters:
        directory: The directory path to create

    Returns:
        None

    Example:
        make_dir(r"E:\\Data\\2024\\09\\17\\var1")
    """
    directory = str(directory)
    if os.path.exists(directory):
        print(f"Directory already exists: {directory}")
        return
    else:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")


# ** 清空文件夹
def clear_folder(folder_path):
    """
    # 描述：清空文件夹
    # 使用示例
    clear_folder(r'E:\\Data\\2024\\09\\17\\var1')
    param        {*} folder_path # 文件夹路径
    """
    folder_path = str(folder_path)
    if os.path.exists(folder_path):
        try:
            # 遍历文件夹中的所有文件和子文件夹
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)
                # 判断是文件还是文件夹
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # 删除文件或链接
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # 删除子文件夹
            # print(f"成功清空文件夹: {folder_path}")
            print(f"Successfully cleared the folder: {folder_path}")
        except Exception as e:
            # print(f"清空文件夹失败: {folder_path}")
            print(f"Failed to clear the folder: {folder_path}")
            print(e)


# ** 清理空文件夹
def remove_empty_folder(path, print_info=1):
    """
    # 描述：清理空文件夹
    # 使用示例
    remove_empty_folder(r'E:\\Data\\2024\\09\\17', print_info=1)
    param        {*} path # 文件夹路径
    param        {*} print_info # 是否打印信息
    """
    path = str(path)
    # 遍历当前目录下的所有文件夹和文件
    for root, dirs, files in os.walk(path, topdown=False):
        # 遍历文件夹列表
        for folder in dirs:
            folder_path = os.path.join(root, folder)
            # 判断文件是否有权限访问
            try:
                os.listdir(folder_path)
            except OSError:
                continue
            # 判断文件夹是否为空
            if not os.listdir(folder_path):
                # 删除空文件夹
                try:
                    os.rmdir(folder_path)
                    print(f"Deleted empty folder: {folder_path}")
                except OSError:
                    if print_info:
                        print(f"Skipping protected folder: {folder_path}")
                    pass


# ** 删除相关文件，可使用通配符
def remove(pattern):
    """
    Delete files or directories that match the given wildcard pattern.

    Parameters:
    pattern : str
        File path or string containing wildcards. For example:
        - r'E:\\Code\\Python\\Model\\WRF\\Radar2\\bzip2-radar-0*'
        - 'bzip2-radar-0*' (assuming you are already in the target directory)

    Usage examples:
    remove(r'E:\\Code\\Python\\Model\\WRF\\Radar2\\bzip2-radar-0*')
    or
    os.chdir(r'E:\\Code\\Python\\Model\\WRF\\Radar2')
    remove('bzip2-radar-0*')

    last updated: 2025-01-10 11:49:13
    """
    pattern = str(pattern)

    # Use glob.glob to get all matching files or directories
    file_list = glob.glob(pattern)

    if not file_list:
        print(f"No files or directories found matching '{pattern}'.")
        return

    for file_path in file_list:
        if os.path.exists(file_path):
            try:
                if os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    print(f"Successfully deleted directory: {file_path}")
                else:
                    os.remove(file_path)
                    print(f"Successfully deleted file: {file_path}")
            except Exception as e:
                print(f"Deletion failed: {file_path}")
                print(f"Error message: {e}")
        else:
            print(f"File or directory does not exist: {file_path}")


# ** 获取文件大小
def file_size(file_path, unit="KB"):
    """
    Description: 获取文件大小

    Args:
    file_path: 文件路径
    unit: 单位（PB、TB、GB、MB、KB）

    Returns:
    文件大小（单位：PB、TB、GB、MB、KB）
    """
    # 检查文件是否存在
    if not os.path.exists(file_path):
        # return "文件不存在"
        # print(f"文件不存在: {file_path}\n返回0.0")
        print(f"File does not exist: {file_path}\nReturn 0.0")
        return 0.0

    # 获取文件大小（字节）
    file_size = os.path.getsize(file_path)

    # 单位转换字典
    unit_dict = {"PB": 1024**5, "TB": 1024**4, "GB": 1024**3, "MB": 1024**2, "KB": 1024}

    # 检查传入的单位是否合法
    if unit not in unit_dict:
        # return "单位不合法，请选择PB、TB、GB、MB、KB中的一个"
        # print("单位不合法，请选择PB、TB、GB、MB、KB中的一个\n返回0.0")
        print("Invalid unit, please choose one of PB, TB, GB, MB, KB\nReturn 0.0")
        return 0.0

    # 转换文件大小到指定单位
    converted_size = file_size / unit_dict[unit]

    return converted_size


# ** 计算文件夹下指定相关文件的平均大小
def mean_size(parent_path, fname, max_num=None, unit="KB"):
    """
    Description:
        Calculate the average size of the specified related files in the folder

    Parameters:
        parent_path: The parent path where the files are located
        fname: The file name pattern to search for
        max_num: The maximum number of files to search for
        unit: The unit of the file size, default is "KB"

    Returns:
        The average size
    """
    flist = find_file(parent_path, fname)
    if flist:
        if max_num:
            flist = flist[: int(max_num)]
        size_list = [file_size(f, unit) for f in flist if file_size(f, unit) > 0]
        if size_list:
            return sum(size_list) / len(size_list)
        else:
            return 0.0
    else:
        return 0.0


def replace_content(source_file, content_dict, key_value=False, target_dir=None, new_name=None):
    """
    直接替换文件中的指定内容并保存到新路径

    参数：
    source_file: 源文件路径
    target_dir: 目标目录路径
    content_dict: 要替换的内容字典 {旧内容: 新内容}
    key_value: 是否按键值对方式替换参数

    返回:
    bool: 替换是否成功
    """
    from ._script.replace_file_concent import replace_direct_content
    if target_dir is None:
        target_dir = os.path.dirname(source_file)
    replace_direct_content(source_file, target_dir, content_dict, key_value=key_value, new_name=new_name)


if __name__ == "__main__":
    # newpath = make_folder('D:/Data/2024/09/17/', 'var1', clear=1)
    # print(newpath)
    pass

    remove(r"I:\\Delete\\test\\*")
