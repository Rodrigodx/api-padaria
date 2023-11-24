import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import Product, User


def say_hello_user(request):
    return render(request, 'polls.html')

from django.http import JsonResponse

def get_all_users(request):
    if request.method == 'GET':
        users = User.objects.all()
        data = [{"id": user.id, "name": user.name, "userProduct": {
            "id": user.userProduct_id,
            "name": user.userProduct.name}} for user in users]
        return JsonResponse({"users": data})
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

            name = data.get('name', None)
            user_product_id  = data.get('userProduct', None)

            if not name or user_product_id  is None:
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            try:
                product = Product.objects.get(pk=user_product_id)
            except Product.DoesNotExist:
                return JsonResponse({'error': 'Product not found'}, status=400)

            user = User.objects.create(name=name, userProduct= product)
            return JsonResponse({'message': 'User created successfully', 'user_id': user.id})

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