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
import random

from django.db.models import Q

import const
from lottery.utils.exception import AwardStatusException
from lottery.models import Award, Exclusion, Winner
from staff.models import Staff


class LotteryHandler:
    def __init__(self, award_id):
        self.award_id = award_id
        self.award = None

    def verify_award(self, is_reward, absent_winner=None):
        """
        验证奖项并得到对应的奖项实例
        """
        self.award = Award.objects.get(pk=self.award_id)
        if is_reward and not self.award.take_in_scene:
            raise AwardStatusException(self.award_id, "该奖项不允许现场重复抽奖")
        if not (is_reward or self.award.status != const.AwardStatus.OVER):
            raise AwardStatusException(self.award_id, "获取奖项失败或者该奖项已结束")
        # 处理因中奖者没在现场，而重新抽奖的情况，将缺席者中奖信息设为无效，不参加剩下抽奖活动
        if absent_winner:
            Winner.objects.filter(staff__name=absent_winner).update(is_valid=False)
        return self.award

    def get_excluded_staff(self):
        """
        获取对应奖项的排除名单
        """
        # 获得全局排除名单
        exclusions = list(
            Staff.objects.filter(exclusionforall__isnull=False).values_list(
                "name", flat=True
            )
        )

        # 获得当前奖项的排除名单
        exclusions.extend(
            Exclusion.objects.filter(award__in=[self.award]).values_list(
                "staff__name", flat=True
            )
        )

        # 排除已经获奖不能再次获奖的名单
        exclusions.extend(
            Winner.objects.all()
            .exclude(Q(award__in=self.award.co_existed_award.all()))
            .values_list("staff__name", flat=True)
        )
        return exclusions

    def get_staff_sample(self, exclusions):
        """
        除去排除人员获得人员样本
        """
        absent_conditions = [True, False] if self.award.can_absence_draw else [False]
        staffs = {
            item["name"]: item
            for item in Staff.objects.filter(
                staff_list=self.award.staff_list, is_absent__in=absent_conditions
            )
            .exclude(absent_reason=2)
            .values("id", "name", "chinese_name", "is_absent")
        }

        sample_in_staff_list1 = set(staffs.keys()) - exclusions
        staffs2 = {
            item["name"]: item
            for item in Staff.objects.filter(
                staff_list=self.award.staff_list2, is_absent__in=absent_conditions
            )
            .exclude(absent_reason=2)
            .values("id", "name", "chinese_name", "is_absent")
        }
        sample_in_staff_list2 = set(staffs2.keys()) - exclusions

        return sample_in_staff_list1, sample_in_staff_list2

    def get_winner_from_sample(self, sample, win_rate, staff_list):
        """
        根据比例获取中奖人员
        """
        if len(sample) >= win_rate:
            selected = random.sample(list(sample), win_rate)
        else:
            selected = list(sample)

        lucky = Staff.objects.filter(staff_list=staff_list, name__in=selected).values(
            "id", "name", "chinese_name", "is_absent"
        )

        return lucky
