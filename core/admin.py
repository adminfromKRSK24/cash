from django.contrib import admin
from .models import *
from rangefilter.filters import DateRangeFilter
from django import forms

# Register your models here.
admin.site.register(Type)
admin.site.register(Category)
admin.site.register(SubCategory)

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_filter = ("id", "name")

@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ("formatted_date", "status", "type", "category", "subcategory", "amount", "comment")
    list_filter = (("date", DateRangeFilter), "status", "type", "category", "subcategory")

    def formatted_date(self, obj):
        return obj.date.strftime("%d.%m.%Y")  # день.месяц.год

    formatted_date.short_description = "Date"       # название колонки
    formatted_date.admin_order_field = "date"       # сортировка по полю date

    formfield_overrides = {
        models.DateField: {
            "widget": forms.DateInput(
                format="%d.%m.%Y",
                attrs={"placeholder": "дд.мм.гггг"}
            ),
            "input_formats": ["%d.%m.%Y"],  # тут Django поймёт этот формат, делаем для ввода
        },
    }
