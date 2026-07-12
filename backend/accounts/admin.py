from django.contrib import admin

from .models import ClientProfile, CreditLimit, DealerProfile, User, CourierProfile

# Register your models here.
admin.site.register(User)
admin.site.register(DealerProfile)
admin.site.register(ClientProfile)
admin.site.register(CreditLimit)
admin.site.register(CourierProfile)