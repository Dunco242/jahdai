from django.urls import path
from . import views

urlpatterns = [
    path('student_registration/', views.student_registration, name='student_registration'),
    path('staff_registration/', views.staff_registration, name='staff_registration'),
    path('', views.student_list, name='student_list'),
    path('staff_list/', views.staff_list, name='staff_list'),
    path('staff_registration/', views.staff_registration, name='staff_registration'),
    path('staff/<int:staff_id>/', views.staff_detail, name='staff_detail'),
    path('student_detail/<int:student_id>/', views.student_detail, name='student_detail'),
    path('allergies/<int:student_id>/', views.allergies, name='allergies'),
    path('add_incident/', views.add_incident, name='add_incident'),
    path('add_milestone/', views.add_milestone, name='add_milestone'),
    path('search_students/', views.search_students, name='search_students'),
    path("autocomplete/students/", views.autocomplete_students, name="autocomplete_students"),
    path("autocomplete/incidents/", views.autocomplete_incidents, name="autocomplete_incidents"),
    path("autocomplete/milestones/", views.autocomplete_milestones, name="autocomplete_milestones"),
    path('update_status/<int:student_id>/', views.update_student_status, name='update_student_status'),
    path('send_email/', views.send_email, name='send_email'),

    # Add more URLs for other views as needed
]
