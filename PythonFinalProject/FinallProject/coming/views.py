from django.shortcuts import render
from .forms import SubscriberForm
from products.models import *


def coming(request):
    name = "Andrew Trots"
    form = SubscriberForm(request.POST or None)
    return render(request, 'coming/coming.html', locals())


def home(request):
    products_images = ProductImage.objects.filter(is_active=True, is_main=True, product__is_active=True)
    print(products_images)
    products_images_phones = products_images.filter(product__category__id=3)
    products_images_robot_cleaner = products_images.filter(product__category__id=2)
    products_images_techno = products_images.filter(product__category__id=1)

    return render(request, 'coming/home.html', locals())
