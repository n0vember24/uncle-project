# from django.utils.decorators import method_decorator
# from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView

from main.models import Product, Category, User, Cart, Favourite


class IndexListView(ListView):
    queryset = Product.objects.order_by('-pub_date')
    template_name = 'index.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductsListView(IndexListView):
    template_name = 'products/list.html'


class ProductView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        reviews = product.review_set.order_by('-date')
        context = {'product': product, 'reviews': reviews}
        return render(request, 'products/view.html', context)

    def post(self, request, slug):
        user = request.user
        product = get_object_or_404(Product, slug=slug)
        text = request.POST['text']
        product.review_set.create(text=text, user=user)
        return redirect('main:view', slug)


class CategoryListView(ListView):
    model = Category
    template_name = 'categories/categories.html'
    context_object_name = 'categories'


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'categories/view.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        context['products'] = Product.objects.filter(category=kwargs['object']).order_by('-pub_date')
        return context


class LogInView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('main:index'))
        return render(request, 'registration/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        try:
            login(request, user)
            return redirect(reverse_lazy('main:index'))
        except AttributeError:
            error_msg = "Saytga kiratotganda nimadi xato ketdi. Iltimos, hammasini tekshirib boshidan urinib ko'ring." \
                        " Agar siz oldin saytda ro'yxatdan o'tmagan bo'lsangiz, iltimos, " \
                        "registratsiya tugmasini bosib, ro'yxatdan o'tib oling"
            data = (username, password)
            return render(request, 'registration/login.html', {'msg': ('danger', error_msg), 'data': data})


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse_lazy('main:index'))
        return render(request, 'registration/register.html')

    def post(self, request):
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        try:
            new_user = User.objects.create_user(
                username, email, password, first_name=first_name, last_name=last_name, phone_number=phone_number)
            new_user.set_password(password)
            user = authenticate(username=username, password=password)
            # IntegrityError - already exists
            login(request, user)
            return redirect(reverse_lazy('main:index'))
        except IntegrityError:
            error_msg = "Bunday usernameli foydalanuvchi allaqachon mavjud. Iltimos, boshqa username tanlang."
            data = (first_name, last_name, username, email, phone_number, password)
            return render(request, 'registration/register.html', {'msg': ('danger', error_msg), 'data': data})


class LogOutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse_lazy('main:index'))


class CartView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'products/cart.html', {'cart': Cart.objects.all()})
        return redirect(reverse_lazy('main:login'))

    def post(self, request):
        product_id = request.POST['product_id']
        product = Cart.objects.filter(product_id=product_id)
        if product.exists():
            product.first().delete()
        else:
            product_count = request.POST['product_count']
            Cart.objects.create(product_id=product_id, user=request.user, count=product_count)
        return redirect(reverse_lazy('main:cart'))


class FavView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'products/fav.html', {'favourites': Favourite.objects.all()})
        return redirect(reverse_lazy('main:login'))

    def post(self, request):
        product_id = request.POST['product_id']
        product = Favourite.objects.filter(product_id=product_id)
        if product.exists():
            product.first().delete()
        else:
            Favourite.objects.create(product_id=product_id, user=request.user)
        return redirect(reverse_lazy('main:favourites'))
