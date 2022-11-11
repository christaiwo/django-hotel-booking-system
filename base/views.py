from distutils import log
import email
import imp
import re
import os
from webbrowser import get
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
# from .models import 
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from datetime import date
import uuid
from django.db.models import Sum
from django.conf import settings
from django.core.mail import send_mail
from django.core import mail
from django.template.loader import render_to_string
from django.template import RequestContext
from rest_framework.response import Response
from django.utils.html import strip_tags
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
# from .forms import 
from PIL import Image
from pathlib import Path
import requests
import json
import socket
import platform
from django.utils import timezone



# general variable is declear here
BASE_DIR = Path(__file__).resolve().parent.parent
date = datetime.datetime.today()
cur_date = datetime.datetime.now()
current_now = timezone.now()
client_ip_address = socket.gethostbyname(socket.gethostname())
device_name = socket.gethostname()
sms_notify = 1
email_notify = 1

paystack_sk = 'Bearer '
paystack_pk = ''

general_list = {
    'site_dev':"Ethion-Tech",
    'dev_link':'https://ethiontech.com',
    'dev_whatsapp':'wa.me/2348145264707',
    'site_name':"Kotel",
    'site_url':"",
    'site_domain':"",
    'currency_symbol':"&#8358;",
    'site_address':"No 1",
    # 'date':date,
    'facebook_link': "",
    'twitter_link':"",
    'instagram_link': "",
    'phone_no':'2348145264707',
    'email':'christaiwo@ethiontech.com',
    'client_ip_address':client_ip_address,
    'device_name':device_name,
    'paystack_sk':paystack_sk,
    'paystack_pk':paystack_pk,

}


# Create your views here.
# test page views
def test(request):
    context = {
        'general_list':general_list,
        'page_name':'Home',
        'page_desc':'Hotel Booking system',
    }

    return render(request, 'test.html', context)



# home views
def home(request):
    categories = category.objects.all()
    context = {
        'general_list':general_list,
        'page_name':'Home',
        'page_desc':'Hotel Booking system',
        'categories':categories,
    }

    return render(request, 'index.html', context)

# about us page
def about(request):
    context = {
        'general_list':general_list,
        'page_name':'Home',
        'page_desc':'About Us',

    }

    return render(request, 'about.html', context)


# contact us page
def contact_us(request):

    # get post input
    if request.method == "POST":
        if request.POST.get('submit') == "contact":
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone_no = request.POST.get('phone_no')
            message = request.POST.get('message') 

            # insert into contact us field 
            contact_insert = contact(name=name, email=email, phone_no=phone_no, message=message, date=cur_date)
            contact_insert.save()
            
            messages.success(request, 'we will get back to you soon')
            return redirect('contact')
    
    context = {
        'general_list':general_list,
        'page_name':'Home',
        'page_desc':'Contact Us',

    }

    return render(request, 'contact.html', context)


# def search page 
def rooms(request):
    if 'category' in request.GET:
        category_get = request.GET['category']
        category_query = category.objects.get(name=category_get)
        rooms = hotel.objects.filter(category_id=category_query.id)
    else:
        rooms = hotel.objects.all()
    context = {
        'general_list':general_list,
        'page_name':'Home',
        'page_desc':'Hotel Booking system',
        'rooms':rooms,

    }
    return render(request, 'rooms.html', context)


# def room page 
def room_view(request, pk):
    if hotel.objects.filter(hotel_id=pk).count():
        rooms = hotel.objects.get(hotel_id=pk)
    else:
        return redirect('rooms')

    context = {
        'general_list':general_list,
        'page_name':'Home',
        'page_desc':'Hotel Booking system',
        'rooms':rooms,

    }


    
    # get the cheout form
    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        room = request.POST.get('room')
        guest = request.POST.get('guest')
        days = request.POST.get('days')
        amount = request.POST.get('amount')

        if check_in != '' and check_out != '' and room != '' and guest != '' :
            booking_id = uuid.uuid4().hex[:10].upper()
            booking_insert = booking(booking_id=booking_id, hotel_id=rooms.id, user_id=user.id, check_in=check_in, check_out=check_out, guest=guest, amount=amount, room=room, date=cur_date)
            booking_insert.save()  

            return redirect(checkout, pk=booking_id) 
        else:
            return redirect(room_view, pk=pk)
    return render(request, 'room-details.html', context)


# def checkout page 
def checkout(request, pk):

    if booking.objects.filter(booking_id=pk).count():
        booking_get = booking.objects.get(booking_id=pk)
    else:
        return redirect('rooms')

    context = {
        'general_list':general_list,
        'page_name':'Home',
        'page_desc':'Hotel Booking system',
        'booking_get':booking_get,

    }
    return render(request, 'checkout.html', context)

def checkout_confirm (request, pk):
    # return redirect('account');
    url = "https://api.paystack.co/transaction/verify/"+pk
    headers = {
        'Authorization': paystack_sk,
        'Cache-Control': 'no-cache',
    }

    # get the result and convert it to a json file
    result=requests.get(url,headers=headers)
    result = result.json()
    main_status = result['status']

    if main_status == True:
        booking_id = result['data']['reference']
        status = result['data']['status']

        if status == 'success' and booking.objects.filter(booking_id=booking_id).exists():
            get_booking = booking.objects.get(booking_id=booking_id)

            if get_booking.status == 1:
                return redirect(checkout_confirmed, pk=pk)
            else:
                booking.objects.filter(booking_id=booking_id).update(status=1)
                hotel.objects.filter(hotel_id=get_booking.hotel.hotel_id).update(status=0)
            return redirect(checkout_confirmed, pk=pk)
        else:
            return redirect('home')




    context = {
        'general_list':general_list,
        'page_name':'Home',
        'page_desc':'Hotel Booking system',
        'result':result,

    }

    return render(request, 'test.html', context)


def checkout_confirmed(request, pk):
    # return redirect('account');
    if  booking.objects.filter(booking_id=pk).exists():
        get_booking = booking.objects.get(booking_id=pk)
    else:
        return redirect('rooms')

    context = {
        'general_list':general_list,
        'page_name':'Home',
        'page_desc':'Hotel Booking system',
        'get_booking':get_booking,

    }

    return render(request, 'checkout-confirmed.html', context)


# for user registeration
def account_register(request):
    context = {
        'general_list':general_list,
        'page_name':'Home',
        'page_desc':'Register',

    }
    if request.user.is_authenticated:
        return redirect('account')
    # check for the form request
    elif request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username').lower()
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_no = request.POST.get('phone_no')
        password = request.POST.get('password')
        address = request.POST.get('address')

        # check if user already exist
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exist')
            return redirect('account_register')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exist')
            return redirect('account_register')
        else:
            # create user 
            user = User.objects.create_user(username, email, password)
            user.last_name = last_name
            user.first_name = first_name
            user.profile.phone_no = phone_no 
            user.profile.address = address 
            user.save()

            # authenticate user and log them in
            login(request, user)

            return redirect('account')

    return render(request, 'account/register.html', context)

# for user login
def account_login(request):
    context = {
        'general_list':general_list,
        'page_name':'Home',
        'page_desc':'Hotel Booking system',

    }

    if request.user.is_authenticated:
        return redirect('account')
    # get the login form 
    elif request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)

            if 'next' in request.GET:
                next_url = request.GET['next']
                return redirect('..'+next_url)
            else:
                return redirect('account')
        else:
            messages.error(request, 'Username OR password is incorrect')
            return redirect('account_login')

            return redirect('account')
    return render(request, 'account/login.html', context)

# for user log out
def account_logout(request):
    logout(request)
    return redirect('account_login')

# for user account
@login_required(login_url=account_login)
def account(request):
    user = User.objects.get(username=request.user)
    # get the cancel id from the url
    if 'cancel' in request.GET:
        booking_id = request.GET['cancel']
        if  booking.objects.filter(booking_id=booking_id).exists():
             booking.objects.filter(booking_id=booking_id).delete()
             return redirect('account')
        else:
            return redirect('account')
    elif request.method == 'POST':
        if request.POST.get('submit') == 'cancel':
            reason = request.POST.get('reason')
            booking_id = request.POST.get('booking_id')

            if canceled_booking.objects.filter(booking_id=booking_id).exists():
                return redirect('account')
            else:
                cancel_insert = canceled_booking(reason=reason, date=cur_date, booking_id=booking_id, user_id=user.id)
                cancel_insert.save()
                return redirect('account_cancellation')
    # content to display 
    context = {
        'general_list':general_list,
        'page_name':'Account',
        'page_desc':'User account',
        'user':user,
    }
    return render(request, 'account/index.html', context)


# for user account cancellatipn
@login_required(login_url=account_login)
def account_cancellation(request):
  # content to display 
    user = User.objects.get(username=request.user)
    context = {
        'general_list':general_list,
        'page_name':'Account',
        'page_desc':'User cancellation',
        'user':user,
    }
    return render(request, 'account/cancellation.html', context)


# for user profile
@login_required(login_url=account_login)
def account_profile(request):
  # content to display 
    user = User.objects.get(username=request.user)

    # get the form post 
    if request.method == 'POST':
        if request.POST.get('submit') == 'update':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone_no = request.POST.get('phone_no')
            address = request.POST.get('address')

            User.objects.filter(username=user.username).update(first_name=first_name, last_name=last_name)
            Profile.objects.filter(user_id=user.id).update(phone_no=phone_no, address=address)

            # user_update.update()
            return redirect('account_profile')


    context = {
        'general_list':general_list,
        'page_name':'Account',
        'page_desc':'User Profile',
        'user':user,
    }
    return render(request, 'account/profile.html', context)


# for change password
@login_required(login_url=account_login)
def account_password(request):
  # content to display 
    user = User.objects.get(username=request.user)

    # get the form post 
    if request.method == 'POST':
        if request.POST.get('submit') == 'update':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone_no = request.POST.get('phone_no')
            address = request.POST.get('address')

            User.objects.filter(username=user.username).update(first_name=first_name, last_name=last_name)
            Profile.objects.filter(user_id=user.id).update(phone_no=phone_no, address=address)

            # user_update.update()
            return redirect('account_profile')
        elif request.POST.get('submit') == "change_password":
            password = request.POST.get('password')
            new_password = request.POST.get('new_password')
            user_auth = authenticate(username=user.username, password=password)
            if user_auth is not None:
                user.set_password(new_password)
                user.save()
                login(request, user)
                messages.success(request, 'UPDATED')
                return redirect('account_password')
            else:
                messages.error(request, 'Password incorect')
                return redirect('account_password')

            return redirect('setting')


    context = {
        'general_list':general_list,
        'page_name':'Account',
        'page_desc':'User Change Password',
        'user':user,
    }
    return render(request, 'account/password.html', context)

# for ticket creation
@login_required(login_url=account_login)
def account_create_ticket(request):
    user = User.objects.get(username=request.user)
    # get the form input
    if request.method == "POST":
        if request.POST.get('submit') == "create":
            issue = request.POST.get('issue') 
            priority = request.POST.get('priority') 
            message = request.POST.get('message')
            ticket_id = uuid.uuid4().hex[:10].upper()
            ticket_create = ticket(user_id=user.id, ticket_id=ticket_id, issue=issue, priority=priority, message=message, date=cur_date)
            ticket_create.save()
            return redirect('account_ticket')


  # content to display 
    context = {
        'general_list':general_list,
        'page_name':'Account',
        'page_desc':'User Create Ticket',
        'user':user,
    }
    return render(request, 'account/create-ticket.html', context)


# for ticket creation
@login_required(login_url=account_login)
def account_ticket(request):
    user = User.objects.get(username=request.user)
  # content to display 
    context = {
        'general_list':general_list,
        'page_name':'Account',
        'page_desc':'User Tickets',
        'user':user,
    }
    return render(request, 'account/ticket.html', context)


# for ticket creation
@login_required(login_url=account_login)
def account_view_ticket(request,pk):
    user = User.objects.get(username=request.user)
    # redirect if no ticket found
    if ticket.objects.filter(ticket_id=pk).exists():
        get_ticket = ticket.objects.get(ticket_id=pk)
    else:
        return redirect('account_ticket')

    # get the form from the user input 
    if request.method == "POST":
        if request.POST.get('reply') == "reply":
            message = request.POST.get('message')
            ticket_reply_insert = ticket_reply(ticket_id=get_ticket.id, message=message, date=cur_date)
            ticket_reply_insert.save()
            # rediect back to the same page
            return redirect('account_view_ticket', pk=pk)
    # content to display 
    context = {
        'general_list':general_list,
        'page_name':'Account',
        'page_desc':'User Tickets',
        'user':user,
        'get_ticket':get_ticket,
    }
    return render(request, 'account/view-ticket.html', context)
