from django.contrib import admin
from .models import User, Category, Complaint, Response, Notification, Feedback

# Register your models here to make them visible in the admin panel.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Complaint)
admin.site.register(Response)
admin.site.register(Notification)
admin.site.register(Feedback)