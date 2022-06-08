from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == 'admin'
        )


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == 'moderator'
        )


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_authenticated
            and request.user.role == 'admin'
        )


class IsAuthorModeratorAdmin(BasePermission):
    """Права доступа: автора, модератора и администратора."""
    message = 'Вы не являетесь автором, модератором или администратором.'

    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS
            or ((request.user and request.user.is_authenticated)
                and request.user.role == 'admin'
                or request.user.role == 'moderator'
                or obj.author == request.user)
        )
