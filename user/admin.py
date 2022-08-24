from django.contrib import admin
from django.contrib.auth.models import Permission
from .models import User,Comment, Images
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea
# Register your models here.

class UserAdminConfig(UserAdmin):
    search_fields = ('email','user_name','first_name','last_name')
    list_filter = ('email','user_name','first_name','last_name','is_active','is_staff')
    ordering = ('-start_date',)
    list_display = ('email','user_name','first_name','is_active','last_name','is_staff')


    fieldsets = (
        (None,{'fields':('email','user_name','first_name','last_name')}),
        ('Permissions',{'fields':('is_staff','is_active')}),
        ('Personal',{'fields':('phoneNumber','dateOfBirth','address')}),
    )

    add_fieldsets = (
        (None,{
            'classes': ('wide',),
            'fields':('email','user_name','first_name','last_name','password1','password2','phoneNumber','dateOfBirth','address','is_active','is_staff')}
        ),
    )


admin.site.register(User,UserAdminConfig)
admin.site.register(Comment)
admin.site.register(Images)