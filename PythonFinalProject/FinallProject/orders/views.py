from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render

from .forms import CheckOutContactForm
from .models import *


def basket_adding(request):
    return_dict = dict()
    session_key = request.session.session_key

    print(f"это request.POST - {request.POST})")

    data = request.POST
    product_id = data.get("product_id")
    nmb = data.get("nmb")
    is_delete = data.get("is_delete")

    if is_delete == 'true':
        deleted_product = ProductInBasket.objects.filter(id=product_id)
        deleted_product.delete()
        # deleted_product.update(is_active=False)
    else:
        new_product, created = ProductInBasket.objects.get_or_create(session_key=session_key, product_id=product_id,
                                                                     is_active=True, defaults={"nmb": nmb})
        if not created:
            new_product.nmb += int(nmb)
            new_product.save(force_update=True)

    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True)
    products_total_nmb = products_in_basket.count()
    return_dict["products_total_nmb"] = products_total_nmb

    return_dict["products"] = list()

    for item in products_in_basket:
        product_dict = dict()
        product_dict["id"] = item.id
        product_dict["name"] = item.product.name
        product_dict["price_per_item"] = item.price_per_item
        product_dict["nmb"] = item.nmb

        return_dict["products"].append(product_dict)

    print(return_dict)

    return JsonResponse(return_dict)


def checkout(request):
    session_key = request.session.session_key
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, is_active=True)
    form = CheckOutContactForm(request.POST or None)
    total_price = 0
    for product_in_basket in products_in_basket:
        total_price += product_in_basket.total_price
    if request.POST:
        print(request.POST)
        if form.is_valid():
            print("All is correct")
            data = request.POST
            name = data.get("name", "any_name")
            phone = data["phone"]
            email = data.get("email", "no_email")
            address = data["address"]
            comment = data.get("comment", "no_comment")
            user, created = User.objects.get_or_create(username=name, defaults={"first_name": name})

            order = Order.objects.create(user=user, customer_name=name, customer_phone=phone, customer_email=email,
                                         customer_address=address, comments=comment, status_id=1)

            for name, value in data.items():
                if name.startswith("product_in_basket_"):
                    basket_id = name.split("product_in_basket_")[1]
                    product_in_basket = ProductInBasket.objects.get(id=basket_id)
                    print(product_in_basket)

                    product_in_basket.nmb = value
                    product_in_basket.order = order
                    product_in_basket.save(force_update=True)

                    ProductInOrder.objects.create(product=product_in_basket.product, nmb=product_in_basket.nmb,
                                                  price_per_item=product_in_basket.price_per_item,
                                                  total_price=product_in_basket.total_price,
                                                  order=order)

        else:
            print("It's not a correct")

    return render(request, 'orders/basket_checkout.html', locals())
