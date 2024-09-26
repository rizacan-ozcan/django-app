from django.contrib import admin
from .models import Contact, About

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at")
    search_fields = ("name", "email")
    list_filter = ("created_at",)

admin.site.register(About)
# Register your models here.
