import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import (
    ContactSubmission,
    InternshipApplication,
    InternshipVacancy,
    TeamMember,
    WorkspaceImage,
    TrainingProgram,          # ← FIX: was missing from import
    ActivityImage,
)


def is_admin(user):
    return user.is_authenticated and user.is_staff


# ──────────────────────────────────────────
# Public views (frontend)
# ──────────────────────────────────────────

def home(request):
    workspace_images = WorkspaceImage.objects.filter(is_active=True)
    activity_images  = ActivityImage.objects.filter(is_active=True)
    return render(request, 'app1/index.html', {
        'workspace_images': workspace_images,
        'activity_images':  activity_images,
    })

def about(request):
    members = TeamMember.objects.filter(is_active=True)
    return render(request, 'app1/about.html', {'team_members': members})

def blog(request):
    return render(request, 'app1/blog.html')

def contact(request):
    if request.method == 'POST':
        if request.content_type and 'application/json' in request.content_type:
            try:
                body = json.loads(request.body)
            except (json.JSONDecodeError, ValueError):
                body = {}
            name            = body.get('name', '').strip()
            email           = body.get('email', '').strip()
            phone           = body.get('phone', '').strip()
            alternate_phone = body.get('alternate_phone', '').strip()
            message         = body.get('message', '').strip()
        else:
            name            = request.POST.get('name', '').strip()
            email           = request.POST.get('email', '').strip()
            phone           = request.POST.get('phone', '').strip()
            alternate_phone = request.POST.get('alternate_phone', '').strip()
            message         = request.POST.get('message', '').strip()

        if name and email and message:
            ContactSubmission.objects.create(
                name            = name,
                email           = email,
                phone           = phone,
                alternate_phone = alternate_phone or None,
                message         = message,
            )
            if request.content_type and 'application/json' in request.content_type:
                return JsonResponse({'success': True, 'message': 'Your message has been sent!'})
            messages.success(request, 'Thank you! Your message has been sent.')
        else:
            if request.content_type and 'application/json' in request.content_type:
                return JsonResponse(
                    {'success': False, 'message': 'Please fill in all required fields.'},
                    status=400
                )
            messages.error(request, 'Please fill in all required fields.')

        return redirect('contact')

    return render(request, 'app1/contact.html')

def detail(request):
    return render(request, 'app1/detail.html')

def feature(request):
    return render(request, 'app1/feature.html')

def careers(request):
    vacancies = InternshipVacancy.objects.filter(is_active=True)
    total_openings = sum(v.openings for v in vacancies)
    return render(request, 'app1/careers.html', {
        'vacancies': vacancies,
        'total_openings': total_openings,
    })

# ── FIX: removed the empty duplicate `def training(request)` that was here.
#    The real one (below, with DB query) is the only definition now.


# ──────────────────────────────────────────
# Internship application submit
# ──────────────────────────────────────────

@require_POST
def submit_internship(request):
    if request.content_type and 'application/json' in request.content_type:
        try:
            body = json.loads(request.body)
        except (json.JSONDecodeError, ValueError):
            body = {}
        data    = body
        cv_file = None
    else:
        data    = request.POST
        cv_file = request.FILES.get('cv_file')

    position  = data.get('position', '').strip()
    full_name = data.get('full_name', '').strip()

    if not position or not full_name:
        return JsonResponse(
            {'success': False, 'message': 'Position and full name are required.'},
            status=400
        )

    if cv_file and cv_file.size > 5 * 1024 * 1024:
        return JsonResponse(
            {'success': False, 'message': 'CV file must be under 5 MB.'},
            status=400
        )

    application = InternshipApplication.objects.create(
        position    = position,
        full_name   = full_name,
        email       = data.get('email', '').strip(),
        phone       = data.get('phone', '').strip(),
        program     = data.get('program', '').strip(),
        institution = data.get('institution', '').strip(),
        skills      = data.get('skills', '').strip(),
        portfolio   = data.get('portfolio', '').strip(),
        motivation  = data.get('motivation', '').strip(),
        cv_file     = cv_file,
    )

    return JsonResponse({
        'success': True,
        'message': 'Application submitted successfully!',
        'id': application.pk,
    })


# ──────────────────────────────────────────
# Admin Login / Logout
# ──────────────────────────────────────────

def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')

    if request.method == 'POST':
        email    = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        user = None
        if email:
            try:
                user_obj = User.objects.get(email__iexact=email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None
            except User.MultipleObjectsReturned:
                user_obj = User.objects.filter(email__iexact=email, is_staff=True).first()
                if user_obj:
                    user = authenticate(request, username=user_obj.username, password=password)

        if user and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')

        messages.error(request, 'Invalid email or password, or account lacks admin access.')

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
    contacts     = ContactSubmission.objects.all()
    applications = InternshipApplication.objects.all()
    vacancies    = InternshipVacancy.objects.all()
    context = {
        'total_contacts':        contacts.count(),
        'unread_contacts':       contacts.filter(is_read=False).count(),
        'total_applications':    applications.count(),
        'pending_applications':  applications.filter(status='pending').count(),
        'active_vacancies':      vacancies.filter(is_active=True).count(),
        'total_team_members':    TeamMember.objects.filter(is_active=True).count(),
        'total_training_programs': TrainingProgram.objects.filter(is_active=True).count(),
        'recent_contacts':       contacts[:5],
        'recent_applications':   applications[:5],
    }
    return render(request, 'app1/admin/dashboard.html', context)


# ──────────────────────────────────────────
# Contact Submissions
# ──────────────────────────────────────────

@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def admin_contacts(request):
    q        = request.GET.get('q', '')
    contacts = ContactSubmission.objects.all()
    if q:
        contacts = contacts.filter(
            Q(name__icontains=q) | Q(email__icontains=q) | Q(message__icontains=q)
        )
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
    q               = request.GET.get('q', '')
    status_filter   = request.GET.get('status', '')
    position_filter = request.GET.get('position', '')
    applications    = InternshipApplication.objects.all()
    if q:
        applications = applications.filter(
            Q(full_name__icontains=q) | Q(email__icontains=q) | Q(position__icontains=q)
        )
    if status_filter:
        applications = applications.filter(status=status_filter)
    if position_filter:
        applications = applications.filter(position=position_filter)
    return render(request, 'app1/admin/applications.html', {
        'applications':    applications,
        'q':               q,
        'status_filter':   status_filter,
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
    if application.cv_file:
        application.cv_file.delete(save=False)
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
            title        = request.POST.get('title', ''),
            department   = request.POST.get('department', ''),
            description  = request.POST.get('description', ''),
            requirements = request.POST.get('requirements', ''),
            duration     = request.POST.get('duration', ''),
            stipend      = request.POST.get('stipend', ''),
            location     = request.POST.get('location', 'Remote / Biratnagar'),
            openings     = int(request.POST.get('openings', 1) or 1),
            category     = request.POST.get('category', 'dev'),
            icon_type    = request.POST.get('icon_type', 'web'),
            skills_tags  = request.POST.get('skills_tags', ''),
            is_active    = request.POST.get('is_active') == 'on',
        )
        messages.success(request, 'Vacancy created successfully!')
        return redirect('admin_vacancies')
    return render(request, 'app1/admin/vacancy_form.html', {'action': 'Create'})


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def admin_vacancy_edit(request, pk):
    vacancy = get_object_or_404(InternshipVacancy, pk=pk)
    if request.method == 'POST':
        vacancy.title        = request.POST.get('title', '')
        vacancy.department   = request.POST.get('department', '')
        vacancy.description  = request.POST.get('description', '')
        vacancy.requirements = request.POST.get('requirements', '')
        vacancy.duration     = request.POST.get('duration', '')
        vacancy.stipend      = request.POST.get('stipend', '')
        vacancy.location     = request.POST.get('location', 'Remote / Biratnagar')
        vacancy.openings     = int(request.POST.get('openings', 1) or 1)
        vacancy.category     = request.POST.get('category', 'dev')
        vacancy.icon_type    = request.POST.get('icon_type', 'web')
        vacancy.skills_tags  = request.POST.get('skills_tags', '')
        vacancy.is_active    = request.POST.get('is_active') == 'on'
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


# ──────────────────────────────────────────
# Team Member Management
# ──────────────────────────────────────────

@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def admin_team_members(request):
    members = TeamMember.objects.all()
    return render(request, 'app1/admin/team_members.html', {'members': members})


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def admin_team_member_create(request):
    if request.method == 'POST':
        member = TeamMember(
            name        = request.POST.get('name', '').strip(),
            post        = request.POST.get('post', '').strip(),
            description = request.POST.get('description', '').strip(),
            github      = request.POST.get('github', '').strip(),
            linkedin    = request.POST.get('linkedin', '').strip(),
            email       = request.POST.get('email', '').strip(),
            order       = int(request.POST.get('order', 0) or 0),
            is_founder  = request.POST.get('is_founder') == 'on',
            is_active   = request.POST.get('is_active') == 'on',
        )
        if request.FILES.get('photo'):
            member.photo = request.FILES['photo']
        member.save()
        messages.success(request, 'Team member added successfully!')
        return redirect('admin_team_members')
    return render(request, 'app1/admin/team_member_form.html', {'action': 'Add'})


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def admin_team_member_edit(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    if request.method == 'POST':
        member.name        = request.POST.get('name', '').strip()
        member.post        = request.POST.get('post', '').strip()
        member.description = request.POST.get('description', '').strip()
        member.github      = request.POST.get('github', '').strip()
        member.linkedin    = request.POST.get('linkedin', '').strip()
        member.email       = request.POST.get('email', '').strip()
        member.order       = int(request.POST.get('order', 0) or 0)
        member.is_founder  = request.POST.get('is_founder') == 'on'
        member.is_active   = request.POST.get('is_active') == 'on'
        if request.FILES.get('photo'):
            if member.photo:
                member.photo.delete(save=False)
            member.photo = request.FILES['photo']
        member.save()
        messages.success(request, 'Team member updated successfully!')
        return redirect('admin_team_members')
    return render(request, 'app1/admin/team_member_form.html', {'action': 'Edit', 'member': member})


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def admin_team_member_delete(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    if member.photo:
        member.photo.delete(save=False)
    member.delete()
    messages.success(request, 'Team member deleted.')
    return redirect('admin_team_members')


# ── Workspace Images ──────────────────────────────────────────────

@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def admin_workspace_images(request):
    images = WorkspaceImage.objects.all()
    return render(request, 'app1/admin/workspace_images.html', {'images': images})


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def admin_workspace_image_create(request):
    if request.method == 'POST':
        title      = request.POST.get('title', '').strip()
        order      = request.POST.get('order', 0)
        is_active  = request.POST.get('is_active') == 'on'
        image_file = request.FILES.get('image')
        if image_file:
            WorkspaceImage.objects.create(
                title=title, order=order, is_active=is_active, image=image_file,
            )
            messages.success(request, 'Workspace image added.')
            return redirect('admin_workspace_images')
        else:
            messages.error(request, 'Please upload an image.')
    return render(request, 'app1/admin/workspace_image_form.html', {'action': 'Add'})


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def admin_workspace_image_edit(request, pk):
    img = get_object_or_404(WorkspaceImage, pk=pk)
    if request.method == 'POST':
        img.title     = request.POST.get('title', '').strip()
        img.order     = request.POST.get('order', 0)
        img.is_active = request.POST.get('is_active') == 'on'
        if request.FILES.get('image'):
            img.image = request.FILES['image']
        img.save()
        messages.success(request, 'Workspace image updated.')
        return redirect('admin_workspace_images')
    return render(request, 'app1/admin/workspace_image_form.html', {'action': 'Edit', 'img': img})


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def admin_workspace_image_delete(request, pk):
    img = get_object_or_404(WorkspaceImage, pk=pk)
    if request.method == 'POST':
        img.delete()
        messages.success(request, 'Image deleted.')
        return redirect('admin_workspace_images')
    return render(request, 'app1/admin/workspace_image_confirm_delete.html', {'img': img})


# ── Public: Training Programs ─────────────────────────────────────

def training(request):
    programs = TrainingProgram.objects.filter(is_active=True)
    return render(request, 'app1/training.html', {'programs': programs})


# ── Public: Training program detail page ─────────────────────────

def training_detail(request, pk):
    program        = get_object_or_404(TrainingProgram, pk=pk, is_active=True)
    other_programs = TrainingProgram.objects.filter(is_active=True).exclude(pk=pk)[:3]
    return render(request, 'app1/training_detail.html', {
        'program':        program,
        'other_programs': other_programs,
    })


# ── Admin: Training Programs list ────────────────────────────────

@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def admin_training_programs(request):
    programs = TrainingProgram.objects.all()
    return render(request, 'app1/admin/training_programs.html', {'programs': programs})


# ── Admin: Create training program ───────────────────────────────

def _clean_syllabus_json(raw):
    """
    Validate the syllabus JSON submitted from the form.
    Returns (cleaned_json_string, error_message_or_None).
    """
    raw = (raw or '').strip()
    if not raw or raw == '[]':
        return '[]', None
    try:
        data = json.loads(raw)
        if not isinstance(data, list):
            return '[]', 'Syllabus JSON must be a list (array). Saved as empty.'
        # strip out any items that are missing required keys
        cleaned = []
        for item in data:
            if isinstance(item, dict) and 'week' in item and 'title' in item and isinstance(item.get('topics'), list):
                cleaned.append(item)
        return json.dumps(cleaned, ensure_ascii=False), None
    except (json.JSONDecodeError, ValueError) as e:
        return '[]', f'Invalid JSON in Syllabus field ({e}). Saved as empty — please re-enter.'


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def admin_training_program_create(request):
    if request.method == 'POST':
        raw_syllabus = request.POST.get('syllabus_json', '[]')
        syllabus_json, syl_err = _clean_syllabus_json(raw_syllabus)
        if syl_err:
            messages.warning(request, f'⚠ Syllabus JSON issue: {syl_err}')

        TrainingProgram.objects.create(
            title           = request.POST.get('title', '').strip(),
            subtitle        = request.POST.get('subtitle', '').strip(),
            description     = request.POST.get('description', '').strip(),
            track           = request.POST.get('track', 'dev'),
            icon            = request.POST.get('icon', 'code'),
            is_featured     = request.POST.get('is_featured') == 'on',
            duration        = request.POST.get('duration', '').strip(),
            batch_size      = request.POST.get('batch_size', 'Max 10 per Batch').strip(),
            mode            = request.POST.get('mode', 'Offline / Online').strip(),
            certificate     = request.POST.get('certificate') == 'on',
            career_support  = request.POST.get('career_support') == 'on',
            price_label     = request.POST.get('price_label', 'Enrollment Fee — Contact Us').strip(),
            whatsapp_text   = request.POST.get('whatsapp_text', '').strip(),
            skills_tags     = request.POST.get('skills_tags', '').strip(),
            syllabus_json   = syllabus_json,
            who_should_join = request.POST.get('who_should_join', '').strip(),
            requirements    = request.POST.get('requirements', '').strip(),
            outcomes        = request.POST.get('outcomes', '').strip(),
            order           = int(request.POST.get('order', 0) or 0),
            is_active       = request.POST.get('is_active') == 'on',
        )
        messages.success(request, 'Training program created successfully!')
        return redirect('admin_training_programs')
    return render(request, 'app1/admin/training_program_form.html', {'action': 'Create'})


# ── Admin: Edit training program ─────────────────────────────────

@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def admin_training_program_edit(request, pk):
    program = get_object_or_404(TrainingProgram, pk=pk)
    if request.method == 'POST':
        raw_syllabus = request.POST.get('syllabus_json', '[]')
        syllabus_json, syl_err = _clean_syllabus_json(raw_syllabus)
        if syl_err:
            messages.warning(request, f'⚠ Syllabus JSON issue: {syl_err}')

        program.title           = request.POST.get('title', '').strip()
        program.subtitle        = request.POST.get('subtitle', '').strip()
        program.description     = request.POST.get('description', '').strip()
        program.track           = request.POST.get('track', 'dev')
        program.icon            = request.POST.get('icon', 'code')
        program.is_featured     = request.POST.get('is_featured') == 'on'
        program.duration        = request.POST.get('duration', '').strip()
        program.batch_size      = request.POST.get('batch_size', 'Max 10 per Batch').strip()
        program.mode            = request.POST.get('mode', 'Offline / Online').strip()
        program.certificate     = request.POST.get('certificate') == 'on'
        program.career_support  = request.POST.get('career_support') == 'on'
        program.price_label     = request.POST.get('price_label', 'Enrollment Fee — Contact Us').strip()
        program.whatsapp_text   = request.POST.get('whatsapp_text', '').strip()
        program.skills_tags     = request.POST.get('skills_tags', '').strip()
        program.syllabus_json   = syllabus_json
        program.who_should_join = request.POST.get('who_should_join', '').strip()
        program.requirements    = request.POST.get('requirements', '').strip()
        program.outcomes        = request.POST.get('outcomes', '').strip()
        program.order           = int(request.POST.get('order', 0) or 0)
        program.is_active       = request.POST.get('is_active') == 'on'
        program.save()
        messages.success(request, 'Training program updated successfully!')
        return redirect('admin_training_programs')
    return render(request, 'app1/admin/training_program_form.html', {
        'action': 'Edit', 'program': program
    })


# ── Admin: Delete training program ───────────────────────────────

@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def admin_training_program_delete(request, pk):
    program = get_object_or_404(TrainingProgram, pk=pk)
    program.delete()
    messages.success(request, 'Training program deleted.')
    return redirect('admin_training_programs')

# ── Admin: Activity Images ────────────────────────────────────────

@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def admin_activity_images(request):
    images = ActivityImage.objects.all()
    return render(request, 'app1/admin/activity_images.html', {'images': images})


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def admin_activity_image_create(request):
    if request.method == 'POST':
        title      = request.POST.get('title', '').strip()
        order      = request.POST.get('order', 0)
        is_active  = request.POST.get('is_active') == 'on'
        image_file = request.FILES.get('image')
        if image_file:
            ActivityImage.objects.create(
                title=title, order=order, is_active=is_active, image=image_file,
            )
            messages.success(request, 'Activity image added.')
            return redirect('admin_activity_images')
        else:
            messages.error(request, 'Please upload an image.')
    return render(request, 'app1/admin/activity_image_form.html', {'action': 'Add'})


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def admin_activity_image_edit(request, pk):
    img = get_object_or_404(ActivityImage, pk=pk)
    if request.method == 'POST':
        img.title     = request.POST.get('title', '').strip()
        img.order     = request.POST.get('order', 0)
        img.is_active = request.POST.get('is_active') == 'on'
        if request.FILES.get('image'):
            img.image = request.FILES['image']
        img.save()
        messages.success(request, 'Activity image updated.')
        return redirect('admin_activity_images')
    return render(request, 'app1/admin/activity_image_form.html', {'action': 'Edit', 'img': img})


@login_required(login_url='admin_login')
@user_passes_test(is_admin, login_url='admin_login')
def admin_activity_image_delete(request, pk):
    img = get_object_or_404(ActivityImage, pk=pk)
    if request.method == 'POST':
        img.delete()
        messages.success(request, 'Activity image deleted.')
        return redirect('admin_activity_images')
    return render(request, 'app1/admin/activity_image_confirm_delete.html', {'img': img})