from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User as CustomUser
from .models import Profile
from .forms import UserChangeForm, UserCreationForm
# from django.utils.translation import ugettext_lazy as _

class UserProfileInline(admin.StackedInline):
    model = Profile

class CustomUserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = CustomUser

    
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active',)
    list_filter = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'is_active',)

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    # here the fields from add user form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'first_name', 'last_name', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

    inlines = [UserProfileInline]
    

admin.site.register(CustomUser, CustomUserAdmin)
