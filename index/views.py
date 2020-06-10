from django.shortcuts import render, redirect, reverse
from dashboard.models import Product, Category
from django.http import JsonResponse

# Create your views here.
def index(request):
	if request.user.is_authenticated:
		return redirect(reverse('dashboard:store', args=['all']))
	products = Product.objects.all().order_by("-id")
	context = {'products':products}
	return render(request, 'index\\index.html', context=context)

def store(request, category):
	if request.user.is_authenticated:
		return redirect(reverse('dashboard:store', args=[category]))
	if category == 'all':
		products = Product.objects.all()
		context = {'products':products}
		return render(request, 'index\\store.html', context=context)
	if category=='Sports':
		category='Sports and Outdoors'
	elif category=='Home_kitchen':
		category='Home and Kitchen'
	elif category=='Tools':
		category='Tools and Home improvement'
	else:
		pass
	category = Category.objects.filter(name=category).first()
	products = Product.objects.filter(category=category.id)
	context = {'products':products}
	return render(request, 'index\\store.html', context=context)

def product_view(request, id):
	if request.user.is_authenticated:
		return redirect(reverse('dashboard:product_view', args=[id]))
	product = Product.objects.filter(id=int(id)).first()
	context = {
	'product':product
	}
	return render(request, 'index\\product_view.html', context=context)