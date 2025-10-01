# api/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        USER = 'User', 'User'
        STAFF = 'Staff', 'Staff'
        ADMIN = 'Admin', 'Admin'

    # The default 'password' and 'email' fields are already in AbstractUser
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.USER)
    contact_no = models.CharField(max_length=15, null=True, blank=True)

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, null=False)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Complaint(models.Model):
    class Status(models.TextChoices):
        PENDING = 'Pending', 'Pending'
        ASSIGNED = 'Assigned', 'Assigned'
        IN_PROGRESS = 'In Progress', 'In Progress'
        RESOLVED = 'Resolved', 'Resolved'
        CLOSED = 'Closed', 'Closed'

    complaint_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=150, null=False)
    description = models.TextField(null=False)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_complaints', limit_choices_to={'role': User.Role.STAFF})
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Response(models.Model):
    response_id = models.AutoField(primary_key=True)
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='responses')
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, limit_choices_to={'role': User.Role.STAFF})
    comment_text = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    class Status(models.TextChoices):
        SENT = 'Sent', 'Sent'
        PENDING = 'Pending', 'Pending'

    notification_id = models.AutoField(primary_key=True)
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)

class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comments = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)