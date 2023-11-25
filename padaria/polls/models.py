from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Order(models.Model):
    clientName = models.CharField(max_length=40)
    orderProduct = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.clientName