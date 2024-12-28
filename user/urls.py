from django.urls import path
from django.contrib import admin

from user.forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:val>', views.CategoryView.as_view(), name='category'),
    path('category-name/<val>', views.CategoryName.as_view(), name='category-name'),
    path('product-detail/<int:pk>', views.ProductDetail.as_view(), name='product-detail'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('Address/', views.Address, name='Address'),
    path('updateAddress/<int:pk>', views.updateAddress.as_view(), name='updateAddress'),
    
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('checkout/', views.checkout.as_view(), name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('orders/', views.orders, name='orders'),
    path('about_us/', views.about_us, name='about_us'),
    
    path('search/', views.search, name='search'),
    
    path('wishlist/', views.show_wishlist, name='showwishlist'),
    path('pluswishlist/', views.plus_wishlist, name='pluswishlist'),
    path('minuswishlist/', views.minus_wishlist, name='minuswishlist'),
    
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/', views.remove_cart, name='removecart'),
    
    path('registration/', views.CustomerRegistrationView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('passwordchange/', auth_views.PasswordChangeView.as_view(template_name='changepassword.html', form_class=MyPasswordChangeForm, success_url='/passwordchangedone'), name='passwordchange'),
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'), name='passwordchangedone'),
    
    path('view-profile/', views.view_profile, name='view_profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('product/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
    path('contact_us/', views.contact_us, name='contact_us'),
    path('remove-from-wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove-from-wishlist'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('', RedirectView.as_view(url='/'), name='redirect_home'),
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "ClickShop"
admin.site.site_title = "ClickShop"
admin.site.site_index_title = "Welcome To ClickShop"