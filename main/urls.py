from django.urls import path
from .views import *

urlpatterns = [
    path('', homepage, name='homepage'),
    # path('detail_page/', detail_page, name='detail'),
    path('contact_page/', contact_page, name='contact'),
    path('course/', course_detail, name='course'),
    path('admission/', admission, name='admission'),
     path('diploma/', diploma, name='diploma'),
      path('cert/', certificate, name='cert'),

    # Student Application URLs
    path('application/new/', StudentApplicationCreateView.as_view(), name='application_create'),
    path('applications/', StudentApplicationListView.as_view(), name='application_list'),
    path('application/<uuid:pk>/', StudentApplicationDetailView.as_view(), name='application_detail'),
    path('application/<uuid:pk>/update-status/', update_application_status, name='update_application_status'),
    path('application/success/', ApplicationSuccessView.as_view(), name='application_success'),  # Add this line
    # Intake URLs
    path('intake/new/', IntakeCreateView.as_view(), name='intake_create'),
    path('intake/<int:pk>/edit/', IntakeUpdateView.as_view(), name='intake_update'),
    path('intakes/', IntakeListView.as_view(), name='intake_list'),
    
    # Programme URLs
    path('programme/new/', ProgrammeCreateView.as_view(), name='programme_create'),
    path('programme/<int:pk>/edit/', ProgrammeUpdateView.as_view(), name='programme_update'),
    path('programmes/', ProgrammeListView.as_view(), name='programme_list'),
    
    # Course URLs
    path('course_detail/', CourseView.as_view(), name='course'),
    path('course/new/', CourseCreateView.as_view(), name='course_create'),
    path('course/<int:pk>/edit/', CourseUpdateView.as_view(), name='course_update'),
    path('courses/', CourseListView.as_view(), name='course_list'),
    
    # Programme Fee URLs
    path('fee/new/', ProgrammeFeeCreateView.as_view(), name='programme_fee_create'),
    path('fee/<int:pk>/edit/', ProgrammeFeeUpdateView.as_view(), name='programme_fee_update'),
    path('fees/', ProgrammeFeeListView.as_view(), name='programme_fee_list'),
]

