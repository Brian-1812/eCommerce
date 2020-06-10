from django.shortcuts import render, redirect, reverse
from .models import *
import json
import datetime
from django.http import JsonResponse


def dashboard(request):
	if not request.user.is_authenticated:
		return redirect(reverse('authenticate:login'))
	customer = request.user.customer
	if customer.order_set.filter(complete=False):
		order_num = customer.order_set.filter(complete=False).first().get_cart_items
	else:
		order_num = 0
	querysets = []
	orders = Order.objects.filter(customer=customer, complete=True).all()
	for queryset in orders:
		querysets.append(queryset.orderitem_set.all())
	products = []
	for order in querysets:
		products.extend([item.product for item in order])
	if products == []:
		context = {'message':"You don't have completed and shipped orders yet.", 'order_num':order_num}
	else:
		context = {'products':products, 'order_num':order_num}
	return render(request, 'dashboard\\dashboard.html', context = context)


def store(request, category):
	if not request.user.is_authenticated:
		return redirect(reverse('authenticate:login'))
	customer = request.user.customer
	if customer.order_set.filter(complete=False):
		order_num = customer.order_set.filter(complete=False).first().get_cart_items
	else:
		order_num = 0
	if category == 'all':
		products = Product.objects.all()
		context = {'products':products, 'order_num':order_num}
		return render(request, 'dashboard\\store.html', context=context)
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
	context = {'products':products, 'order_num':order_num}
	return render(request, 'dashboard\\store.html', context=context)


def product_view(request, id):
	if not request.user.is_authenticated:
		return redirect(reverse('authenticate:login'))
	customer = request.user.customer
	if customer.order_set.filter(complete=False):
		order_num = customer.order_set.filter(complete=False).first().get_cart_items
	else:
		order_num = 0
	product = Product.objects.filter(id=int(id)).first()
	context = {
	'product':product,
	'order_num':order_num
	}
	return render(request, 'dashboard\\product_view.html', context=context)


def checkout(request, id):
	if not request.user.is_authenticated:
		return redirect(reverse('authenticate:login'))
	customer = request.user.customer
	if customer.order_set.filter(complete=False):
		order_num = customer.order_set.filter(complete=False).first().get_cart_items
	else:
		order_num = 0
	order = Order.objects.filter(id=id).first()
	total_cost = order.get_cart_total
	items = order.orderitem_set.all()
	context = {
		'total_cost':total_cost,
		'items': items,
		'order_num':order_num
		}
	return render(request, 'dashboard\\checkout.html', context=context)


def cart(request):
	if not request.user.is_authenticated:
		return redirect(reverse('authenticate:login'))
	customer = request.user.customer
	if customer.order_set.filter(complete=False):
		order_num = customer.order_set.filter(complete=False).first().get_cart_items
	else:
		order_num = 0
	customer = request.user.customer
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	items = order.orderitem_set.all()
	context = {'items':items, 'order':order, 'order_num':order_num}
	return render(request, 'dashboard\\cart.html', context)



def updateItem(request):
	if not request.user.is_authenticated:
		return redirect(reverse('authenticate:login'))
	if request.is_ajax() and request.method=='POST':
		product_id = request.POST['productId']
		action = request.POST['action']
		customer = request.user.customer
		product = Product.objects.filter(id=product_id).first()
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
		response = {'message':f"{product.name} is added to your cart!"}
		if action == 'add':
			orderItem.quantity = 1
		elif action == 'remove':
			orderItem.quantity -= 1
		elif action == 'increment':
			orderItem.quantity += 1
		else:
			response = {'message':"Invalid action"}
		orderItem.save()
		if orderItem.quantity <= 0:
			orderItem.delete()
		return JsonResponse(response, safe=False, status=200)
	else:
		return JsonResponse({'message':'Some error occured'}, safe=False, status=404)

def processOrder(request):
	if not request.user.is_authenticated:
		return redirect(reverse('authenticate:login'))
	data = json.loads(request.body)
	shipping = data['form']['shipping']
	transaction_id = datetime.datetime.now().timestamp()
	customer = request.user.customer
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	total = float(data['form']['total'])
	order.transaction_id = transaction_id
	if float(total) == float(order.get_cart_total):
		order.complete = True
	order.save()
	if shipping==True:
		ShippingAddress.objects.create(
				customer=customer,
				order=order,
				address = data['shipping']['street'],
				city = data['shipping']['city'],
				zipcode = data['shipping']['zipcode'],
				country = data['shipping']['country'],
				)
	return JsonResponse('Payment complete!', safe=False)