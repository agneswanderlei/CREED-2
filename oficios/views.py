from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, CreateView, DetailView, UpdateView, DeleteView
)
from . import models
from presos.models import Presos
from . import forms
from django.contrib.auth.mixins import (
    LoginRequiredMixin
)
from django.http import JsonResponse
from django.db.models import Q
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.platypus import PageTemplate, BaseDocTemplate, Frame, Table, TableStyle, Paragraph

from django.http import HttpResponse
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.units import inch
import os
from io import BytesIO
from PyPDF2 import PdfWriter, PdfReader
from reportlab.lib.enums import TA_JUSTIFY



class OficiosCreate(CreateView):
    model = models.Oficios
    form_class = forms.OficiosForm
    template_name = 'oficios_create.html'
    success_url = reverse_lazy('oficios_list')

    def dispatch(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Verifica se é uma requisição AJAX
            term = request.GET.get('q')
            presos = models.Presos.objects.filter(Q(name_full__icontains=term) | Q(number_doc__icontains=term))
            response_content = list(presos.values())
            return JsonResponse(response_content, safe=False)
        return super().dispatch(request, *args, **kwargs)


class OficiosList(ListView):
    model = models.Oficios
    template_name = 'oficios_list.html'
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


class OficiosDetail(DetailView):
    model = models.Oficios
    template_name = 'oficios_detail.html'


class OficiosUpdate(UpdateView):
    model = models.Oficios
    form_class = forms.OficiosForm
    template_name = 'oficios_update.html'
    success_url = reverse_lazy('oficios_list')

    def dispatch(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Verifica se é uma requisição AJAX
            term = request.GET.get('q')
            presos = models.Presos.objects.filter(Q(name_full__icontains=term) | Q(number_doc__icontains=term))
            response_content = list(presos.values())
            return JsonResponse(response_content, safe=False)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        print(self.object.date_send)  # Verifique se a data está carregando corretamente
        return super().get(request, *args, **kwargs)

class OficiosDelete(DeleteView):
    model = models.Oficios
    template_name = 'oficios_delete.html'
    success_url = reverse_lazy('oficios_list')


# Função para criar a marca d'água repetitiva
def adicionar_marca_dagua(canvas, doc, nome_usuario, destinatario):
    largura, altura = letter  # Define a orientação paisagem
    canvas.setFont("Helvetica-Bold", 16)  # Fonte da marca d'água
    canvas.setFillColorRGB(0.85, 0.85, 0.85)  # Cor cinza claro

    canvas.saveState()  # Salva o estado atual do canvas
    canvas.rotate(45)  # Rotaciona o canvas 45 graus para diagonal

    texto_marca_dagua = f"AC49 {nome_usuario} {destinatario}"  # Texto personalizado
    # Calcula a largura do texto
    largura_texto = stringWidth(texto_marca_dagua, "Helvetica-Bold", 16)
    print(int(largura_texto))
    espacamento_x = int(largura_texto) + 20
    espacamento_y = 40
    # Adiciona a marca d'água repetitiva
    for x in range(-int(largura), int(largura) * 2, espacamento_x):
        for y in range(-int(altura), int(altura) * 2, espacamento_y):
            canvas.drawString(x, y, texto_marca_dagua)

    canvas.restoreState()  # Restaura o estado original do canvas


# Função para criar cabeçalho e rodapé
def adicionar_cabecalho_rodape(canvas, doc):
    largura, altura = letter  # Tamanho da página
    
    # Configuração do texto
    canvas.setFont("Helvetica-Bold", 22)  # Fonte em negrito
    canvas.setFillColorRGB(1, 0, 0)  # Cor vermelha (RGB)
    # Calcula centro da página
    centro_horizontal = largura / 2
   
    # Cabeçalho
    canvas.drawCentredString(centro_horizontal - 5, altura - 30, "RESERVADO")  # Posição superior esquerda

    # Título adicional: "Sistema de Controle de Presos no CREED - SCPC"
    canvas.setFont("Helvetica", 16)  # Fonte menor para o título adicional
    canvas.setFillColorRGB(0, 0, 0)  # Cor preta (RGB)
    canvas.drawCentredString(centro_horizontal, altura - 55, "Sistema de Controle de Presos no CREED - SCPC")  # Texto logo abaixo

    # Configuração do texto
    canvas.setFont("Helvetica-Bold", 22)  # Fonte em negrito
    canvas.setFillColorRGB(1, 0, 0)  # Cor vermelha (RGB)
    # Rodapé
    canvas.drawCentredString(centro_horizontal - 5, 20, "RESERVADO")  # Posição inferior esquerda
    


def gerar_relatorio_pdf(request):
    # Configura o arquivo PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_oficios.pdf"'

    # Obtém o nome do usuário logado
    nome_usuario = request.user.codigo_usuario or "Usuário"
    senha = request.GET.get('senha')
    destinatario = request.GET.get('dest')
    tipo_prisao = request.GET.get('tipo_prisao')
    n_pront = request.GET.get('n_pront')
    n_oficio = request.GET.get('n_oficio')
    n_sei = request.GET.get('n_sei')
    date_send1 = request.GET.get('date_send1')
    date_send2 = request.GET.get('date_send2')
    print(f'Destinatario: {tipo_prisao}')

    # Use BytesIO para gerar o PDF em memória
    buffer = BytesIO()

    # Criar o documento
    doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            leftMargin=inch / 2,
            rightMargin=inch / 2,
            topMargin=inch,
            bottomMargin=inch,
        )

    # Tamanho da página
    largura, altura = letter

    # Estilo do título
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    title_style.fontSize = 16
    title_style.alignment = 1

    # Adiciona o título "RELATÓRIO"
    title = Paragraph("RELATÓRIO", title_style)

    # Dados para a tabela
    oficios = models.Oficios.objects.all()
    if tipo_prisao:
        oficios = oficios.filter(tipo_prisao__exact=tipo_prisao)
    if n_oficio:
        oficios = oficios.filter(n_oficios__icontains=n_oficio)
    if n_pront:
        oficios = oficios.filter(n_pront_presos__number_doc__exact=n_pront)
    if n_sei:
        oficios = oficios.filter(n_sei__icontains=n_sei)
    if date_send1 and date_send2:
        oficios = oficios.filter(date_send__range=[date_send1, date_send2]) # Filtra intervalos
    if date_send1:
        oficios = oficios.filter(date_send__gte=date_send1)
    if date_send2:
        oficios = oficios.filter(date_send__lte=date_send2)    

    data = [["Nº Ofício", "Nº SEI", "Data", "Tipo de Prisão", 'Descrição']]

    styles.add(ParagraphStyle(
            name='Justifield',
            parent=styles['Normal'],
            alignment=TA_JUSTIFY,
            wordWrap='CJK',
            fontSize=12,
            leading=18
            )
        )
    
    for oficio in oficios:
        data.append([
            oficio.n_oficios,
            oficio.n_sei,
            oficio.date_send.strftime("%d/%m/%Y"),
            oficio.tipo_prisao,
            Paragraph(oficio.descricao, styles['Justifield'])
        ])

    # Criação da tabela
    table = Table(data, colWidths=[75, 50, 75, 100, 300],)

    # Estilo da tabela

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    table.setStyle(style)
    
    # Altura estimada da tabela
    table_width = sum([100, 100, 100, 200])  # Soma das larguras das colunas
    central_x = (largura - table_width) / 2  # Calcula posição central

    # Configuração do frame (centralizado horizontalmente)
    frame = Frame(central_x, 30, table_width, altura - 100, id="frame")

    # Template com cabeçalho, rodapé e marca d'água
    template = PageTemplate(
        id="custom",
        frames=[frame],
        onPage=lambda c, d: (adicionar_marca_dagua(c, d, nome_usuario, destinatario),
                             adicionar_cabecalho_rodape(c, d))
    )
    doc.addPageTemplates([template])

    # Adicionar os elementos ao PDF
    elements = [title, table]

    # Gera o PDF
    doc.build(elements,
              onFirstPage=lambda c, d: (adicionar_marca_dagua(c, d, nome_usuario, destinatario),
                                        adicionar_cabecalho_rodape(c, d)),
              onLaterPages=lambda c, d: (adicionar_marca_dagua(c, d, nome_usuario, destinatario),
                                        adicionar_cabecalho_rodape(c, d)))
    
                
    # Proteger o PDF com senha usando PyPDF2
    buffer.seek(0)
    pdf_reader = PdfReader(buffer)
    pdf_writer = PdfWriter()

    for page in pdf_reader.pages:
        pdf_writer.add_page(page)

    # Adicionar senha
    senhas = senha
    pdf_writer.encrypt(senhas)

    # Salvar PDF final protegido no response
    output = BytesIO()
    pdf_writer.write(output)
    output.seek(0)
    response.write(output.read())

    return response
