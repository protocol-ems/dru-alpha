from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow isAdmin of an object to edit it.
    Assumes the model instance has an `isAdmin` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.company == request.user.company and request.user.isAdmin == True


class IsSameCompanyOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        message = "you must be the owner of this document"
        return obj.company == request.user.company
