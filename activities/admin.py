from django.contrib import admin
from activities.models import Activity


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    
    list_display = [
        "name",
        "creator",
        "type",
        "created", 
        "modified",
    ]
    ordering = ("-modified",)
# Register your models here.
