from django.contrib import admin
from .models import * 
# Register your models here.

admin.site.register(user)
admin.site.register(card_details)
admin.site.register(account_status)
admin.site.register(reccuring_account_status)

