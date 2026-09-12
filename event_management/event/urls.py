from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register('category', CategoryViewSet)
router.register('event', EventsViewsets)

urlpatterns = router.urls

