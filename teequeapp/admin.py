from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import *

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'is_staff', 'is_active', 'last_login']
    list_filter = ('is_staff', 'is_active', 'country')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'about', 'phonenumber', 'country', 'birth_date')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('date_joined',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active', 'groups', 'user_permissions')}
        ),
    )
    readonly_fields = ('last_login', 'date_joined')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'get_service_title', 'order_status')

    def get_service_title(self, obj):
        return obj.service.title
    get_service_title.short_description = 'Service'

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Seller)
admin.site.register(Buyer)
admin.site.register(Service)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Rating)
admin.site.register(Order)
admin.site.register(OrderItem, OrderItemAdmin)