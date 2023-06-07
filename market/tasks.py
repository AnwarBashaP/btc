import requests
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from market.models import StocksAlertsModel


@shared_task
def send_price_alert_email(user_email):
    subject = 'Price Alert Triggered'
    message = 'The target price has been reached!'
    recipient_list = [user_email]
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)


@shared_task
def check_price_and_send_alerts():
    stocks_list = requests.get(
        'https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false').json()
    for stock in stocks_list:
        alerts = StocksAlertsModel.objects.filter(name__contains=stock['name'], triggered=False,
                                                  alert_price=stock['current_price'])
        for alert in alerts:
            send_price_alert_email.delay(alert.created_by.email)
            alert.triggered = True
            alert.save()
