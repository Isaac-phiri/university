from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, ListView, DetailView, TemplateView
from django.urls import reverse_lazy
from .models import StudentApplication, Intake, Programme, Course, ProgrammeFee
from .forms import (
    StudentApplicationForm, 
    IntakeForm, 
    ApplicationStatusLogForm, 
    ProgrammeForm, 
    CourseForm, 
    ProgrammeFeeForm
)


# Student Application Views
class StudentApplicationCreateView(CreateView):
    model = StudentApplication
    form_class = StudentApplicationForm
    template_name = 'detail.html'
    success_url = reverse_lazy('application_success')
    
    def form_valid(self, form):
        # Capture IP address
        form.instance.ip_address = self.request.META.get('REMOTE_ADDR')
        messages.success(self.request, 'Your application has been submitted successfully!')
        return super().form_valid(form)

class ApplicationSuccessView(TemplateView):
    template_name = 'application_success.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Application Submitted'
        return context

class StudentApplicationListView(ListView):
    model = StudentApplication
    template_name = 'student_application_list.html'
    context_object_name = 'applications'
    paginate_by = 10


class StudentApplicationDetailView(DetailView):
    model = StudentApplication
    template_name = 'student_application_detail.html'
    context_object_name = 'application'


# Intake Views
class IntakeCreateView(CreateView):
    model = Intake
    form_class = IntakeForm
    template_name = 'intake_form.html'
    success_url = reverse_lazy('intake_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Intake created successfully!')
        return super().form_valid(form)


class IntakeUpdateView(UpdateView):
    model = Intake
    form_class = IntakeForm
    template_name = 'intake_form.html'
    success_url = reverse_lazy('intake_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Intake updated successfully!')
        return super().form_valid(form)


class IntakeListView(ListView):
    model = Intake
    template_name = 'intake_list.html'
    context_object_name = 'intakes'


# Programme Views
class ProgrammeCreateView(CreateView):
    model = Programme
    form_class = ProgrammeForm
    template_name = 'programme_form.html'
    success_url = reverse_lazy('programme_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Programme created successfully!')
        return super().form_valid(form)


class ProgrammeUpdateView(UpdateView):
    model = Programme
    form_class = ProgrammeForm
    template_name = 'programme_form.html'
    success_url = reverse_lazy('programme_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Programme updated successfully!')
        return super().form_valid(form)


class ProgrammeListView(ListView):
    model = Programme
    template_name = 'programme_list.html'
    context_object_name = 'programmes'


# Course Views
class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'course_form.html'
    success_url = reverse_lazy('course_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Course created successfully!')
        return super().form_valid(form)

class CourseView(TemplateView):
    template_name = 'course-details.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Application Submitted'
        return context

class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'course_form.html'
    success_url = reverse_lazy('course_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Course updated successfully!')
        return super().form_valid(form)


class CourseListView(ListView):
    model = Course
    template_name = 'course_list.html'
    context_object_name = 'courses'


# Programme Fee Views
class ProgrammeFeeCreateView(CreateView):
    model = ProgrammeFee
    form_class = ProgrammeFeeForm
    template_name = 'programme_fee_form.html'
    success_url = reverse_lazy('programme_fee_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Fee structure created successfully!')
        return super().form_valid(form)


class ProgrammeFeeUpdateView(UpdateView):
    model = ProgrammeFee
    form_class = ProgrammeFeeForm
    template_name = 'programme_fee_form.html'
    success_url = reverse_lazy('programme_fee_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Fee structure updated successfully!')
        return super().form_valid(form)


class ProgrammeFeeListView(ListView):
    model = ProgrammeFee
    template_name = 'programme_fee_list.html'
    context_object_name = 'fees'


# Application Status Update View
def update_application_status(request, pk):
    application = get_object_or_404(StudentApplication, pk=pk)
    
    if request.method == 'POST':
        form = ApplicationStatusLogForm(request.POST)
        if form.is_valid():
            status_log = form.save(commit=False)
            status_log.application = application
            status_log.changed_by = request.user
            status_log.save()
            
            # Update the application status
            application.status = status_log.status
            application.save()
            
            messages.success(request, 'Application status updated successfully!')
            return redirect('application_detail', pk=pk)
    else:
        form = ApplicationStatusLogForm(initial={'application': application, 'status': application.status})
    
    return render(request, 'update_application_status.html', {
        'form': form,
        'application': application
    })

def admission(request):
    return render(request, 'admission.html')

def diploma(request):
    return render(request, 'diploma.html')
def certificate(request):
    return render(request, 'cert.html')

def homepage(request):
    return render(request, "index.html")

# def detail_page(request):
#     return render(request, 'detail.html')

def contact_page(request):
    return render(request, 'contact.html')

def course_detail(request):
    return render(request, 'course_detail.html')