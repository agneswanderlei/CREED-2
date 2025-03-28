from django.shortcuts import render
from django.views.generic import ListView, DetailView
from oficios.models import Oficios
from django.shortcuts import get_object_or_404, render
from presos.models import Presos


def relatoriohome(request):
    presos = Presos.objects.all()
    return render(request, 'relatorio_index.html',  {'preso': presos})


def presos_detail(request, pk):
    naa = request.GET.get('n_pront')
    print(f'number doc {naa}')
    # Busca o preso pelo número do documento (PK)
    preso = get_object_or_404(Presos, pk=pk)
    
    # Obtém todos os ofícios relacionados ao preso
    oficios = preso.oficioss.all()  # Acessa a relação ManyToMany usando o `related_name` definido no model Oficios

    # Renderiza o template parcial com os dados do preso e seus ofícios
    return render(request, 'partials/presos_detail.html', {
        'preso': preso,
        'oficios': oficios,
    })


def presos_detail2(request):
    n_pront = request.GET.get('n_pront')
    
    n_oficio = request.GET.get('n_oficio')
    n_sei = request.GET.get('n_sei')
    date_send1 = request.GET.get('date_send1')
    date_send2 = request.GET.get('date_send2')
    tipo_prisao = request.GET.get('tipo_prisao')

    presos = Presos.objects.filter(number_doc__exact=n_pront).get('sector')
    # oficios = presos.oficioss.all()

    print(f'teste {presos}')

    return render(request, 'partials/presos_detail.html')

class RelatorioList(ListView):
    model = Oficios
    template_name = 'partials\presos_detail.html'
    context_object_name = 'oficios'

    def get_queryset(self):
        queryset = super().get_queryset()
        n_oficio = self.request.GET.get('n_oficio')
        n_sei = self.request.GET.get('n_sei')
        date_send1 = self.request.GET.get('date_send1')
        date_send2 = self.request.GET.get('date_send2')
        tipo_prisao = self.request.GET.get('tipo_prisao')
        n_pront = self.request.GET.get('n_pront')


        if n_oficio:
            queryset = queryset.filter(n_oficios__icontains=n_oficio)
        if n_sei:
            queryset = queryset.filter(n_sei__icontains=n_sei)
        if date_send1:
            queryset = queryset.filter(date_send__gte=date_send1)
        if date_send2:
            queryset = queryset.filter(date_send__lte=date_send2)
        if tipo_prisao:
            queryset = queryset.filter(tipo_prisao__iexact=tipo_prisao)
        if n_pront:
            queryset = queryset.filter(n_pront_presos__number_doc__exact=n_pront)

        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        n_pront = self.request.GET.get('n_pront')

        # Verifica se o número do prontuário foi fornecido e obtém os dados do preso
        if n_pront:
            context['preso'] = Presos.objects.filter(number_doc__exact=n_pront).first()
        else:
            context['preso'] = None

        return context