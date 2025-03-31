from django.contrib import admin
from .models import *

class ApplicationStatusLogInline(admin.TabularInline):
    model = ApplicationStatusLog
    extra = 0
    readonly_fields = ('timestamp', 'changed_by', 'status', 'notes')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False

@admin.register(StudentApplication)
class StudentApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'course', 'status', 'application_date')
    list_filter = ('status', 'course', 'intake', 'country')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('application_id', 'application_date', 'last_updated')
    inlines = [ApplicationStatusLogInline]
    fieldsets = (
        ('Application Information', {
            'fields': ('application_id', 'status', 'application_date', 'last_updated')
        }),
        ('Course Information', {
            'fields': ('course', 'intake')
        }),
        ('Personal Information', {
            'fields': ('name', 'email', 'phone', 'gender', 'date_of_birth')
        }),
        ('Address Information', {
            'fields': ('physical_address', 'country', 'nationality')
        }),
        ('Documents', {
            'fields': ('national_id',)
        }),
        ('Additional Information', {
            'fields': ('how_did_you_hear', 'questions_or_comments')
        }),
        ('Metadata', {
            'fields': ('ip_address', 'marketing_consent'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if change and 'status' in form.changed_data:
            ApplicationStatusLog.objects.create(
                application=obj,
                status=obj.status,
                changed_by=request.user,
                notes=f"Status changed through admin by {request.user.username}"
            )
        super().save_model(request, obj, form, change)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code')

@admin.register(Intake)
class IntakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'application_deadline', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(ApplicationStatusLog)
class ApplicationStatusLogAdmin(admin.ModelAdmin):
    list_display = ('application', 'status', 'timestamp', 'changed_by')
    list_filter = ('status',)
    search_fields = ('application__name',)
    readonly_fields = ('application', 'status', 'timestamp', 'changed_by', 'notes')

@admin.register(Programme)
class ProgrammeAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'level', 'duration', 'study_mode', 'is_active')
    list_filter = ('level', 'study_mode', 'is_active')
    search_fields = ('name', 'code')
    prepopulated_fields = {'code': ('name',)}
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'level', 'duration', 'total_credits', 'study_mode')
        }),
        ('Descriptions', {
            'fields': ('description', 'entry_requirements', 'career_prospects'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active',)
        })
    )

@admin.register(ProgrammeFee)
class ProgrammeFeeAdmin(admin.ModelAdmin):
    list_display = ('programme', 'study_mode', 'fee_per_semester', 'effective_from', 'is_current')
    list_filter = ('programme__level', 'study_mode', 'is_current')
    search_fields = ('programme__name', 'programme__code')
    date_hierarchy = 'effective_from'