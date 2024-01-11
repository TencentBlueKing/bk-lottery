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
# Generated by Django 1.11.2 on 2019-01-15 19:39


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0002_auto_20190104_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='is_absent',
            field=models.BooleanField(
                default=False,
                verbose_name='\u662f\u5426\u5230\u73b0\u573a'),
        ),
    ]