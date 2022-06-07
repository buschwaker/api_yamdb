from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == 'admin'
        return False


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == 'moderator'
        return False


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        elif request.user.is_authenticated:
            return request.user.role == 'admin'
        return False


class IsAuthorModeratorAdmin(BasePermission):
    """Права доступа: автора, модератора и администратора."""
    message = ('Вы не являетесь автором, модератором или администратором.')

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif obj.author == request.user:
            return True
        elif (request.user.is_authenticated
              and request.user.role == 'moderator'):
            return True
        elif (request.user.is_authenticated
              and request.user.role == 'admin'):
            return True
