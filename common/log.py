# coding=utf-8
"""
TencentBlueKing is pleased to support the open source community by making 蓝鲸智云-抽奖系统(BlueKing-BK-LOTTERY) available.
Copyright (C) 2017-2023 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at https://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
# pylint: disable=broad-except
"""
@summary: 始化logger实例(对logging的封装)
@usage：
          >>> from common.log import logger
          >>> logger.error(u'系统开小差了！')
"""

# 使用python的logging模块，配合settings的LOGGING属性
import logging
import sys
import traceback

# root--用于平台的日志记录
logger_detail = logging.getLogger("root")
# component--用于组件调用的日志记录
logger_component = logging.getLogger("component")


class logger_traceback:
    """
    详细异常信息追踪
    """

    def __init__(self):
        pass

    def error(self, message=""):
        """
        error 日志
        """
        message = self.get_error_info(message)
        logger_detail.error(message)

    def info(self, message=""):
        """
        info 日志
        """
        message = self.get_error_info(message)
        logger_detail.info(message)

    def warning(self, message=""):
        """
        warning 日志
        """
        message = self.get_error_info(message)
        logger_detail.warning(message)

    def debug(self, message=""):
        """
        debug 日志
        """
        message = self.get_error_info(message)
        logger_detail.debug(message)

    def critical(self, message=""):
        """
        critical 日志
        """
        message = self.get_error_info(message)
        logger_detail.critical(message)

    def get_error_info(self, message):
        """
        获取日志信息
        """
        try:
            info = sys.exc_info()
            from common.request_middlewares import get_x_request_id

            requestID = get_x_request_id(True)
            if requestID:
                message = "%s【requestID:%s】" % (message, requestID)
            for filename, lineno, function, text in traceback.extract_tb(info[2]):
                msg = "%s line: %s in %s" % (filename, lineno, function)
                message = "%s;%s\n%s\n" % (message, msg, text)
            sys.exc_clear()
            return message
        except Exception:
            return message


# traceback--打印详细错误日志
logger = logger_traceback()
