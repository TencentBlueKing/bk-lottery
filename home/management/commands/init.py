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
# pylint: disable=broad-except,W0613
from django.core.management.base import BaseCommand

from home.models import AppMetaConfig


class Command(BaseCommand):
    help = "用于初始化系统配置表的配置数据"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.stdout.write("start init home_appmetaconfig table......")
        page_config = [
            {
                "conf_name": "winner_backgroud_color",
                "conf_value": "#f5e1a4",
                "remark": "中奖结果名单的背景色（单位：十六进制颜色值）",
                "name": "中奖结果方块背景色",
                "conf_type": "0",
            },
            {
                "conf_name": "winner_p_color",
                "conf_value": "#2D69DE",
                "remark": "中奖结果名单的字体色（单位：十六进制颜色值）",
                "name": "中奖结果方块字色",
                "conf_type": "0",
            },
            {
                "conf_name": "award_p_color",
                "conf_value": "#2877E0",
                "remark": "奖项标题的字体色（单位：十六进制颜色值），参考值："
                "#FDE154(黄色-默认)、#2877E0(蓝色) 、#6D5CCE(紫色)",
                "name": "奖项标题字色",
                "conf_type": "0",
            },
            {
                "conf_name": "winner_button",
                "conf_value": "150",
                "remark": "开始和结束抽奖按钮的位置（单位：像素）",
                "name": "开始和结束抽奖按钮",
                "conf_type": "1",
            },
            {
                "conf_name": "winner_nums",
                "conf_value": "191",
                "remark": "中奖结果每页最多显示的中奖人数（正整数）",
                "name": "中奖结果页-每页总数",
                "conf_type": "2",
            },
            {
                "conf_name": "winner_lines",
                "conf_value": "22",
                "remark": "中奖结果每页显示的行数（正整数）",
                "name": "中奖结果页-每页行数",
                "conf_type": "2",
            },
            {
                "conf_name": "winner_line_nums",
                "conf_value": "22",
                "remark": "中奖结果每行显示的中奖人数（正整数）",
                "name": "中奖结果页-每页列数",
                "conf_type": "2",
            },
            {
                "conf_name": "head_portrait_style",
                "conf_value": "non_head_portrait",
                "remark": "中奖结果人员卡片展示风格：携带头像和用户姓名（head_portrait）、"
                "纯中奖用户姓名（non_head_portrait）、按照原始48区间风格（null或此字段为空）",
                "name": "中奖结果显示",
                "conf_type": "2",
            },
            {
                "conf_name": "time_interval",
                "conf_value": "1",
                "remark": "中奖结果轮播，每页显示的间隔时间（单位：秒）",
                "name": "翻页间隔时长",
                "conf_type": "3",
            },
            {
                "conf_name": "time_presentation",
                "conf_value": "1",
                "remark": "中奖结果轮播，每页呈现的停留时长（单位：秒）",
                "name": "翻页停留时长",
                "conf_type": "3",
            },
            {
                "conf_name": "icon_package",
                "conf_value": "head_portrait",
                "remark": "控制抽奖页面的头像风格：使用头像（head_portrait）、使用logo图片（logo）、为空则使用系统默认样式",
                "name": "抽奖动画效果风格",
                "conf_type": "4",
            },
            {
                "conf_name": "pageturning",
                "conf_value": "vertical",
                "remark": "翻页方式参数：上下翻页（vertical）、左右翻页（horizontal）",
                "name": "轮播-翻页",
                "conf_type": "6",
            },
            {
                "conf_name": "is_play",
                "conf_value": "true",
                "remark": "开启轮播开关：开启，默认（true）、关闭（false）",
                "name": "轮播-开关",
                "conf_type": "6",
            },
            {
                "conf_name": "effect",
                "conf_value": "default",
                "remark": "轮播效果：推动效果（default）、不断重复轮播的渐变效果（fade）、立方体效果（cube）、"
                "封面流效果（coverflow）、翻转效果（flip）、卡片效果（cards）、系统默认原始风格（空字符串 或 null）",
                "name": "轮播-效果",
                "conf_type": "6",
            },
            {
                "conf_name": "is_end_play",
                "conf_value": "true",
                "remark": "到最后一页停止轮播：默认轮播到最后一页停止（true）、不断从头开始轮播（false）",
                "name": "轮播-循环控制",
                "conf_type": "6",
            },
            {
                "conf_name": "pointer_style",
                "conf_value": "0",
                "remark": "鼠标样式风格取值：默认风格（0）、风格1（1）",
                "name": "鼠标风格",
                "conf_type": "7",
            },
            {
                "conf_name": "award_style",
                "conf_value": "1",
                "remark": "抽奖的奖项展示风格：水滴风格（0）、稳赢风格（1）、玩偶风格（1）、星空风格（2）",
                "name": "抽奖系统风格",
                "conf_type": "8",
            },
            {
                "conf_name": "author_name",
                "conf_value": "",
                "remark": "页面底部和技术支持元素内容，默认为空",
                "name": "技术支持内容",
                "conf_type": "9",
            },
            {
                "conf_name": "font_family",
                "conf_value": "",
                "remark": "字体样式：IEG需求字体（FZZZHONGJW）、为空则使用系统默认字体",
                "name": "字体",
                "conf_type": "10",
            },
            {
                "conf_name": "need_top",
                "conf_value": "false",
                "remark": "是否需要顶部中间的图标：需要（true）、不需要（false）",
                "name": "顶部图标",
                "conf_type": "11",
            },
            {
                "conf_name": "need_top_left",
                "conf_value": "true",
                "remark": "是否需要顶部左边的图标：需要（true）、不需要（false）",
                "name": "顶部图标",
                "conf_type": "11",
            },
            {
                "conf_name": "need_award_image",
                "conf_value": "block",
                "remark": "是否需要展示奖项图片：需要（block）、不需要（none）",
                "name": "顶部图标",
                "conf_type": "11",
            },
            {
                "conf_name": "bg_music",
                "conf_value": "fearless.mp3",
                "remark": "抽奖背景音乐设置，默认joy.mp3",
                "name": "抽奖背景音乐",
                "conf_type": "12",
            },
            {
                "conf_name": "need_pause_audio",
                "conf_value": "off",
                "remark": "抽奖显示名单的时候是否暂停音乐",
                "name": "显示名单音乐开关",
                "conf_type": "12",
            },
            {
                "conf_name": "audio_start_time",
                "conf_value": "20",
                "remark": "抽奖音乐播放开始时间，可以设置高潮部分的时间点，单位(s)",
                "name": "抽奖音乐播放开始时间",
                "conf_type": "12",
            },
            {
                "conf_name": "department",
                "conf_value": "IEG",
                "remark": "--",
                "name": "抽奖组织信息",
                "conf_type": "12",
            },
            {
                "conf_name": "portrait_packet_name",
                "conf_value": "head_portrait",
                "remark": "--",
                "name": "存放头像文件夹的名称",
                "conf_type": "13",
            },
        ]
        try:
            for config in page_config:
                is_exists = AppMetaConfig.objects.filter(conf_name=config["conf_name"])
                if not is_exists:
                    AppMetaConfig.objects.create(**config)
                else:
                    configuration_item = is_exists.first()
                    configuration_item.remark = config["remark"]
                    configuration_item.name = config["name"]
                    configuration_item.conf_type = config["conf_type"]
                    configuration_item.save()
            self.stdout.write("init home_appmetaconfig table success......")
        except Exception as e:
            self.stderr.write("init home_appmetaconfig table error {0}".format(e))
