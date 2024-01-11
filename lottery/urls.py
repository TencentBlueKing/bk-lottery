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
    url(r"^award/([0-9]+)/$", views.get_award_view),
    url(r"^award/([0-9]+)/update/$", views.set_award_prize),
    url(r"^award/([0-9]+)/winners/$", views.select_all_winners_by_award),
    url(r"^award/more/$", views.get_draw_again_view),  # 再抽一次
    url(r"^check_status/$", views.check_status),
    url(r"^check_winners/$", views.check_winners),
    url(r"^winners/$", views.get_winners_view),
    url(r"^winners/all/$", views.get_all_winners),
    url(r"^winners/download/$", views.download_winners_list),
    url(r"^wheels/$", views.get_all_wheels),
)
