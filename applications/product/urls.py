from django.urls import include, path
from rest_framework.routers import DefaultRouter

from applications.product.views import ProductAPIView, CommentAPIView, ReviewAPIView

router = DefaultRouter()

router.register('review', ReviewAPIView)
router.register('comment', CommentAPIView)
router.register('', ProductAPIView)


urlpatterns = router.urls


