from rest_framework import  serializers

from market.models import StocksAlertsModel


class StocksAlertSerializer(serializers.ModelSerializer):

    class Meta:
        model = StocksAlertsModel
        fields = '__all__'