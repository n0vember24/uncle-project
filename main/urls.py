from django.urls import path

from main.views import (
    IndexListView, ProductView, ProductsListView, CategoryListView, CategoryDetailView, LogInView, LogOutView,
    RegisterView, CartView, FavView
)


def index(request): pass


app_name = 'main'
urlpatterns = [
    # Index
    path('', IndexListView.as_view(), name='index'),

    # Products
    path('products/', ProductsListView.as_view(), name='products'),
    path('products/<slug:slug>/', ProductView.as_view(), name='view'),

    # Categories
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category-view'),

    # Brands
    path('brands/', index, name='brands'),
    path('brands/<slug:slug>/', index, name='brand-view'),

    # Country
    path('countries/', index, name='countries'),
    path('countries//<slug:slug>/', index, name='country-view'),

    # Auth
    path('login/', LogInView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogOutView.as_view(), name='logout'),

    # Account
    path('cart/', CartView.as_view(), name='cart'),
    path('favourites/', FavView.as_view(), name='favourites'),
    path('settings/', index, name='settings'),
]
