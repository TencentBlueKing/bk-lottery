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
# pylint: disable=W0613
import base64
import io

from django.conf import settings
from django import forms
from django.contrib import admin, messages
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponseRedirect
from PIL import Image

from lottery.models import Award, Exclusion, ExclusionForAll, Winner

# Register your models here.


def make_thumb(file, default_width=300):
    """
    生成缩略图/压缩图
    """
    pixbuf = Image.open(file)
    width, height = pixbuf.size

    # 如果宽度大于default_width，则进行压缩
    if width > default_width:
        delta = width / default_width
        height = int(height / delta)
        pixbuf.thumbnail((default_width, height), Image.ANTIALIAS)

    temp_file = io.BytesIO()
    pixbuf.save(temp_file, pixbuf.format)
    return temp_file


def my_clean(self):
    form_data = self.cleaned_data
    if form_data["win_rate"] < 0 or form_data["win_rate2"] < 0:
        raise forms.ValidationError("输入的中奖人数不能为负数！")
    if form_data["number"] != abs(form_data["win_rate"]) + abs(form_data["win_rate2"]):
        raise forms.ValidationError("输入的中奖人数不符合要求！请重新填写！")
    if (
        form_data.get("staff_list2", None)
        and form_data["staff_list"] == form_data["staff_list2"]
    ):
        raise forms.ValidationError("不能选择两个相同的关联名单！")
    return form_data


@admin.register(Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "prize",
        "sequence",
        "times",
        "number",
        "status",
        "take_in_scene",
        "is_add_exclusion",
    ]
    exclude = ["image"]
    actions = ["make_activated", "make_all_acticated"]
    fieldsets = (
        (None, {"fields": ("name", "prize", "picture", "status")}),
        (
            "设置",
            {
                "fields": (
                    "sequence",
                    "need_input",
                    "take_in_scene",
                    "can_absence_draw",
                    "is_add_exclusion",
                    "co_existed_award",
                )
            },
        ),
        (
            None,
            {
                "fields": (
                    "number",
                    "staff_list",
                    "win_rate",
                    "staff_list2",
                    "win_rate2",
                ),
                "description": '<span style="color:red">*每次中奖人数要等于名单1和名单2中奖人数之和，且关联名单1与关联名单2不可相同</span>',
            },
        ),
    )

    def save_form(self, request, form, change):
        """
        Given a ModelForm return an unsaved instance. ``change`` is True if
        the object is being changed, and False if it's being added.
        """
        new_object = form.save(commit=False)
        file = request.FILES.get("picture", None)
        if file:
            new_object.compressed_picture = InMemoryUploadedFile(
                make_thumb(new_object.picture.file),
                None,
                new_object.picture.name,
                None,
                0,
                None,
            )
        new_object.save()
        return new_object

    def make_activated(self, request, queryset):
        if queryset.count() > 1:
            self.message_user(request, "只允许一个奖项为激活状态", level=messages.ERROR)
        else:
            queryset.update(status=1)
            # 重新激活之后，去掉奖项对应的中奖人员
            Winner.objects.filter(award_id=queryset.first().id).delete()

    make_activated.short_description = "更新为激活状态"

    def make_all_acticated(self, request, queryset):
        awards = Award.objects.all()
        awards.update(status=1)
        # 重新激活之后，去掉已中奖人员
        Winner.objects.all().delete()

    make_all_acticated.short_description = "激活全部奖项"

    def make_inactivated(self, request, queryset):
        queryset.update(status=0)
        count = queryset.count()
        self.message_user(request, "%d条记录更新为未激活状态" % count, level=messages.SUCCESS)

    make_inactivated.short_description = "更新为未激活状态"

    def response_change(self, request, obj, post_url_continue=None):
        next = request.GET.get("next", None)
        if next is not None:
            return HttpResponseRedirect(settings.SITE_URL)
        else:
            return super(AwardAdmin, self).response_change(request, obj)

    def response_add(self, request, obj, post_url_continue=None):
        next = request.GET.get("next", None)
        if next is not None:
            return HttpResponseRedirect(settings.SITE_URL)
        else:
            return super(AwardAdmin, self).response_add(request, obj)

    def get_form(self, request, obj=None, **kwargs):
        form = admin.ModelAdmin.get_form(self, request, obj, **kwargs)
        form.clean = my_clean
        return form

    def save_model(self, request, obj, form, change):
        file = request.FILES.get("picture", None)
        if file:
            compressed_file_string = base64.b64encode(
                obj.compressed_picture.file.read()
            )
            encodedString = base64.b64encode(obj.picture.file.read())
            obj.image = "data:image/jpg;base64," + encodedString.decode()
            obj.compressed_image = (
                "data:image/jpg;base64," + compressed_file_string.decode()
            )
            obj.save()
        else:
            obj.save()
        if obj.status == 1:
            Winner.objects.filter(award_id=obj.id).delete()


@admin.register(Winner)
class WinnerAdmin(admin.ModelAdmin):
    list_display = ["staff", "award", "remark"]
    actions = ["delete_all"]

    def delete_all(self, request, queryset):
        Winner.objects.all().delete()

    delete_all.short_description = "删除全部"


@admin.register(Exclusion)
class ExclusionAdmin(admin.ModelAdmin):
    list_display = ["staff"]


class WheelItemAdmin(admin.ModelAdmin):
    list_display = ["title"]


@admin.register(ExclusionForAll)  # noqa
class WinnerAdmin(admin.ModelAdmin):
    list_display = ["staff"]
    actions = ["delete_all"]

    def delete_all(self, request, queryset):
        ExclusionForAll.objects.all().delete()

    delete_all.short_description = "删除全部"
