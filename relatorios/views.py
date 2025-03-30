from django.shortcuts import render
from oficios.models import Oficios
from presos.models import Presos

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from datetime import datetime
from reportlab.pdfbase.pdfmetrics import stringWidth



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
        # Obtém os dados:
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
        hora = datetime.now().strftime("%H:%M:%S")  # Formata a hora (horas:minutos:segundos)

        # n_pront = request.GET.get('n_pront')
        print(n_pront)

        # Busca o preso no banco de dados
        preso = Presos.objects.filter(number_doc=n_pront).first()
        prontuario = preso.number_doc if preso else None
        nome_preso = preso.name_full if preso else "Preso não encontrado"
        tipo_pront = preso.type_doc if preso else None
        funcao = preso.posto_grad if preso else None
        instituicao = preso.institutions if preso else None
        estado = preso.state_origin if preso else None
        setor = preso.sector if preso else None
        foto = preso.photo.path if preso and preso.photo else None
        
        # Adiciona a Imagem se existir
        if foto:
            try:
                c.drawImage(foto, 35, altura - 245, 125, 125)
            except Exception as e:
                c.drawString(30,altura - 125, f'Erro ao carregar a imagem {e}')
        else:
            c.drawString(30,altura - 125, 'Preso não possui foto.')



        # Adiciona um título no topo do PDF
        c.setFont("Helvetica-Bold", 14)
        c.drawString(30, altura - 30, "RELATÓRIO DE PRISIONEIROS")
        c.setFont("Helvetica", 10)
        c.drawString(30, altura - 50, "Gerado por: Sistema de Gestão Prisional")
        c.drawString(30, altura - 65, f"Data: {data}")  # Pode ser dinâmico
        c.drawString(30, altura - 75, f"Hora: {hora}")  # Pode ser dinâmico


        # Adiciona texto no PDF
        c.setFont("Helvetica-Bold", 12)
        c.drawString(30, altura - 105, "Ficha do prisioneiro")

        # Adiciona uma linha horizontal
        c.setStrokeColorRGB(0.5,0.5,0.5)
        # c.setFillColorRGB(0.5,0.5,0.5) #Define a cor do fundo
        c.roundRect(30,altura-250,550,140,3,) #Desenha o retangulo

        c.setFont("Helvetica", 12)
        # c.line(30, altura - 110, largura - 30, altura - 110)


        c.drawString(165, altura - 130, f"Prontuário:")  # Pode ser dinâmico
        c.drawString(165, altura - 150, f"Tipo de Prontuário:")  # Pode ser dinâmico
        c.drawString(165, altura - 170, f"Nome:")  # Pode ser dinâmico
        c.drawString(165, altura - 190, f"Função:")  # Pode ser dinâmico
        c.drawString(165, altura - 210, f"Setor:")  # Pode ser dinâmico
        c.drawString(165, altura - 230, f"Instituição:")  # Pode ser dinâmico
        c.drawString(int(stringWidth(f'Instituição: {instituicao}','Helvetica', 12)) + 175, altura - 230, f"Estado:")  # Pode ser dinâmico
        print(int(stringWidth('Prontuário','Helvetica', 12)))
        c.setFont("Helvetica-Bold", 12)
        c.drawString(int(stringWidth('Prontuário:','Helvetica', 12)) + 170, altura - 130, prontuario)  # Pode ser dinâmico
        c.drawString(int(stringWidth('Tipo de Prontuário:','Helvetica', 12)) + 170, altura - 150, f'{tipo_pront}')  # Pode ser dinâmico
        c.drawString(int(stringWidth('Nome:','Helvetica', 12)) + 170, altura - 170, nome_preso)  # Pode ser dinâmico
        c.drawString(int(stringWidth('Função:','Helvetica', 12)) + 170, altura - 190, f'{funcao}')  # Pode ser dinâmico
        c.drawString(int(stringWidth('Setor:','Helvetica', 12)) + 170, altura - 210, f'{setor}')  # Pode ser dinâmico
        c.drawString(int(stringWidth('Instituição:','Helvetica', 12)) + 170, altura - 230, f'{instituicao}')  # Pode ser dinâmico
        c.drawString(int(stringWidth('Estado:','Helvetica', 12)) + int(stringWidth(f'Instituição: {instituicao}','Helvetica', 12)) + 180, altura - 230, f'{estado}')  # Pode ser dinâmico

        # CONFIG NOME HISTÓRICO
        c.setStrokeColorRGB(0.5,0.5,0.5)
        c.setFillColorRGB(0.5,0.5,0.5) #Define a cor do fundo
        c.roundRect(30,altura-275,550,20,10,fill=True) #Desenha o retangulo
        c.setFillColorRGB(1,1,1) # Define a cor do texto
        c.setFont("Helvetica-Bold", 12)
        c.drawString((largura - int(stringWidth('HISTÓRICO:','Helvetica', 12))) / 2, altura - 270, "HISTÓRICO")
        # Finaliza o PDF
        c.save()

        return response
