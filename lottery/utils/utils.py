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
# pylint: disable=broad-except
from django.http import HttpResponse
from django.utils.encoding import escape_uri_path
from PIL import Image

from lottery.models import Winner


def save_winners(staffs, award):
    winners = []
    Winner.objects.filter(award=award).update(is_valid=False)
    for staff in staffs:
        winners.append(Winner(award=award, staff_id=staff["id"], remark=None))
    Winner.objects.bulk_create(winners)


def xls_to_response(xls, filename):
    response = HttpResponse(content_type="application/ms-execl")
    response["Content-Disposition"] = "attachment; filename*=utf-8''{}.xls".format(
        escape_uri_path(filename)
    )
    xls.save(response)
    return response


def thumbnail(path, savefile="", width=None, height=None, q=150):
    """
    压缩并保存到文件
    """
    img = Image.open(path)
    w, h = img.size
    width, height = width or (w * q // 1000), height or (h * q // 1000)
    img.thumbnail((width, height))
    if not savefile:
        savefile = "{}_{}x{}.{}".format(path, width, height, img.format.lower())
    img.save(savefile, img.format)
