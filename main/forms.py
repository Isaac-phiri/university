from django import forms
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column, HTML, Div
from crispy_forms.bootstrap import PrependedText, InlineRadios, TabHolder, Tab
from django_countries.widgets import CountrySelectWidget
from .models import (
    StudentApplication, 
    Intake, 
    ApplicationStatusLog, 
    Programme, 
    Course, 
    ProgrammeFee
)


class StudentApplicationForm(forms.ModelForm):
    class Meta:
        model = StudentApplication
        exclude = ['application_id', 'status', 'application_date', 'last_updated', 'ip_address']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'country': CountrySelectWidget(attrs={'class': 'custom-select'}),
        }
        labels = {
            'marketing_consent': _('I agree to receive marketing communications'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.form_tag = True
        self.helper.form_id = 'student-application-form'
        self.helper.layout = Layout(
            HTML('<h2 class="mb-4">Student Application Form</h2>'),
            
            Fieldset(
                'Course Information',
                Row(
                    Column('course', css_class='form-group col-md-6'),
                    Column('intake', css_class='form-group col-md-6'),
                    css_class='form-row'
                ),
            ),
            
            Fieldset(
                'Personal Information',
                Row(
                    Column('name', css_class='form-group col-md-12'),
                    css_class='form-row'
                ),
                Row(
                    Column('email', css_class='form-group col-md-6'),
                    Column(PrependedText('phone', '<i class="fa fa-phone"></i>'), css_class='form-group col-md-6'),
                    css_class='form-row'
                ),
                Row(
                    Column(InlineRadios('gender'), css_class='form-group col-md-6'),
                    Column('date_of_birth', css_class='form-group col-md-6'),
                    css_class='form-row'
                ),
            ),
            
            Fieldset(
                'Address Information',
                Row(
                    Column('physical_address', css_class='form-group col-md-12'),
                    css_class='form-row'
                ),
                Row(
                    Column('country', css_class='form-group col-md-6'),
                    Column('nationality', css_class='form-group col-md-6'),
                    css_class='form-row'
                ),
            ),
            
            Fieldset(
                'Documents',
                'national_id',
                HTML('<p class="text-muted">Please upload a scanned copy of your national ID or passport</p>'),
            ),
            
            Fieldset(
                'Additional Information',
                'how_did_you_hear',
                'questions_or_comments',
            ),
            
            Div(
                'marketing_consent',
                css_class='custom-control custom-checkbox mb-4'
            ),
            
            Div(
                Submit('submit', 'Submit Application', css_class='btn btn-primary btn-lg'),
                HTML('<a href="{% url "home" %}" class="btn btn-secondary btn-lg ml-2">Cancel</a>'),
                css_class='text-center'
            )
        )


class IntakeForm(forms.ModelForm):
    class Meta:
        model = Intake
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'application_deadline': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            HTML('<h2 class="mb-4">Intake Information</h2>'),
            
            Row(
                Column('name', css_class='form-group col-md-12'),
                css_class='form-row'
            ),
            Row(
                Column('start_date', css_class='form-group col-md-6'),
                Column('end_date', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            'application_deadline',
            'is_active',
            
            Div(
                Submit('submit', 'Save Intake', css_class='btn btn-primary'),
                HTML('<a href="{% url "intake_list" %}" class="btn btn-secondary ml-2">Cancel</a>'),
                css_class='text-right mt-3'
            )
        )


class ApplicationStatusLogForm(forms.ModelForm):
    class Meta:
        model = ApplicationStatusLog
        fields = ['application', 'status', 'notes']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            HTML('<h2 class="mb-4">Update Application Status</h2>'),
            
            'application',
            'status',
            'notes',
            
            Div(
                Submit('submit', 'Update Status', css_class='btn btn-primary'),
                HTML('<a href="{% url "application_list" %}" class="btn btn-secondary ml-2">Cancel</a>'),
                css_class='text-right mt-3'
            )
        )


class ProgrammeForm(forms.ModelForm):
    class Meta:
        model = Programme
        exclude = ['created_at', 'updated_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            HTML('<h2 class="mb-4">Programme Information</h2>'),
            
            TabHolder(
                Tab('Basic Information',
                    Row(
                        Column('name', css_class='form-group col-md-8'),
                        Column('code', css_class='form-group col-md-4'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('level', css_class='form-group col-md-6'),
                        Column('study_mode', css_class='form-group col-md-6'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('duration', css_class='form-group col-md-6'),
                        Column('total_credits', css_class='form-group col-md-6'),
                        css_class='form-row'
                    ),
                    'is_active',
                ),
                Tab('Details',
                    'description',
                    'entry_requirements',
                    'career_prospects',
                ),
            ),
            
            Div(
                Submit('submit', 'Save Programme', css_class='btn btn-primary'),
                HTML('<a href="{% url "programme_list" %}" class="btn btn-secondary ml-2">Cancel</a>'),
                css_class='text-right mt-3'
            )
        )


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            HTML('<h2 class="mb-4">Course Information</h2>'),
            
            'programme',
            Row(
                Column('name', css_class='form-group col-md-8'),
                Column('code', css_class='form-group col-md-4'),
                css_class='form-row'
            ),
            Row(
                Column('credits', css_class='form-group col-md-6'),
                Column('semester', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            'is_core',
            'description',
            'learning_outcomes',
            'is_active',
            
            Div(
                Submit('submit', 'Save Course', css_class='btn btn-primary'),
                HTML('<a href="{% url "course_list" %}" class="btn btn-secondary ml-2">Cancel</a>'),
                css_class='text-right mt-3'
            )
        )


class ProgrammeFeeForm(forms.ModelForm):
    class Meta:
        model = ProgrammeFee
        fields = '__all__'
        widgets = {
            'effective_from': forms.DateInput(attrs={'type': 'date'}),
            'effective_until': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        self.helper.layout = Layout(
            HTML('<h2 class="mb-4">Programme Fee Structure</h2>'),
            
            'programme',
            'study_mode',
            Row(
                Column('fee_per_semester', css_class='form-group col-md-4'),
                Column('registration_fee', css_class='form-group col-md-4'),
                Column('other_charges', css_class='form-group col-md-4'),
                css_class='form-row'
            ),
            Row(
                Column('effective_from', css_class='form-group col-md-6'),
                Column('effective_until', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            'is_current',
            
            Div(
                Submit('submit', 'Save Fee Structure', css_class='btn btn-primary'),
                HTML('<a href="{% url "programme_fee_list" %}" class="btn btn-secondary ml-2">Cancel</a>'),
                css_class='text-right mt-3'
            )
        )

