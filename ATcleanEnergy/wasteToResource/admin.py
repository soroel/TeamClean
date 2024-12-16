from django.contrib import admin

# Register your models here.
from .models import Profile, WasteListing, Transaction

admin.site.register(Profile)
admin.site.register(WasteListing)
admin.site.register(Transaction)
