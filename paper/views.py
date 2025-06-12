from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views.generic import CreateView

from .forms import SubjectForm, QuestionForm
from .models import Subject, Question, ExamResult


def is_staff_user(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(is_staff_user)
def SubjectCreateView(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subject_list')
    else:
        form = SubjectForm()
    return render(request, 'paper/SubjectCreateView.html', {'form': form})

@login_required
@user_passes_test(is_staff_user)
def subject_list_staff(request):
    subjects = Subject.objects.all()
    return render(request, 'paper/SubjectListView.html', {'subjects': subjects})

@login_required
@user_passes_test(is_staff_user)
def delete_subject(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    subject.delete()
    return redirect('subject_list')

class QuestionCreateView(CreateView):
    model = Question
    fields = '__all__'
    template_name = 'paper/QuestionCreateView.html'

@login_required
@user_passes_test(is_staff_user)
def update_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    form = QuestionForm(request.POST or None, instance=question)
    if form.is_valid():
        form.save()
        return redirect('subject_list')
    return render(request, 'paper/QuestionUpdateView.html', {'form': form})

@login_required
@user_passes_test(is_staff_user)
def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == 'POST':
        question.delete()
        return redirect('subject_list')
    return render(request, 'paper/QuestionDeleteView.html', {'question': question})

@login_required
@user_passes_test(is_staff_user)
def manage_questions(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    questions = Question.objects.filter(subject=subject)

    if request.method == 'POST':
        if 'add_question' in request.POST:
            add_form = QuestionForm(request.POST)
            if add_form.is_valid():
                question = add_form.save(commit=False)
                question.subject = subject
                question.save()
                return redirect('manage_questions', subject_id=subject.id)

        elif 'update_question' in request.POST:
            question_id = request.POST.get('question_id')
            question = get_object_or_404(Question, id=question_id, subject=subject)
            update_form = QuestionForm(request.POST, instance=question)
            if update_form.is_valid():
                update_form.save()
                return redirect('manage_questions', subject_id=subject.id)

        elif 'delete_question' in request.POST:
            question_id = request.POST.get('question_id')
            question = get_object_or_404(Question, id=question_id, subject=subject)
            question.delete()
            return redirect('manage_questions', subject_id=subject.id)

    question_forms = {q.id: QuestionForm(instance=q) for q in questions}
    return render(request, 'paper/manage_questions.html', {
        'subject': subject,
        'questions': questions,
        'add_form': QuestionForm(),
        'question_forms': question_forms,
    })


@login_required
def subject_list_student(request):
    subjects = Subject.objects.all()
    return render(request, 'paper/subject_list_student.html', {'subjects': subjects})

@login_required
def take_exam(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    questions = Question.objects.filter(subject=subject)

    if not questions:
        return render(request, 'paper/no_question.html', {'subject': subject})

    if ExamResult.objects.filter(student=request.user, subject=subject).exists():
        return render(request, 'paper/already_taken.html', {'subject': subject})

    # Session-based timer (reload protection)
    session_key = f'exam_start_time_{subject_id}'
    if session_key not in request.session:
        request.session[session_key] = timezone.now().isoformat()

    # Use session time (parsed safely)
    try:
        start_time = parse_datetime(request.session[session_key])
    except Exception:
        start_time = timezone.now()
        request.session[session_key] = start_time.isoformat()

    elapsed = (timezone.now() - start_time).total_seconds()
    remaining = max(subject.duration_minutes * 60 - int(elapsed), 0)


    if request.method == 'POST':
        score = 0
        for question in questions:
            selected = request.POST.get(f'question_{question.id}')
            if selected and selected == question.correct_option:
                score += 1

        ExamResult.objects.create(
            student=request.user,
            subject=subject,
            score=score,
            total=questions.count()
        )
        request.session.pop(session_key, None)
        return redirect('exam_result', pk=subject.id)

    # GET = Show exam
    return render(request, 'paper/take_exam.html', {
        'subject': subject,
        'questions': questions,
        'duration_seconds': remaining
    })

@login_required
def submit_exam(request, paper_id):
    subject = get_object_or_404(Subject, id=paper_id)
    questions = Question.objects.filter(subject=subject)
    session_key = f'exam_start_time_{subject.id}'

    if ExamResult.objects.filter(student=request.user, subject=subject).exists():
        return redirect('exam_result', pk=subject.id)

    score = 0
    if request.method == 'POST':
        for question in questions:
            selected = request.POST.get(f'question_{question.id}')
            if selected and selected == question.correct_option:
                score += 1

        ExamResult.objects.create(
            student=request.user,
            subject=subject,
            score=score,
            total=questions.count()
        )

        if session_key in request.session:
            del request.session[session_key]

        return redirect('exam_result', pk=subject.id)

    return redirect('take_exam', subject_id=subject.id)

@login_required
def exam_result(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    result = get_object_or_404(ExamResult, student=request.user, subject=subject)
    return render(request, 'paper/exam_result.html', {
        'subject': subject,
        'score': result.score,
        'total': result.total,
        'date_taken': result.date_taken,
    })

# -------------------------------
# Reports
# -------------------------------
@login_required
def student_result_report(request):
    results = ExamResult.objects.filter(student=request.user).select_related('subject')
    return render(request, 'paper/student_report.html', {'results': results})

@login_required
@user_passes_test(is_staff_user)
def all_results_report(request):
    results = ExamResult.objects.select_related('student', 'subject').order_by('-date_taken')
    return render(request, 'paper/all_results.html', {'results': results})

# -------------------------------
# Dashboards
# -------------------------------
@login_required
@user_passes_test(is_staff_user)
def dashboard_view_staff(request):
    return render(request, 'dashboardstaff.html', {
        'subjects_count': Subject.objects.count(),
        'questions_count': Question.objects.count(),
        'exams_taken': ExamResult.objects.count()
    })

@login_required
def student_dashboard_view(request):
    if request.user.is_staff:
        return redirect('dashboard')

    # Replace any get_full_name() call with username
    full_name = request.user.full_name

    return render(request, 'student_dashboard.html', {
        'full_name': full_name,
        'subjects_count': Subject.objects.count(),
        'questions_count': Question.objects.count(),
        'exams_taken': ExamResult.objects.filter(student=request.user).count()
    })
