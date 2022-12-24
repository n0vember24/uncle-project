from django.contrib import admin

from .models import *

models = (User, Category, Brand, Country, Product, ProductImage, Review, Favourite, Cart)

admin.site.register(models)
