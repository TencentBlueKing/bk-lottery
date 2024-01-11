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

from django.db import models

# Create your models here.


class StaffList(models.Model):
    name = models.CharField("名单名称", max_length=32, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "名单"
        verbose_name_plural = "名单"
        ordering = ["id"]

    def __str__(self):
        return self.name


class Staff(models.Model):
    name = models.CharField("英文名", max_length=16)
    chinese_name = models.CharField("中文名", max_length=64, blank=True, null=True)
    department = models.CharField("部门", max_length=64, blank=True, null=True)
    phone = models.CharField("电话", max_length=16, blank=True, null=True)
    avatar = models.CharField("头像", max_length=256, blank=True, null=True)
    is_absent = models.BooleanField("是否缺席", default=False)
    absent_reason = models.IntegerField(
        "缺席原因", choices=[(0, "未缺席"), (1, "因公请假"), (2, "因私请假"), (3, "外部人员")], default=0
    )
    remark = models.CharField("备注", max_length=256, blank=True, null=True)

    staff_list = models.ForeignKey(
        StaffList, verbose_name="名单名称", on_delete=models.CASCADE
    )

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "Staff"
        verbose_name_plural = "Staff"

    def __eq__(self, other):
        if isinstance(other, Staff):
            return other.name == self.name and other.staff_list == self.staff_list
        return False

    def __hash__(self):
        return hash((self.name, self.staff_list.pk))

    def __str__(self):
        return self.name
