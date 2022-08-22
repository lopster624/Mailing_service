from django.urls import path, include
from rest_framework.routers import DefaultRouter

from mailing.views import ClientViewSet, MailingViewSet

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'mailings', MailingViewSet)


urlpatterns = [
    path(r'', include(router.urls)),

]