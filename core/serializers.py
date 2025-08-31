from rest_framework import serializers
from .models import *

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'

class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    type = TypeSerializer()

    class Meta:
        model = Category
        fields = '__all__'

class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = SubCategory
        fields = '__all__'

class HistorySerializer(serializers.ModelSerializer):
    # Для чтения
    data = serializers.DateField(read_only=True)
    status_display = StatusSerializer(source='status', read_only=True)
    type_display = TypeSerializer(source='type', read_only=True)
    category_display = CategorySerializer(source='category', read_only=True)
    subcategory_display = SubCategorySerializer(source='subcategory', read_only=True)

    # Для записи (по ID)
    status = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all(), write_only=True)
    type = serializers.PrimaryKeyRelatedField(queryset=Type.objects.all(), write_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)
    subcategory = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all(), write_only=True)

    class Meta:
        model = History
        fields = [
            'id', 'data', 'amount', 'comment',
            'status', 'status_display',
            'type', 'type_display',
            'category', 'category_display',
            'subcategory', 'subcategory_display',
        ]

    def validate(self, data):
        category = data.get('category')
        type_ = data.get('type')
        subcategory = data.get('subcategory')

        if category and type_ and category.type != type_:
            raise serializers.ValidationError("Категория не принадлежит выбранному типу.")

        if subcategory and category and subcategory.category != category:
            raise serializers.ValidationError("Подкатегория не принадлежит выбранной категории.")

        return data