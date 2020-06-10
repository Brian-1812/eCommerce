from django.urls import path
from . import views

app_name = 'dashboard'
urlpatterns = [
	path('dashboard', views.dashboard, name = 'dashboard'),
	path("store/<str:category>/", views.store, name = 'store'),
	path("product_view/<int:id>/", views.product_view, name = 'product_view'),
	path('checkout/<int:id>/', views.checkout, name = 'checkout'),
	path('update_item', views.updateItem, name = 'updateItem'),
	path('cart', views.cart, name = 'cart'),
	path("process_order", views.processOrder, name = 'processOrder'),
]