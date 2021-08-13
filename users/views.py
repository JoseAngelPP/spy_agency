from django.db.models import manager
from django.db.models.query_utils import Q
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from users.forms import CreateCustomUserForm, UpdateCustomUserForm
from users.models import Boss, CustomUser, ManagerHitman
from django.contrib.auth import REDIRECT_FIELD_NAME, login, logout
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic.base import RedirectView, TemplateView
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from urllib.parse import urlparse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.

class HomeView(TemplateView):
    template_name = "home.html"

class LoginView(FormView):
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'login.html'

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        """
        Returns the view with csrf protection and cache disabled.
        """
        return super(LoginView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        If user is already logged in redirect him with function
        """
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super(LoginView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        """
        The user has provided valid credentials (this was checked in AuthenticationForm.is_valid()). So now we
        """
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        """
        Defines the success url to redirect to
        """
        if self.success_url:
            redirect_to = self.success_url
        else:
            redirect_to = self.request.REQUEST.get(
                self.redirect_field_name, '')

        netloc = urlparse(redirect_to)[1]
        if not redirect_to:
            redirect_to = settings.LOGIN_REDIRECT_URL
        # Security check -- don't allow redirection to a different host.
        elif netloc and netloc != self.request.get_host():
            redirect_to = settings.LOGIN_REDIRECT_URL
        return redirect_to

    def set_test_cookie(self):
        """
        Sets a cookie to ensure login can be saved.
        """
        self.request.session.set_test_cookie()

    def check_and_delete_test_cookie(self):
        """
        Check if the test cookie works and deletes it.
        """
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()
            return True
        return False

    def post(self, request, *args, **kwargs):
        """
        Same as django.views.generic.edit.ProcessFormView.post(), but adds test cookie stuff
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            self.check_and_delete_test_cookie()
            return self.form_valid(form)
        else:
            self.set_test_cookie()
            return self.form_invalid(form)


class LogoutView(RedirectView):
    url = '/login'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class CreateCustomUserView(CreateView):
    model = CustomUser
    form_class = CreateCustomUserForm
    template_name = 'customuser_form.html'

    def get_context_data(self, **kwargs):
        context = super(CreateCustomUserView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        return super(CreateCustomUserView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('users:login')


class UpdateCustomUserView(PermissionRequiredMixin, UpdateView):
    permission_required = 'users.change_customuser'
    model = CustomUser
    form_class = UpdateCustomUserForm
    template_name = 'update_user_form.html'

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""

        kwargs = super(UpdateCustomUserView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['managers'] = Boss.objects.filter(rol=1)
        context['hitman'] = get_object_or_404(CustomUser, pk=self.kwargs.pop('pk'))
        if context['hitman'].rol == 0:
            manager = CustomUser.objects.get(id=context['hitman'].id).lackeys.all().exclude(rol=2)
            context['manager'] = manager.last() if manager else []
        else:
            lackeys = Boss.objects.get(id=context['hitman'].id).lackeys.all()
            context['lackeys'] = lackeys if lackeys else []
        return context

    def form_valid(self, form):
        updated_user = form.instance
        current_manager = updated_user.lackeys.all().exclude(rol=2)
        current_manager = current_manager[0] if current_manager else None
        new_manager = Boss.objects.get(id=self.request.POST['manager']) if 'manager' in self.request.POST else None
        if current_manager != new_manager and self.request.user.rol == 2:
            updated_user.lackeys.remove(current_manager)
            updated_user.lackeys.add(new_manager)
        return super(UpdateCustomUserView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('users:hitmen_list')


# class DetailCustomUserView(PermissionRequiredMixin, DetailView):
#     permission_required = 'users.view_customuser'
#     model = CustomUser
#     template_name = 'user_detail.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['user'] = self.request.user
#         context['hitman'] = get_object_or_404(CustomUser, pk=self.kwargs.pop('pk'))
#         if context['hitman'].rol == 0:
#             manager = CustomUser.objects.get(id=context['hitman'].id).lackeys.all().exclude(rol=2)
#             context['manager'] = manager.last() if manager else []
#         else:
#             lackeys = Boss.objects.get(id=context['hitman'].id).lackeys.all()
#             context['lackeys'] = lackeys if lackeys else []
#         return context


class ListHitmenView(PermissionRequiredMixin, ListView):
    permission_required = 'users.view_customuser'
    model = CustomUser
    template_name = 'hitmen_list.html'

    def get_context_data(self, **kwargs):
        context = super(ListHitmenView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.rol == 1:
            context['hitmen'] = Boss.objects.get(id=user.id).lackeys.all()
        elif user.rol == 2:
            context['hitmen'] = CustomUser.objects.all()
        return context