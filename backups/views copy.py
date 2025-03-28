# esse código ta adicionando duplicado

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
    if n_pront:
        preso_name = Presos.objects.filter(number_doc=n_pront)[0]

        testemodel = teste(name=preso_name)
        testemodel.save()
        dbteste = teste.objects.all()
        context = {
            'presosnamex': dbteste
        }
        print('add', context)
        context.clear()
    else:
        preso_name = ""
        context = {}
    
    return render(request, 'partials/list_add_presos.html', context)


class Delete_presosx(DeleteView):
    model = teste
    template_name = 'partials/list_add_presos.html'
    context_object_name = 'presosnamex'
    success_url = reverse_lazy('listaddpresosx')
    print('delete', context_object_name)

class list_presosx(ListView):
    model = teste
    template_name = 'partials/list_add_presos.html'
    context_object_name = 'presosnamex'
    print('list', context_object_name)