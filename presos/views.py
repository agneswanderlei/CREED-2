from django.urls import reverse_lazy
from django.views.generic import (
    ListView, CreateView, DetailView, UpdateView, DeleteView
)
from . import models
from .forms import PresosForm
from django.contrib.auth.mixins import (
    LoginRequiredMixin
)


class PresosList(LoginRequiredMixin, ListView):
    model = models.Presos
    template_name = 'presos_list.html'
    context_object_name = 'presos'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        number_doc = self.request.GET.get('number_doc')
        postos = self.request.GET.get('posto')
        states = self.request.GET.get('estado')
        institutions = self.request.GET.get('instituicao')

        if name:
            queryset = queryset.filter(name_full__icontains=name)

        if number_doc:
            queryset = queryset.filter(number_doc__exact=number_doc)

        if postos:
            queryset = queryset.filter(posto_grad__id=postos)

        if states:
            queryset = queryset.filter(state_origin__id=states)

        if institutions:
            queryset = queryset.filter(institutions__id=institutions)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['postos'] = models.PostGrad.objects.all()
        context['estados'] = models.States.objects.all()
        context['instituicoes'] = models.Institution.objects.all()   
        context['form'] = PresosForm()     
        return context


class PresosCreate(CreateView):
    model = models.Presos
    template_name = 'Presos_create.html'
    form_class = PresosForm
    success_url = reverse_lazy('presos_list')

    def form_valid(self, form):
        # Aqui adicionamos o usuário logado no campo modified_by
        form.instance.modified_by = self.request.user
        return super().form_valid(form)

    


class PresosDetail(DetailView):
    model = models.Presos
    template_name = 'presos_detail.html'


class PresosUpdate(UpdateView):
    model = models.Presos
    template_name = 'presos_update.html'
    form_class = PresosForm
    success_url = reverse_lazy('presos_list')

    def form_valid(self, form):
        # Aqui adicionamos o usuário logado no campo modified_by
        form.instance.modified_by = self.request.user
        return super().form_valid(form)

    

class PresosDelete(DeleteView):
    model = models.Presos
    template_name = 'presos_delete.html'
    success_url = reverse_lazy('presos_list')
