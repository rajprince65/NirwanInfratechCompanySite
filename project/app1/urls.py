# ─────────────────────────────────────────────
# Add these lines to your existing urls.py urlpatterns list.
# ─────────────────────────────────────────────

# ── Public: Training Detail ───────────────────────────────────────────
# path('training/<int:pk>/', views.training_detail, name='training_detail'),

# ── Admin: Training Programs ──────────────────────────────────────────
# path('myadmin/training/',                          views.admin_training_programs,        name='admin_training_programs'),
# path('myadmin/training/create/',                   views.admin_training_program_create,  name='admin_training_program_create'),
# path('myadmin/training/<int:pk>/edit/',            views.admin_training_program_edit,    name='admin_training_program_edit'),
# path('myadmin/training/<int:pk>/delete/',          views.admin_training_program_delete,  name='admin_training_program_delete'),

# ─────────────────────────────────────────────
# Full updated urlpatterns for easy copy-paste:
# ─────────────────────────────────────────────

from django.urls import path
from . import views

urlpatterns = [
    # ── Frontend ──────────────────────────────────────────────────
    path('',                views.home,             name='home'),
    path('about/',          views.about,            name='about'),
    path('blog/',           views.blog,             name='blog'),
    path('contact/',        views.contact,          name='contact'),
    path('detail/',         views.detail,           name='detail'),
    path('feature/',        views.feature,          name='feature'),
    path('careers/',        views.careers,          name='careers'),
    path('training/',       views.training,         name='training'),
    path('training/<int:pk>/', views.training_detail, name='training_detail'),  # NEW

    # ── Internship application submit ─────────────────────────────
    path('apply/', views.submit_internship, name='submit_internship'),

    # ── Admin Auth ────────────────────────────────────────────────
    path('myadmin/login/',  views.admin_login,      name='admin_login'),
    path('myadmin/logout/', views.admin_logout,     name='admin_logout'),

    # ── Admin Dashboard ───────────────────────────────────────────
    path('myadmin/',        views.admin_dashboard,  name='admin_dashboard'),

    # ── Contacts ──────────────────────────────────────────────────
    path('myadmin/contacts/',                 views.admin_contacts,          name='admin_contacts'),
    path('myadmin/contacts/<int:pk>/',        views.admin_contact_detail,    name='admin_contact_detail'),
    path('myadmin/contacts/<int:pk>/delete/', views.admin_contact_delete,    name='admin_contact_delete'),

    # ── Applications ──────────────────────────────────────────────
    path('myadmin/applications/',                 views.admin_applications,       name='admin_applications'),
    path('myadmin/applications/<int:pk>/',        views.admin_application_detail, name='admin_application_detail'),
    path('myadmin/applications/<int:pk>/delete/', views.admin_application_delete, name='admin_application_delete'),

    # ── Vacancies ─────────────────────────────────────────────────
    path('myadmin/vacancies/',                views.admin_vacancies,       name='admin_vacancies'),
    path('myadmin/vacancies/create/',         views.admin_vacancy_create,  name='admin_vacancy_create'),
    path('myadmin/vacancies/<int:pk>/edit/',  views.admin_vacancy_edit,    name='admin_vacancy_edit'),
    path('myadmin/vacancies/<int:pk>/delete/',views.admin_vacancy_delete,  name='admin_vacancy_delete'),

    # ── Team Members ──────────────────────────────────────────────
    path('myadmin/team/',                views.admin_team_members,       name='admin_team_members'),
    path('myadmin/team/create/',         views.admin_team_member_create, name='admin_team_member_create'),
    path('myadmin/team/<int:pk>/edit/',  views.admin_team_member_edit,   name='admin_team_member_edit'),
    path('myadmin/team/<int:pk>/delete/',views.admin_team_member_delete, name='admin_team_member_delete'),

    # ── Workspace Images ──────────────────────────────────────────
    path('myadmin/workspace/',                views.admin_workspace_images,       name='admin_workspace_images'),
    path('myadmin/workspace/create/',         views.admin_workspace_image_create, name='admin_workspace_image_create'),
    path('myadmin/workspace/<int:pk>/edit/',  views.admin_workspace_image_edit,   name='admin_workspace_image_edit'),
    path('myadmin/workspace/<int:pk>/delete/',views.admin_workspace_image_delete, name='admin_workspace_image_delete'),

    # ── Training Programs ─────────────────────────────────────────  NEW
    path('myadmin/training/',                views.admin_training_programs,       name='admin_training_programs'),
    path('myadmin/training/create/',         views.admin_training_program_create, name='admin_training_program_create'),
    path('myadmin/training/<int:pk>/edit/',  views.admin_training_program_edit,   name='admin_training_program_edit'),
    path('myadmin/training/<int:pk>/delete/',views.admin_training_program_delete, name='admin_training_program_delete'),
    path('myadmin/activity/',                views.admin_activity_images,       name='admin_activity_images'),
path('myadmin/activity/create/',         views.admin_activity_image_create, name='admin_activity_image_create'),
path('myadmin/activity/<int:pk>/edit/',  views.admin_activity_image_edit,   name='admin_activity_image_edit'),
path('myadmin/activity/<int:pk>/delete/',views.admin_activity_image_delete, name='admin_activity_image_delete'),
]
