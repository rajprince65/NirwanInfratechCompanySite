from django.contrib import admin
from .models import (
    ContactSubmission,
    InternshipApplication,
    InternshipVacancy,
    TeamMember,
    WorkspaceImage,
    TrainingProgram,
    ActivityImage,
)


@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'submitted_at', 'is_read')
    list_filter = ('is_read',)
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('submitted_at',)


@admin.register(InternshipApplication)
class InternshipApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'status', 'submitted_at', 'is_read')
    list_filter = ('status', 'position')
    search_fields = ('full_name', 'email')
    readonly_fields = ('submitted_at',)


@admin.register(InternshipVacancy)
class InternshipVacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'openings', 'is_active', 'created_at')
    list_editable = ('is_active',)
    search_fields = ('title', 'description')


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'order', 'is_founder', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('name', 'post')


@admin.register(WorkspaceImage)
class WorkspaceImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'uploaded_at')
    list_editable = ('order', 'is_active')
    search_fields = ('title',)
    readonly_fields = ('uploaded_at',)


@admin.register(TrainingProgram)
class TrainingProgramAdmin(admin.ModelAdmin):
    list_display  = ('title', 'track', 'duration', 'is_featured', 'is_active', 'order', 'created_at')
    list_editable = ('order', 'is_active', 'is_featured')
    list_filter   = ('track', 'is_active', 'is_featured', 'certificate', 'career_support')
    search_fields = ('title', 'subtitle', 'description', 'skills_tags')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'subtitle', 'description', 'track', 'icon', 'is_featured')
        }),
        ('Program Details', {
            'fields': ('duration', 'batch_size', 'mode', 'certificate', 'career_support',
                       'price_label', 'whatsapp_text', 'skills_tags')
        }),
        ('Syllabus (JSON)', {
            'fields': ('syllabus_json',),
            'description': (
                'Enter a JSON array. Each item: {"week":"Week 1–2","title":"Topic Title","topics":["Point 1","Point 2"]}'
            )
        }),
        ('Detail Page Content', {
            'fields': ('who_should_join', 'requirements', 'outcomes'),
            'classes': ('collapse',),
        }),
        ('Display Control', {
            'fields': ('order', 'is_active', 'created_at', 'updated_at')
        }),
    )

@admin.register(ActivityImage)
class ActivityImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'uploaded_at')
    list_editable = ('order', 'is_active')
    search_fields = ('title',)
    readonly_fields = ('uploaded_at',)