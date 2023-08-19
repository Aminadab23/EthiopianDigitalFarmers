from django.contrib import admin
from . import models

# Register your models here.
# from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
# admin.site.register(OutstandingToken)


admin.site.register(models.User)
admin.site.register(models.Product)
admin.site.register(models.Catagory)
admin.site.register(models.About)
admin.site.register(models.UserCart)
from rest_framework.authtoken.models import Token
admin.site.register(Token)