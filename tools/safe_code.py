# -*- encoding:utf-8 -*-
from __future__ import absolute_import

import sys
import time
from functools import wraps

__all__ = ["ExceptionHandler", "fail_safe"]


class ExceptionHandler(object):
    def __init__(self, silent=True, recover_handler=None, error_return=None):
        """
        https://docs.python.org/2.5/whatsnew/pep-343.html
        Args:
            silent: 是否抛出异常
            recover_handler: 异常时恢复函数
            error_return: silent=True错误时返回值
        """
        self.recover_handler = recover_handler
        self.silent = silent
        self.error_return = error_return

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        """
        返回值为True， 则忽略异常
        """
        # 有异常
        if exc_type and exc_value and traceback:
            if self.recover_handler:
                self.recover_handler(exc_type, exc_value, traceback)
            return self.silent
        return True

    def __call__(self, func):
        @wraps(func)
        def inner(*args, **kwargs):
            self.__enter__()
            try:
                res = func(*args, **kwargs)
            except:
                silent = self.__exit__(*sys.exc_info())
                if not silent:
                    raise
                return self.error_return
            else:
                self.__exit__(None, None, None)
                return res

        return inner


def fail_safe(recover_handler=None, error_return=None):
    """
    @fail_safe() or with fail_safe():
    Returns: python with context
    :param recover_handler:
    :param error_return:
    """
    return ExceptionHandler(silent=True, recover_handler=recover_handler, error_return=error_return)
