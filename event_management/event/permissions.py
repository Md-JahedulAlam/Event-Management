from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # return request.user.is_authenticated and request.user.is_staff
        return (
            request.user.is_authenticated
            and request.user.role == 'admin'
            and request.user.is_staff
        )