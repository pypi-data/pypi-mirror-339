
# -*- codeing = utf-8 -*-
# @Name：hhDecorator
# @Version：1.0.0
# @Author：立树
# @CreateTime：2025-04-01 20:00
# @UpdateTime：2025-04-01 20:00

from functools import wraps

# 方法只执行一次
def once(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not wrapper.isRunned:
            wrapper.isRunned = True
            return func(self, *args, **kwargs)
        else:
            return self
    wrapper.isRunned = False
    return wrapper
