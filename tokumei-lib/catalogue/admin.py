from django.contrib import admin
from .models import Booktitle, Bookitem, CircAccount
# Register your models here.
admin.site.register(Booktitle)
admin.site.register(Bookitem)
admin.site.register(CircAccount)