from django.contrib import admin

from .models import Motion, Door

# Register your models here.
class MotionAdmin(admin.ModelAdmin):
    list_display = ('motion_type', 'motion_date', 'was_published_recently')

admin.site.register(Motion,MotionAdmin)


class DoorAdmin(admin.ModelAdmin):
    list_display = ('door_type', 'door_date','was_published_recently')
    
admin.site.register(Door, DoorAdmin)
