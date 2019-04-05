from django.contrib import admin
from .models.profile import Profile
from .models.reset_password_code import ResetPasswordCode
from .models.user import User
from .models.libraries import Library, LibraryItem

class UserAdmin(admin.ModelAdmin):
    exclude = ('groups', 'user_permissions')


admin.site.register(Profile)
admin.site.register(ResetPasswordCode)
admin.site.register(User, UserAdmin)
admin.site.register(Library)
