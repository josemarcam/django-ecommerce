from django.contrib import admin
from users.models import User

# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "username",
        "first_name",
        "email",
        "is_staff",
        "is_trusty",
    ]
    list_filter = ["username", "first_name", "email"]
    list_editable = ["is_staff", "is_trusty"]
