from django.forms import model_to_dict
from django.shortcuts import render, redirect
from rest_framework import generics
from django.http import JsonResponse
from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import NewUserForm, CommentForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
import json
import datetime




from .models import *

# Create your views here.
from .serializers import ProductSerializer


def store(request):

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)


class BookListView(ListView):
    model = Product
    template_name = 'store/store.html'
    context_object_name = 'filter_books'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            customer = self.request.user
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            # items = order.orderritem_set.all()
            cartItems = order.get_cart_items
        else:
            order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
            cartItems = order['get_cart_items']
        context['cartItems'] = cartItems
        return context

    def get_queryset(self):
        genre_id = self.kwargs.get('pk')
        print(f'***********************{genre_id}**************')
        if genre_id:
            queryset = self.model.objects.filter(
                genre_id=genre_id)
            return queryset
        queryset = self.model.objects.all()
        return queryset

def cart(request):

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        cartItems = order['get_cart_items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)



def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping':False}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    elif action == 'delete':
        orderItem.quantity = (orderItem.quantity * 0)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float['form']['total']
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()
        print(order.shipping)

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )

        return JsonResponse('Payment submitted..', safe=False)


class ViewDetailView(DetailView):
    model = Product
    template_name = 'store/views.html'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ViewDetailView, self).get_context_data(**kwargs)
        comments = Comment.objects.filter(post=self.get_object())
        context['comments'] = comments
        context['form'] = CommentForm

        # if request.method == "POST":
        #     form = CommentForm(request.POST or None)
        #     if form.is_valid():
        #
        #         form = form.save(commit=False)
        #         if request.POST.get("news_parent", None):
        #             form.news_parent_id = int(request.POST.get("news_parent"))
        #             if request.POST.get("parent", None):
        #                 form.parent_id = int(request.POST.get("parent"))
        #         form.news_parent_id = pk
        #         form.user = request.user
        #         form.save()
                # return HttpResponseRedirect(request.path)

        # if self.request.user.is_authenticated:
        #     # customer = self.request.user.customer
        #     # order, created = Order.objects.get_or_create(customer=customer, complete=False)
        #     # cartItems = order.get_cart_items
        # # else:
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']
        context['cartItems'] = cartItems
        return context

# class New_list(DetailView):
#     model = Product
#     template_name = 'store/new_list.html'
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(New_list, self).get_context_data(**kwargs)
#         # if self.request.user.is_authenticated:
#         #     customer = self.request.user.customer
#         #     order, created = Order.objects.get_or_create(customer=customer, complete=False)
#         #     cartItems = order.get_cart_items
#         # else:
#         order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
#         cartItems = order['get_cart_items']
#         context['cartItems'] = cartItems
#         return context
#
#     def new_list(request):
#         books = Product.objects.order_by('-published_date')[:5]
#         return render(request, 'store/new_list.html', {'books': books})





class SearchResultsView(ListView):
    model = Product
    template_name = 'store/store.html'
    context_object_name = 'products'

    def get_queryset(self):

        query = self.request.GET.get('q')
        print(query)
        object_list = Product.objects.filter(name__icontains=query)
        print(len(object_list))
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        # if self.request.user.is_authenticated:
        #     # customer = self.request.user.customer
        #     # order, created = Order.objects.get_or_create(customer=customer, complete=False)
        #     # cartItems = order.get_cart_items
        # # else:
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']
        context['cartItems'] = cartItems
        return context


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("store")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="store/register.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("store")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="store/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("store")

def new_list(request):
    books = Product.objects.order_by('-published_date')[:5]
    return render(request, 'store/new_list.html', {'books': books})

def popular_list(request):
    book = Product.objects.order_by('-popular_list')[:5]
    return render(request, 'store/popular_list.html', {'books': book})

class ProductAPIView(APIView):
    def get(self, request):
        lst = Product.objects.all().values()
        return Response({'names': list(lst)})

    def post(self, request):
        post_new = Product.objects.create(
            name=request.data['name'],
            description=request.data['description'],
            genre=request.data['genre']
        )
        return Response({'post': model_to_dict(post_new)})


# class ProductAPIView(generics.ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer








