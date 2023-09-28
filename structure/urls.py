from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import UserViewSet, GroupViewSet, LessonViewSet, LessonOfProductView,ProductStatsViewSet

router = DefaultRouter()
router.register(r'lessons_views', LessonViewSet, 'lesson')
router.register(r'users', UserViewSet, 'user')
#router.register(r'lessons_product/<int:product_id>/', LessonOfProductView, 'lessons-product')
router.register(r'product-stats', ProductStatsViewSet, basename='product-stats')


urlpatterns = [
    path('', include(router.urls)),
]
