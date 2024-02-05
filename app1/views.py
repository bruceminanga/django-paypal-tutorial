from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from .models import Order
from django.shortcuts import render, HttpResponse, redirect, \
    get_object_or_404, reverse
    
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal


# Create your views here.
def index(request):
    
    return render(request, 'payments/index.html')


def process_payment(request):
    request.session['order_id'] = '1'
    order_id = request.session.get('order_id')
    print(f'my order id is {order_id}')
    order = get_object_or_404(Order, id=order_id)
    host = request.get_host()


    # What you want the button to do.
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '%.2f' % Decimal(order.total_cost()).quantize(Decimal('.01')),
        'item_name': 'Order {}'.format(order.id),
        'invoice': str(order.id),
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('payment_done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('payment_cancelled')),
    }

    form=PayPalPaymentsForm(initial=paypal_dict)
    context={'form':form}
    print(context)
    return render(request, 'payments/process_payment.html', {'order': order, 'form': form})
    #return HttpResponse(f"Visit count:{request.session['visit']}")
    
@csrf_exempt
def payment_done(request):
    return render(request, 'ecommerce_app/payment_done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'ecommerce_app/payment_cancelled.html')

def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
        #...
        #...

            cart.clear(request)

            request.session['order_id'] = o.id
            return redirect('process_payment')


    else:
        form = CheckoutForm()
        return render(request, 'ecommerce_app/checkout.html', locals())
