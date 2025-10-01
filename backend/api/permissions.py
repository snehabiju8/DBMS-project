# api/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Allows full access to Admin users, but read-only access to others.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.role == 'Admin'

class IsStaffUser(BasePermission):
    """
    Allows access only to Staff or Admin users.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (request.user.role == 'Staff' or request.user.role == 'Admin')

class IsOwnerOrStaff(BasePermission):
    """
    Allows owners of an object or staff/admin to edit it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        # For a Complaint object, the owner is the 'user' field
        is_owner = obj.user == request.user
        is_staff_or_admin = request.user.role in ['Staff', 'Admin']
        return is_owner or is_staff_or_admin