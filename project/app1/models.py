from django.db import models


# ─────────────────────────────────────────────
# CONTACT MODEL
# ─────────────────────────────────────────────
class ContactSubmission(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    # optional field (FIXED)
    alternate_phone = models.CharField(max_length=15, null=True, blank=True)

    message = models.TextField()

    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Contact Submission'
        verbose_name_plural = 'Contact Submissions'

    def __str__(self):
        return f"{self.name} – {self.submitted_at.strftime('%d %b %Y')}"


# ─────────────────────────────────────────────
# INTERNSHIP APPLICATION MODEL
# ─────────────────────────────────────────────
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

    cv_file = models.FileField(upload_to='cvs/', blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Internship Application'
        verbose_name_plural = 'Internship Applications'

    def __str__(self):
        return f"{self.full_name} – {self.position}"

    def cv_filename(self):
        if self.cv_file:
            return self.cv_file.name.split('/')[-1]
        return None


# ─────────────────────────────────────────────
# INTERNSHIP VACANCY MODEL
# ─────────────────────────────────────────────
class InternshipVacancy(models.Model):

    CATEGORY_CHOICES = [
        ('dev', 'Development'),
        ('design', 'Design'),
        ('marketing', 'Marketing'),
    ]

    ICON_CHOICES = [
        ('web', 'Web (blue)'),
        ('mobile', 'Mobile (green)'),
        ('marketing', 'Marketing (amber)'),
        ('design', 'Design (pink)'),
    ]

    title = models.CharField(max_length=200)
    department = models.CharField(max_length=100, blank=True)
    description = models.TextField()
    requirements = models.TextField(blank=True)

    duration = models.CharField(max_length=100, blank=True)
    stipend = models.CharField(max_length=100, blank=True)

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='dev'
    )

    icon_type = models.CharField(
        max_length=20,
        choices=ICON_CHOICES,
        default='web'
    )

    location = models.CharField(
        max_length=100,
        blank=True,
        default='Remote / Biratnagar'
    )

    openings = models.PositiveIntegerField(default=1)

    skills_tags = models.CharField(
        max_length=300,
        blank=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Internship Vacancy'
        verbose_name_plural = 'Internship Vacancies'

    def __str__(self):
        return self.title

    def skills_list(self):
        if not self.skills_tags:
            return []
        return [s.strip() for s in self.skills_tags.split(',') if s.strip()]


# ─────────────────────────────────────────────
# TEAM MEMBER MODEL
# ─────────────────────────────────────────────
class TeamMember(models.Model):
    name        = models.CharField(max_length=200)
    post        = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    github      = models.URLField(blank=True)
    linkedin    = models.URLField(blank=True)
    email       = models.EmailField(blank=True)
    photo       = models.ImageField(upload_to='team/', blank=True, null=True)
    is_founder  = models.BooleanField(default=False)
    order       = models.PositiveIntegerField(default=0)
    is_active   = models.BooleanField(default=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Team Member'
        verbose_name_plural = 'Team Members'

    def __str__(self):
        return f"{self.name} – {self.post}"

    def photo_url(self):
        if self.photo:
            return self.photo.url
        return None


# ─────────────────────────────────────────────
# WORKSPACE IMAGE MODEL
# ─────────────────────────────────────────────
class WorkspaceImage(models.Model):
    title       = models.CharField(max_length=200, blank=True, help_text="Optional caption shown on hover")
    image       = models.ImageField(upload_to='workspace/')
    order       = models.PositiveIntegerField(default=0, help_text="Lower = appears first")
    is_active   = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'uploaded_at']
        verbose_name = 'Workspace Image'
        verbose_name_plural = 'Workspace Images'

    def __str__(self):
        return self.title or f"Workspace Image #{self.pk}"

    def image_url(self):
        if self.image:
            return self.image.url
        return None


# ─────────────────────────────────────────────
# TRAINING PROGRAM MODEL
# ─────────────────────────────────────────────
class TrainingProgram(models.Model):

    TRACK_CHOICES = [
        ('flagship', 'Flagship Program'),
        ('dev',      'Dev Track'),
        ('design',   'Design Track'),
        ('data',     'Data Track'),
    ]

    ICON_CHOICES = [
        ('mobile-alt',  'Mobile'),
        ('globe',       'Web'),
        ('paint-brush', 'Design'),
        ('python',      'Python / Data'),
        ('code',        'Code / General'),
        ('database',    'Database'),
        ('robot',       'AI / ML'),
    ]

    # ── Basic info ─────────────────────────────
    title       = models.CharField(max_length=200)
    subtitle    = models.CharField(max_length=300, blank=True,
                                   help_text="Short tech stack line, e.g. React Native · Next.js · Node.js")
    description = models.TextField(help_text="Main description shown on the card and detail page")
    track       = models.CharField(max_length=20, choices=TRACK_CHOICES, default='dev')
    icon        = models.CharField(max_length=40, choices=ICON_CHOICES, default='code',
                                   help_text="Font Awesome icon name (without 'fa-')")
    is_featured = models.BooleanField(default=False,
                                      help_text="Featured programs are highlighted (dark header style)")

    # ── Meta ───────────────────────────────────
    duration       = models.CharField(max_length=100, blank=True, help_text="e.g. 16 Weeks")
    batch_size     = models.CharField(max_length=50,  blank=True, default='Max 10 per Batch')
    mode           = models.CharField(max_length=100, blank=True, default='Offline / Online')
    certificate    = models.BooleanField(default=True)
    career_support = models.BooleanField(default=False)
    price_label    = models.CharField(max_length=200, blank=True, default='Enrollment Fee — Contact Us',
                                      help_text="Shown in card footer, e.g. 'Rs. 25,000' or 'Contact Us'")
    whatsapp_text  = models.CharField(max_length=300, blank=True,
                                      help_text="Pre-filled WhatsApp message for Enroll button")

    # ── Skills shown as tags ───────────────────
    skills_tags = models.CharField(max_length=500, blank=True,
                                   help_text="Comma-separated skill tags, e.g. React Native, Next.js, Node.js")

    # ── Syllabus weeks (stored as JSON) ────────
    # Format: [{"week": "Week 1–2", "title": "Foundations", "topics": ["HTML", "CSS", "JS Basics"]}]
    syllabus_json = models.TextField(
        blank=True,
        default='[]',
        help_text=(
            'JSON array of week objects. Each object must have: '
            '"week" (label), "title" (week title), "topics" (array of strings). '
            'Example: [{"week":"Week 1","title":"Foundations","topics":["HTML","CSS"]}]'
        )
    )

    # ── Additional rich content ────────────────
    who_should_join = models.TextField(blank=True,
                                       help_text="Who this program is for (plain text, one point per line)")
    requirements    = models.TextField(blank=True,
                                       help_text="Prerequisites / requirements (one per line)")
    outcomes        = models.TextField(blank=True,
                                       help_text="What students will be able to do after (one per line)")

    # ── Display control ────────────────────────
    order     = models.PositiveIntegerField(default=0, help_text="Lower = appears first")
    is_active = models.BooleanField(default=True)

    # ── Timestamps ─────────────────────────────
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Training Program'
        verbose_name_plural = 'Training Programs'

    def __str__(self):
        return self.title

    def skills_list(self):
        if not self.skills_tags:
            return []
        return [s.strip() for s in self.skills_tags.split(',') if s.strip()]

    def get_syllabus(self):
        """Return parsed syllabus list; empty list on error."""
        import json
        try:
            data = json.loads(self.syllabus_json or '[]')
            return data if isinstance(data, list) else []
        except (ValueError, TypeError):
            return []

    def track_label(self):
        return dict(self.TRACK_CHOICES).get(self.track, self.track)

# ─────────────────────────────────────────────
# ACTIVITY IMAGE MODEL
# ─────────────────────────────────────────────
class ActivityImage(models.Model):
    title       = models.CharField(max_length=200, blank=True, help_text="Optional caption shown on hover")
    image       = models.ImageField(upload_to='activity/')
    order       = models.PositiveIntegerField(default=0, help_text="Lower = appears first")
    is_active   = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'uploaded_at']
        verbose_name = 'Activity Image'
        verbose_name_plural = 'Activity Images'

    def __str__(self):
        return self.title or f"Activity Image #{self.pk}"

    def image_url(self):
        if self.image:
            return self.image.url
        return None