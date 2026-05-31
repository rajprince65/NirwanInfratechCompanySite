from django.db import models


class ContactSubmission(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Contact Submission'
        verbose_name_plural = 'Contact Submissions'

    def __str__(self):
        return f"{self.name} – {self.submitted_at.strftime('%d %b %Y')}"


class InternshipApplication(models.Model):
    POSITION_CHOICES = [
        ('Web Development Intern', 'Web Development Intern'),
        ('Mobile App Development Intern', 'Mobile App Development Intern'),
        ('Digital Marketing Intern', 'Digital Marketing Intern'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewing', 'Reviewing'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    position = models.CharField(max_length=100, choices=POSITION_CHOICES)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    program = models.CharField(max_length=100, blank=True)
    institution = models.CharField(max_length=200, blank=True)
    skills = models.CharField(max_length=300, blank=True)
    portfolio = models.URLField(blank=True)
    motivation = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Internship Application'
        verbose_name_plural = 'Internship Applications'

    def __str__(self):
        return f"{self.full_name} – {self.position}"


class InternshipVacancy(models.Model):
    title = models.CharField(max_length=200)
    department = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    requirements = models.TextField(blank=True)
    duration = models.CharField(max_length=100, blank=True, help_text="e.g. 3 months")
    stipend = models.CharField(max_length=100, blank=True, help_text="e.g. Rs 5,000/month")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Internship Vacancy'
        verbose_name_plural = 'Internship Vacancies'

    def __str__(self):
        return self.title
