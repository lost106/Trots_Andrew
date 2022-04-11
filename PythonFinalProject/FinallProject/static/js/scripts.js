$(document).ready(function () {
    let form = $('#form_buying_product');
    console.log((form))

    function basketUpdating(product_id, nmb, is_delete) {
        let data = {};
        data.product_id = product_id;
        data.nmb = nmb;
        data["csrfmiddlewaretoken"] = $('#form_buying_product [name="csrfmiddlewaretoken"]').val();

        if (is_delete) {
            data["is_delete"] = true
        }

        let url = form.attr("action");

        console.log(data);

        $.ajax({
            url: url,
            type: 'POST',
            data: data,
            cache: true,
            success: function (data) {
                console.log('OK');
                console.log(data.products_total_nmb);
                if (data.products_total_nmb || data.products_total_nmb === 0) {
                    $('#basket_total_nmb').text('  (' + data.products_total_nmb + ')')
                    console.log(data.products);
                    $('#basket_items').html("")
                    //добавление товара в корзину
                    $.each(data.products, function (k, v) {
                        $('#basket_items').append('<li class="dropdown-item">'
                            + v.name + ', ' + v.nmb + 'шт. ' + 'по  ' + v.price_per_item + ' BYN  ' +
                            '<a class="delete-item" href="" data-product_id="' + v.id + '">x</a>' +
                            '</li>');
                    })
                }

            },
            error: function () {
                console.log('error')
            }
        })


    }


    form.on('submit',function (e) {
        e.preventDefault();
        let nmb = $('#number').val()
        let submit_btn = $('#submit_btn');
        let product_id = submit_btn.data('product_id');
        let product_name = submit_btn.data('name');
        let product_price = submit_btn.data('price');
        basketUpdating(product_id, nmb, is_delete = false)


    });

    $(document).on('click', '.delete-item', function (e) {
        e.preventDefault()
        product_id = $(this).data("product_id");
        nmb = 0;
        basketUpdating(product_id, nmb, is_delete = true)
    });
    function calculatingBasketAmount(){
        let total_order_amount = 0;
        $('.total-product-in-basket-amount').each(function() {
            total_order_amount = total_order_amount + parseFloat($(this).text());
        });
        $('#total_order_amount').text(total_order_amount.toFixed(2));
    }

    $(document).on('change', ".product-in-basket-nmb", function(){
        let current_nmb = $(this).val();
        let current_tr = $(this).closest('tr');
        let current_price = parseFloat(current_tr.find('.product-price').text()).toFixed(2);
        let total_amount = parseFloat(current_nmb*current_price).toFixed(2);
        current_tr.find('.total-product-in-basket-amount').text(total_amount);

        calculatingBasketAmount();
    });


});

// (function(a){a.fn.cycle=function(d){
//     let c=a("img",this),e=c.length-1,b=0;c.each(function(f){a(this).css({position:"absolute","z-index":e-f})});
//     setInterval(function(){g()},d.interval);
//     let g=function(){c.eq(b).animate({opacity:0},d.speed,function(){
//         a(this).css({"z-index":0,opacity:1}).siblings().css("z-index",function(f,h){
//             return parseInt(h)+1});b<e?b++:b=0})}}})(jQuery)


// $('.advert-item').cycle({
// interval: 4000,
// speed: 1000
// });
//
//
//  let angle = 0;
// function galleryspin(sign) {
// spinner = document.querySelector("#spinner");
// if (!sign) { angle = angle + 45; } else { angle = angle - 45; }
// spinner.setAttribute("style","-webkit-transform: rotateY("+ angle +"deg); -moz-transform: rotateY("+ angle +"deg); transform: rotateY("+ angle +"deg);");
// }
