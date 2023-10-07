from django.contrib import admin
from core.models import Event

# Register your models here.

class EventAdmin(admin.ModelAdmin):
    "Customise event display on Django admin page"
    list_display = ('title', 'date', 'created')
    
admin.site.register(Event, EventAdmin)
