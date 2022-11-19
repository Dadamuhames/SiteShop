from django.urls import path
from . import views


urlpatterns = [
    path('buy', views.buy_page, name='buying_page'),
    path('makeorder', views.make_order, name='make_order'),
    path('manage_orders', views.control_orders, name='manage-page'),
    path('order/<int:pk>', views.ViewOrders.as_view(), name='view_orders'),
    path('buy_prod', views.buyProduct, name='buy_single_prod'),
    path('change_status/<int:ord_id>', views.change_staus, name='chang_st'),
    path('my_order', views.my_orders, name='my_orders'),
    path('cansel_orders/<int:id>', views.cansel_order, name='cansel_orders'),
    path('paycom', views.TestView.as_view())
]