from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Fields shown in the list view
    list_display = (
        "id",
        "username",
        "email",
        "is_active",
        "is_staff",
        "date_joined",
        "last_login",
    )

    # Fields you can filter by (right sidebar)
    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
    )

    # Fields you can search by (top search box)
    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )

    # Default ordering
    ordering = ("-date_joined",)

    # Show detailed info grouping in the edit view
    fieldsets = (
        ("Account Info", {"fields": ("username", "email", "password")}),
        (
            "Personal Info",
            {"fields": ("first_name", "last_name")},
        ),
        (
            "Permissions",
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        (
            "Important Dates",
            {"fields": ("last_login", "date_joined")},
        ),
    )

    # Fields that are read-only (can’t be edited)
    readonly_fields = ("last_login", "date_joined")