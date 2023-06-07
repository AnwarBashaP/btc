from django.urls import path
from .views import StockAlertCreateView, StockView, StockAlertDeleteView, StockAlertRetrieveView

urlpatterns = [
    path('alerts/create/', StockAlertCreateView.as_view()),
    path('alerts/retrieve/', StockAlertRetrieveView.as_view()),
    path('alerts/delete/<int:pk>/', StockAlertDeleteView.as_view()),
    path('stocks/', StockView.as_view())
]