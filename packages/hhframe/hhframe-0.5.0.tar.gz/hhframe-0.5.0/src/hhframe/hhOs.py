
# -*- codeing = utf-8 -*-
# @Name：hhOs
# @Version：2.2.0
# @Author：立树
# @CreateTime：2021-07-04 02:19
# @UpdateTime：2025-04-03 20:30

"""
功能：
- readFile 读取文件功能
- writeFile 写入文件功能
- createFile 创建文件功能
- resetFile 重置文件功能
- editFile 修改文件功能
- copyFile 复制文件功能
- moveFile 移动文件功能
- isFile 判断是否是文件功能
- remove 删除文件和文件夹功能
- copyFolder 复制文件夹功能
- moveFolder 移动文件夹功能
- createFolder 创建文件夹功能
- getFolderList 获取文件夹列表功能
- isFolder 判断是否是文件夹功能
更新：
- 新增 isExist 判断文件或文件夹是否存在功能
"""

import os
import shutil
from . import hhUtils
from .hhResult import Result

# 打开文件（文本类型的文件）
# file: 文件路径（文件）
# encoding: 编码格式
def readFile(file = "", encoding = "utf-8"):
    # 状态
    result = Result().initMethod()
    result.state = True
    result.file = file
    result.filePath = filePath = hhUtils.getAbsolutePath(file, depth = 2)
    result.content = ""
    result.msg = ""

    # 参数判断
    if file == "":
        return result.setState(False).setMsg("Error - 缺少参数（file）").print("error")

    # 路径判断
    if not os.path.exists(filePath):
        return result.setState(False).setMsg(f"Error - 文件路径不存在（'{file}'）").print("error")

    try:
        with open(filePath, mode = "r", encoding = encoding) as f:
            contt = f.read()
            result.content = contt
            return result.setState(True).setMsg("文件读取成功").print("info")
    except Exception as err:
        return result.setState(False).setMsg(f"{str(err)}").print("error")

# 编辑文件（内部函数）
# file: 文件路径（文件）
# content: 文件内容
# mode: 打开模式（w+、a+）
# encoding: 编码格式
# msg: 提示消息
# isOverwrite: 是否覆盖目标文件
def writeFile(file = "", content = "", mode = "w+", encoding = "utf-8", isOverwrite = True, msg = "文件写入成功"):
    # 状态
    result = Result().initMethod(depth = 2)
    result.state = True
    result.file = file
    result.filePath = filePath = hhUtils.getAbsolutePath(file, depth = 3)
    result.content = content
    result.msg = ""

    # 参数判断
    if file == "":
        return result.setState(False).setMsg("Error - 请补全参数（file）").print("error")
    
    # 是否覆盖
    if os.path.exists(filePath) and not isOverwrite:
        return result.setState(False).setMsg(f"Error - 文件已存在（'{file}'）").print("error")

    # 路径检测
    if file.find("/") > -1:
        if not file.endswith("/"):
            # 匹配内容：
            # - [./][dir/].filename
            # - [./][dir/]filename
            # - [./][dir/]filename.ext
            dir = os.path.split(filePath)[0]
            if not os.path.exists(dir):
                os.makedirs(dir)
        else:
            # 匹配内容：
            # - ./
            # - ./dir/
            # - ./dir/dir/
            # - ../dir/
            # - dir/dir/
            return result.setState(False).setMsg(f"Error - file 参数不合法（'{file}'不是有效的文件路径）").print("error")
    else:
        # 匹配内容：
        # - .filename
        # - filename
        # - filename.ext
        pass

    try:
        with open(filePath, mode, encoding = encoding) as f:
            f.write(content)
            f.seek(0)
            content = f.read()
            result.content = content
            return result.setState(False).setMsg(msg).print("info")
    except IsADirectoryError:
        return result.setState(False).setMsg(f"Error - file 参数不合法（'{file}'不是有效的文件路径）").print("error")
    except IOError as err:
        return result.setState(False).setMsg(f"{str(err)}").print("error")

# 创建文件（文本类型的文件）
def createFile(file = "", content = "", encoding = "utf-8"):
    return writeFile(file, content, "w+", encoding, isOverwrite = False, msg = "文件创建成功")

# 重置文件（文本类型的文件）
def resetFile(file = "", content = "", encoding = "utf-8"):
    return writeFile(file, content, "w+", encoding, isOverwrite = True, msg = "文件重置成功")

# 修改文件（文本类型的文件）
def editFile(file = "", content = "", encoding = "utf-8"):
    return writeFile(file, content, "a+", encoding, isOverwrite = True, msg = "文件修改成功")

# 复制文件
# src: 源文件路径（文件）
# target: 目标文件路径（文件、文件夹）
# isOverwrite: 是否覆盖目标文件
# isKeepMeta: 是否保留元信息（如创建时间、修改时间）
# isKeepPermission: 是否保留文件权限
def copyFile(src, target, isOverwrite = False, isKeepMeta = True, isKeepPermission = True):
    # 状态
    result = Result().initMethod()
    result.state = True
    result.src = src
    result.srcPath = srcPath = hhUtils.getAbsolutePath(src, depth = 2)
    result.target = target
    result.targetPath = targetPath = hhUtils.getAbsolutePath(target, depth = 2)

    # 源文件判断
    if os.path.isdir(srcPath):
        return result.setState(False).setMsg(f"Error - src 必须是文件（'{src}'）").print("error")
    if not os.path.exists(srcPath):
        return result.setState(False).setMsg(f"Error - 文件不存在（'{src}'）").print("error")
    
    # 源文件的文件名
    srcFileName = os.path.split(srcPath)[1]

    # 目标文件判断
    if os.path.exists(targetPath):
        if os.path.isdir(targetPath):
            # target 路径存在，并且是文件夹，生成目标文件路径
            result.targetPath = targetPath = os.path.abspath(os.path.join(targetPath, srcFileName))
            # print(11, targetPath)
        else:
            # target 路径存在，并且是文件，不做处理
            # print(12, targetPath)
            pass
    else:
        if target.endswith("/"):
            # target 路径不存在，并且是文件夹，生成目标文件路径
            result.targetPath = targetPath = os.path.abspath(os.path.join(targetPath, srcFileName))
            # print(13, targetPath)
        else:
            # target 路径不存在，并且是文件，不做处理
            # print(14, targetPath)
            pass
    
    # 确保目标文件夹存在
    targetFilePath = os.path.split(targetPath)[0]
    if not os.path.exists(targetFilePath):
        os.makedirs(targetFilePath)
    
    # 是否覆盖目标文件
    if os.path.exists(targetPath) and not isOverwrite:
        return result.setState(False).setMsg(f"Error - 目标文件已存在（'{target}'）").print("error")
    
    try:
        if isKeepMeta:
            # 复制范围：✅ 内容、✅ 权限、✅ 元数据‌
            shutil.copy2(srcPath, targetPath)
        elif isKeepPermission:
            # 复制范围：✅ 内容、✅ 权限、⭕️ 元数据‌
            shutil.copy(srcPath, targetPath)
        else:
            # 复制范围：✅ 内容、❌ 权限、⭕️ 元数据‌
            shutil.copyfile(srcPath, targetPath)

        return result.setMsg("文件复制成功").print("info")
    except Exception as err:
        return result.setState(False).setMsg(f"文件复制失败 - {str(err)}").print("error")

# 复制文件夹
# src: 源文件夹路径（文件夹）
# target: 目标文件夹路径（文件夹）
# isAllowTargetExist: 是否允许目标文件夹存在
def copyFolder(src, target, isAllowTargetExist = True):
    # 状态
    result = Result().initMethod()
    result.state = True
    result.src = src
    result.srcPath = srcPath = hhUtils.getAbsolutePath(src, depth = 2)
    result.target = target
    result.targetPath = targetPath = hhUtils.getAbsolutePath(target, depth = 2)

    try:
        shutil.copytree(srcPath, targetPath, dirs_exist_ok = isAllowTargetExist, symlinks = True)
        return result.setState(True).setMsg("文件夹复制成功").print("info")
    except NotADirectoryError:
        return result.setState(False).setMsg(f"Error - src 必须是文件夹（'{src}'）").print("error")
    except FileExistsError:
        return result.setState(False).setMsg(f"Error - target 已存在（'{target}'）").print("error")
    except Exception as err:
        return result.setState(False).setMsg(f"文件夹复制失败 - {str(err)}").print("error")

# 移动文件
# src: 源文件路径（文件）
# target: 目标文件路径（文件、文件夹）
# isOverwrite: 是否覆盖目标文件
def moveFile(src, target, isOverwrite = False):
    # 状态
    result = Result().initMethod()
    result.state = True
    result.src = src
    result.srcPath = srcPath = hhUtils.getAbsolutePath(src, depth = 2)
    result.target = target
    result.targetPath = targetPath = hhUtils.getAbsolutePath(target, depth = 2)

    # 源文件判断
    if os.path.isdir(srcPath):
        return result.setState(False).setMsg(f"Error - src 必须是文件（'{src}'）").print("error")
    if not os.path.exists(srcPath):
        return result.setState(False).setMsg(f"Error - 文件不存在（'{src}'）").print("error")
    
    # 源文件的文件名
    srcFileName = os.path.split(srcPath)[1]

    # 目标文件判断
    if os.path.exists(targetPath):
        if os.path.isdir(targetPath):
            # target 路径存在，并且是文件夹，生成目标文件路径
            result.targetPath = targetPath = os.path.abspath(os.path.join(targetPath, srcFileName))
            # print(11, targetPath)
        else:
            # target 路径存在，并且是文件，不做处理
            # print(12, targetPath)
            pass
    else:
        if target.endswith("/"):
            # target 路径不存在，并且是文件夹，生成目标文件路径
            result.targetPath = targetPath = os.path.abspath(os.path.join(targetPath, srcFileName))
            # print(13, targetPath)
        else:
            # target 路径不存在，并且是文件，不做处理
            # print(14, targetPath)
            pass
    
    # 确保目标文件夹存在
    targetFilePath = os.path.split(targetPath)[0]
    if not os.path.exists(targetFilePath):
        os.makedirs(targetFilePath)
    
    # 是否覆盖目标文件
    if os.path.exists(targetPath) and not isOverwrite:
        return result.setState(False).setMsg(f"Error - 目标文件已存在（'{target}'）").print("error")
    
    try:
        shutil.move(srcPath, targetPath)
        return result.setMsg("文件移动成功").print("info")
    except Exception as err:
        return result.setState(False).setMsg(f"文件移动失败 - {str(err)}").print("error")

# 移动文件夹
# src: 源文件夹路径（文件夹）
# target: 目标文件夹路径（文件夹）
# isAllowTargetExist: 是否允许目标文件夹存在
def moveFolder(src, target, isAllowTargetExist = True):
    # 状态
    result = Result().initMethod()
    result.state = True
    result.src = src
    result.srcPath = srcPath = hhUtils.getAbsolutePath(src, depth = 2)
    result.target = target
    result.targetPath = targetPath = hhUtils.getAbsolutePath(target, depth = 2)

    # 判断 src 存在并且是文件
    if os.path.exists(srcPath):
        if os.path.isfile(srcPath):
            return result.setState(False).setMsg(f"Error - src 必须是文件夹（'{src}'）").print("error")
    else:
        return result.setState(False).setMsg(f"Error - src 路径不存在（'{src}'）").print("error")
    
    # target 存在，先复制 src 到 target 下，然后删除 src
    if os.path.exists(targetPath):
        if isAllowTargetExist:
            try:
                shutil.copytree(srcPath, targetPath, dirs_exist_ok = isAllowTargetExist, symlinks = True)
                shutil.rmtree(srcPath)
                return result.setState(True).setMsg("文件夹移动成功").print("info")
            except FileExistsError:
                return result.setState(False).setMsg(f"Error - target 必须是文件夹，当前传入的是已存在的文件（'{target}'）").print("error")
            except Exception as err:
                return result.setState(False).setMsg(f"文件夹移动失败 - {str(err)}").print("error")
        else:
            return result.setState(False).setMsg(f"Error - target 已存在（'{target}'）").print("error")
    
    try:
        shutil.move(srcPath, targetPath)
        return result.setState(True).setMsg("文件夹移动成功").print("info")
    except FileNotFoundError:
        return result.setState(False).setMsg(f"Error - src 不存在（'{src}'）").print("error")
    except FileExistsError:
        return result.setState(False).setMsg(f"Error - target 必须是文件夹，当前传入的是已存在的文件（'{target}'）").print("error")
    except Exception as err:
        return result.setState(False).setMsg(f"文件夹移动失败 - {str(err)}").print("error")

# 删除文件、文件夹
# path: 文件、文件夹路径
def remove(path = ""):
    # 状态
    result = Result().initMethod()
    result.state = True
    result.path = path
    result.absPath = absPath = hhUtils.getAbsolutePath(path, depth = 2)
    result.records = []
    result.msg = ""

    # 参数判断
    if path == "":
        return result.setState(False).setMsg("Error - 缺少参数（path）").print("error")

    # 屏蔽风险操作
    if path == "." or path == "./" or path[0] == "/" or path.find("..") > -1:
        return result.setState(False).setMsg(f"Error - 路径无法删除（'{path}'）").print("error")
    
    # 路径判断
    if not os.path.exists(absPath):
        return result.setState(False).setMsg(f"Error - 路径不存在（'{absPath}'）").print("error")

    # 删除
    try:
        if os.path.isfile(absPath):
            # 删除文件
            os.remove(absPath)
            result.records.append(absPath)
            return result.setState(True).setMsg("文件删除成功").print("info")
        else:
            # 删除当前文件夹下的所有文件、子文件夹
            # os.removedirs() 递归删除目录树中的‌空目录‌，从最深层子目录开始，逐级向上删除，直到遇到非空目录或根目录。
            # os.rmdir() 删除单个空的目录。
            # shutil.rmtree() 则可以删除非空目录，但更危险。
            for root, dirs, files in os.walk(absPath, topdown = False):
                # print("root - ", root, dirs, files)
                for name in files:
                    file = os.path.join(root, name).replace("\\", "/")
                    # print("file - ", file)
                    if os.path.exists(file):
                        os.remove(file)
                        result.records.append(file)
                for name in dirs:
                    dir = os.path.join(root, name).replace("\\", "/")
                    # print("folder - ", dir)
                    if os.path.exists(dir):
                        os.rmdir(dir)
                        result.records.append(dir)
            # 删除当前文件夹
            os.rmdir(absPath)
            result.records.append(absPath)

            return result.setState(True).setMsg("文件夹删除成功").print("info")
    except IOError as err:
        return result.setState(False).setMsg(f"{str(err)}").print("error")

# 创建文件夹
def createFolder(path = "", isAllowTargetExist = True):
    # 状态
    result = Result().initMethod()
    result.state = True
    result.path = path
    result.absPath = absPath = hhUtils.getAbsolutePath(path, depth = 2)

    # 参数判断
    if path == "":
        return result.setState(False).setMsg("Error - 缺少参数（path）").print("error")

    try:
        os.makedirs(absPath, exist_ok = isAllowTargetExist)
        return result.setState(True).setMsg("文件夹创建成功").print("info")
    except TypeError as err:
        return result.setState(False).setMsg(f"文件夹创建失败 - 参数 path 无效（'{path}'） - {str(err)}").print("error")
    except FileExistsError as err:
        return result.setState(False).setMsg(f"文件夹创建失败 - 目标已存在（'{path}'） - {str(err)}").print("error")
    except Exception as err:
        return result.setState(False).setMsg(f"文件夹创建失败 - {str(err)}").print("error")

# 判断是否是文件
# path: 文件、文件夹路径
def isFile(path = ""):
    # 路径转换
    absPath = hhUtils.getAbsolutePath(path, depth = 2)
    # 状态
    result = Result().initMethod()
    result.state = os.path.isfile(absPath)
    result.path = path
    result.absPath = absPath
    return result.print("info")

# 判断文件或文件夹是否存在功能
# path: 文件、文件夹路径
def isExist(path = ""):
    # 路径转换
    absPath = hhUtils.getAbsolutePath(path, depth = 2)
    # 状态
    result = Result().initMethod()
    result.state = os.path.exists(absPath)
    result.path = path
    result.absPath = absPath
    return result.print("info")

# 判断是否是文件夹
# path: 文件、文件夹路径
def isFolder(path = ""):
    # 路径转换
    absPath = hhUtils.getAbsolutePath(path, depth = 2)
    # 状态
    result = Result().initMethod()
    result.state = os.path.isdir(absPath)
    result.path = path
    result.absPath = absPath
    return result.print("info")

# 获取文件夹列表
# path: 文件、文件夹路径
def getFolderList(path = ""):
    # 路径转换
    absPath = hhUtils.getAbsolutePath(path, depth = 2)
    # 状态
    result = Result().initMethod()
    result.path = path
    result.absPath = absPath
    result.state = True
    result.list = []
    result.all = []
    result.fileList = []
    result.folderList = []
    try:
        for item in os.listdir(absPath):
            itemPath = os.path.join(absPath, item)
            itemObj = {
                "name": item,
                "path": itemPath,
                "type": "",
            }
            if os.path.isdir(itemPath):
                itemObj["type"] = "folder"
                result.folderList.append(itemObj)
            else:
                itemObj["type"] = "file"
                result.fileList.append(itemObj)
            result.list.append(item)
            result.all.append(itemObj)
        return result.setMsg("文件夹列表获取成功").print("info")
    except Exception as err:
        return result.setState(False).setMsg(f"{str(err)}").print("error")
