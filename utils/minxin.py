from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views import View
from django.utils.decorators import classonlymethod

class LoginRequiredMixin(TemplateView):
    @classonlymethod
    def as_view(cls, **initkwargs):
        print(cls.__name__)
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)