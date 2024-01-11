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
# pylint: disable=broad-except,W0613,R0915,R0913,R0912,R0914
import os
import random

from django.conf import settings
from django.db import DatabaseError
from django.http import JsonResponse, StreamingHttpResponse
from django.utils.encoding import escape_uri_path

from common.log import logger
from common.mymako import render_mako_js_context
from home.models import AppMetaConfig
from lottery.models import Award
from staff.handler import UploadStaffFileHandler
from staff.models import Staff
from staff.utils.exception import StaffListTypeError


# Create your views here.


def get_all_staff(request, awardID):
    """
    获取所有中奖者名单
    """
    try:
        award = Award.objects.get(id=awardID)
    except Award.DoesNotExist as e:
        logger.error("ERROR: Can't get staff by award (%s)" % e)
        return JsonResponse(
            {"staffs": [], "message": "无法获得奖项对应名单中的staff", "result": False}
        )
    staffs = list(
        Staff.objects.filter(staffList=award.staff_list).values("name", "avatar")
    )
    random.shuffle(staffs)
    return JsonResponse({"staffs": staffs, "message": "", "result": True})


def get_head_portrait(request):
    """
    获得头像地址
    """
    avatars = []
    portrait_packet_name = AppMetaConfig.objects.filter(
        conf_name="portrait_packet_name"
    ).first()
    if portrait_packet_name:
        img_path = os.path.join(
            settings.STATIC_PATH, "avatars", portrait_packet_name.conf_value
        )
        if os.path.exists(img_path):
            avatars = [
                "{0}/{1}".format(portrait_packet_name.conf_value, i)
                for i in os.listdir(img_path)
            ]
    return render_mako_js_context(
        request, "/makojs/avatars.js", {"avatar_head_portrait": avatars}
    )


def get_all_staff_as_js(request, awardID):
    """
    给前端返回rtxs数组
    """
    try:
        award = Award.objects.get(id=awardID)
        staffs = list(Staff.objects.filter(staff_list=award.staff_list)) + list(
            Staff.objects.filter(staff_list=award.staff_list2)
        )

        random.shuffle(staffs)
    except Award.DoesNotExist as e:
        logger.error("ERROR: Can't get staff by award (%s)" % e)
        staffs = []
    return render_mako_js_context(request, "/makojs/rtx.js", {"rtxs": staffs})


def save_staff_from_excel(request):
    """
    导入中奖者名单
    """
    file = request.FILES.get("excel", None)
    if not file:
        return JsonResponse({"result": False, "message": "请上选择要上传的传文件"})

    try:
        handler = UploadStaffFileHandler(file)
        handler.save_staffs_info()
    except StaffListTypeError:
        return JsonResponse({"result": False, "message": "文件类型不支持"})
    except DatabaseError as e:
        logger.error(e)
        return JsonResponse({"result": False, "message": "数据库操作异常，请检查日志"})

    return JsonResponse({"result": True, "message": "导入成功"})


def download(request):
    """
    下载导入抽奖者的人员模版
    """
    types = request.GET.get("types", "xlsx")
    filename = "抽奖名单格式.{}".format(types)
    files_path = os.path.join(settings.STATIC_PATH, "template")

    upload_dir = files_path  # 预期的上传目录
    file_name = filename  # 用户传入的文件名
    absolute_path = os.path.join(upload_dir, file_name)
    normalized_path = os.path.normpath(absolute_path)
    if not normalized_path.startswith(upload_dir):  # 检查最终路径是否在预期的上传目录中
        raise IOError()

    if not os.path.exists(normalized_path):
        return JsonResponse({"result": False, "message": "不存在指定类型模板文件"})

    def download_chunk(files, chunk_size=1024):
        with open(files, "rb") as f:
            while True:
                chunk_stream = f.read(chunk_size)
                if chunk_stream:
                    yield chunk_stream
                else:
                    break

    response = StreamingHttpResponse(download_chunk(files=normalized_path))
    response["Content-Type"] = "application/octet-stream"
    response["Content-Disposition"] = "attachment;filename={}".format(
        escape_uri_path(filename)
    )
    return response
