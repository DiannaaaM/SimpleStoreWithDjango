from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name", help_text="Category Name")
    description = models.TextField(verbose_name="Description", help_text="Description", blank=True, null=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name", help_text="Product Name")
    price = models.FloatField(verbose_name="Price", help_text="Price")
    description = models.TextField(verbose_name="Description", help_text="Description", null=True, blank=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name="Category", help_text="Category", on_delete=models.CASCADE,
                                 null=True, blank=True)
    image = models.ImageField(upload_to='images/', verbose_name="Image", null=True, blank=True, help_text="Image")
    is_published = models.BooleanField(default=False, verbose_name="Published", help_text="Is Published")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True,
                              related_name='products', verbose_name='Owner', help_text='Product Owner')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date Added", help_text="Date Added", blank=True,
                                      null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date Last Modified", help_text="Date Last Modified",
                                      null=True, blank=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ["description", "name"]
        permissions = (
            ("can_unpublish_product", "Can unpublish product"),
        )

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
