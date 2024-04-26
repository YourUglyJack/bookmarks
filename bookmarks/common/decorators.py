from django.http import HttpResponseBadRequest
from functools import wraps


def ajax_required(f):
    @wraps(f)
    def wrap(request, *args, **kwargs):
        if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)

    return wrap
