from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema
from .models import *
from .serializers import StatusSerializer, TypeSerializer, CategorySerializer, SubCategorySerializer, HistorySerializer
from django.views.generic import TemplateView

# views.py
from django.middleware.csrf import get_token
from django.http import JsonResponse

def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

class FrontendAppView(TemplateView):
    template_name = 'index.html'


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    @extend_schema(
        summary="Получить список статусов",
        description="Возвращает список доступных статусов"
    )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

    @extend_schema(
        summary="Получить список типов",
        description="Возвращает список типов"
    )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @extend_schema(
        summary="Получить список категорий",
        description="Возвращает список типов"
    )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

    @extend_schema(
        summary="Получить список категорий",
        description="Возвращает список типов"
    )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class HistoryViewSet(viewsets.ModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer

    @extend_schema(
        summary="Получить историю транзакций",
        description="Возвращает список транзакций"
    )

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)