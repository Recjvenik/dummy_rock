from django.urls import path
from . import views

app_name = 'school'

urlpatterns = [
    path('', views.school_dashboard, name='dashboard'),
    path('classroom/<int:classroom_id>/', views.classroom_detail, name='classroom_detail'),
    path('classroom/<int:classroom_id>/student/<int:student_id>/', views.student_report, name='student_report'),
    path('create-classroom/', views.create_classroom, name='create_classroom'),
    path('classroom/<int:classroom_id>/assign/', views.create_assignment, name='create_assignment'),
    path('join/<str:code>/', views.join_classroom, name='join_classroom'),
    path('classroom/<int:classroom_id>/export/<str:fmt>/', views.export_class_report, name='export_class_report'),
]
