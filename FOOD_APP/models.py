from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.
userchoices=(
    (1,"Admin"),
    (2,"Employee"),
    (3,"Client")
)

orderstatus=(
    (1,"Ordered"),
    (2,"Pending"),
    (3,"Delivered"),
    (4,"Cancelled")
)


class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['phone_number','username']

    name = models.CharField(max_length=100,null=True,blank=True)
    user_type = models.IntegerField(default=1,choices=userchoices)
    phone_number = models.CharField(max_length=10,null=True,blank=True)
    email = models.EmailField(null=True,blank=True,unique=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        if self.name:
            return self.name
        else:
           return self.username


class Food_items(models.Model):
    item_name = models.CharField(max_length=30, null=True, blank=True)
    item_code = models.CharField(max_length=10, null=True, blank=True)
    category = models.CharField(max_length=30, null=True, blank=True)
    description = models.CharField(max_length=40, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    price = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True)
    old_price = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(null=True, blank=True, unique=True)
    house_no = models.CharField(max_length=10, null=True, blank=True)
    land_mark = models.CharField(max_length=40, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    district = models.CharField(max_length=30, null=True, blank=True)
    pin_code = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.house_no


class Order(models.Model):
     item = models.ForeignKey(Food_items, on_delete=models.CASCADE)
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     quantity = models.IntegerField(null=True, blank=True)
     order_date = models.DateTimeField(null=True,blank=True)
     total_price = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True)
     status = models.IntegerField(default=1, choices=orderstatus)


class Cart(models.Model):
      item = models.ForeignKey(Food_items, on_delete=models.CASCADE)
      user = models.ForeignKey(User, on_delete=models.CASCADE)
      quantity = models.IntegerField(null=True, blank=True)
      item_total = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True)


class Notification(models.Model):
     message = models.TextField()
     user = models.ForeignKey(User, on_delete=models.CASCADE)
     read = models.BooleanField(default=False)
     datetime = models.DateTimeField(auto_now_add=True)

     def __str__(self):
         return self.message
