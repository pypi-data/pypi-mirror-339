
# -*- codeing = utf-8 -*-
# @Name：hhConfig
# @Version：1.0.0
# @Author：立树
# @CreateTime：2025-04-02 13:50
# @UpdateTime：2025-04-08 03:45

import os
import json
from .hhUtils import getAbsolutePath

class Config():
    # 初始化
    def __init__(self):
        # 基础配置
        self.name = "hhframe"
        self.version = "0.5.0"
        self.author = "立树"
        self.mode = "run"
        # self.mode = "debug"

        # 快代理
        self.kuaiProxyConfig = {
            "enable": False,
            "path": ""
        }
        self.__findKuaiProxyConfigFile()

    # 打印结果
    def __str__(self):
        return json.dumps(self.__dict__, ensure_ascii = False, indent = 4)
    
    # 自动查找快代理的配置文件
    def __findKuaiProxyConfigFile(self):
        for depth, (root, dirs, files) in enumerate(os.walk(os.getcwd(), topdown = True)):
            # print("root - ", root)
            # print("files - ", files)
            # print("=" * 50)

            # 遍历 2 层
            if depth >= 1:
                dirs.clear()

            # 过滤无效文件夹
            for dir in dirs:
                if dir in [".venv", "venv", ".git", ".idea", "dist", "build", "__pycache__"]:
                    dirs.remove(dir)

            # 筛选配置文件
            for file in files:
                if file in ["hhKuaiProxyConfig.json"]:
                    self.kuaiProxyConfig["path"] = os.path.join(root, file)
                    return
    
    # 设置快代理
    def setKuaiProxyConfig(self, config):
        try:
            if config.get("enable") != None:
                self.kuaiProxyConfig["enable"] = config.get("enable")
            if config.get("path") != None:
                self.kuaiProxyConfig["path"] = getAbsolutePath(config.get("path"), depth = 2)
        except Exception:
            pass

hhConfig = Config()
