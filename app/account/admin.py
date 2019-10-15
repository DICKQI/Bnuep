from django.contrib import admin
from .models import UserAccount

# Register your models here.

@admin.register(UserAccount)
class UserAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['name', 'student_id', 'phone_number']
    list_filter = ['grade', 'major']
    search_fields = ['name', 'student_id']