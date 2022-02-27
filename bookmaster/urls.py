from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('books/', views.BookListView.as_view(), name='books'),
    path('genre/<int:pk>/', views.BookListView.as_view(), name='genre'),

    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('views/<int:pk>/', views.ViewDetailView.as_view(), name="view_item"),
]