import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Product, Order


def say_hello_user(request):
    return render(request, 'polls.html')

from django.http import JsonResponse

def get_all_users(request):
    if request.method == 'GET':
        orders = Order.objects.all()
        data = [{"id": orders.id, "clientName": orders.name, "userProduct": {
            "id": orders.orderProduct_id,
            "name": orders.orderProduct.name}} for order in orders]
        return JsonResponse({"orders": data})
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)


def get_all_products(request):
    product = Product.objects.all()
    data = [{"id":product.id,"name": product.name} for product in product]
    return JsonResponse({"product": data})

@csrf_exempt
@require_POST
def create_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))

            name = data.get('clientName', None)
            order_product_id  = data.get('userProduct', None)

            if not name or order_product_id  is None:
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            try:
                product = Product.objects.get(pk=order_product_id)
            except Product.DoesNotExist:
                return JsonResponse({'error': 'Product not found'}, status=400)

            order = Order.objects.create(clientName=name, orderProduct= product)
            return JsonResponse({'message': 'User created successfully', 'user_id': order.id})

        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Error creating user: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})




@csrf_exempt
@require_POST
def create_product(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))

            name = data.get('name', None)

            if not name:
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            product = Product.objects.create(name=name)
            return JsonResponse({'message': 'User created successfully', 'product_id': product.id})

        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Error creating user: {str(e)}'}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'})