from django.contrib.auth.models import AbstractUser
from django.db.models import Model, SlugField, CharField, ImageField, ForeignKey, SET, JSONField, TextField, FloatField, \
    IntegerField, DateTimeField, CASCADE


class User(AbstractUser):
    phone_number = CharField(max_length=20, null=True, blank=True)


class Category(Model):
    slug = SlugField(max_length=100)
    name = CharField(max_length=100)
    icon = ImageField(upload_to='icons/category')

    def __str__(self):
        return f'{self.name}'


class Brand(Model):
    slug = SlugField(max_length=100)
    name = CharField(max_length=100)
    icon = ImageField(upload_to='icons/brand')

    def __str__(self):
        return f'{self.name}'


class Country(Model):
    slug = SlugField(max_length=100)
    name = CharField(max_length=100)
    flag = ImageField(upload_to='icons/flag')

    def __str__(self):
        return f'{self.name}'


class Product(Model):
    slug = SlugField(max_length=250)
    title = CharField(max_length=100)
    category = ForeignKey(Category, SET('Unknown'))
    brand = ForeignKey(Brand, SET('Unknown'))
    model = CharField(max_length=150)
    made = ForeignKey(Country, SET('Unknown'))
    details = JSONField(null=True, blank=True)
    description = TextField(null=True, blank=True)
    price = FloatField()
    discount = IntegerField(default=0)
    count = IntegerField(default=1)
    pub_date = DateTimeField(auto_now=True)
    edit_date = DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'


class ProductImage(Model):
    product = ForeignKey(Product, CASCADE)
    image = ImageField(upload_to='products')

    def __str__(self):
        return f'{self.product}'


class Review(Model):
    product = ForeignKey(Product, CASCADE)
    user = ForeignKey(User, SET('Deleted'))
    text = CharField(max_length=200)
    date = DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product} {self.user}'


class Favourite(Model):
    product = ForeignKey(Product, CASCADE)
    user = ForeignKey(User, CASCADE)

    def __str__(self):
        return f'{self.product}'


class Cart(Model):
    product = ForeignKey(Product, CASCADE)
    user = ForeignKey(User, CASCADE)
    count = IntegerField(default=1)

    class Meta:
        ordering = ('count',)

    def __str__(self):
        return f'{self.product}'
