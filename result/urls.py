from django.urls import path

from . import views

urlpatterns = [
    # Student: All subjects report
    path('my-report/', views.student_report_view, name='student_report'),

    # Student: Report for a specific subject
    path('my-report/<int:subject_id>/', views.subject_report_view, name='subject_report'),

    # Staff: View all results
    path('all/', views.all_results_report, name='all_results'),

]
