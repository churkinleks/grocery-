from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsStaffOrReadOnly(BasePermission):

    def has_permission(self, request, view) -> bool:
        if request.method in SAFE_METHODS:
            return True
        if request.user and request.user.is_staff:
            return True
        return False
