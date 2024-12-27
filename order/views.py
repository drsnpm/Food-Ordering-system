from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Category, Product, Customer, Order
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.views import View
from .middlewares.auth import auth_middleware
from django.utils.decorators import method_decorator

class Index(View):
    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart', {})
        quantity = cart.get(product, 0)
        remove = remove == 'True'
        if remove:
            if quantity <= 1:
                cart.pop(product)
            else:
                cart[product] = quantity - 1
        else:
            cart[product] = quantity + 1

        request.session['cart'] = cart
        category_id = request.GET.get('category')
        if category_id:
            return redirect(f'/?category={category_id}')
        return redirect('homepage')

    def get(self, request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        categories = Category.objects.all()
        category_id = request.GET.get('category')
        if category_id and category_id.isdigit():
            products = Product.objects.filter(category_id=category_id)
        else:
            products = Product.objects.all()
        data = {
            'products': products,
            'categories': categories,
            'selected_category': category_id if category_id and category_id.isdigit() else None,
        }
        return render(request, 'order/index.html', data)

class Login(View):
    return_url = None
    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, 'order/login.html')
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.objects.filter(email=email).first()
        if customer:
            pass_match = check_password(password, customer.password)
            if pass_match:
                request.session['customer'] = customer.id
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('homepage')
            else:
                error_msg = "Email or Password Invalid"
        else:
            error_msg = "Email or Password Invalid"
        return render(request, 'order/login.html', {'error': error_msg})


class SignUp(View):
    def get(self, request):
        return render(request, 'order/signup.html')
    def post(self, request):
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        uname = request.POST.get('uname')
        password = request.POST.get('password')

        error_msg = None
        if Customer.objects.filter(uname=uname).exists():
            error_msg = "User name already exists"
        elif Customer.objects.filter(email=email).exists():
            error_msg = "Email already exists"
        elif Customer.objects.filter(mobile=mobile).exists():
            error_msg = "Mobile number already exists"
        
        if len(name) < 4:
            error_msg = "Name must be at least 4 characters long."
        elif len(mobile) < 10:
            error_msg = "Mobile number must be 10 characters long or more."
        elif len(password) < 8:
            error_msg = "Password must be 8 charcter"
        if not error_msg:
            customer = Customer.objects.create(name=name, email=email, mobile=mobile, uname=uname, password=password)
            customer.password = make_password(customer.password)
            customer.save()
            return redirect('login')
        else:
            return render(request, 'order/signup.html', {'error':error_msg})
    
def Logout(request):
    request.session.clear()
    return redirect('login')


class Cart(View):
    @method_decorator(auth_middleware)
    def get(self, request):
        ids = list(request.session.get('cart').keys())
        products = Product.objects.filter(id__in=ids)
        return render(request, 'order/cart.html',{'products':products})


class CheckOut(View):
    @method_decorator(auth_middleware)
    def post(self, request):
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.objects.filter(id__in=list(cart.keys()))
        for product in products:
            order = Order(customer = Customer(id = customer),
                           product = product,
                           price = product.price,
                           address = address,
                           mobile = mobile,
                           quantity = cart.get(str(product.id)))
            order.save()
        request.session['cart'] = {}
        return render(request, 'order/payment.html')

class Payment(View):
    @method_decorator(auth_middleware)
    def post(self, request):
        return redirect('orders')
        
class OrderView(View):
    @method_decorator(auth_middleware)
    def get(self, request):
        customer = request.session.get('customer')
        orders = Order.objects.filter(customer=customer).order_by('-date')
        return render(request, 'order/orders.html',{'orders':orders})


class Profile(View):
    def get(self, request):
        customer = request.session.get('customer')
        customer_id = request.session.get('customer')
        if customer_id:
            try:
                customer = Customer.objects.get(id=customer_id)
            except Customer.DoesNotExist:
                pass
        return render(request, 'order/profile.html',{'customer':customer})


class Updateprofile(View):
    def get(self, request):
        customer_id = request.session.get('customer')
        customer = Customer.objects.get(id=customer_id)
        return render(request, 'order/updateprofile.html', {'customer': customer})
    def post(self, request):
        customer_id = request.session.get('customer')
        customer = Customer.objects.get(id=customer_id)
        error_msg = None
        name = request.POST.get('name')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        uname = request.POST.get('uname')
        if Customer.objects.filter(email=email).exclude(id=customer_id).exists():
            error_msg = "Email already exists"
        elif Customer.objects.filter(mobile=mobile).exclude(id=customer_id).exists():
            error_msg = "Mobile number already exists"
        if len(name) < 4:
            error_msg = "Name must be at least 4 characters long."
        elif len(mobile) < 10:
            error_msg = "Mobile number must be 10 characters long or more."
        if not error_msg:
            customer.name = name
            customer.email = email
            customer.mobile = mobile
            customer.uname = uname        
            customer.save()
            return redirect('profile')
        return render(request, 'order/updateprofile.html', {'customer': customer, 'error': error_msg})


class UpdatePassword(View):
    def get(self, request):
        return render(request, 'order/update-password.html')
    def post(self, request):
        customer_id = request.session.get('customer')
        oldpass = request.POST.get('oldpass')
        newpass = request.POST.get('newpass')
        customer = Customer.objects.get(id=customer_id)
        if check_password(oldpass, customer.password):
            if oldpass == newpass:
                error_msg = "The new password cannot be the same as the current password"
                return render(request, 'order/update-password.html', {'error': error_msg})
            else:
                customer.password = make_password(newpass)
                customer.save()
                success_msg = "Your password has been updated successfully"
                return render(request, 'order/update-password.html', {'success': success_msg})
        else:
            error_msg = "Invalid current password"
            return render(request, 'order/update-password.html', {'error': error_msg})

from django.shortcuts import redirect, get_object_or_404

def delete_order(request, order_id):
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id)
        order.delete()
    return redirect('orders')

def remove_from_cart(request, product_id):
    cart = request.session.get('cart')
    
    if cart:
        cart.pop(str(product_id), None)
        request.session['cart'] = cart

    return redirect('cart')