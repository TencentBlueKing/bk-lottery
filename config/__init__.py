# -*- coding: utf-8 -*-
"""
TencentBlueKing is pleased to support the open source community by making 蓝鲸智云-抽奖系统(BlueKing-BK-LOTTERY) available.
Copyright (C) 2017-2023 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at https://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""


__all__ = ["celery_app", "RUN_VER", "APP_CODE", "SECRET_KEY", "BASE_DIR"]

import os

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from blueapps.core.celery import celery_app


def get_env_or_raise(key):
    """Get an environment variable, if it does not exist, raise an exception"""
    value = os.environ.get(key)
    if not value:
        raise RuntimeError(
            (
                'Environment variable "{}" not found, you must set this variable to run this application.'
            ).format(key)
        )
    return value


# app 基本信息
RUN_VER = "open"
# SaaS应用ID
APP_ID = os.environ.get("BKPAAS_APP_ID", "test_app_id")
# SaaS安全密钥，注意请勿泄露该密钥
APP_TOKEN = os.environ.get("BKPAAS_APP_SECRET", "test_app_secret")
BK_PAAS_HOST = os.environ.get("BKAPP_PAAS_HOST", "test_bk_paas_host")

APP_CODE = APP_ID
SECRET_KEY = APP_TOKEN

os.environ["APP_ID"] = APP_ID
os.environ["APP_TOKEN"] = APP_TOKEN
os.environ["BK_PAAS_HOST"] = BK_PAAS_HOST

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MAKO_TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
MAKO_TEMPLATE_MODULE_DIR = os.path.join(BASE_DIR, "templates_module", APP_TOKEN)
