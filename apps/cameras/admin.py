from django.contrib import admin
from apps.cameras.models import Room
from apps.cameras.models import Camera


class CamsInline(admin.TabularInline):
    model = Camera
    extra = 1

class RoomAdmin(admin.ModelAdmin):
    model = Room
    inlines = [
        CamsInline,
    ]

admin.site.register(Room, RoomAdmin)
