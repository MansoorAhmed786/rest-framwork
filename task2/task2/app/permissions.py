# from rest_framework import permissions

# class IsManagerOrReadOnly(permissions.BasePermission):
#     def has_permission(self, request, view):
#         pass
#         # if request.method in permissions.SAFE_METHODS:
#         #     return True
#         # return request.user and request.user.is_authenticated

#     def has_object_permission(self, request, view, obj):
#         pass
#         # if request.method in permissions.SAFE_METHODS:
#         #     return True
#         # return obj.manager == request.user
