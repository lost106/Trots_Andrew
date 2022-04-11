from django.shortcuts import render

from products.models import *


def product(request, product_id):
    product_po_id = Product.objects.get(id=product_id)
    print(product_po_id)
    return render(request, 'products/product.html', locals())
