from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField(max_length = 150, null=True)
	email = models.EmailField(null=True)

	def __str__(self):
		return self.user.username


class Category(models.Model):
	name = models.CharField(max_length = 150, null=True)
	
	def __str__(self):
		return self.name

class Product(models.Model):
	name = models.CharField(max_length = 150, null=True)
	price = models.DecimalField(max_digits = 7, decimal_places=2)
	digital = models.BooleanField(default = False, null = True, blank=True)
	category = models.ManyToManyField(Category)
	image = models.ImageField(null=True, blank=True)


	def __str__(self):
		return self.name

class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete = models.CASCADE, null = True)
	date_ordered = models.DateTimeField(auto_now_add = True)
	complete = models.BooleanField(default = False, null = True, blank=False)
	transaction_id = models.CharField(max_length = 150, null=True)

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total

	def __str__(self):
		if self.customer:
			return f"Order {self.id}: {self.customer.name}"
		return "No orders"

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete = models.SET_NULL, null = True, blank=True)
	order = models.ForeignKey(Order, on_delete = models.CASCADE, null = True, blank=True)
	date_added = models.DateTimeField(auto_now_add = True)
	quantity = models.IntegerField(default=0, blank=True, null=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total

	def __str__(self):
		if self.order and self.order.customer:
			return f"{self.order.customer.name}: {self.product}"
		return "No order items"

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete = models.CASCADE, null = True)
	order = models.ForeignKey(Order, on_delete = models.CASCADE, null = True)
	address = models.CharField(max_length = 150, null=False)
	city = models.CharField(max_length = 150, null=False)
	country = models.CharField(max_length = 150, null=False)
	zipcode = models.CharField(max_length = 150, null=False)
	date_added = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.address

