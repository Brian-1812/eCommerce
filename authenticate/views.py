from django.shortcuts import render, reverse, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .forms import CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from dashboard.models import Customer
# Create your views here.

def register(request):
	if not request.user.is_authenticated:
		if request.method == 'POST':
			f = CreateUserForm(request.POST)
			if f.is_valid():
				f.save()
				username = request.POST["username"]
				user = User.objects.filter(username = username).first()
				Customer.objects.create(user=user, name=user.username, email=user.email)
				customer = user.customer
				messages.success(request, "Account created successfully")
				return redirect(reverse('authenticate:login'))
			else:
				f = CreateUserForm()
				messages.warning(request, "Password must contain at least 8 characters including numbers and special characters")
				return render(request, 'authenticate/register.html', {'form': f})

		else:
			f = CreateUserForm()
			return render(request, 'authenticate/register.html', {'form': f})
	else:
		return HttpResponseRedirect(reverse('dashboard:store', args=['all']))

def login_view(request):
	if not request.user.is_authenticated:
		if request.method == "POST":
			username = request.POST.get('username')
			password = request.POST.get('password')
			user = authenticate(request, username = username, password = password)

			if user is not None:
				login(request, user)
				return HttpResponseRedirect(reverse('dashboard:store', args=['all']))
			else:
				messages.warning(request, "Invalid credentials")
				return render(request, "authenticate\\login.html")
		else:
			return render(request, "authenticate\\login.html")
	else:
		return HttpResponseRedirect(reverse('dashboard:store', args=['all']))

def logout_view(request):
	logout(request)
	messages.success(request, "You have logged out successfully")
	return HttpResponseRedirect(reverse('index:store', args=['all']))