from django.urls import path, include
from rest_framework.routers import DefaultRouter

from applications.order import views

router = DefaultRouter()
router.register('', views.OrderViewSet)

urlpatterns = [
    path('confirmation/<uuid:confirm_code>/', views.OrderConfirm.as_view()),
    path('', include(router.urls))
]
