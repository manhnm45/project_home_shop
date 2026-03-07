from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.db.models import Max
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
from django.core.cache import cache
# import rabbitmq
# from process_postgre_db import PostgreSQLProcessor
# Create your views here.
def get_home(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'home.html',context)

# def query_db(request):
#     db = PostgreSQLProcessor(dbname="postgres", user="postgres", password="1")
#     db.connect()
#     data = db.fetch_users()
#     return render(request, 'home.html', {'data': data})



def render_ai_search(request):
    print("oke")
    return render(request, 'ai_search.html')

@api_view(['POST'])
@parser_classes([JSONParser])
def upload_item(request):
    # image = request.FILES.get('image')
    name = request.data.get("name")
    # print("name", name)
    img_path, cost = Product().get_img_path_and_cost(name)
    if img_path is None:
        return render(request, 'ai_search.html')
    if img_path.startswith("/home/minhanh/Downloads/project_home/web_sell/"):
        img_path = img_path.replace("/home/minhanh/Downloads/project_home/web_sell/", "/")
    
    # print("img_path", img_path)
    cache.set('latest_ai_result', {
        'img_path': img_path,
        'cost': cost
    }, timeout=60)  # giữ trong 60 giây

    return Response({ 'status': 'ok' })

@api_view(['GET'])
def get_latest_result(request):
    result = cache.get('latest_ai_result')
    if result:
        return Response(result)
    else:
        return Response({ 'img_path': '', 'cost': '' })

def update_item(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.cost = request.POST.get('cost')
        product.Image_path = request.POST.get('Image_path')
        product.save()
        return redirect('home')
    context = {'product': product}
    return render(request, 'update_item.html', context)

def delete_item(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('home')
    context = {'product': product}
    return render(request, 'delete_item.html', context)

def create_item(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        cost = request.POST.get('cost')
        image = request.FILES['image']
        
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        image_path = fs.url(filename)
        
        # Calculate new ID manually since DB does not auto-increment
        max_id = Product.objects.aggregate(Max('Id'))['Id__max']
        new_id = (max_id + 1) if max_id is not None else 1
        
        product = Product(Id=new_id, name=name, cost=cost, Image_path=image_path)
        product.save()
        
        return redirect('home')
    return render(request, 'add_item.html')