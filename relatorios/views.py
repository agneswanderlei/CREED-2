from django.shortcuts import render
from django.views.generic import ListView, DetailView
from oficios.models import Oficios
from django.shortcuts import get_object_or_404, render
from presos.models import Presos


def relatoriohome(request):
    presos = Presos.objects.all()
    return render(request, 'relatorio_index.html',  {'preso': presos})


def relatorio_detail(request):
    if request.method == 'POST':
        n_pront = request.POST.get('n_pront')  # Obtém o Nº do Prontuário
        presos = Presos.objects.filter(number_doc__exact=n_pront).first()  # Busca o preso correspondente
        
        # Busca os ofícios relacionados ao preso
        oficios = Oficios.objects.filter(n_pront_presos__number_doc__exact=n_pront)

        print(f'Preso: {presos}')
        print(f'Ofícios: {oficios}')

        return render(request, 'partials/presos_detail.html', {
            'preso': presos,  # Passa o preso para o contexto
            'oficios': oficios  # Passa os ofícios associados
        })

    return render(request, 'partials/presos_detail.html')
