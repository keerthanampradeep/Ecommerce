from django.urls import path
from User_App import views
from django.conf.urls.static import static

urlpatterns = [
    path('user_home',views.user_home,name ="user_home"),
    path('register',views.register,name ="register"),
    path('signup_error',views.signup_error,name="signup_error"),
    path('user_login',views.user_login,name="user_login"),
    path('login_error',views.login_error,name="login_error"),
    path('product_home/<int:m_id>',views.product_home,name="product_home"),
    path('product',views.product,name="product"),
    path('user_logout',views.user_logout,name="user_logout"),
    path('add_to_cart/<int:pk>', views.add_to_cart, name="add_to_cart"),
    path('view_cart', views.view_cart, name="view_cart"),
    path('remove_from_cart/<int:pk>', views.remove_from_cart, name="remove_from_cart"),
    path('buy-now/<int:item_id>' ,views.buy_now,name="buy_now"),
    path('buy-now-success' ,views.buy_now_success,name='buy_now_success'),
    path('add_delivery_address/<int:r_id>', views.add_delivery_address, name="add_delivery_address"),
    path('add_review/<int:v_id>',views.add_review,name="add_review"),
    path('create_payment/<int:order_id>/', views.create_payment, name='create_payment'),
    path('payment_success/<int:payment_id>/', views.payment_success, name='payment_success'),
    path('view_profile',views.view_profile,name="view_profile"),
    path('search',views.search_products, name='search_products'),














   

]

    
     
    