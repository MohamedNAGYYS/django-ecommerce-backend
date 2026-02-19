from . import views
from django.urls import path


urlpatterns = [
    path('products/', views.AllProducts.as_view(),name='products'),
    path('orders/', views.OrderView.as_view(), name='orders'),
    path('add_cart/', views.AddCart.as_view(), name='add_cart'),
    path('view_cart/', views.CartView.as_view(), name='view_cart'),
    path('delete_from_cart/', views.DeleteFromCart.as_view(), name='delete_from'),
    path('checkout/', views.CheckOut.as_view(), name='checkout'),
    path('payment/',views.PaymentView.as_view(),name='payment'),
]