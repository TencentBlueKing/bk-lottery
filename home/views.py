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
from django.http import HttpResponse

from common.mymako import render_mako_context
from lottery.models import Award

# Create your views here.


def get_home_views(request):
    """
    1 获得首页模版
    2 查询所有的奖项的数据，并按照sequence排序
    """
    message = ""
    result = True
    awards = Award.objects.order_by("sequence")
    return render_mako_context(
        request,
        "/home/home.html",
        {
            "awards": awards,
            "message": message,
            "result": result,
        },
    )


def get_guide_view(request):
    """
    帮助页面
    """
    return render_mako_context(request, "/home/lottery_guides.html", {})


def debug_request(request):
    resp = []
    resp.append("<div>HEADERS</div>")
    headers = sorted(request.META.items(), key=lambda item: item[0])
    for key, value in headers:
        resp.append("<div>")
        resp.append("<strong>{}</strong>: ".format(key))
        resp.append(str(value))
        resp.append("</div>")
    return HttpResponse(
        "Hello, world. Your blueking app is running successfully now." + "".join(resp)
    )
