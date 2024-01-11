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
import json
import os
from os import path

import xlrd
from django.conf import settings
from django.contrib.staticfiles import finders
from django.db import DatabaseError

from home.models import AppMetaConfig
from .models import Staff, StaffList
from .utils.exception import StaffListTypeError


class UploadStaffFileHandler:
    staff_png_url = settings.CEPH_STATIC_URL

    def __init__(self, file):
        self.file = file
        self.file_name, self.suffix = os.path.splitext(self.file.name)
        self.latest_staffs = []
        if self.suffix not in [".json", ".xlsx", ".xls"]:
            raise StaffListTypeError(self.file_name)
        # 创建或取出同名的文件对象
        self.staff_list, self.is_create = StaffList.objects.get_or_create(
            name=self.file_name
        )

    def analysis_staffs(
            self, staff, chinese_name, department, is_absent, staff_list, absent_reason
    ):
        candidate = Staff(
            name=staff,
            chinese_name=chinese_name,
            remark="",
            department=department,
            is_absent=is_absent,
            staff_list=staff_list,
            absent_reason=absent_reason,
        )
        # 查找在 static/avatars/head_portrait 路径下是否有该员工的路径, 否则使用默认头像路径
        portrait_packet_name = AppMetaConfig.objects.filter(
            conf_name="portrait_packet_name"
        ).first()
        avatar_path = path.join(
            "avatars",
            portrait_packet_name.conf_value
            if portrait_packet_name
            else "head_portrait",
            "{}.png".format(staff),
        ).replace("\\", "/")
        if finders.find(avatar_path):
            candidate.avatar = path.join(self.staff_png_url, avatar_path).replace(
                "\\", "/"
            )
        else:
            candidate.avatar = path.join(
                self.staff_png_url, "avatars/default.png"
            ).replace("\\", "/")
        self.latest_staffs.append(candidate)

    def read_file(self):
        return (
            self.read_json_file() if self.suffix == ".json" else self.read_excel_file()
        )

    def read_json_file(self):
        json_staff = self.file.read().decode("utf-8").replace("\r", "").split("\n")
        for item in json_staff:
            if not item:
                continue
            staff_name = json.loads(item)
            is_absent = False
            if staff_name.get("absent_reason", 0) in [1, 2]:
                is_absent = True

            self.analysis_staffs(
                staff_name.get("staff_account_name"),
                staff_name.get("staff_display_name"),
                staff_name.get("manager_position_level_name_cn"),
                is_absent,
                self.staff_list,
                staff_name.get("absent_reason", 0),
            )

        return self.latest_staffs

    def read_excel_file(self):
        excel = xlrd.open_workbook(file_contents=self.file.read())
        sheet = excel.sheet_by_index(0)
        for row in range(1, sheet.nrows):
            if any(sheet.row_values(row)):
                staff = sheet.cell_value(row, 0)
                chinese_name = sheet.cell_value(row, 1)
                department = sheet.cell_value(row, 2)
                try:
                    absent_reason = int(sheet.cell_value(row, 3))
                except ValueError:
                    absent_reason = 0
                is_absent = absent_reason in [1, 2]
                self.analysis_staffs(
                    staff,
                    chinese_name,
                    department,
                    is_absent,
                    self.staff_list,
                    absent_reason,
                )

        return self.latest_staffs

    def save_staffs_info(self):
        # 得到已经存在的同名名单中的人员信息，无同名名单则为空
        existed_staffs = list(Staff.objects.filter(staff_list=self.staff_list))
        # 得到最新的人员信息
        latest_staffs = self.read_file()

        # 分别获取更新、删除、新增的人员
        deleted_staff_names = [
            staff.name for staff in existed_staffs if staff not in latest_staffs
        ]
        create_staffs = [
            staff for staff in latest_staffs if staff not in existed_staffs
        ]
        update_staffs = []
        dict_latest_staffs = {staff.name: staff for staff in latest_staffs}
        for staff in existed_staffs:
            if staff.name in dict_latest_staffs.keys():
                dict_latest_staffs[staff.name].id = staff.id
                update_staffs.append(dict_latest_staffs[staff.name])

        try:
            Staff.objects.filter(
                staff_list=self.staff_list, name__in=deleted_staff_names
            ).delete()
            Staff.objects.bulk_update(
                update_staffs, ["department", "avatar", "is_absent", "remark"]
            )
            Staff.objects.bulk_create(create_staffs)
        except DatabaseError as e:
            # 导入失败时要删除创建的名单，若名单关联着存在，则保留
            if self.is_create:
                StaffList.objects.filter(name=self.file_name).delete()
            raise e
