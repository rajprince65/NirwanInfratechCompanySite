from django.urls import path
from . import views

urlpatterns = [
    # ── Frontend (unchanged) ──────────────────────────
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('detail/', views.detail, name='detail'),
    path('feature/', views.feature, name='feature'),
    path('careers/', views.careers, name='careers'),
    path('training/', views.training, name='training'),

    # ── Internship application submit ─────────────────
    path('apply/', views.submit_internship, name='submit_internship'),

    # ── Admin Auth ────────────────────────────────────
    path('myadmin/login/', views.admin_login, name='admin_login'),
    path('myadmin/logout/', views.admin_logout, name='admin_logout'),

    # ── Admin Dashboard ───────────────────────────────
    path('myadmin/', views.admin_dashboard, name='admin_dashboard'),

    # ── Contacts ──────────────────────────────────────
    path('myadmin/contacts/', views.admin_contacts, name='admin_contacts'),
    path('myadmin/contacts/<int:pk>/', views.admin_contact_detail, name='admin_contact_detail'),
    path('myadmin/contacts/<int:pk>/delete/', views.admin_contact_delete, name='admin_contact_delete'),

    # ── Applications ──────────────────────────────────
    path('myadmin/applications/', views.admin_applications, name='admin_applications'),
    path('myadmin/applications/<int:pk>/', views.admin_application_detail, name='admin_application_detail'),
    path('myadmin/applications/<int:pk>/delete/', views.admin_application_delete, name='admin_application_delete'),

    # ── Vacancies ─────────────────────────────────────
    path('myadmin/vacancies/', views.admin_vacancies, name='admin_vacancies'),
    path('myadmin/vacancies/create/', views.admin_vacancy_create, name='admin_vacancy_create'),
    path('myadmin/vacancies/<int:pk>/edit/', views.admin_vacancy_edit, name='admin_vacancy_edit'),
    path('myadmin/vacancies/<int:pk>/delete/', views.admin_vacancy_delete, name='admin_vacancy_delete'),
]
