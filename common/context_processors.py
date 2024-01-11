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
"""
context_processor for common(setting)

** 除setting外的其他context_processor内容，均采用组件的方式(string)
"""
from django.conf import settings

from home.models import AppMetaConfig


def mysetting(request):
    try:
        conf = AppMetaConfig.objects.get(conf_name="department")
        department = conf.conf_value
    except AppMetaConfig.DoesNotExist:
        department = "部门"

    return {
        "MEDIA_URL": settings.MEDIA_URL,  # MEDIA_URL
        "STATIC_URL": settings.STATIC_URL,  # 本地静态文件访问
        "CEPH_STATIC_URL": settings.CEPH_STATIC_URL,
        "STATIC_VERSION": settings.STATIC_VERSION,
        "APP_CODE": settings.APP_CODE,  # 在蓝鲸系统中注册的  "应用编码"
        "APP_PATH": request.get_full_path(),
        "SITE_URL": settings.SITE_URL,  # URL前缀
        "site_url": settings.SITE_URL,
        "DEPARTMENT": department,
    }
