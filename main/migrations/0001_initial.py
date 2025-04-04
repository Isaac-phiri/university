# Generated by Django 5.1.7 on 2025-03-25 08:19

import django.core.validators
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=2, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Intake',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('application_deadline', models.DateField()),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Programme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=20, unique=True)),
                ('level', models.CharField(choices=[('certificate', 'Certificate'), ('diploma', 'Diploma'), ('bachelors', "Bachelor's Degree"), ('masters', "Master's Degree"), ('phd', 'PhD'), ('post_doc', 'Post-Doctoral')], default='bachelors', max_length=20)),
                ('duration', models.PositiveSmallIntegerField(help_text='Duration in months', validators=[django.core.validators.MinValueValidator(3), django.core.validators.MaxValueValidator(120)])),
                ('total_credits', models.PositiveSmallIntegerField(help_text='Total credits required for completion', validators=[django.core.validators.MinValueValidator(30), django.core.validators.MaxValueValidator(360)])),
                ('study_mode', models.CharField(choices=[('full_time', 'Full Time'), ('part_time', 'Part Time'), ('online', 'Online'), ('hybrid', 'Hybrid')], default='full_time', max_length=20)),
                ('description', models.TextField(blank=True)),
                ('entry_requirements', models.TextField(blank=True)),
                ('career_prospects', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=20)),
                ('credits', models.PositiveSmallIntegerField(default=10, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(60)])),
                ('is_core', models.BooleanField(default=True)),
                ('semester', models.PositiveSmallIntegerField(choices=[(1, 'Semester 1'), (2, 'Semester 2'), (3, 'Semester 3'), (4, 'Semester 4')], default=1)),
                ('description', models.TextField(blank=True)),
                ('learning_outcomes', models.TextField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('programme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='main.programme')),
            ],
            options={
                'unique_together': {('programme', 'code')},
            },
        ),
        migrations.CreateModel(
            name='StudentApplication',
            fields=[
                ('application_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('applied', 'Applied'), ('under_review', 'Under Review'), ('interview_scheduled', 'Interview Scheduled'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('enrolled', 'Enrolled'), ('deferred', 'Deferred')], default='applied', max_length=20)),
                ('application_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator()])),
                ('phone', models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('gender', models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other'), ('prefer_not_to_say', 'Prefer not to say')], max_length=20, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('physical_address', models.CharField(blank=True, max_length=225, null=True)),
                ('nationality', models.CharField(blank=True, max_length=100, null=True)),
                ('national_id', models.FileField(blank=True, null=True, upload_to='applications/national_ids/')),
                ('how_did_you_hear', models.TextField(blank=True, null=True, verbose_name='How did you hear about us?')),
                ('questions_or_comments', models.TextField(blank=True, null=True, verbose_name='Your message/questions')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('marketing_consent', models.BooleanField(default=False)),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='applications', to='main.country')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='applications', to='main.course')),
                ('intake', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='applications', to='main.intake')),
            ],
            options={
                'verbose_name': 'Student Application',
                'verbose_name_plural': 'Student Applications',
                'ordering': ['-application_date'],
            },
        ),
        migrations.CreateModel(
            name='ApplicationStatusLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('applied', 'Applied'), ('under_review', 'Under Review'), ('interview_scheduled', 'Interview Scheduled'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('enrolled', 'Enrolled'), ('deferred', 'Deferred')], max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('changed_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status_logs', to='main.studentapplication')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='ProgrammeFee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('study_mode', models.CharField(choices=[('full_time', 'Full Time'), ('part_time', 'Part Time'), ('online', 'Online'), ('hybrid', 'Hybrid')], max_length=20)),
                ('fee_per_semester', models.DecimalField(decimal_places=2, help_text='Fee per semester in local currency', max_digits=10)),
                ('registration_fee', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('other_charges', models.DecimalField(decimal_places=2, default=0.0, help_text='Other mandatory charges', max_digits=10)),
                ('effective_from', models.DateField()),
                ('effective_until', models.DateField(blank=True, null=True)),
                ('is_current', models.BooleanField(default=True)),
                ('programme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fees', to='main.programme')),
            ],
            options={
                'unique_together': {('programme', 'study_mode', 'effective_from')},
            },
        ),
    ]
