
# -*- codeing = utf-8 -*-
# @Name：hhUtils
# @Version：1.0.0
# @Author：立树
# @CreateTime：2025-03-31 01:48

"""
功能：
- getAbsolutePath 获取当前文件相对路径的绝对路径
- importModule 动态导入包
"""

import sys
import os
import importlib
# from pathlib import Path

# 获取当前文件相对路径的绝对路径
# 调用方式：getAbsolutePath("../", 2)
def getAbsolutePath(path = "", depth = 1):
    try:
        # 获取调用者的文件路径
        caller_frame = sys._getframe(depth)  # 获取调用方的栈帧
        caller_path = os.path.abspath(caller_frame.f_code.co_filename)
        # print(f"[ 调用者文件路径 ] - {caller_path}")

        # 获取当前文件的文件夹路径
        curDir = os.path.dirname(caller_path)
        # 加入路径参数
        resDir = os.path.join(curDir, path)
        # 获取绝对路径
        absDir = os.path.abspath(resDir)
        return absDir
    except Exception as err:
        return path

# 获取当前文件的上级目录（绝对路径）
# 调用方式：getParentDir(__file__)
# def getParentDir(filePath):
#     return Path(filePath).resolve().parent.parent

# 动态导入包
# 调用方式：importModule("../../src/hhframe/hhUtils")
def importModule(modulePath):
    if "/" in modulePath:
        # 获取模块路径、模块名称
        moduleDir, moduleName = os.path.split(modulePath)

        # 追加模块查询目录
        moduleDir = getAbsolutePath(moduleDir, depth = 2)
        sys.path.append(moduleDir)

        # 导入模块
        module = importlib.import_module(moduleName)
        return module
    else:
        module = importlib.import_module(modulePath)
        return module
