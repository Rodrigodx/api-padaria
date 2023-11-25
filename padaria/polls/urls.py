from django.urls import path

from . import views

urlpatterns = [
    path('', views.say_hello_user),
    path('product', views.get_all_products),
    path('order', views.get_all_orders),
    path('createO', views.create_order),
    path('createP', views.create_product)
]