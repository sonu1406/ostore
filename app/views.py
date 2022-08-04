
from django import views
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import Customer,Product,OrderPlaced,Cart
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class ProductView(View):
    def get(self,request):
        topwears=Product.objects.filter(category='TW')
        bottomwears=Product.objects.filter(category='BW')
        mobiles=Product.objects.filter(category='M')
        return render(request,'app/home.html',{'topwears':topwears,'bottomwears':bottomwears,'mobiles':mobiles})


class ProductDeatil(View):
    def get(self,request,pk):
        product=Product.objects.get(pk=pk)
        already_item_in_cart=False
        if request.user.is_authenticated:
            already_item_in_cart=Cart.objects.filter(Q(product=product.id) &Q(user=request.user)).exists()
        print(already_item_in_cart)
        return render(request,'app/productdetail.html',{'product':product,'already_item_in_cart':already_item_in_cart})
 


@login_required
def add_to_cart(request):
    user=request.user
    product_id=request.GET.get('prod_id')
    product=Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user=request.user
        cart=Cart.objects.filter(user=user)
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user==user]
        if cart_product:
            for p in cart_product:
                temp=(p.quantity*p.product.discounted_price)
                amount+=temp
                total=amount+shipping_amount
            return render(request,'app/addtocart.html',{'carts':cart,'totalamount':total,'amount':amount})
        else:
            return render(request,'app/emptycart.html')


@login_required
def plus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
                temp=(p.quantity*p.product.discounted_price)
                amount+=temp
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':amount+shipping_amount
        }
        return JsonResponse(data)


@login_required
def minus_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
                temp=(p.quantity*p.product.discounted_price)
                amount+=temp
        data={
            'quantity':c.quantity,
            "amount":amount,
            "totalamount":amount+shipping_amount
        }
        return JsonResponse(data)


@login_required
def remove_cart(request):
    if request.method=='GET':
        prod_id=request.GET['prod_id']
        c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
                temp=(p.quantity*p.product.discounted_price)
                amount+=temp
        data={
            'amount':amount,
            'totalamount':amount+shipping_amount
        }
        return JsonResponse(data)






@login_required
def buy_now(request):
    return render(request, 'app/buynow.html')

@login_required
def address(request):
    add=Customer.objects.filter(user=request.user)
    return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

@login_required
def orders(request):
    op=OrderPlaced.objects.filter(user=request.user)
    return render(request,'app/orders.html',{'order_placed':op})
@login_required
def mobile(request,data=None):
    if data==None:
        mobiles=Product.objects.filter(category='M')
    elif data=='Mi' or data=='Iphone':
        mobiles=Product.objects.filter(category='M').filter(brand=data)
    elif data=="below":
        mobiles=Product.objects.filter(category='M').filter(discounted_price__lt=50000)
    elif data=="above":
        mobiles=Product.objects.filter(category='M').filter(discounted_price__gt=50000)
    
    return render(request, 'app/mobile.html',{'mobiles':mobiles})

def laptop(request,data=None):
    if data==None:
        laptop=Product.objects.filter(category='L')
    elif data=='Azus' or data=='apple' or data=="Alien-Ware":
        laptop=Product.objects.filter(category='L').filter(brand=data)
    elif data=="below":
        laptop=Product.objects.filter(category='L').filter(discounted_price__lt=50000)
    elif data=="above":
        laptop=Product.objects.filter(category='L').filter(discounted_price__gt=50000)
    
    return render(request, 'app/laptop.html',{'laptop':laptop})

def bottom(request,data=None):
    if data==None:
        bottom=Product.objects.filter(category='BW')
    elif data=="Celio":
        bottom=Product.objects.filter(category='BW').filter(brand=data)
    elif data=="Louise Phillipe":
        bottom=Product.objects.filter(category='BW').filter(brand=data)
    elif data=="Lee":
        bottom=Product.objects.filter(category='BW').filter(brand=data)
    elif data=="code":
        bottom=Product.objects.filter(category='BW').filter(brand=data)

    return render(request, 'app/bottom.html',{'bottom':bottom})

def top(request,data=None):
    if data==None:
        top=Product.objects.filter(category='TW')
    elif data=="allen-solly":
        top=Product.objects.filter(category='TW').filter(brand=data)
    elif data=="US-Polo":
        top=Product.objects.filter(category='TW').filter(brand=data)
    elif data=="Celio":
        top=Product.objects.filter(category='TW').filter(brand=data)
    elif data=="peoples":
        top=Product.objects.filter(category='TW').filter(brand=data)

    return render(request, 'app/top.html',{'top':top})




def login(request):
 return render(request, 'app/login.html')

class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',{'form':form})
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congartulations !! Registered Succesfully')
            form.save()
        return render(request,'app/customerregistration.html',{'form':form})


@login_required
def payment_done(request):
    user=request.user
    custid=request.GET.get('custid')
    customer=Customer.objects.get(id=custid)
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect('orders')




@login_required
def checkout(request):
    user=request.user
    add=Customer.objects.filter(user=user)
    cart=Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount=70.0
    cart_product=[p for p in Cart.objects.all() if p.user==request.user]
    if cart_product:
        for p in cart_product:
                temp=(p.quantity*p.product.discounted_price)
                amount+=temp
    total=amount+shipping_amount
    return render(request, 'app/checkout.html',{'add':add,'totalamount':total,'carts':cart})

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form=CustomerProfileForm
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
    def post(self,request):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            usr=request.user
            name=form.cleaned_data['name']
            locality=form.cleaned_data['locality']
            city=form.cleaned_data['city']
            state=form.cleaned_data['state']
            zipcode=form.cleaned_data['zipcode']
            reg=Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,'Congatulation!! Profile Update Successfully')
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
            
