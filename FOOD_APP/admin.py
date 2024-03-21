from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)

admin.site.register(Food_items)

admin.site.register(Address)

admin.site.register(Order)

admin.site.register(Cart)

admin.site.register(Notification)
