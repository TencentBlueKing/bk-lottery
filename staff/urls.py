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
from django.conf.urls import url

from . import views

urlpatterns = (
    url(r"^all/([0-9]+)/$", views.get_all_staff),
    url(r"^static_head_portrait/$", views.get_head_portrait),
    url(r"^static/all/([0-9]+)/$", views.get_all_staff_as_js),
    url(r"^upload/$", views.save_staff_from_excel),
    url(r"^download/$", views.download),
)