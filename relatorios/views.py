from django.shortcuts import render
from oficios.models import Oficios
from presos.models import Presos

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from datetime import datetime


def relatoriohome(request):
    presos = Presos.objects.all()
    return render(request, 'relatorio_index.html',  {'preso': presos})

def relatorio_detail(request):
    if request.method == 'POST':
        # Obtém os dados dos campos do formulário
        n_pront = request.POST.get('n_pront')  # Nº do Prontuário
        n_oficio = request.POST.getlist('n_oficio')  # IDs dos Ofícios selecionados (multi-select)
        n_sei = request.POST.get('n_sei')  # Nº SEI
        date_send1 = request.POST.get('date_send1')  # Data Inicial
        date_send2 = request.POST.get('date_send2')  # Data Final
        tipo_prisao = request.POST.get('tipo_prisao')  # Tipo de Prisão

        # Inicializa o queryset com todos os ofícios
        oficios = Oficios.objects.all()

        # Aplica os filtros dinamicamente
        if n_pront:
            oficios = oficios.filter(n_pront_presos__number_doc__exact=n_pront)

        if n_oficio:
            oficios = oficios.filter(id__in=n_oficio)  # Filtra pelos IDs dos ofícios selecionados

        if n_sei:
            oficios = oficios.filter(n_sei__icontains=n_sei)  # Busca parcial pelo Nº SEI

        if date_send1 and date_send2:
            oficios = oficios.filter(date_send__range=[date_send1, date_send2])  # Filtra por intervalo de datas

        elif date_send1:  # Apenas data inicial
            oficios = oficios.filter(date_send__gte=date_send1)

        elif date_send2:  # Apenas data final
            oficios = oficios.filter(date_send__lte=date_send2)

        if tipo_prisao:
            oficios = oficios.filter(tipo_prisao__exact=tipo_prisao)  # Filtra pelo tipo de prisão

        # Busca o preso correspondente (se necessário)
        presos = Presos.objects.filter(number_doc__exact=n_pront).first() if n_pront else None


        # Renderiza os dados filtrados para o template
        return render(request, 'partials/presos_detail.html', {
            'preso': presos,  # Passa o preso para o contexto
            'oficios': oficios  # Passa os ofícios filtrados
        })

    return render(request, 'partials/presos_detail.html')

# def relatorio_detail(request):
#     if request.method == 'POST':
#         n_pront = request.POST.get('n_pront')  # Obtém o Nº do Prontuário
#         presos = Presos.objects.filter(number_doc__exact=n_pront).first()  # Busca o preso correspondente
        
#         # Busca os ofícios relacionados ao preso
#         oficios = Oficios.objects.filter(n_pront_presos__number_doc__exact=n_pront)

#         print(f'Preso: {presos}')
#         print(f'Ofícios: {oficios}')

#         return render(request, 'partials/presos_detail.html', {
#             'preso': presos,  # Passa o preso para o contexto
#             'oficios': oficios  # Passa os ofícios associados
#         })

#     return render(request, 'partials/presos_detail.html')



def get_oficios(request):
    n_pront = request.GET.get("n_pront")
    if n_pront:
        # Filtra os ofícios vinculados ao número de prontuário
        oficios = Oficios.objects.filter(n_pront_presos__number_doc=n_pront)
        return render(request, "partials/oficios_options.html", {"oficios": oficios})
    return render(request, "partials/oficios_options.html", {"oficios": []})




def gerar_pdf(request):
    if request.method == 'GET':
        n_pront = request.GET.get('n_pront')
        print(f'teste {n_pront}')
        
        # Configura o tipo de arquivo como PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="meu_relatorio.pdf"'

        # Cria o canvas para desenhar o PDF
        c = canvas.Canvas(response, pagesize=letter)

        # Define o tamanho da página
        largura, altura = letter
        data = datetime.now().strftime("%d/%m/%Y")
        # Obtém o número do prontuário do formulário
        # n_pront = request.GET.get('n_pront')
        print(n_pront)

        # Busca o preso no banco de dados
        preso = Presos.objects.filter(number_doc=n_pront).first()
        nome_preso = preso.name_full if preso else "Preso não encontrado"


        # Adiciona um título no topo do PDF
        c.setFont("Helvetica-Bold", 14)
        c.drawString(30, altura - 30, "RELATÓRIO DE PRISIONEIROS")
        c.setFont("Helvetica", 10)
        c.drawString(30, altura - 50, "Gerado por: Sistema de Gestão Prisional")
        c.drawString(30, altura - 65, f"Data: {data}")  # Pode ser dinâmico


        # Adiciona texto no PDF
        c.setFont("Helvetica-Bold", 12)
        c.drawString(30, altura - 100, "Ficha do prisioneiro")

        # Adiciona uma linha horizontal
        c.line(30, altura - 110, largura - 30, altura - 110)
        c.drawString(30, altura - 120, f"Nome do preso: {nome_preso}")  # Pode ser dinâmico
        # Finaliza o PDF
        c.save()

    return response
