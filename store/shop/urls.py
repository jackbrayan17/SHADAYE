from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
#   
    path('products/', views.product_list, name='product_list'),
#    path('login/', auth_views.LoginView.as_view(), name='login'),  # ✅ Add this
#     path('logout/', auth_views.LogoutView.as_view(), name='logout'),
#     path('signup/', auth_views.SignupView.as_view(), name='signup'),
    
    path("login/", views.user_login, name="login"),
    path("signup/", views.user_signup, name="signup"),
    path("logout/", views.user_logout, name="logout"),
    
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
     path('update-cart-quantity/', views.update_cart_quantity, name='update_cart_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('submit-testimonial/', views.submit_testimonial, name='submit_testimonial'),
    
    # Admin routes
    path('admin/testimonials/', views.manage_testimonials, name='manage_testimonials'),
    path('admin/testimonials/approve/<int:testimonial_id>/', views.approve_testimonial, name='approve_testimonial'),
    path('admin/testimonials/delete/<int:testimonial_id>/', views.delete_testimonial, name='delete_testimonial'),
]
