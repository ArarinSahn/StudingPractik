from django.contrib import admin

from myapp.models import Status, PayMethod, DateConductEvent, Event, Roles

admin.site.register(Status)
admin.site.register(PayMethod)
admin.site.register(Event)
admin.site.register(DateConductEvent)
admin.site.register(Roles)
# Register your models here.
