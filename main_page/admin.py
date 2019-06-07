from django.contrib import admin
from main_page.models import User
 
 
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
