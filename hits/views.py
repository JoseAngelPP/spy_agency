from django.views.generic.detail import DetailView
from users.models import Boss, CustomUser, ManagerHitman
from django.urls import reverse_lazy
from hits.models import Hit
from hits.forms import CreateHitForm
from django.shortcuts import get_object_or_404, render
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.views.generic.list import ListView
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.contrib.auth.mixins import PermissionRequiredMixin

# Create your views here.

class CreateHitView(PermissionRequiredMixin, CreateView):
    permission_required = 'hits.add_hit'
    model = Hit
    form_class = CreateHitForm
    template_name = 'hit_form.html'

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""

        kwargs = super(CreateHitView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CreateHitView, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super(CreateHitView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('hits:hits_list')


class ListHitsView(ListView):
    model = Hit
    template_name = 'hits_list.html'

    def get_context_data(self, **kwargs):
        context = super(ListHitsView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.rol == 1:
            lackeys = Boss.objects.get(id=user.id).lackeys.all()
            context['hits'] = Hit.objects.filter(Q(hitman=user) | Q(hitman__in=lackeys))
        elif user.rol == 2:
            context['hits'] = Hit.objects.all()
        else:
            context['hits'] = Hit.objects.filter(hitman=user)
        
        return context


class UpdateHitView(UpdateView):
    model = Hit
    form_class = CreateHitForm
    template_name = 'hit_form.html'

    def get_form_kwargs(self):
        """ Passes the request object to the form class.
         This is necessary to only display members that belong to a given user"""

        kwargs = super(UpdateHitView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(UpdateHitView, self).get_context_data(**kwargs)
        context['hit'] = get_object_or_404(Hit, pk=self.kwargs.pop('pk'))
        return context

    def form_valid(self, form):
        return super(UpdateHitView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('hits:hits_list')


# class DetailHitView(FormView):

    # model = Hit
    # template_name = 'hit_detail.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     return context

    # def get_initial(self):
    #     # call super if needed
    #     return {'target_name': 1}