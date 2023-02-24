"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render,redirect
from django.http import HttpRequest
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .decorators import unauthenticated_user, allowed_users
from django.contrib.auth.decorators import login_required
from django import forms
from django.forms import ModelForm
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import *
from django.shortcuts import render
from django.http import JsonResponse
import import json
from .models import * 
from .utils import cookieCart, cartData, guestOrder



#ENGI

@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user')
        else:
            messages.info(request, 'Username OR password is incorrect')
    context = {}
    return render(request, 'app/login.html', context)
	



class CreateUserForm(UserCreationForm):
        class Meta:
            model = User
            fields = ['username', 'email', 'password1', 'password2']


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def user(request):
    context = {}
    return render( request,'app/user.html', context)



@unauthenticated_user
def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            
       
            messages.success(request, 'Account was created')
            return redirect('login')

    context = {'form':form}
    return render( request,'app/register.html', context)

@unauthenticated_user
#@allowed_users(allowed_roles=['admin'])
#@allowed_users(allowed_roles=['customer'])
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'app/account_settings.html', context)




class CustomerForm(ModelForm):
	    class Meta:
             model = Customer
             fields = '__all__'
             exclude = ['user']

             
widgets = {
			'bio': forms.Textarea(attrs={'class': 'form-control'}),
			'website_url': forms.TextInput(attrs={'class': 'form-control', }),
			'facebook_url': forms.TextInput(attrs={'class': 'form-control'}),
			'twitter_url': forms.TextInput(attrs={'class': 'form-control'}),
			'instagram_url': forms.TextInput(attrs={'class': 'form-control'}),			
			'pinterest_url': forms.TextInput(attrs={'class': 'form-control'}),			
		}


class CreateUserForm(UserCreationForm):
        class Meta:
            model = User
            fields = ['username', 'email', 'password1', 'password2']




   
class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "app/user.html" 
            




@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'core/password.html', {'form': form}) 




#SRORE

def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)