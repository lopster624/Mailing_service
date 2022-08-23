from django.urls import path, include
from rest_framework.routers import DefaultRouter

from mailing.views import ClientViewSet, MailingViewSet, MailingStatisticViewSet

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'mailings', MailingViewSet)
router.register(r'mailing-statistics', MailingStatisticViewSet, basename='mailing-statistics')


urlpatterns = [
    path(r'', include(router.urls)),

]