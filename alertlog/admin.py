from django.contrib import admin
from .models import  Hostnames, Roles, Filterlog 
# Register your models here.


admin.site.register(Hostnames)
admin.site.register(Roles)
admin.site.register(Filterlog)
