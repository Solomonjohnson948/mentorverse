from django.db import models
from django.contrib.auth.models import User


class Mentor(models.Model):
    name = models.CharField(max_length=100)
    expertise = models.CharField(max_length=150)
    bio = models.TextField()

    image = models.ImageField(
        upload_to='mentors/',
        blank=True,
        null=True
    )

    rating = models.DecimalField(max_digits=2, decimal_places=1, default=4.5)
    reviews = models.PositiveIntegerField(default=0)
    company = models.CharField(max_length=100, blank=True, null=True)
    price = models.PositiveIntegerField(default=0, help_text="Session price in Dollars")
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Booking(models.Model):

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Declined', 'Declined'),
        ('Completed', 'Completed'),
        ('Refunded', 'Refunded'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('Unpaid', 'Unpaid'),
        ('Paid', 'Paid'),
        ('Refunded', 'Refunded'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)

    customer_name = models.CharField(max_length=100)
    email = models.EmailField()

    date = models.DateField()
    time = models.TimeField()

    reason = models.TextField(
        blank=True,
        null=True,
        help_text="Reason for booking this mentorship session"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='Unpaid'
    )

    admin_note = models.TextField(
        blank=True,
        null=True,
        help_text="Optional note from admin when confirming, declining or refunding"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} → {self.mentor.name} ({self.status})"


class Profile(models.Model):
    FIELD_CHOICES = [
        ('Software Engineering', 'Software Engineering'),
        ('AI', 'AI'),
        ('Cybersecurity', 'Cybersecurity'),
        ('UI/UX', 'UI/UX'),
        ('Data Science', 'Data Science'),
        ('Cloud Computing', 'Cloud Computing'),
    ]

    GOAL_CHOICES = [
        ('Get Internship', 'Get Internship'),
        ('Build Startup', 'Build Startup'),
        ('Learn New Skill', 'Learn New Skill'),
        ('Career Growth', 'Career Growth'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    field = models.CharField(max_length=50, choices=FIELD_CHOICES)
    goal = models.CharField(max_length=50, choices=GOAL_CHOICES)

    def __str__(self):
        return self.full_name


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)

    rating = models.PositiveIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} reviewed {self.mentor.name}"