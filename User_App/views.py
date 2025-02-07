from django.shortcuts import render,redirect,get_object_or_404
from User_App.models import *
from Admin_App.models import *
from django.contrib.auth.hashers import make_password
from django.db.models import Q 
from .models import DeliveryAddress
from .forms import DeliveryAddressForm
from django.contrib import messages
from .forms import SearchForm
from Admin_App.models import Item, Category  # Import the models from the admin app








# Create your views here.
def user_home(request):
    c = Item.objects.all()
    user_name=request.session.get('user_name', None)
    context = {
        'c':c,
        'user_name':user_name,
    }
    return render(request,"user_home.html",context)

def register(request):
    if request.method =="POST":
        username=request.POST['username']
        email=request.POST['email']
        phone=request.POST['phone']
        password=request.POST['password']
        repassword = request.POST['repassword']

        if Viewers.objects.filter(Q(username__iexact=username) | Q(email__iexact=email)).exists():
             error_message = "Username or email already exists. Please choose another option."
             return render(request, "signup_error.html", {
                'error_message': error_message, 
                'username': username,
                'email': email,
                'phone': phone
            })

        if password == repassword:
            
            Viewers.objects.create(
                username=username,
                email=email,
                phone=phone,
                password=password
            )
            return redirect('user_home')  
        else:
            return redirect('signup_error')

    return render(request, "user_home.html")


def signup_error(request):
     return render(request, "signup_error.html")


def user_login(request):
    email=request.POST['email']
    password=request.POST['password']
    if Viewers.objects.filter(email=email,password=password).exists():
        data = Viewers.objects.filter(email=email, password=password).values('id','username').first()
        request.session['user_id'] = data['id']
        request.session['user_name'] = data['username']
        return redirect('user_home')
    
    else:
        return redirect('login_error')



def login_error(request):
    return render(request,'login_error.html')






def product_home(request,m_id):
    details=Item.objects.filter(id = m_id)
    detail = get_object_or_404(Item,id=m_id)
    review = detail.comment_set.all()
    context = {
        'details' :details,
        'detail' :detail,
        'review' :review,


        }
    return render(request,"product_home.html",context)


def product(request):
    b = Category.objects.all()
    context = {
        'b':b
    }
    if request.method=="POST":

        item_name =request.POST['item_name']
        item_category  =request.POST['category']
        item_picture  =request.FILES['item_picture']
        item_price = request.POST['item_price']
        product_description  =request.POST['product_description']
        
        
        Item.objects.create(

            item_name = item_name,
            item_category  = Category.objects.get(id=item_category),
            item_picture  = item_picture,
            item_price  = item_price,
            product_description = product_description
        )

def user_logout(request):
    request.session.delete()
    return redirect('user_home')

def add_to_cart(request, pk):
    user = Viewers.objects.first()
    product = get_object_or_404(Item, pk=pk)
    cart_item, created = Cart.objects.get_or_create(user=user , product=product)
    

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')

def view_cart(request):
    user = Viewers.objects.first()
    cart_items= Cart.objects.filter(user=user)
    total = sum(item.total_price() for item in cart_items)
    return render(request, 'view_cart.html' , {'cart_items': cart_items, 'total': total})

def remove_from_cart(request,pk):
    cart_item = get_object_or_404(Cart, pk=pk)
    cart_item.delete()
    return redirect('view_cart')







def buy_now(request, item_id):
    if 'user_id' not in request.session:
        return redirect('user_home')
    
    user = get_object_or_404(Viewers, id=request.session['user_id'])
    product = get_object_or_404(Item, id=item_id)
    quantity = 1  # Default quantity
    size = "M"  # Default size
    color = "Black"  # Default color
    total_price = product.item_price * quantity  # Fix calculation


    

    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        size = request.POST.get("size", "M")  # Get selected size
        color = request.POST.get("color", "Black")  # Get selected color
        total_price = product.item_price * quantity  # Correct calculation using DecimalField

        try:
            # Create a new BuyNow record
            buy_now_record = BuyNow.objects.create(
                user=user,
                product=product,
                quantity=quantity,
                size=size,
                color=color,
                payment_status='Pending'  # Ensures payment status is set to Pending

            )
            print("BuyNow record created successfully:", buy_now_record)

            # Redirect to add_delivery_address with the BuyNow record ID
            return redirect("add_delivery_address", r_id=buy_now_record.id)

        except Exception as e:
            print("Error creating BuyNow record:", e)
            return render(request, "buy_now.html", {
                "product": product,
                "quantity": quantity,
                "size": size,
                "color": color,
                "total_price": total_price,
                "error": str(e)
            })

    return render(request, "buy_now.html", {
         "product": product,
        "quantity": quantity,
        "size": size,
        "color": color,
        "total_price": total_price
    })








        
        
       

def buy_now_success(request):
    return render(request,"buy_now_success.html")
    

def add_delivery_address(request, r_id):
    if 'user_id' not in request.session:
        return redirect('login_error')

    user_id = request.session['user_id']

    user = get_object_or_404(Viewers, id=user_id)

    try:
        buy_now_record = get_object_or_404(BuyNow, id=r_id)
    except Exception as e:
        return render(request, 'add_delivery_address.html', {'error': f"Order not found: {str(e)}"})

    if request.method == "POST":
        phone_number = request.POST.get('contact_num')
        address_line_1 = request.POST.get('address_line_1')
        address_line_2 = request.POST.get('address_line_2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country')

        if not phone_number or not address_line_1 or not city or not state:
            return render(request, 'add_delivery_address.html', {
                'buy_now_record': buy_now_record,
                'error': 'Please fill out all required fields.'
            })

        DeliveryAddress.objects.create(
            user=user,
            phone_number=phone_number,
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            city=city,
            state=state,
            orders=buy_now_record,
            postal_code=postal_code,
            country=country
        )
        return redirect('create_payment',order_id=buy_now_record.id)


    return render(request, 'add_delivery_address.html', {
        'buy_now_record': buy_now_record
    })
 

            

def view_delivery_address(request):
     delivery_addresses = DeliveryAddress.objects.filter(user=request.user)

     context = {
        'delivery_addresses': delivery_addresses
     }

     return render(request, 'view_delivery_address.html', context)

def delete_delivery_address(request, pk):
    address = get_object_or_404(DeliveryAddress, pk=pk)
    if address.user == request.user:
        address.delete()
    return redirect('view_delivery_addresses')


def add_review(request,v_id):
    print("+++++++++++++++++++++++++++++++++++++++++++++++++")
    if 'user_id' not in request.session:
        return redirect('login_error')
    if request.method == 'POST':
        print("---------------------------------------------------")
        text = request.POST.get('comment_text')
        if text:
            item = get_object_or_404(Item,id=v_id)
            user_id = request.session['user_id']
            data =Viewers.objects.get(id=user_id)

            review.objects.create(
                item = item,
                user=data,
                text=text
                )
        return redirect('product_home',m_id=v_id)
    return redirect('product_home',m_id=v_id)




def create_payment(request, order_id):
    if 'user_id' not in request.session:
        return redirect('user_login')  

    user = get_object_or_404(Viewers, id=request.session['user_id'])
    buy_now_record = get_object_or_404(BuyNow, id=order_id)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')

        if not payment_method:
            messages.error(request, "Please select a payment method.")
            return render(request, 'payment_page.html', {'product': buy_now_record.product, 'buy_now_record': buy_now_record})

        try:
            # Create a payment record
            payment = Payment.objects.create(
                user=user,
                orders=buy_now_record,
                payment_method=payment_method,
                payment_status='COMPLETED'  # Set Payment Status Here!

            )

            # Update the BuyNow record's payment_status
            buy_now_record.payment_status = 'Completed'
            buy_now_record.save(update_fields=['payment_status'])  # Save only this field

            # Redirect to payment success page
            messages.success(request, "Payment successfully processed!")
            return redirect('payment_success', payment_id=payment.id)

        except Exception as e:
            messages.error(request, f"Payment failed: {e}")
            return render(request, 'payment_page.html', {'product': buy_now_record.product, 'buy_now_record': buy_now_record})

    return render(request, 'payment_page.html', {'product': buy_now_record.product, 'buy_now_record': buy_now_record})

def payment_success(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)

    # Ensure BuyNow record is actually marked as completed before showing success page
    if payment.orders.payment_status != 'Completed':
        messages.error(request, "Payment has not been processed successfully.")
        return redirect('create_payment', order_id=payment.orders.id)

    return render(request, 'payment_success.html', {'payment': payment})


def view_profile(request):
    if 'user_id' not in request.session:
        return redirect('login_error')
    
    user_id = request.session['user_id']
    user_name = request.session.get('user_name')
    viewer = get_object_or_404(Viewers, id=user_id)

    # Fetch user's cart and orders (optional)
    cart_items = Cart.objects.filter(user=viewer)
    orders = BuyNow.objects.filter(user=viewer)
    reviews = review.objects.filter(user=viewer)

    context = {
        'viewer': viewer,
        'user_name': user_name,
        'cart_items': cart_items,
        'orders': orders,
        'reviews': reviews,
    }

    return render(request, "view_profile.html", context)


def search_products(request):
    query = request.POST.get('query', '')  # Get search query from POST request
    results = Item.objects.filter(item_name__icontains=query)  # Filter items by name

    return render(request, 'search_results.html', {'results': results, 'query': query})















    
     
























    
           








        
       
        




