
# -*- codeing = utf-8 -*-
# @Name：hhKuaiProxy
# @Version：1.0.0
# @Author：立树
# @CreateTime：2025-04-06 22:29
# @UpdateTime：2025-04-08 13:49

# 快代理 API 文档（https://www.kuaidaili.com/doc/api/）
# 密钥令牌相关接口
# - 获得密钥令牌 API：https://auth.kdlapi.com/api/get_secret_token
# - 检测密钥令牌 API：https://auth.kdlapi.com/api/check_secret_token
# 账号相关接口
# - 获取账户余额 API：https://dev.kdlapi.com/api/getaccountbalance
# - 获取账户订单列表 API：https://dev.kdlapi.com/api/getaccountorders
# - 获取订单密钥 API：https://dev.kdlapi.com/api/getordersecret
# 订单相关接口
# - 创建订单 API：https://dev.kdlapi.com/api/createorder
# - 续费订单 API：https://dev.kdlapi.com/api/reneworder
# - 获取订单信息 API：https://dev.kdlapi.com/api/getorderinfo
# - 获取订单到期时间 API：https://dev.kdlapi.com/api/getorderexpiretime
# - 开启/关闭自动续费 API：https://dev.kdlapi.com/api/setautorenew
# - 关闭订单 API：https://dev.kdlapi.com/api/closeorder
# 私密代理相关接口
# - 获取私密代理IP API：https://dps.kdlapi.com/api/getdps
# - 检测私密代理有效性 API：https://dps.kdlapi.com/api/checkdpsvalid
# - 获取私密代理可用时长 API：https://dps.kdlapi.com/api/getdpsvalidtime
# - 获取订单IP提取余额 API：https://dps.kdlapi.com/api/getipbalance
# - 查询私密代理地区和运营商 API：https://dps.kdlapi.com/api/dpsresources
# 白名单相关接口
# - 获取IP白名单 API：https://dev.kdlapi.com/api/getipwhitelist
# - 设置IP白名单 API：https://dev.kdlapi.com/api/setipwhitelist
# - 添加白名单IP API：https://dev.kdlapi.com/api/addwhiteip
# - 删除白名单IP API：https://dev.kdlapi.com/api/delwhiteip
# 通用接口
# - 获取代理鉴权信息 API：https://dev.kdlapi.com/api/getproxyauthorization
# 工具接口
# - 获取指定地区编码 API：https://dev.kdlapi.com/api/getareacode
# - 获取 UA API：https://dev.kdlapi.com/api/getua
# - 获取本机 IP API：https://dev.kdlapi.com/api/getmyip

"""
功能：
- getSecretToken 获取秘钥
- getSecretAuth 获取鉴权信息
- getSecretProxyInfo 获取私密代理信息
- getNewSecretProxy 获取新的私密代理 IP
- checkProxyIpValid 检测私密代理 IP 有效性
- getSecretProxy 获取私密代理 IP
- getOrderExpireTime 获取订单到期时间
- getUserAgent 获取 UA
- getMyIp 获取本机 IP
"""

import time
from . import hhJson
from . import hhRequest
from .hhConfig import hhConfig
from .hhResult import Result


# 快代理异常类
# class KdlException(Exception):
#     """异常类"""

#     def __init__(self, code=None, message=None):
#         self.code = code
#         if sys.version_info[0] < 3 and isinstance(message, unicode):
#             message = message.encode("utf8")
#         self.message = message
#         self._hint_message = "[KdlException] code: {} message: {}".format(self.code, self.message)

#     @property
#     def hint_message(self):
#         return self._hint_message

#     @hint_message.setter
#     def hint_message(self, value):
#         self._hint_message = value

#     def __str__(self):
#         if sys.version_info[0] < 3 and isinstance(self.hint_message, unicode):
#             self.hint_message = self.hint_message.encode("utf8")
#         return self.hint_message


# 发送请求（内部函数）
def _sendRequest(api = "", params = {}, method = "get", methodDepth = 2, pathDepth = 4):
    # 状态
    result = Result().initMethod(depth = methodDepth)
    result.code = -1
    result.state = True
    result.config = ""
    result.configContent = {}
    result.api = api
    result.params = params
    result.data = ""
    result.msg = ""

    # 配置文件
    ConfigFilePath = hhConfig.kuaiProxyConfig["path"]
    if not ConfigFilePath:
        return result.setState(False).setMsg("未检测到配置文件，请使用 hhConfig.setKuaiProxyConfig() 进行配置")

    # 读取配置文件
    config = hhJson.read(ConfigFilePath, depth = pathDepth).data
    if not config:
        return result.setState(False).setMsg("配置文件读取失败")
    else:
        result.config = ConfigFilePath
        result.configContent = config

    # 发送请求
    if method == "get":
        res = hhRequest.get(
            url = api,
            params = {
                "secret_id": config["secret_id"],
                "signature": config["secret_key"],
                "sign_type": "token",
                **params,
            },
        )
    else:
        res = hhRequest.post(
            url = api,
            data = {
                "secret_id": config["secret_id"],
                "secret_key": config["secret_key"],
                "sign_type": "token",
                **params,
            },
        )
    
    # 处理异常请求
    if res.code != 200:
        return result.setState(False).setCode(res.code).setMsg("接口请求失败")
    
    # 处理异常响应
    res = res.response.data
    code = res["code"]
    msg = res["msg"]
    if code != 0:
        return result.setState(False).setCode(code).setMsg(f"接口请求失败 - {msg}")

    return result.setState(True).setCode(code).setData(res["data"]).setMsg("接口请求成功")


# 获取订单到期时间 API
def getOrderExpireTime():
    result = _sendRequest(
        api = "https://dev.kdlapi.com/api/getorderexpiretime",
    )
    
    if result.state:
        return result.print("info")
    else:
        return result.print("error")

# 获取本机 IP API
def getMyIp():
    result = _sendRequest(
        api = "https://dev.kdlapi.com/api/getmyip",
    )

    if result.state:
        return result.print("info")
    else:
        return result.print("error")

# 获取 UA API
# num: 数量
# device: 设备类型
#   - all: 全部
#   - pc: 电脑
#   - mobile: 手机
#   - pad: 平板
# platform: 平台类型
#   - all: 全部
#   - win: Windows
#   - macos: MacOS
#   - linux: Linux
#   - ios: iOS
#   - android: Android
# browser: 浏览器类型
#   - all: 全部
#   - chrome: Chrome
#   - firefox: Firefox
#   - ie: IE
#   - weixin: 微信内置浏览器
def getUserAgent(num = 1, device = "all", platform = "all", browser = "all"):
    result = _sendRequest(
        api = "https://dev.kdlapi.com/api/getua",
        params = {
            "num": num,
            "dt": device,
            "platform": platform,
            "browser": browser,
        }
    )

    if result.state:
        return result.print("info")
    else:
        return result.print("error")

# 获取密钥 API
# 说明：在调用快代理 API 接口时，secret_token 可以代替 secret_key 进行身份验证
def getSecretToken():
    # 状态
    result = Result().initMethod()
    result.code = -1
    result.state = True
    result.config = ""
    result.data = {}
    result.msg = ""

    # 配置文件
    ConfigFilePath = hhConfig.kuaiProxyConfig["path"]
    if ConfigFilePath:
        result.config = ConfigFilePath
    else:
        return result.setState(False).setMsg("未检测到配置文件，请使用 hhConfig.setKuaiProxyConfig() 进行配置").print("error")

    # 读取配置文件
    config = hhJson.read(ConfigFilePath, depth = 3).data
    if config:
        secret_token = config["secret_token"]
        expire_time = config["secret_token_expire_time"] or 0
    else:
        return result.setState(False).setMsg("配置文件读取失败").print("error")
    
    # 还有3分钟过期时更新
    if float(expire_time) - 3 * 60 < time.time() or secret_token == "":
        result = _sendRequest(
            api = "https://auth.kdlapi.com/api/get_secret_token",
            method = "post",
        )

        # 处理异常响应
        if not result.state:
            return result.print("error")
        
        # 处理正常响应
        secret_token = result.data["secret_token"]
        expire_seconds = result.data["expire"]
        create_time = time.time()
        expire_time = create_time + expire_seconds
        config["secret_token"] = secret_token
        config["secret_token_expire_seconds"] = expire_seconds
        config["secret_token_expire_time"] = f"{expire_time:.6f}"
        config["secret_token_create_time"] = f"{create_time:.6f}"
        hhJson.save(result.config, config, depth = 3)
        return result.setMsg("秘钥（token）获取成功").print("info")
    else:
        result.code = 0
        result.data = {
            "secret_token": secret_token,
            "expire": config["secret_token_expire_seconds"] or 0,
        }
        return result.setMsg("秘钥（token）获取成功").print("info")


# 获取代理鉴权信息 API
# 说明：快代理的私密代理使用方式有3种（此处为第2种实现方案-授权认证）
# 1. 用户名密码认证，必须使用用户名、密码、代理 IP
#    proxies = {
#        "http": "http://username:password@xxx.xxx.xxx.xxx:xxxx",
#        "https": "http://username:password@xxx.xxx.xxx.xxx:xxxx",
#    }
# 2. 授权认证，必须使用代理授权信息（形式：）
#    proxies = {
#        "http": "http://xxx.xxx.xxx.xxx:xxxx",
#        "https": "http://xxx.xxx.xxx.xxx:xxxx",
#    }
#    headers = {
#        "Proxy-Authorization": "%(type)s %(credentials)s" % {"type": type, "credentials": credentials},
#    }
# 3. 白名单方式（需提前设置白名单）
#    proxies = {
#        "http": "http://xxx.xxx.xxx.xxx:xxxx",
#        "https": "http://xxx.xxx.xxx.xxx:xxxx",
#    }
def getSecretAuth():
    result = _sendRequest(
        api = "https://dev.kdlapi.com/api/getproxyauthorization",
    )

    # 处理异常响应
    if not result.state:
        return result.print("error")

    auth = result.data
    auth = "{} {}".format(auth["type"], auth["credentials"])

    # 保存到配置文件
    config = result.configContent
    config["secret_auth"] = auth
    hhJson.save(result.config, config, depth = 3)

    result.auth = auth
    return result.setMsg("鉴权信息（auth）获取成功").print("info")


# 获取私密代理 IP API
def getNewSecretProxy(methodDepth = 2, pathDepth = 4):
    result = _sendRequest(
        api = "https://dps.kdlapi.com/api/getdps/",
        params = {
            "num": 1,
            "pt": 1,
            "sep": 1,
            "format": "json",
        },
        methodDepth = methodDepth,
        pathDepth = pathDepth,
    )

    # 处理异常响应
    if not result.state:
        return result.print("error")

    config = result.configContent
    username = config["username"]
    password = config["password"]
    proxyIp = result.data["proxy_list"][0]
    proxies = {
        "http": "http://" + "%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxyIp},
        "https": "http://" + "%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxyIp},
    }

    # 保存私密代理 IP 池
    config["secret_proxy"] = result.data["proxy_list"]
    hhJson.save(result.config, config, depth = pathDepth - 1)

    result.proxyIp = proxyIp
    result.proxies = proxies
    return result.setMsg("获取私密代理 IP 成功").print("info")


# 检测私密代理有效性 API
def checkProxyIpValid(proxyIp = "", methodDepth = 2, pathDepth = 4):
    result = _sendRequest(
        api = "https://dps.kdlapi.com/api/checkdpsvalid",
        params = {
            "proxy": [proxyIp],
        },
        methodDepth = methodDepth,
        pathDepth = pathDepth,
    )

    if result.state:
        if result.data[proxyIp]:
            return result.setState(True).setMsg(f"代理 IP 有效（{proxyIp}）").print("info")
        else:
            return result.setState(False).setMsg(f"代理 IP 无效（{proxyIp}）").print("error")
    else:
        return result.print("error")


# 获取私密代理信息 API
def getSecretProxyInfo(proxies = {}):
    result = hhRequest.get(
        # url = "http://www.baidu.com",
        # url = "http://api.houheaven.com/api/egg/request/method/get?p1=v1&p2=v2",
        # url = "https://dev.kdlapi.com/testproxy",  # 返回私密代理对应的 IP 地址
        url = "https://my.ip.cn/json/",
        proxies = proxies,
        headers = {
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Origin": "https://www.ip.cn",
            "Pragma": "no-cache",
            "Referer": "https://www.ip.cn/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "macOS",
        },
        # timeout = (5, 5)
    )
    return result


# 获取私密代理 IP API
# isGetProxyInfo: 是否获取私密代理信息
def getSecretProxy(isGetProxyInfo = False):
    # 状态
    result = Result().initMethod()
    result.code = -1
    result.state = True
    result.config = ""
    result.proxyIp = ""
    result.proxies = {}
    result.proxyInfo = {}
    result.msg = ""

    # 配置文件
    ConfigFilePath = hhConfig.kuaiProxyConfig["path"]
    if not ConfigFilePath:
        return result.setState(False).setMsg("未检测到配置文件，请使用 hhConfig.setKuaiProxyConfig() 进行配置").print("error")
    else:
        result.config = ConfigFilePath

    # 读取配置文件
    config = hhJson.read(ConfigFilePath, depth = 3).data
    if not config:
        return result.setState(False).setMsg("配置文件读取失败").print("error")
    
    # 获取私密代理 IP
    proxies = config["secret_proxy"] if "secret_proxy" in config else []
    proxyIp = proxies[0] if len(proxies) else ""
    if proxyIp:
        result = checkProxyIpValid(proxyIp, methodDepth = 3, pathDepth = 5)
        if result.state:
            config = result.configContent
            username = config["username"]
            password = config["password"]
            proxies = {
                "http": "http://" + "%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxyIp},
                "https": "http://" + "%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": proxyIp},
            }
            result.proxyIp = proxyIp
            result.proxies = proxies
            result.setMsg("获取私密代理 IP 成功").print("info")
        else:
            result = getNewSecretProxy(methodDepth = 3, pathDepth = 5)
    else:
        result = getNewSecretProxy(methodDepth = 3, pathDepth = 5)

    # 获取私密代理信息
    if isGetProxyInfo:
        res = getSecretProxyInfo(result.proxies)
        if res.state:
            result.proxyInfo = res.response.data["data"]
        else:
            result.proxyInfo = {}
    
    return result
