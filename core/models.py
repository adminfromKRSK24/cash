from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from smart_selects.db_fields import ChainedForeignKey

# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='categories')

    class Meta:
        unique_together = ('name', 'type')

    def __str__(self):
        return f"{self.name} ({self.type})"

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategory')

    class Meta:
        unique_together = ('name', 'category')

    def __str__(self):
        return f"{self.name} ({self.category})"

class History(models.Model):
    # date = models.DateField(auto_now_add=True)
    date = models.DateField(default=timezone.now)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)
    # category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    category = ChainedForeignKey(
        Category,
        chained_field="type",        # поле в этой модели
        chained_model_field="type",  # поле в модели Category
        show_all=False,
        auto_choose=True,
        sort=True,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    subcategory = ChainedForeignKey(
        SubCategory,
        chained_field="category",       # зависит от поля category
        chained_model_field="category", # поле в SubCategory
        show_all=False,
        auto_choose=True,
        sort=True,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    # subcategory = models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return (
            f"Дата: {self.date}, "
            f"Сумма: {self.amount}, "
            f"Статус: {self.status}, "
            f"Тип: {self.type}, "
            f"Категория: {self.category}, "
            f"Подкатегория: {self.subcategory}, "
            f"Комментарий: {self.comment or '—'}"
        )

    def clean(self):
        if self.category and self.type and self.category.type != self.type:
            raise ValidationError("Категория не принадлежит выбранному типу.")
        if self.subcategory and self.category and self.subcategory.category != self.category:
            raise ValidationError("Подкатегория не принадлежит выбранной категории.")