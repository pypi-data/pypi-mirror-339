
# -*- codeing = utf-8 -*-
# @Name：hhRequest
# @Version：1.0.0
# @Author：立树
# @CreateTime：2025-04-05 00:57
# @UpdateTime：2025-04-05 00:57

"""
功能：
- get 发送 GET 请求功能
- post 发送 POST 请求功能
"""

import re
import sys
import requests
from . import hhKuaiProxy
from .hhResult import Result, EmptyClass
from .hhConfig import hhConfig

# 用户代理（User Agent，简称 UA）
UserAgents = {
    "Mac-Chrome-V133": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
}

# 请求头
Headers = {
    "base": {
        
    }
}

# 发送 GET 请求
# url: 请求的 URL
# params: 请求参数
# headers: 请求头
def get(url = "", params = {}, headers = {}, proxies = {}, enableKuaiProxy = None, timeout = 30):
    # 状态
    result = Result().initMethod()
    result.code = -1
    result.state = True
    result.url = url
    result.request = EmptyClass()
    result.request.headers = headers
    result.request.params = params
    result.request.proxy = proxies
    result.request.timeout = timeout
    result.response = EmptyClass()
    result.response.method = "GET"
    result.response.headers = {}
    result.response.data = {}
    result.response.text = ""
    result.msg = ""

    # 参数判断
    if url == "":
        return result.setState(False).setMsg("Error - 缺少参数（url）").print("error")
    
    # 快代理
    # 说明：为了防止 hhRequest、hhKuaiProxy 相互调用产生冲突，此处会过滤掉 hhKuaiProxy 模块的调用
    flag1 = not sys._getframe(1).f_code.co_filename.endswith("hhframe/hhKuaiProxy.py")
    flag2 = enableKuaiProxy if enableKuaiProxy != None else hhConfig.kuaiProxyConfig["enable"]
    flag3 = hhConfig.kuaiProxyConfig["path"] != ""
    if flag1 and flag2 and flag3:
        configFile = hhConfig.kuaiProxyConfig["path"]
        result.request.proxy = proxies = hhKuaiProxy.getSecretProxy(configFile).proxies

    # 发送请求
    try:
        response = requests.get(
            url = url,
            params = params,
            headers = headers,
            proxies = proxies,
            timeout = timeout,
        )
        result.code = response.status_code
        result.response.headers = dict(response.headers)
        result.response.data = response.json() if re.match(r"^[\[|\{]", response.text) else {}
        result.response.text = response.text if not re.match(r"^[\[|\{]", response.text) else ""
        return result.setState(True).setMsg("请求成功").print("info")
    except Exception as err:
        return result.setState(False).setMsg(f"请求失败 - {str(err)}").print("error")


# 发送 POST 请求
# url: 请求的 URL
# data: 请求参数
# json: 请求参数
# headers: 请求头
def post(url = "", data = {}, json = {}, headers = {}, proxies = {}, enableKuaiProxy = None, timeout = 30):
    # 状态
    result = Result().initMethod()
    result.code = -1
    result.state = True
    result.url = url
    result.request = EmptyClass()
    result.request.headers = headers
    result.request.data = data
    result.request.json = json
    result.request.proxy = proxies
    result.request.timeout = timeout
    result.response = EmptyClass()
    result.response.method = "POST"
    result.response.headers = {}
    result.response.data = {}
    result.response.text = ""
    result.msg = ""

    # 参数判断
    if url == "":
        return result.setState(False).setMsg("Error - 缺少参数（url）").print("error")

    # 快代理
    # 说明：为了防止 hhRequest、hhKuaiProxy 相互调用产生冲突，此处会过滤掉 hhKuaiProxy 模块的调用
    flag1 = not sys._getframe(1).f_code.co_filename.endswith("hhframe/hhKuaiProxy.py")
    flag2 = enableKuaiProxy if enableKuaiProxy != None else hhConfig.kuaiProxyConfig["enable"]
    flag3 = hhConfig.kuaiProxyConfig["path"] != ""
    if flag1 and flag2 and flag3:
        configFile = hhConfig.kuaiProxyConfig["path"]
        result.request.proxy = proxies = hhKuaiProxy.getSecretProxy(configFile).proxies

    # 发送请求
    try:
        response = requests.post(
            url = url,
            data = data,
            json = json,
            headers = headers,
            proxies = proxies,
            timeout = timeout,
        )
        result.code = response.status_code
        result.response.headers = dict(response.headers)
        result.response.data = response.json() if re.match(r"^[\[|\{]", response.text) else {}
        result.response.text = response.text if not re.match(r"^[\[|\{]", response.text) else ""
        return result.setState(True).setMsg("请求成功").print("info")
    except Exception as err:
        return result.setState(False).setMsg(f"请求失败 - {str(err)}").print("error")
