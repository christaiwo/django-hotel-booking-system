from os import name
from re import template
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('test', views.test, name="test"),
    path('', views.home, name="home"),
    path('about', views.about, name="about"),
    path('contact-us', views.contact_us, name="contact"),
    path('rooms', views.rooms, name="rooms"),
    path('rooms/<str:pk>', views.room_view, name="room_view"),
    path('checkout/<str:pk>', views.checkout, name="checkout"),
    path('checkout-confirm/<str:pk>', views.checkout_confirm, name="checkout_confirm"),
    path('checkout-confirmed/<str:pk>', views.checkout_confirmed, name="checkout_confirmed"),



    # for user area 
    path('account/register', views.account_register, name="account_register"),
    path('account/login', views.account_login, name="account_login"),
    path('account/logout', views.account_logout, name="account_logout"),
    path('account/', views.account, name="account"),
    path('account/cancellation', views.account_cancellation, name="account_cancellation"),
    path('account/profile', views.account_profile, name="account_profile"),
    path('account/change-password', views.account_password, name="account_password"),
    path('account/create-ticket', views.account_create_ticket, name="account_create_ticket"),
    path('account/ticket', views.account_ticket, name="account_ticket"),
    path('account/view-ticket/<str:pk>', views.account_view_ticket, name="account_view_ticket"),


]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)


# handler404 = "base.views.page_not_found_view"
# handler500 = "base.views.internal_server_error_found_view"