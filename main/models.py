from django.db import models
from django.core.validators import validate_email, RegexValidator
from django.utils.translation import gettext_lazy as _
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django_countries.fields import CountryField

class StudentApplication(models.Model):
    class Status(models.TextChoices):
        APPLIED = 'applied', _('Applied')
        UNDER_REVIEW = 'under_review', _('Under Review')
        INTERVIEW_SCHEDULED = 'interview_scheduled', _('Interview Scheduled')
        ACCEPTED = 'accepted', _('Accepted')
        REJECTED = 'rejected', _('Rejected')
        ENROLLED = 'enrolled', _('Enrolled')
        DEFERRED = 'deferred', _('Deferred')

    class Gender(models.TextChoices):
        MALE = 'male', _('Male')
        FEMALE = 'female', _('Female')
        OTHER = 'other', _('Other')
        PREFER_NOT_TO_SAY = 'prefer_not_to_say', _('Prefer not to say')


    # Application Information
    application_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=20,choices=Status.choices,default=Status.APPLIED)
    application_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    # Course Information
    course = models.ForeignKey('Course',on_delete=models.SET_NULL,null=True,blank=True,related_name='applications')
    intake = models.ForeignKey('Intake',on_delete=models.SET_NULL,null=True,blank=True,related_name='applications')
    # Personal Information
    name = models.CharField(max_length=255)
    email = models.EmailField(validators=[validate_email])
    phone = models.CharField(max_length=20,validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ]
    )
    gender = models.CharField(max_length=20,choices=Gender.choices,null=True,blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    # Address Information
    physical_address = models.CharField(max_length=225, null=True, blank=True)
    country = CountryField(blank_label="(select country)")
    nationality = models.CharField(max_length=100, null=True, blank=True)
    
    # Documents
    national_id = models.FileField(upload_to='applications/national_ids/',null=True,blank=True)
    # Additional Information
    how_did_you_hear = models.TextField(_('How did you hear about us?'),null=True,blank=True)
    questions_or_comments = models.TextField(_('Your message/questions'),null=True,blank=True)
    
    # Metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    marketing_consent = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - {self.course} ({self.get_status_display()})"
    
    class Meta:
        ordering = ['-application_date']
        verbose_name = _('Student Application')
        verbose_name_plural = _('Student Applications')


class Intake(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    application_deadline = models.DateField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name


class ApplicationStatusLog(models.Model):
    application = models.ForeignKey(StudentApplication,on_delete=models.CASCADE,related_name='status_logs')
    status = models.CharField(max_length=20,choices=StudentApplication.Status.choices)
    changed_by = models.ForeignKey('auth.User',on_delete=models.SET_NULL,null=True,blank=True
)
    timestamp = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.application} -> {self.get_status_display()} at {self.timestamp}"
    
    class Meta:
        ordering = ['-timestamp']

class Programme(models.Model):
    class Level(models.TextChoices):
        CERTIFICATE = 'certificate', _('Certificate')
        DIPLOMA = 'diploma', _('Diploma')
        BACHELORS = 'bachelors', _('Bachelor\'s Degree')
        MASTERS = 'masters', _('Master\'s Degree')
        PHD = 'phd', _('PhD')
        POST_DOC = 'post_doc', _('Post-Doctoral')

    class StudyMode(models.TextChoices):
        FULL_TIME = 'full_time', _('Full Time')
        PART_TIME = 'part_time', _('Part Time')
        ONLINE = 'online', _('Online')
        HYBRID = 'hybrid', _('Hybrid')

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, unique=True)
    level = models.CharField(max_length=20,choices=Level.choices,default=Level.BACHELORS)
    duration = models.PositiveSmallIntegerField(help_text=_("Duration in months"),validators=[MinValueValidator(3), MaxValueValidator(120)])
    total_credits = models.PositiveSmallIntegerField(help_text=_("Total credits required for completion"),validators=[MinValueValidator(30), MaxValueValidator(360)])
    study_mode = models.CharField(max_length=20,choices=StudyMode.choices,default=StudyMode.FULL_TIME)
    description = models.TextField(blank=True)
    entry_requirements = models.TextField(blank=True)
    career_prospects = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_level_display()} in {self.name} ({self.code})"

class Course(models.Model):
    programme = models.ForeignKey(Programme,on_delete=models.CASCADE,related_name='courses')
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20)
    credits = models.PositiveSmallIntegerField(default=10,validators=[MinValueValidator(1), MaxValueValidator(60)])
    is_core = models.BooleanField(default=True)
    semester = models.PositiveSmallIntegerField(choices=[(1, 'Semester 1'), (2, 'Semester 2'), (3, 'Semester 3'), (4, 'Semester 4')],default=1)
    description = models.TextField(blank=True)
    learning_outcomes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('programme', 'code')

    def __str__(self):
        return f"{self.code} - {self.name} ({self.programme})"

class ProgrammeFee(models.Model):
    programme = models.ForeignKey(Programme,on_delete=models.CASCADE,related_name='fees')
    study_mode = models.CharField(max_length=20,choices=Programme.StudyMode.choices)
    fee_per_semester = models.DecimalField(max_digits=10,decimal_places=2,help_text=_("Fee per semester in local currency"))
    registration_fee = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    other_charges = models.DecimalField(max_digits=10,decimal_places=2,default=0.00,help_text=_("Other mandatory charges"))
    effective_from = models.DateField()
    effective_until = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.programme} - {self.get_study_mode_display()} Fee Structure"

    class Meta:
        unique_together = ('programme', 'study_mode', 'effective_from')