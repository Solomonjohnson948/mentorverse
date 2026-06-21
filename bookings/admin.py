from django.contrib import admin
from .models import Mentor, Booking, Profile, Review


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'expertise',
        'company',
        'price',
        'rating',
        'reviews',
        'is_featured',
    )

    list_filter = (
        'is_featured',
        'rating',
    )

    search_fields = (
        'name',
        'expertise',
        'company',
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'customer_name',
        'email',
        'mentor',
        'date',
        'time',
        'status',
        'payment_status',
        'created_at',
    )

    list_filter = (
        'status',
        'payment_status',
        'date',
        'mentor',
    )

    search_fields = (
        'customer_name',
        'email',
        'mentor__name',
        'user__username',
    )

    readonly_fields = (
        'user',
        'mentor',
        'customer_name',
        'email',
        'date',
        'time',
        'reason',
        'payment_status',
        'created_at',
    )

    fieldsets = (
        ('Booking Information', {
            'fields': (
                'user',
                'mentor',
                'customer_name',
                'email',
                'date',
                'time',
                'reason',
            )
        }),

        ('Admin Decision', {
            'fields': (
                'status',
                'payment_status',
                'admin_note',
            )
        }),

        ('System Information', {
            'fields': (
                'created_at',
            )
        }),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'user',
        'gender',
        'field',
        'goal',
    )

    list_filter = (
        'field',
        'goal',
        'gender',
    )

    search_fields = (
        'full_name',
        'user__username',
        'field',
        'goal',
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'mentor',
        'rating',
        'created_at',
    )

    search_fields = (
        'user__username',
        'mentor__name',
        'comment',
    )

    list_filter = (
        'rating',
        'created_at',
    )