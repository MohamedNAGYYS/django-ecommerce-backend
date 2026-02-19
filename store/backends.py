from myapp.models import Users
from rest_framework import permissions


class IsAdminUserRole(permissions.BasePermission):
    def has_permission(self, request,view):
        
        # Return True if user is authenticated and is already an admin.
        return (request.user.is_authenticated and request.user.role==Users.RoleChocies.ADMIN)
    
