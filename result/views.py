from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404

from paper.models import ExamResult, Subject


def is_staff_user(user):
    return user.is_authenticated and user.is_staff

# STUDENT: All Results
@login_required
def student_report_view(request):
    results = ExamResult.objects.filter(student=request.user).select_related('subject')
    report = []
    for result in results:
        percentage = (result.score / result.total * 100) if result.total > 0 else 0
        report.append({
            'subject': result.subject.name,
            'score': result.score,
            'total': result.total,
            'percentage': round(percentage, 2),
            'date_taken': result.date_taken,
        })
    student_name = f"{request.user.full_name}".strip() or request.user.username
    return render(request, 'paper/student_report.html', {
        'report': report,
        'student': student_name,
    })

# STUDENT: Detailed Result
@login_required
def subject_report_view(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    result = ExamResult.objects.filter(subject=subject, student=request.user).first()
    percentage = (result.score / result.total * 100) if result and result.total > 0 else 0
    return render(request, 'paper/my_report.html', {
        'subject': subject,
        'result': result,
        'percentage': round(percentage, 2)
    })

# STAFF: View all student results
@login_required
@user_passes_test(is_staff_user)
def all_results_report(request):
    results = ExamResult.objects.select_related('student', 'subject').order_by('-date_taken')
    return render(request, 'paper/all_results.html', {'results': results})


from django.shortcuts import render

def index_view(request):
    return render(request, 'index.html')
