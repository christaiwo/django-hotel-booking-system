from django.contrib import admin
from .models import *

class FooAdmin(admin.ModelAdmin):
    inlines = (hotel_gallery,)
    save_as = True


# Register your models here.
admin.site.register(Profile)
admin.site.register(category)
admin.site.register(hotel)
admin.site.register(hotel_gallery)
admin.site.register(booking)
admin.site.register(canceled_booking)
admin.site.register(ticket)
admin.site.register(ticket_reply)
admin.site.register(contact)