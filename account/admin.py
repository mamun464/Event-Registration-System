from django.contrib import admin
from .models import CustomUser,EventRegistration
from django.contrib.auth.admin import UserAdmin

class UserAdminConfig(UserAdmin):
    search_fields = ('email', 'fullName','phone_no',)
    list_filter =('is_active','is_staff','is_superuser')
    ordering = ('id','phone_no')
    list_display =('id','email','fullName','phone_no','user_profile_img','is_active','is_staff','is_superuser','last_login')

    fieldsets = (
    (None, {'fields': ('fullName', 'email', 'phone_no', 'password',)}),
    ('Personal', {'fields': ('user_profile_img',)}),
    ('Permission', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_manager')}),
    )

    add_fieldsets = (
        (None,{
            'classes': ('wide',),
            'fields': ('fullName','email','phone_no','user_profile_img','password1','password2','is_active','is_staff','is_superuser')}
        ),
    )

class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'slot', 'registration_date')
    list_filter = ('user', 'slot__event', 'registration_date')
    search_fields = ['user__full_name', 'slot__event__title']

admin.site.register(EventRegistration, EventRegistrationAdmin)
    

admin.site.register(CustomUser,UserAdminConfig)

# Register your models here.
