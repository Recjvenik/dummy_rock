from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import School, Classroom, Assignment, DailyChallenge, ChallengeCompletion
from .decorators import teacher_required
from .exports import export_class_csv
from modules.models import Module

User = get_user_model()


@teacher_required
def school_dashboard(request):
    """Teacher's school overview — classrooms, quick stats, recent activity."""
    school = getattr(request, 'school', None)
    classrooms = Classroom.objects.filter(teacher=request.user).select_related('school')
    if school:
        all_classrooms = Classroom.objects.filter(school=school).select_related('teacher')
    else:
        all_classrooms = classrooms

    context = {
        'classrooms': classrooms,
        'all_classrooms': all_classrooms,
        'school': school,
        'total_students': sum(c.students.count() for c in classrooms),
    }
    return render(request, 'school/dashboard.html', context)


@teacher_required
def classroom_detail(request, classroom_id):
    """Classroom view: student table, assignments, class leaderboard."""
    classroom = get_object_or_404(Classroom, pk=classroom_id)

    # Only teacher of this classroom or school_admin may view
    if request.user.role not in ('admin', 'school_admin') and classroom.teacher != request.user:
        messages.error(request, 'You do not have access to this classroom.')
        return redirect('/school/')

    students = classroom.students.all().order_by('first_name', 'last_name')
    assignments = classroom.assignments.select_related('module').order_by('-created_at')

    # Build leaderboard from gamification (graceful fallback)
    leaderboard = []
    for s in students:
        try:
            from gamification.models import UserXP
            xp_obj = UserXP.objects.filter(user=s).first()
            xp = xp_obj.total_xp if xp_obj else 0
            level = xp_obj.level if xp_obj else 1
        except Exception:
            xp = level = 0
        leaderboard.append({'user': s, 'xp': xp, 'level': level})
    leaderboard.sort(key=lambda x: x['xp'], reverse=True)

    context = {
        'classroom': classroom,
        'students': students,
        'assignments': assignments,
        'leaderboard': leaderboard[:10],
    }
    return render(request, 'school/classroom_detail.html', context)


@teacher_required
def student_report(request, classroom_id, student_id):
    """Per-student drill-down for a teacher."""
    classroom = get_object_or_404(Classroom, pk=classroom_id)
    student = get_object_or_404(User, pk=student_id)

    try:
        from gamification.models import UserXP
        from modules.models import UserProgress
        profile = UserXP.objects.filter(user=student).first()
        progress_qs = UserProgress.objects.filter(user=student).select_related('module').order_by('-last_accessed')
    except Exception:
        profile = None
        progress_qs = []

    context = {
        'classroom': classroom,
        'student': student,
        'profile': profile,
        'progress_list': progress_qs,
    }
    return render(request, 'school/student_report.html', context)


@teacher_required
def create_classroom(request):
    """Create a new classroom."""
    school = getattr(request, 'school', None)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        grade = request.POST.get('grade', '')
        if name and grade:
            classroom = Classroom.objects.create(
                school=school or _get_or_create_demo_school(request.user),
                teacher=request.user,
                name=name,
                grade=int(grade),
            )
            messages.success(request, f'Classroom "{name}" created! Join code: {classroom.join_code}')
            return redirect(f'/school/classroom/{classroom.pk}/')
        else:
            messages.error(request, 'Please provide a classroom name and grade.')
    return render(request, 'school/create_classroom.html', {'school': school})


def _get_or_create_demo_school(user):
    """Fallback: create a demo school for a teacher without a school FK."""
    school, _ = School.objects.get_or_create(
        name='Demo School',
        defaults={
            'city': 'India',
            'contact_email': user.email,
            'subscription_tier': 'free',
        }
    )
    return school


@teacher_required
def create_assignment(request, classroom_id):
    """Assign a module to a classroom."""
    classroom = get_object_or_404(Classroom, pk=classroom_id)
    modules = Module.objects.filter(is_published=True).order_by('order')

    if request.method == 'POST':
        module_id = request.POST.get('module_id')
        title = request.POST.get('title', '').strip()
        instructions = request.POST.get('instructions', '').strip()
        due_date_str = request.POST.get('due_date', '')
        status = request.POST.get('status', 'active')

        if module_id and title:
            module = get_object_or_404(Module, pk=module_id)
            due_date = None
            if due_date_str:
                from datetime import date
                try:
                    due_date = date.fromisoformat(due_date_str)
                except ValueError:
                    pass

            Assignment.objects.create(
                classroom=classroom,
                module=module,
                title=title,
                instructions=instructions,
                due_date=due_date,
                status=status,
                created_by=request.user,
            )
            messages.success(request, f'Assignment "{title}" created.')
            return redirect(f'/school/classroom/{classroom_id}/')

    return render(request, 'school/create_assignment.html', {
        'classroom': classroom,
        'modules': modules,
    })


@login_required
def join_classroom(request, code):
    """Student self-enrollment via 8-char join code."""
    classroom = get_object_or_404(Classroom, join_code=code.upper())

    if request.user in classroom.students.all():
        messages.info(request, f'You are already in {classroom.name}!')
        return redirect('/')

    classroom.students.add(request.user)

    # Set school FK on user if not set
    if hasattr(request.user, 'school_id') and not request.user.school_id:
        request.user.school = classroom.school
        request.user.save(update_fields=['school'])

    messages.success(request, f'Welcome to {classroom.school.name} — {classroom.name}! 🎉')
    return redirect('/')


@teacher_required
def export_class_report(request, classroom_id, fmt='csv'):
    """Download class report as CSV."""
    classroom = get_object_or_404(Classroom, pk=classroom_id)
    return export_class_csv(classroom)
