from django.contrib import admin
from .models import(
    Employee
)
# Register your models here.
@admin.register(Employee)
class PersonAdmin(admin.ModelAdmin):
    list_display = ("name","city", "birthday", "email", "phone")
    pass