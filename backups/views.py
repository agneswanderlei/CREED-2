from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, CreateView, DetailView, UpdateView, DeleteView
)
from . import models
from presos.models import Presos, teste
from . import forms
from django.contrib.auth.mixins import (
    LoginRequiredMixin
)
l_name_presos = []

class OficiosCreate(CreateView):
    model = models.Oficios
    form_class = forms.OficiosForm
    template_name = 'oficios_create.html'
    success_url = reverse_lazy('oficios_list.html')


class OficiosList(ListView):
    model = models.Oficios
    template_name = 'oficios_list.html'
    context_object_name = 'oficios'


def list_presos(request):
    n_pront = request.POST.get('n_prontuario')
    if n_pront:
        presos = Presos.objects.filter(number_doc=n_pront)[0]
        context = {
            'presosx': presos
        }
    else:
        presos = ""
        context = {}
    return render(request, 'partials/result_preso.html', context)


def add_presosx(request):
    
    n_pront = request.POST.get('n_prontuario')
    l_name_presos.append(n_pront)
    print(l_name_presos)
    if n_pront:
        presos = Presos.objects.filter(number_doc=n_pront)[0]
        context = {
            'presosnamex': presos
        }
        print(context)
    else:
        presos = ""
        context = {}
    
    print(presos)
    return render(request, 'partials/list_add_presos.html', context)
