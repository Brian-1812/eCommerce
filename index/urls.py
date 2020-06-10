from django.urls import path
from . import views

app_name = 'index'
urlpatterns = [
	path('', views.index, name = 'index'),
	path("store/<str:category>/", views.store, name = 'store'),
	path("product_view/<int:id>/", views.product_view, name = 'product_view'),
]