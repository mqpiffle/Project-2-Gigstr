from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Event
from django.utils.translation import gettext_lazy as _
# ~~ This loads in the 'default' admin page
# and appends our custom ifon to the bottom

class AccountAdmin(UserAdmin):
    # form = UserCreateForm2
    # add_form = UserCreateForm2
    search_fields = ('email', )
    readonly_fields = ('date_joined', 'last_login')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('User Details'), {'fields': ('first_name', 'last_name', 'role')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
            (
                None,
                {
                    'classes': ('wide',),
                    'fields': ('username', 'password1', 'password2', 'role'),
                },
            ),
        )

# class CustomUserAdmin(UserAdmin):
#     fieldsets = (
#         *UserAdmin.fieldsets,
#         (
#             'Custom Fields',
#             {
#                 'fields': (
#                     'role',
#                 ),
#             },
#         ),
#     )

# admin.site.register(CustomUser, CustomUserAdmin)

# ~~ This loads in the 'default admin page
# and allows us to insert oucustom info where we want it
# inline to add inputs to signup form
# ~~ This is actually for submittin/displaying
# two forms as one
# class UserRolesInline(admin.StackedInline):
#     model = CustomUser
#     can_delete = False

# class UserAdmin(AuthUserAdmin):
#     def add_view(self, *args, **kwargs):
#         self.inlines = [UserRolesInline]
#         return super(UserAdmin, self).add_view(*args, **kwargs)

fields = list(UserAdmin.fieldsets)
fields[1] = ('User Details', {'fields': ('first_name', 'last_name', 'email', 'role')})
UserAdmin.fieldsets = tuple(fields)

admin.site.register(CustomUser, AccountAdmin)
admin.site.register(Event)