from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

fields = list(UserAdmin.fieldsets)
fields[1] = ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'role', 'website', 'description', 'image')})
UserAdmin.fieldsets = tuple(fields)

admin.site.register(User, UserAdmin)


# class CustomUserAdmin(UserAdmin):
#     fieldsets = (
#         *UserAdmin.fieldsets,
#         (
#             'New Fields',
#             {
#                 'fields': (
#                     'role',
#                     'website',
#                     'description',
#                     'image',
#                 ),
#             },
#         ),
#     )

# admin.site.register(User, CustomUserAdmin)
