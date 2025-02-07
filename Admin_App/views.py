from django.shortcuts import render,redirect
from Admin_App.models import *
from User_App.models import *
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError


# Create your views here.
def admin_home(request):
    return render(request,"Admin_home.html")

def add_product(request):
    category = Category.objects.all()
    context = {
        'category':category
    }
    if request.method=="POST":

        item_name =request.POST['item_name']
        item_category  =request.POST['category']
        item_picture  =request.FILES['item_picture']
        item_price = request.POST['item_price']
        product_description  =request.POST['description']
        
        
        Item.objects.create(

            item_name = item_name,
            item_category  = Category.objects.get(id=item_category),
            item_picture  = item_picture,
            item_price  = item_price,
            product_description = product_description
           


        )

    return render(request,"add_product.html", context)

def manage_product(request):
    c = Item.objects.all()
    context={
        'c':c

    }
    return render(request,"manage_product.html",context)

def view_category(request):
    f=Category.objects.all()
    context={
        'f':f

    }
    return render(request,"view_category.html",context)

def category_add(request):
    if request.method=="POST":
        name =request.POST['name']
        image = request.FILES['image']
        Category.objects.create(
            name=name,
            image=image
        )
    return render(request,"category_add.html")

def manage_category(request):
    m=Category.objects.all()
    context={
        'm': m

    }

    return render(request,"manage_category.html",context)

def category_view(request):
    g=Category.objects.all()
    context={
        'g':g

    }

    return render(request,"category_view.html",context)

def category_delete(request,gd_id):
    Category.objects.filter(id=gd_id).delete() 
    return redirect("manage_category")


def category_update(request,u_id):
    u= Category.objects.filter(id=u_id)
    context = {
        'u':u
    }
    return render(request,"category_update.html",context)

def product_update(request,t_id):
    t= Item.objects.filter(id=t_id)
    n = Category.objects.all()
    context = {
        't':t,
        'n' :n
        
    }
    return render(request,"product_update.html",context)



def update_product(request,l_id):
    n= Category.objects.all()
    context = {
        'e':e
    }
    if request.method=="POST":

        item_name =request.POST['item_name']
        item_category=request.POST['item_category']
        item_price=request.POST['item_price']
        product_description=request.POST['item_product_description']
        try:
            item_picture=request.FILES['item_picture']
            fs=FileSystemStorage()
            file=fs.save(item_picture.name,item_picture)
        except MultiValueDictKeyError:
            file=Item.objects.get(id=l_id).item_picture
        Item.objects.filter(id=l_id).update(
            item_name = item_name,
            item_category  = Category.objects.get(id=item_category),
            item_picture  = item_picture,
            item_price  = item_price,
            product_description = product_description
           

        )
        return redirect("view_product")
    return render(request,"product_update.html",context)

def view_product(request,):
    a= Item.objects.all()                       
    context = {
        'a':a
    }
   

    return render(request,"view_product.html",context)

def product_delete(request,p_id):

    Item.objects.filter(id=p_id).delete()
    return redirect("manage_product")


        

def update_category(request,p_id):
    if request.method=="POST":
        name=request.POST['name']
        try:
            image=request.FILES['image']
            fs=FileSystemStorage()
            file=fs.save(image.name,image)
        except MultiValueDictKeyError:
            file=Category.objects.get(id=p_id).image
        Category.objects.filter(id=p_id).update(
            name=name,
            image=file
        )

        return redirect("category_view")
    return render(request,"category_update.html")


def view_user(request):
    k=Viewers.objects.all()
    context={
        'k':k
    }

    return render(request,"view_user.html",context)


def view_review(request):
    l=review.objects.all()
    context={
        'l':l
    }
    return render(request,"view_review.html",context)



def view_orders(request):
    orders = BuyNow.objects.all().select_related('user', 'product')  # Fetch orders
    payments = Payment.objects.all().select_related('user', 'orders')  # Fetch payments

    return render(request, 'view_order.html', {'orders': orders, 'payments': payments})


    


 
 