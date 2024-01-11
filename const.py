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


# lottery
class AwardStatus:
    INACTIVATED = 0
    ACTIVATED = 1
    OVER = 2


class AbsentReason:
    NOT_ABSENT = 0
    LEAVE_FOR_BUSINESS = 1
    LEAVE_FOR_PERSON = 2
    OUTSIDERS = 3


# 抽奖首页的配置常量
all_config_name = [
    "winner_button",
    "winner_p_color",
    "award_p_color",
    "winner_backgroud_color",
    "winner_nums",
    "winner_line_nums",
    "head_portrait_style",
    "time_interval",
    "time_presentation",
    "pageturning",
    "is_play",
    "effect",
    "is_end_play",
    "author_name",
    "need_top",
    "need_top_left",
    "need_award_image",
    "font_family",
    "bg_music",
    "need_pause_audio",
    "audio_start_time",
    "award_style",
    "pointer_style",
]

default_config = {
    "winner_nums": 191,
    "winner_line_nums": 22,
    "time_interval": 2,
    "time_presentation": 1,
    "winner_backgroud_color": "#F9EDDF",
    "winner_p_color": "#000",
    "award_p_color": "#000",
    "winner_play_style": 0,
    "head_portrait_style": "non_head_portrait",
    "pageturning": "vertical",
    "is_play": "true",
    "effect": "default",
    "is_end_play": "true",
    "need_top": "false",
    "need_top_left": "true",
    "need_award_image": "block",
    "font_family": "",
    "bg_music": "joy.mp3",
    "need_pause_audio": "on",
    "author_name": "",
    "audio_start_time": 0,
    "winner_button": "150",
    "award_style": 1,
    "pointer_style": 0,
}

version_config = {
    "v_1": {
        "lucky_top": "13%",
        "need_top": False,
    },
    "v_2": {"lucky_top": "20%", "need_top": False},
    "v_3": {"lucky_top": "20%"},
}
