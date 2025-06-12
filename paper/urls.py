from django.urls import path

from . import views

urlpatterns = [
    # Subject Management (Staff)
    path('subjects/create/', views.SubjectCreateView, name='create_subject'),
    path('subjects/<int:pk>/delete/', views.delete_subject, name='delete_subject'),
    path('subjects/staff/', views.subject_list_staff, name='subject_list'),

    # Subject List (Student)
    path('subjects/', views.subject_list_student, name='subject_list_student'),

    # Question Management (Staff)
    path('subjects/<int:subject_id>/questions/', views.manage_questions, name='manage_questions'),
    path('questions/create/', views.QuestionCreateView.as_view(), name='create_question'),
    path('questions/<int:pk>/update/', views.update_question, name='update_question'),
    path('questions/<int:pk>/delete/', views.delete_question, name='delete_question'),

    # Exam Participation (Student)
    path('subject/<int:subject_id>/take/', views.take_exam, name='take_exam'),
    path('subject/<int:pk>/result/', views.exam_result, name='exam_result'),

    # Result Reports
    path('student/reports/', views.student_result_report, name='student_report'),
    path('staff/reports/', views.all_results_report, name='all_results'),

    # Dashboards
    path('dashboard/', views.dashboard_view_staff, name='dashboard'),
    path('student/dashboard/', views.student_dashboard_view, name='student_dashboard'),
path('exam/<int:paper_id>/submit/', views.submit_exam, name='submit_exam'),

]
