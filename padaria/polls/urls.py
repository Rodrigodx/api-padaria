from django.urls import path

from . import views

urlpatterns = [
    path('', views.say_hello_user),
    path('product', views.get_all_products),
    path('user', views.get_all_users),
    path('createU', views.create_user),
    path('createP', views.create_product)
]