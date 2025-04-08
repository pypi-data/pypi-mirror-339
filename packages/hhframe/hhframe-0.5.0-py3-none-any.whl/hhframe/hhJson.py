
# -*- codeing = utf-8 -*-
# @Name：hhJson
# @Version：1.1.0
# @Author：立树
# @CreateTime：2025-04-02 19:32
# @UpdateTime：2025-04-07 08:53

"""
功能：
- save        保存 json 文件功能
- read        读取 json 文件功能
- parse       解析 json 字符串功能
- stringify   字符串化 json 功能
- view        打印 json 功能
更新：
- read        新增 depth 参数
- save        新增 depth 参数
"""

import os
import json
# import types
from . import hhUtils
from .hhResult import Result

# 打印 json 功能（内部函数）
# def _printJson(self):
#     indent = self.indent if "indent" in self.__dict__ else 4
#     res = json.dumps(self.data, indent = indent, ensure_ascii = False, sort_keys = False)
#     print(res)
#     return self

# 保存 json 文件功能
# 功能描述：直接将 Python 对象‌写入文件‌，无需手动转换字符串
# 适用场景‌：需将数据持久化保存到文件时使用
# 参数说明：
# - file: 文件路径
# - data: Python 对象（如字典、列表）‌
# - indent: 缩进长度
def save(file = "", data = {}, indent = 4, depth = 2):
    # 状态
    result = Result().initMethod()
    result.state = True
    result.file = file
    result.filePath = filePath = hhUtils.getAbsolutePath(file, depth = depth)
    result.data = data
    result.indent = indent
    result.msg = ""
    # result.printJson = _printJson.__get__(result)              # 绑定方法 - 方式一
    # result.printJson = types.MethodType(_printJson, result)    # 绑定方法 - 方式二

    # 参数判断
    if str(file).endswith(".json") == False:
        return result.setState(False).setMsg("Error - 文件名后缀必须为 .json").print("error")
    
    # 校验 data 类型是否正确
    if type(data) != dict and type(data) != list and type(data) != tuple:
        return result.setState(False).setMsg("Error - data 类型错误，必须为有效 JSON（dict | list | tuple）").print("error")

    # 确保文件夹存在
    folderPath = os.path.split(filePath)[0]
    if os.path.exists(folderPath) == False:
        os.makedirs(folderPath)
    
    try:
        with open(filePath, "w", encoding = "utf-8") as f:
            json.dump(data, f, indent = indent, ensure_ascii = False, sort_keys = False)
        return result.setState(True).setMsg(f"JSON 文件保存成功").print("info")
    except Exception as err:
        return result.setState(False).setMsg(f"JSON 文件保存失败 - {str(err)}").print("error")

# 读取 json 文件功能
# 功能描述：读取文件内容并解析为 Python 对象（如字典、列表）‌
# 参数说明：
# - file: 文件路径
def read(file = "", depth = 2):
    # 状态
    result = Result().initMethod()
    result.state = True
    result.file = file
    result.filePath = filePath = hhUtils.getAbsolutePath(file, depth = depth)
    result.data = None
    result.msg = ""
    # result.printJson = _printJson.__get__(result)              # 绑定方法 - 方式一
    # result.printJson = types.MethodType(_printJson, result)    # 绑定方法 - 方式二

    # 参数判断
    if str(file).endswith(".json") == False:
        return result.setState(False).setMsg("Error - 文件名后缀必须为 .json").print("error")
    
    try:
        with open(filePath, "r", encoding = "utf-8") as f:
            result.data = json.load(f)
        return result.setState(True).setMsg(f"JSON 文件读取成功").print("info")
    except Exception as err:
        return result.setState(False).setMsg(f"JSON 文件读取失败 - {str(err)}").print("error")

# 字符串化 json 功能
# 功能描述：将 Python 对象（如字典、列表）‌转换为 JSON 格式的字符串
# 参数说明：
# - data: Python 对象（如字典、列表）‌
# - indent: 缩进长度
def stringify(data = {}, indent = 4):
    # 状态
    result = Result().initMethod()
    result.state = True
    result.data = ""
    result.msg = ""

    try:
        result.data = json.dumps(data, indent = indent, ensure_ascii = False, sort_keys = False)
        return result.setState(True).setMsg("JSON 字符串化成功").print("info")
    except Exception as err:
        return result.setState(False).setMsg(f"JSON 字符串化失败 - {str(err)}").print("error")

# 解析 json 字符串功能
# 功能描述：将 JSON 格式的字符串转换为 Python 对象（如字典、列表）‌
# 参数说明：
# - string: JSON 格式的字符串
def parse(string = ""):
    # 状态
    result = Result().initMethod()
    result.state = True
    result.data = None
    result.msg = ""

    try:
        result.data = json.loads(string)
        return result.setState(True).setMsg("JSON 解析成功").print("info")
    except Exception as err:
        return result.setState(False).setMsg(f"JSON 解析失败 - {str(err)}").print("error")

# 打印 json 功能
def view(data = {}):
    # 状态
    method = Result().initMethod().method
    result = json.dumps(data, indent = 4, ensure_ascii = False, sort_keys = False)

    print("\n")
    print(f"[ {method} ] - 数据如下：", )
    print(result)
    print("\n")
