from django.contrib import admin

class UserAdmin(admin.ModelAdmin):
    """
    User Admin Form
    """
    list_display = ('full_name', 'email', 'is_active', 'is_staff', 'last_login')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    readonly_fields = ('id', 'last_login', 'token', 'created', 'updated')
    search_fields = ('first_name', 'last_name', 'email')
    fieldsets = (
        ('Personal', {
            'fields': ('first_name', 'last_name')
        }),
        ('Account', {
            'fields': ('id', 'email', 'last_login', 'token', 'created', 'updated')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        }),
    )

    def full_name(self, obj):
        return obj.get_full_name()

admin.site.register(models.User, UserAdmin)
