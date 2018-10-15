from django.conf.urls import url, include
from rest_framework import routers

from screens.views import ScreensView

router = routers.SimpleRouter()
router.register(r'^screens', ScreensView)

urlpatterns = [
    url(r'^', include(router.urls)),
]