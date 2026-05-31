import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import ContactSubmission, InternshipApplication, InternshipVacancy


def is_admin(user):
    return user.is_authenticated and user.is_staff


# ──────────────────────────────────────────
# Public views (frontend – unchanged)
# ──────────────────────────────────────────

def home(request):
    return render(request, 'app1/index.html')

def about(request):
    return render(request, 'app1/about.html')

def blog(request):
    return render(request, 'app1/blog.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()
        if name and email and message:
            ContactSubmission.objects.create(name=name, email=email, message=message)
            messages.success(request, 'Thank you! Your message has been sent.')
        else:
            messages.error(request, 'Please fill in all required fields.')
        return redirect('contact')
    return render(request, 'app1/contact.html')

def detail(request):
    return render(request, 'app1/detail.html')

def feature(request):
    return render(request, 'app1/feature.html')

def careers(request):
    vacancies = InternshipVacancy.objects.filter(is_active=True)
    return render(request, 'app1/careers.html', {'vacancies': vacancies})

def training(request):
    return render(request, 'app1/training.html')


# ──────────────────────────────────────────
# Internship application submit (AJAX/POST)
# ──────────────────────────────────────────

@require_POST
def submit_internship(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        data = request.POST

    InternshipApplication.objects.create(
        position=data.get('position', ''),
        full_name=data.get('full_name', ''),
        email=data.get('email', ''),
        phone=data.get('phone', ''),
        program=data.get('program', ''),
        institution=data.get('institution', ''),
        skills=data.get('skills', ''),
        portfolio=data.get('portfolio', ''),
        motivation=data.get('motivation', ''),
    )
    return JsonResponse({'success': True, 'message': 'Application submitted successfully!'})


# ──────────────────────────────────────────
# Admin Login / Logout
# ──────────────────────────────────────────

def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        messages.error(request, 'Invalid credentials or insufficient permissions.')
    return render(request, 'app1/admin/login.html')


def admin_logout(request):
    logout(request)
    return redirect('admin_login')


# ──────────────────────────────────────────
# Admin Dashboard
# ──────────────────────────────────────────

@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def admin_dashboard(request):
    contacts = ContactSubmission.objects.all()
    applications = InternshipApplication.objects.all()
    vacancies = InternshipVacancy.objects.all()
    context = {
        'total_contacts': contacts.count(),
        'unread_contacts': contacts.filter(is_read=False).count(),
        'total_applications': applications.count(),
        'pending_applications': applications.filter(status='pending').count(),
        'active_vacancies': vacancies.filter(is_active=True).count(),
        'recent_contacts': contacts[:5],
        'recent_applications': applications[:5],
    }
    return render(request, 'app1/admin/dashboard.html', context)


# ──────────────────────────────────────────
# Contact Submissions
# ──────────────────────────────────────────

@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def admin_contacts(request):
    q = request.GET.get('q', '')
    contacts = ContactSubmission.objects.all()
    if q:
        contacts = contacts.filter(Q(name__icontains=q) | Q(email__icontains=q) | Q(message__icontains=q))
    return render(request, 'app1/admin/contacts.html', {'contacts': contacts, 'q': q})


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def admin_contact_detail(request, pk):
    contact = get_object_or_404(ContactSubmission, pk=pk)
    contact.is_read = True
    contact.save()
    return render(request, 'app1/admin/contact_detail.html', {'contact': contact})


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def admin_contact_delete(request, pk):
    contact = get_object_or_404(ContactSubmission, pk=pk)
    contact.delete()
    messages.success(request, 'Contact submission deleted.')
    return redirect('admin_contacts')


# ──────────────────────────────────────────
# Internship Applications
# ──────────────────────────────────────────

@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def admin_applications(request):
    q = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    position_filter = request.GET.get('position', '')
    applications = InternshipApplication.objects.all()
    if q:
        applications = applications.filter(
            Q(full_name__icontains=q) | Q(email__icontains=q) | Q(position__icontains=q)
        )
    if status_filter:
        applications = applications.filter(status=status_filter)
    if position_filter:
        applications = applications.filter(position=position_filter)
    return render(request, 'app1/admin/applications.html', {
        'applications': applications,
        'q': q,
        'status_filter': status_filter,
        'position_filter': position_filter,
    })


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def admin_application_detail(request, pk):
    application = get_object_or_404(InternshipApplication, pk=pk)
    application.is_read = True
    application.save()
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(InternshipApplication.STATUS_CHOICES):
            application.status = new_status
            application.save()
            messages.success(request, f'Status updated to {new_status}.')
        return redirect('admin_application_detail', pk=pk)
    return render(request, 'app1/admin/application_detail.html', {'application': application})


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def admin_application_delete(request, pk):
    application = get_object_or_404(InternshipApplication, pk=pk)
    application.delete()
    messages.success(request, 'Application deleted.')
    return redirect('admin_applications')


# ──────────────────────────────────────────
# Vacancy Management
# ──────────────────────────────────────────

@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def admin_vacancies(request):
    vacancies = InternshipVacancy.objects.all()
    return render(request, 'app1/admin/vacancies.html', {'vacancies': vacancies})


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def admin_vacancy_create(request):
    if request.method == 'POST':
        InternshipVacancy.objects.create(
            title=request.POST.get('title', ''),
            department=request.POST.get('department', ''),
            description=request.POST.get('description', ''),
            requirements=request.POST.get('requirements', ''),
            duration=request.POST.get('duration', ''),
            stipend=request.POST.get('stipend', ''),
            is_active=request.POST.get('is_active') == 'on',
        )
        messages.success(request, 'Vacancy created successfully!')
        return redirect('admin_vacancies')
    return render(request, 'app1/admin/vacancy_form.html', {'action': 'Create'})


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def admin_vacancy_edit(request, pk):
    vacancy = get_object_or_404(InternshipVacancy, pk=pk)
    if request.method == 'POST':
        vacancy.title = request.POST.get('title', '')
        vacancy.department = request.POST.get('department', '')
        vacancy.description = request.POST.get('description', '')
        vacancy.requirements = request.POST.get('requirements', '')
        vacancy.duration = request.POST.get('duration', '')
        vacancy.stipend = request.POST.get('stipend', '')
        vacancy.is_active = request.POST.get('is_active') == 'on'
        vacancy.save()
        messages.success(request, 'Vacancy updated successfully!')
        return redirect('admin_vacancies')
    return render(request, 'app1/admin/vacancy_form.html', {'action': 'Edit', 'vacancy': vacancy})


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def admin_vacancy_delete(request, pk):
    vacancy = get_object_or_404(InternshipVacancy, pk=pk)
    vacancy.delete()
    messages.success(request, 'Vacancy deleted.')
    return redirect('admin_vacancies')
