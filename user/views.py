from base64 import urlsafe_b64decode
from http.client import ACCEPTED
from django.db.models import Count
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
import razorpay
from .models import STATUS_CHOICES, Product, Cart, Customer, Payment, OrderPlaced, Wishlist
from .forms import ContactMessageForm, CustomerRegistrationForm, CustomerProfileForm, ReviewForm
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.conf import settings
from user.models import Customer, Payment, OrderPlaced, Cart
from django.http import HttpResponseRedirect




def home(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).count()
        wishitem = Wishlist.objects.filter(user=request.user).count()
    return render(request, 'index.html', locals())

class CategoryView(View):
    def get(self, request, val):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = Cart.objects.filter(user=request.user).count()
            wishitem = Wishlist.objects.filter(user=request.user).count()
        product = Product.objects.filter(category=val)
        name = Product.objects.filter(category=val).values('name')
        return render(request, 'category.html', locals())

class CategoryName(View):
    def get(self, request, val):
        products = Product.objects.filter(name=val)
        category_name = products[0].category.name if products else None
        category_names = Product.objects.filter(category=category_name).values_list('category__name', flat=True).distinct()
        sorted_category_names = sorted(category_names, key=lambda x: x.lower())
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = Cart.objects.filter(user=request.user).count()
            wishitem = Wishlist.objects.filter(user=request.user).count()
        return render(request, 'category.html', {'sorted_category_names': sorted_category_names, 'category_name': category_name, 'totalitem': totalitem})

class ProductDetail(View):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        wishlist = None
        totalitem = Cart.objects.filter(user=request.user).count() if request.user.is_authenticated else 0
        wishitem = Wishlist.objects.filter(user=request.user).count() if request.user.is_authenticated else 0
        review_form = ReviewForm()  # Create review form instance
        return render(request, 'productdetail.html', {'product': product, 'totalitem': totalitem, 'wishlist': wishlist, 'wishitem': wishitem})

    def post(self, request, pk):
        if request.user.is_authenticated:
            product = get_object_or_404(Product, pk=pk)
            totalitem = Cart.objects.filter(user=request.user).count()
            wishitem = Wishlist.objects.filter(user=request.user).count()
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
                messages.success(request, 'Review added successfully.')
            else:
                messages.error(request, 'Failed to add review. Please check your input.')
            return render(request, 'productdetail.html', {'product': product, 'totalitem': totalitem, 'wishitem': wishitem, 'review_form': review_form})
        else:
            return render(request, 'productdetail.html', {'error': 'You need to login to post a review.'})


class CustomerRegistrationView(View):
    template_name = 'register.html'

    def get(self, request):
        form = CustomerRegistrationForm()
        total_item = 0
        wishitem = 0
        if request.user.is_authenticated:
            total_item = Cart.objects.filter(user=request.user).count()
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, self.template_name, {'form': form, 'total_item': total_item})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulations! Profile saved successfully')
            # Redirect to the login page
            return HttpResponseRedirect(reverse('login'))
        else:
            messages.warning(request, 'Invalid input data')

        return render(request, self.template_name, {'form': form})


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'profile.html', {'form': form, 'totalitem': totalitem, 'wishitem': wishitem})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            gender = form.cleaned_data['gender']
            Address = form.cleaned_data['Address']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            pincode = form.cleaned_data['pincode']
            country = form.cleaned_data['country']

            reg = Customer.objects.create(
                user=user, name=name, gender=gender, Address=Address,
                mobile=mobile, city=city, state=state, pincode=pincode, country=country
            )
            messages.success(request, 'Congratulations! Profile saved successfully')
        else:
            messages.warning(request, 'Invalid input data')
        return render(request, 'profile.html', {'form': form})


#Fetch the Address data from database to display on the adress page so we use only def function 
@login_required
def Address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'address.html',locals())


@method_decorator(login_required, name='dispatch')
class updateAddress(View):
    template_name = 'updateAddress.html'

    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request, self.template_name, locals())

    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)
        add = Customer.objects.get(pk=pk)

        if 'delete_Address' in request.POST:
            # Handle delete action
            add.delete()
            
            return redirect("Address")

        if form.is_valid():
            add.name = form.cleaned_data['name']
            add.gender = form.cleaned_data['gender']
            add.Address = form.cleaned_data['Address']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.pincode = form.cleaned_data['pincode']
            add.country = form.cleaned_data['country']
            add.save()
        
        else:
            messages.warning(request, "Invalid Input Data")

        return redirect("Address")

@login_required
def add_to_cart(request):
    if request.method == 'GET':
        product_id = request.GET.get('prod_id')
        product = Product.objects.get(id=product_id)
        Cart(user=request.user, product=product).save()
        return redirect('/cart')

from django.contrib.auth.models import AnonymousUser

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = sum(p.quantity * p.product.dis_price for p in cart)
        totalamount = amount + 50
        totalitem = len(cart)
        wishitem = len(Wishlist.objects.filter(user=user))
    else:
        cart = []
        totalamount = 0
        totalitem = 0
        wishitem = 0

    return render(request, 'addtocart.html', {'cart': cart, 'totalamount': totalamount, 'totalitem': totalitem, 'wishitem': wishitem, 'amount': amount})

@login_required
def show_wishlist(request):
    user = request.user
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    product = Wishlist.objects.filter(user=user)
    return render(request, 'wishlist.html',locals())


@method_decorator(login_required,name='dispatch')
class checkout(View):
    def get(self,request):
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.dis_price
            famount = famount + value
        totalamount = famount + 50
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {"amount": razoramount, "currency": "INR", "receipt": "order_rcptid_12"}
        payment_response = client.order.create(data=data)
        print(payment_response)
        # {'id': 'order_Mi1nTAhBIHxzwe', 'entity': 'order', 'amount': 12004000, 'amount_paid': 0, 'amount_due': 12004000, 'currency': 'INR', 'receipt': 'order_rcptid_12', 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': [], 'created_at': 1695963600}
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user = user,
                amount = totalamount,
                razorpay_order_id = order_id,
                razorpay_payment_status = order_status
            )
            payment.save()
        return render(request, 'checkout.html',locals())

@login_required
def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    
    if not cust_id:
        # If cust_id is empty, return an error response
        return HttpResponse("Customer ID is missing", status=400)

    user = request.user

    try:
        customer = Customer.objects.get(id=cust_id)
    except Customer.DoesNotExist:
        # If customer does not exist, return an error response
        return HttpResponse("Invalid customer ID", status=400)

    try:
        payment = Payment.objects.get(razorpay_order_id=order_id)
    except Payment.DoesNotExist:
        # If payment does not exist, return an error response
        return HttpResponse("Invalid payment ID", status=400)

    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()

    # Save order details
    order_details = []
    cart = Cart.objects.filter(user=user)
    for c in cart:
        order = OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity, payment=payment)
        order.save()
        order_details.append(f"Product: {c.product.name}, Quantity: {c.quantity}")

        c.delete()

    # Send confirmation email to the user
    subject = 'Order Confirmation'
    message = f'Thank you for your order. Your payment has been successfully processed.\n\n'
    message += f'Order ID: {order_id}\nPayment ID: {payment_id}\n\n'
    message += 'Ordered Products:\n'
    message += '\n'.join(order_details) + '\n\n'
    message += 'You can view your order details on our website:\n'
    message += request.build_absolute_uri(reverse('orders'))

    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = [user.email]

    try:
        send_mail(subject, message, from_email, to_email, fail_silently=False)
        messages.success(request, 'Payment successful. An email confirmation has been sent.')
    except Exception as e:
        messages.error(request, f'Payment successful, but failed to send confirmation email. Error: {e}')

    return redirect('orders')

from django.shortcuts import render
from .models import OrderPlaced

@login_required
def orders(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    
    order_placed = OrderPlaced.objects.filter(user=request.user).order_by('-ordered_date')  # Reverse the order of the queryset
    
    return render(request, 'orders.html', {'order_placed': order_placed, 'totalitem': totalitem, 'wishitem': wishitem})

@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.dis_price
            amount = amount + value
        totalamount = amount + 50  
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.dis_price
            amount = amount + value
        totalamount = amount + 50  
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.dis_price
            amount = amount + value
        totalamount = amount + 40  
        data={
            'amount':amount,
            'totalamount':totalamount
        }
        return JsonResponse(data)
    
def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user,product=product).save()
        data={
            'message':'wishlist Added Successfully' 
        }
        return JsonResponse(data)

def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user,product=product).delete()
        data={
            'message':'wishlist Remove Successfully' 
        }
        return JsonResponse(data)
from django.shortcuts import redirect
from .models import Wishlist

def remove_from_wishlist(request, product_id):
    if request.method == 'POST':
        user = request.user
        product = Product.objects.get(id=product_id)
        wishlist_item = Wishlist.objects.filter(user=user, product=product)
        
        if wishlist_item.exists():
            wishlist_item.delete()
            
    return redirect('showwishlist')

def search(request):
    query = request.GET['search']
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
       
    product = Product.objects.filter(Q(name__icontains=query))
    return render(request, 'search.html',locals())
    
def update_order_status(request, order_id, new_status):
    order = razorpay.Order.objects.get(pk=order_id)
    order.status = new_status
    order.save()
    

def about_us(request):
    return render(request, 'about_us.html')



def contact_us(request):
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            # Add success message
            messages.success(request, 'Your message has been submitted successfully!')
            return redirect('contact_us')
    else:
        form = ContactMessageForm()

    return render(request, 'contact_us.html', {'form': form})


def view_profile(request):
    user = request.user
    customer = Customer.objects.filter(user=user).first()
    
    context = {
        'user': user,
        'customer': customer
    }
    return render(request, 'view_profile.html', context)
@login_required
def edit_profile(request):
    user = request.user
    customer = Customer.objects.filter(user=user).first()
    
    if request.method == 'POST':
        # Handle form submission for updating profile
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        address = request.POST.get('address')
        city = request.POST.get('city')
        mobile = request.POST.get('mobile')
        pincode = request.POST.get('pincode')
        state = request.POST.get('state')
        country = request.POST.get('country')
        
        # Update customer details
        customer.name = name
        customer.gender = gender
        customer.address = address
        customer.city = city
        customer.mobile = mobile
        customer.pincode = pincode
        customer.state = state
        customer.country = country
        customer.save()
        
        # Redirect to view profile page after saving changes
        return redirect('view_profile')
    
    context = {
        'user': user,
        'customer': customer
    }
    return render(request, 'edit_profile.html', context)


from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login')

from django.shortcuts import render

def privacy_policy(request):
    return render(request, 'privacy_policy.html')
# views.py

from django.shortcuts import render


