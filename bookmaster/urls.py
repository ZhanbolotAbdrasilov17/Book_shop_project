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
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
    path("new_list/", views.new_list, name="new_list"),
    path("popular_list/", views.popular_list, name="popular_list")


]