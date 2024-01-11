# coding=utf-8
"""
TencentBlueKing is pleased to support the open source community by making 蓝鲸智云-抽奖系统(BlueKing-BK-LOTTERY) available.
Copyright (C) 2017-2023 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at https://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
# pylint: disable=broad-except,W0613,R0915,R0913,R0912,R1702,R0914
import json
import random

import xlwt
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404

import const
from common.mymako import (
    render_json,
    render_mako_context,
    render_mako_js_context,
    render_mako_tostring_context,
)
from home.models import AppMetaConfig
from lottery.utils.decorator import execute_time
from lottery.utils.exception import AwardStatusException
from lottery.utils.handlers import LotteryHandler
from lottery.models import Award, Exclusion, ExclusionForAll, WheelItem, Winner
from lottery.utils.utils import save_winners, xls_to_response
from staff.models import Staff


def get_award_view(request, award_id):
    """
    抽奖首页视图函数
    """
    award = get_object_or_404(Award, id=award_id)
    awards = list(Award.objects.order_by("sequence"))

    last_award = None
    next_award = None

    # 按sequence属性排序，得到所要抽奖奖品的前驱后继，用于抽奖页面切换不同的抽奖页面
    for index, item in enumerate(awards):
        if item.id == int(award_id):
            if index > 0:
                last_award = awards[index - 1]
            if index < len(awards) - 1:
                next_award = awards[index + 1]

    # 获得页面样式的自定义配置
    configs = get_version_config(request, award)
    configs.update(
        {
            "award": award,
            "last_award": last_award,
            "next_award": next_award,
        }
    )

    return render_mako_context(request, "/lottery/award.html", configs)


def get_draw_again_view(request):
    """
    重新抽取的逻辑实现
    通过当前给出的奖项id进行复制
    """
    award_id = request.GET["award_id"]
    award = get_object_or_404(Award, id=award_id)
    award.name = "嘉宾奖"
    award.prize = "神秘掉落"
    award.status = const.AwardStatus.ACTIVATED
    award.pk = None  # 以原award记录为原型复制一条新的award记录
    award.save()

    award.save(update_fields=["name"])

    for exclusion in Exclusion.objects.filter(award__id=award_id):
        exclusion.award.add(award)
    next_award = (
        Award.objects.filter(sequence__gt=award.sequence).order_by("sequence").first()
    )
    configs = get_version_config(request, award)
    configs.update(
        {
            "award": award,
            "last_award": None,
            "next_award": next_award,
        }
    )

    html = render_mako_tostring_context(request, "/lottery/award.html", configs)

    return render_json({"result": True, "award_id": award.id, "html": html})


def get_version_config(request, award):
    """
    获取中奖页面的自定义配置
    """
    # 从数据库中得到页面样式的自定义配置
    page_config = {
        item.conf_name: item.conf_value
        for item in AppMetaConfig.objects.filter(conf_name__in=const.all_config_name)
    }

    # 从请求中获得页面样式的版本信息，否者取默认值
    version = request.GET.get("v", "USE_APPCONFIG")
    if version == "USE_APPCONFIG":
        award_style = page_config.get("award_style", 1)
        version = award_style
    else:
        award_style = version

    # 将数据库中存储的样式配置构造成键值对，没有的配置则使用默认值
    config_res = const.version_config.get(f"v_{version}", {})
    for config in const.all_config_name:
        config_res[config] = page_config.get(config, const.default_config[config])

    # 加入奖项的图片和展示图片样式的版本信息
    config_res.update(
        {
            "award_style": award_style,
            "award_image": award.image,
        }
    )
    # 根据奖项的可中奖者的数量，配置中奖页面中展示每个中奖者框的大小
    max_width = 1640
    if award.number > 1000:
        max_width = 2100
    elif award.number == 6:
        max_width = 1200
    elif award.number > 20 and award.number <= 60:
        max_width = 1900
    elif award.number == 8:
        max_width = 1440

    return {"version": version, "max_width": max_width, "version_config": config_res}


def check_status(request):
    """
    返回每个奖项的状态(是否已激活)
    """
    award_status_list = [
        {"id": award["id"], "name": award["name"], "status": award["status"]}
        for award in Award.objects.values("id", "name", "status")
    ]
    return render_json(
        {
            "result": True,
            "message": award_status_list,
        }
    )


def set_award_prize(request, award_id):
    """
    现场输入奖品页面中更新奖项奖品的接口
    """
    prize_args = request.POST.get("prize", None)
    if not prize_args:
        return JsonResponse({"result": False, "message": "缺少接口必要参数"})
    else:
        try:
            # 以 【奖项名称 奖品名称 (数量 份)】 这种格式进分隔
            split_award_input = prize_args.strip().split("(")
            split_name_prize = split_award_input[0].strip().split(" ")
            name, prize = split_name_prize[0], split_name_prize[1]
            win_rate = int(split_award_input[-1].replace("份)", ""))

            award = Award.objects.get(id=award_id)
            Award.objects.filter(id=award_id).update(name=name, prize=prize)

            # 更新中奖人数
            if win_rate > 0:
                if award.number != win_rate:
                    change_number = award.number - win_rate
                    win_rate1, win_rate2 = (
                        award.win_rate,
                        award.win_rate2 if award.win_rate2 else 0,
                    )
                    if change_number < 0:
                        # 增加抽奖人数，并判断增加后的抽奖人数是否大于人员的人数
                        list1_staff_num = Staff.objects.filter(
                            staff_list=award.staff_list
                        ).count()
                        list2_staff_num = (
                            Staff.objects.filter(staff_list=award.staff_list2).count()
                            if award.staff_list2
                            else 0
                        )
                        win_rate1 = (
                            award.win_rate + abs(change_number)
                            if award.win_rate + abs(change_number) < list1_staff_num
                            else list1_staff_num
                        )
                        # 如果在关联名单1加满了，就在关联名单2上加
                        if award.win_rate + abs(change_number) > list1_staff_num:
                            remaining_num = (
                                award.win_rate + abs(change_number) - list1_staff_num
                            )
                            if not award.staff_list2 or remaining_num > list2_staff_num:
                                return JsonResponse(
                                    {"result": False, "message": "设定的中奖人数大于候选者人数"}
                                )
                            win_rate2 = award.win_rate2 + remaining_num
                    else:
                        # 减少抽奖人数
                        if award.win_rate:
                            temp = award.win_rate - change_number
                            win_rate1 = 0 if temp < 0 else temp
                        if award.win_rate2 and temp < 0:
                            win_rate2 = award.win_rate2 + temp
                    Award.objects.filter(id=award_id).update(
                        number=win_rate, win_rate=win_rate1, win_rate2=win_rate2
                    )
            else:
                return JsonResponse({"result": False, "message": "奖项人数至少为1份"})
        except Award.DoesNotExist:
            return JsonResponse({"result": False, "message": "修改的奖项不存在"})
        except Exception:
            return JsonResponse(
                {"result": False, "message": "修改的奖项格式错误【奖项名称 奖品名称 (数量 份)】"}
            )
    return JsonResponse({"result": True, "message": "修改成功"})


@execute_time
@transaction.atomic
def select_all_winners_by_award(request, award_id):
    """
    根据奖项的配置随机选择奖项的所有中奖者
    """
    if not settings.DEBUG and not request.user.is_superuser:
        return HttpResponseForbidden()

    selected = []
    try:
        # 用于判断是否为因缺席而重新抽奖的情况
        is_reward = json.loads(request.POST.get("is_reward"))
        absent_winner = request.POST.get("absent_winner")
        handler = LotteryHandler(award_id)
        award = handler.verify_award(is_reward, absent_winner)
    except ObjectDoesNotExist:
        return JsonResponse({"result": False, "message": "该奖项不存在"})
    except AwardStatusException as e:
        return JsonResponse({"result": False, "message": e.message})

    # 将无法参加抽奖的人员进行排除
    exclusions = set(handler.get_excluded_staff())
    sample_in_staff_list1, sample_in_staff_list2 = handler.get_staff_sample(exclusions)

    # 对得到的人员样本进行抽奖逻辑
    selected.extend(
        handler.get_winner_from_sample(
            sample_in_staff_list1, award.win_rate, award.staff_list
        )
    )
    selected.extend(
        handler.get_winner_from_sample(
            sample_in_staff_list2, award.win_rate2, award.staff_list2
        )
    )
    if not selected:
        return JsonResponse(
            {
                "result": False,
                "message": "当前无符合条件的抽奖样本人员",
            }
        )

    # 如果是重新抽取，则只抽取一个中奖者. 并将上次有效的中奖者取出来返回给前端
    if is_reward:
        selected = [random.choice(selected)]
        selected.extend(
            Staff.objects.filter(
                winner__award_id=award_id, winner__is_valid=True
            ).values("id", "name", "chinese_name", "is_absent")
        )
    # 中奖人员中的缺席人员要报备
    for item in selected:
        item["chinese_name"] = (
            "{}(报备)".format(item["chinese_name"])
            if item["is_absent"]
            else item["chinese_name"]
        )

    # 更新数据库
    save_winners(selected, award)
    award.set_finish()

    # 加入到排除名单
    if award.is_add_exclusion:
        staffs_obj = Staff.objects.filter(name__in=[item["name"] for item in selected])
        guys = [ExclusionForAll(staff=item) for item in staffs_obj]
        ExclusionForAll.objects.bulk_create(guys)

    return JsonResponse({"winners": selected, "result": True})


def get_winners_view(request):
    """
    查看当前中奖者页面
    """
    return render_mako_context(
        request,
        "/lottery/winners.html",
        {
            "plan": "",
            "message": "",
            "result": True,
        },
    )


def get_all_winners(request):
    """
    获取当前中奖者列表
    用于初始化kendo的Grid
    """
    winners = (
        Winner.objects.exclude(is_valid=False).select_related("staff").order_by("award")
    )
    winners = [
        {
            "name": winner.staff.name,
            "chineseName": winner.staff.chinese_name,
            "department": winner.staff.department,
            "award": winner.award.name,
            "prize": winner.award.prize,
            "is_valid": "是" if winner.is_valid else "否",
        }
        for winner in winners
    ]

    return JsonResponse(winners, safe=False)


def download_winners_list(request):
    """
    下载中奖者的excel表格
    """
    winners = Winner.objects.filter(is_valid=True)

    wb = xlwt.Workbook()
    ws = wb.add_sheet("中奖者名单")

    fields = ["staff帐号", "中文名", "部门", "奖项", "奖品名称", "备注"]

    for index, field in enumerate(fields):
        ws.write(0, index, field)

    for index, winner in enumerate(winners):
        ws.write(index + 1, 0, winner.staff.name)
        ws.write(index + 1, 1, winner.staff.chinese_name)
        ws.write(index + 1, 2, winner.staff.department)
        ws.write(index + 1, 3, winner.award.name)
        ws.write(index + 1, 4, winner.award.prize)
        ws.write(index + 1, 5, winner.remark)

    return xls_to_response(wb, "中奖者名单")


def get_all_wheels(request):
    wheel_items = WheelItem.objects.all()
    return render_mako_js_context(
        request,
        "/makojs/wheel.js",
        {
            "wheelItems": wheel_items,
        },
    )


def check_winners(request):
    """
    获取奖项中奖名单
    """
    data = request.POST

    award_id = data["name"]
    award = Award.objects.filter(pk=award_id)

    status = award[0].status
    winners = Winner.objects.filter(award_id=award_id, is_valid=True).select_related(
        "staff"
    )

    winner_list = [
        {
            "name": item.staff.name,
            "chinese_name": item.staff.chinese_name,
            "avatar": item.staff.avatar,
        }
        for item in winners
    ]
    return JsonResponse(
        {"number": len(winner_list), "winner_list": winner_list, "status": status}
    )
