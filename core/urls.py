from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from . import views

from .views import StatusViewSet, TypeViewSet, CategoryViewSet, SubCategoryViewSet, HistoryViewSet, FrontendAppView

router = DefaultRouter()
router.register(r'statuses', StatusViewSet)
router.register(r'types', TypeViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubCategoryViewSet)
router.register(r'history', HistoryViewSet)


urlpatterns = [
    # path('', views.index, name='index'),

    path('api/', include(router.urls)),
    path('api/get-csrf-token/', views.get_csrf_token, name='get-csrf-token'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    re_path(r'^.*$', FrontendAppView.as_view(), name='frontend'),
]