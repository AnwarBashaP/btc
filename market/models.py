import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class StocksAlertsModel(models.Model):
    name = models.CharField(max_length=255, verbose_name='Stock Name')
    alert_price = models.DecimalField(max_digits=15, decimal_places=2, verbose_name='Stocks alert Price')
    triggered = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,  related_name='Created_by_user', on_delete=models.CASCADE,
                                   null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'stocks_alerts'
        verbose_name = 'Stock Alert'
        verbose_name_plural = 'Stock Alerts'

    def __str__(self):
        return self.name