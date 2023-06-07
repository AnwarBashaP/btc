import django_filters
import requests
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework import generics, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from market.models import StocksAlertsModel
from market.serializer import StocksAlertSerializer

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


# Create your views here.
class StockAlertCreateView(generics.CreateAPIView):
    """
        POST api/alerts/create/
        GET api/alerts/create/
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = StocksAlertSerializer
    pagination_class = LimitOffsetPagination
    model = StocksAlertsModel
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

    filterset_fields = ['id', 'name', 'triggered', 'alert_price']

    def perform_create(self, serializer):
        cache.delete("stocks")
        serializer.save(created_by=self.request.user, status=True)
        cache.set('stocks', self.model.objects.filter(created_by=self.request.user))


# Create your views here.
class StockAlertRetrieveView(generics.ListAPIView):
    """
        GET api/alerts/create/
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = StocksAlertSerializer
    pagination_class = LimitOffsetPagination
    model = StocksAlertsModel
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]

    filterset_fields = ['id', 'name', 'triggered', 'alert_price']

    def get_queryset(self):
        alerts = StocksAlertsModel.objects.first()

        triggered = str(self.request.query_params.get('triggered')).capitalize()
        if triggered in ['True', 'False']:
            qs = self.model.objects.filter(created_by=self.request.user,
                                             triggered=triggered)
            cache.set('stocks', qs)
            return qs
        if stocks := cache.get('stocks'):
            return stocks
        qs = self.model.objects.filter(created_by=self.request.user)
        cache.set('stocks', qs)
        return qs


class StockAlertDeleteView(generics.DestroyAPIView):
    """
        DELETE api/alerts/delete/<pk>
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = StocksAlertSerializer
    model = StocksAlertsModel

    def get_queryset(self):
        return self.model.objects.filter(pk=self.kwargs['pk'], created_by=self.request.user)

    def perform_destroy(self, instance):
        return instance.delete()


class StockView(APIView):
    """
        POST api/stocks/
    """
    permission_classes = (AllowAny,)

    def get(self, request):
        stocks_data = requests.get(
            'https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false')
        return Response(stocks_data.json(), status=status.HTTP_200_OK)
