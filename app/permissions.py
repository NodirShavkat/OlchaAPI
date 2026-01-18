from rest_framework.permissions import BasePermission
from datetime import timedelta
from django.utils import timezone


class UpdatePermission(BasePermission):
    # def has_permission(self, request, view):
        
    #     weekday = datetime.today().weekday()
        
    #     return weekday >= 0 and weekday <= 4
    
    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True


class UpdateWithinHoursPermission(BasePermission):
    allowed_hours = 4

    def has_object_permission(self, request, view, obj):
        if request.method not in ['PUT', 'PATCH']:
            return True

        created_field = getattr(obj, 'created_at', None) or getattr(obj, 'created', None)
        if created_field is None:
            return True

        time_diff = timezone.now() - created_field
        return time_diff <= timedelta(hours=self.allowed_hours)

