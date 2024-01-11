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


class AppMetaConfig(models.Model):
    """
    APP相关配置
    """

    name = models.CharField("配置中文名称", max_length=100)
    conf_name = models.CharField("配置名称", max_length=64)
    conf_value = models.TextField("配置值")
    remark = models.TextField("备注")
    conf_type = models.CharField("配置项分类", max_length=10, default="0")

    def __unicode__(self):
        return "APP配置"

    class Meta:
        verbose_name = "配置表"
        verbose_name_plural = "配置表"
