from re import template
from django.conf import settings
from django.urls import path
from app import views
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm,MyPassWordChange,MyPasswordResetForm,MySetPasswordForm
urlpatterns = [
    path('', views.ProductView.as_view(),name='home'),
    path('product-detail/<int:pk>', views.ProductDeatil.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/',views.show_cart,name='showcart'),
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>', views.mobile, name='mobiledata'),
    path('bottom/', views.bottom, name='bottom'),
    path('bottom/<slug:data>', views.bottom, name='bottomwear'),
    path('top/', views.top, name='top'),
    path('top/<slug:data>', views.top, name='topwear'),

    path('laptop/', views.laptop, name='laptop'),
    path('laptop/<slug:data>', views.laptop, name='laptopdata'),
    

    path('accounts/login/', auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm),name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name="logout"),
    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=MyPassWordChange,success_url='/passwordchangedone/'),name="passwordchange"),
    path('passwordchangedone/',auth_views.PasswordChangeDoneView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name="app/passwordreset.html",form_class=MyPasswordResetForm),name='password_reset'),
    
    
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name="app/passwordresetdone.html"),name='password_reset_done'),
    
    
    
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="app/passwordresetconform.html",form_class=MySetPasswordForm),name='password_reset_confirm'),
    
    
    
    
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name="app/passwordresetcompleted.html"),name='password_reset_complete'),


    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone',views.payment_done,name='payment'),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
