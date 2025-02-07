from django.urls import path
from Admin_App import views

urlpatterns = [
    path('home',views.admin_home,name ="admin_home"),
    path('add',views.add_product,name ="add_product"),
    path('manage',views.manage_product,name ="manage_product"),
    path('view',views.view_category,name ="view_category"),
    path('category_add',views.category_add,name ="category_add"),
    path('manage_category',views.manage_category,name ="manage_category"),
    path('product_delete/<int:p_id>',views.product_delete,name ="product_delete"),

    path('category_view',views.category_view,name ="category_view"),
    path('category_delete/<int:gd_id>',views.category_delete,name="category_delete"),
    path('category_update/<int:u_id>',views.category_update,name="category_update"),
    path('update_category/<int:p_id>',views.update_category,name="update_category"),
    path('update_product/<int:l_id>',views.update_product,name="update_product"),
    path('view_product',views.view_product,name="view_product"),
    path('product_update/<int:t_id>',views.product_update,name="product_update"),
    path('view_user',views.view_user,name="view_user"),
    path('view_review',views.view_review,name="view_review"),
    path('view_orders',views.view_orders,name="view_orders"),


]