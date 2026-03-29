from django.urls import path
from .views import OrderCreateView, OrderStatusView
from . import views
urlpatterns = [
    # Path for creating a new order
    path('', OrderCreateView.as_view(), name='order-create'),

    # Path for checking an order status (Polling)
    path('<int:pk>/status/', OrderStatusView.as_view(), name='order-status'),

    # Path for listing all orders
    path('all/', views.order_list, name='order-list'),
]