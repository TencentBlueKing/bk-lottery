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

from staff.models import Staff, StaffList

# Create your models here.


class Award(models.Model):
    """
    奖项表
    说明：设置奖项的必要信息(中奖总人数，中奖者名单，所属中奖计划等)，还可设置以下开关
        1. 是否需要短信进行通知: 给中奖者发送短信
        2. 是否现场输入奖品: 奖品名称可以现场输入，为了方便重抽，抽奖页面有再抽一次按钮
        3. 是否所有人都可以抽奖: 如果打开该设置，则该奖项中奖候选人将包含之前已中过奖的人员，否则则不包括
        4. 是否现场领奖: 如果打开该设置，则对于每个中奖人员都可以实现重抽(当中奖人缺席)
        5. 是否可以现场更改人数
        6. 中奖人员是否添加到排除名单(设置了所有人抽奖的也不能中奖)
    """

    name = models.CharField("奖项名称", max_length=64)
    number = models.IntegerField("每次中奖人数", default=1)
    staff_list = models.ForeignKey(
        StaffList,
        verbose_name="关联名单1",
        on_delete=models.PROTECT,
        related_name="staff_list",
    )
    win_rate = models.IntegerField("名单1中奖人数", default=0)
    staff_list2 = models.ForeignKey(
        StaffList,
        verbose_name="关联名单2",
        on_delete=models.PROTECT,
        related_name="staff_list_2",
        null=True,
        blank=True,
    )
    win_rate2 = models.IntegerField("名单2中奖人数", default=0)

    times = models.IntegerField("抽奖次数", default=1)
    prize = models.CharField("奖品", max_length=64)
    status = models.IntegerField(
        "状态",
        default=1,
        choices=(
            (0, "未激活"),
            (1, "已激活"),
            (2, "已结束"),
        ),
    )
    sequence = models.IntegerField("顺序", default=0)
    picture = models.ImageField("奖品图片", upload_to="award")
    compressed_picture = models.ImageField(
        "压缩图片", upload_to="compressed_award", null=True, blank=True
    )
    compressed_image = models.TextField(null=True, blank=True)
    image = models.TextField(null=True, blank=True)

    need_input = models.BooleanField("是否现场输入奖品", default=False)
    change_win_rate_inplace = models.BooleanField("是否可以现场更改中奖人数", default=False)
    ignore_animation = models.BooleanField("是否跳过抽奖动画", default=True)

    is_add_exclusion = models.BooleanField("中奖人员是否加到排除名单", default=False)
    take_in_scene = models.BooleanField("是否现场领奖", default=False)
    can_absence_draw = models.BooleanField("报备的人是否可以抽奖", default=True)
    co_existed_award = models.ManyToManyField(
        "Award", help_text="可以共同抽取的奖项", default=None, blank=True
    )

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = "奖项"
        verbose_name_plural = "奖项"

    def set_finish(self):
        self.status = 2
        self.save()

    def __str__(self):
        return self.name


class Winner(models.Model):
    """
    中奖者表
    说明: 每个中奖者属于一个特定的奖项对象和一个人员对象
    """

    staff = models.ForeignKey(Staff, verbose_name="中奖者名称", on_delete=models.CASCADE)
    award = models.ForeignKey(Award, verbose_name="奖项", on_delete=models.CASCADE)
    is_valid = models.BooleanField("中奖是否生效", default=True)
    # 对于用到大转盘的奖项，将会记录大转盘的结果
    remark = models.CharField("备注", max_length=256, null=True, blank=True)

    def __unicode__(self):
        return "winner %s for %s" % (self.staff.name, self.award.name)

    class Meta:
        verbose_name = "中奖人员"
        verbose_name_plural = "中奖人员"

    def __str__(self):
        return self.staff.name


class Exclusion(models.Model):
    """
    排除名单表
    说明: 每个奖项的中奖者候选名单将排除该名单上的人员
          该表为特定奖项特定的排除人员
    """

    staff = models.ForeignKey(Staff, verbose_name="中奖者名称", on_delete=models.CASCADE)
    award = models.ManyToManyField(Award, verbose_name="奖项")

    def __unicode__(self):
        return "exclusion：%s" % self.staff.name

    class Meta:
        verbose_name = "排除名单"
        verbose_name_plural = "排除名单"

    def __str__(self):
        return self.staff.name


class ExclusionForAll(models.Model):
    """
    排除名单
    说明: 所有奖项都排除该名单上的人员，包括设置了所有人中奖选项的奖项
    """

    staff = models.ForeignKey(Staff, verbose_name="中奖者名称", on_delete=models.CASCADE)

    def __unicode__(self):
        return "exclusion：%s" % self.staff.name

    class Meta:
        verbose_name = "排除名单ForAll"
        verbose_name_plural = "排除名单ForAll"

    def __str__(self):
        return self.staff.name


class WheelItem(models.Model):
    title = models.CharField("标题", max_length=16)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = "大转盘项"
        verbose_name_plural = "大转盘项"
