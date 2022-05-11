from django.db import models
from account.models import UserProfile

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    thumbnail = models.ImageField(upload_to="images", null=True)
    description = models.TextField()
    price = models.IntegerField()
    quantity = models.IntegerField()
    seller_detail = models.TextField(max_length=200)

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    items = models.ManyToManyField("OrderItem", related_name="order")
    ordered = models.BooleanField(default=False)
    order_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.id)

    def get_cart_total(self):
        orderitems = self.items.all()
        total = sum([item.get_total() for item in orderitems])
        return total

    def get_total_items(self):
        orderitems = self.items.all()
        total = sum([item.quantity for item in orderitems])
        return total

    


class OrderItem(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.product.name}"

    def get_total(self):
        total = self.product.price * self.quantity
        return total

