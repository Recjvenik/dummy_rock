from .models import School


class SchoolBrandingMiddleware:
    """
    Injects request.school for authenticated users who belong to a school.
    base.html can then show school logo in the sidebar when request.school.logo exists.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.school = None
        if request.user.is_authenticated:
            school_fk = getattr(request.user, 'school', None)
            if school_fk_id := getattr(request.user, 'school_id', None):
                try:
                    request.school = School.objects.get(pk=school_fk_id)
                except School.DoesNotExist:
                    pass
        return self.get_response(request)
