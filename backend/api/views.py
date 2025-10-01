# api/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import User, Category, Complaint, Response, Notification, Feedback
from .permissions import IsAdminOrReadOnly, IsOwnerOrStaff, IsStaffUser
from .serializers import (
    UserSerializer, CategorySerializer, ComplaintSerializer,
    ResponseSerializer, NotificationSerializer, FeedbackSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    Only Admins can access this.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and managing complaint categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class ComplaintViewSet(viewsets.ModelViewSet):
    """
    API endpoint for filing and tracking complaints.
    """
    queryset = Complaint.objects.all() # <-- THIS LINE WAS MISSING
    serializer_class = ComplaintSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrStaff]

    def get_queryset(self):
        """
        Admins/Staff see all complaints.
        Regular users only see their own.
        """
        if self.request.user.is_staff:
            return Complaint.objects.all()
        return Complaint.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Automatically set the user when a complaint is created."""
        serializer.save(user=self.request.user)

class ResponseViewSet(viewsets.ModelViewSet):
    """
    API endpoint for staff responses to complaints.
    """
    queryset = Response.objects.all()
    serializer_class = ResponseSerializer
    permission_classes = [IsStaffUser]

class NotificationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for user notifications.
    """
    queryset = Notification.objects.all() # <-- THIS LINE WAS MISSING
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Users can only see their own notifications.
        """
        return Notification.objects.filter(user=self.request.user)

class FeedbackViewSet(viewsets.ModelViewSet):
    """
    API endpoint for user feedback on resolved complaints.
    """
    queryset = Feedback.objects.all() # <-- THIS LINE WAS MISSING
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrStaff]

    def get_queryset(self):
        """
        Admins/Staff see all feedback.
        Regular users only see their own.
        """
        if self.request.user.is_staff:
            return Feedback.objects.all()
        return Feedback.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Automatically set the user when feedback is submitted."""
        serializer.save(user=self.request.user)