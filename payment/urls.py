from django.urls import path
from . import views


urlpatterns = [
    path('', views.order_view, name="order_view"),
    path('register/', views.register, name="register"),
    path('token/', views.gettoken, name="token"),
]