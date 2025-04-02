from django.shortcuts import render
from oficios.models import Oficios
from presos.models import Presos

from django.http import HttpResponse
from reportlab.lib.utils import simpleSplit

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.pdfmetrics import stringWidth
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, PageTemplate, Frame
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import Image, Spacer, HRFlowable
from reportlab.lib.enums import TA_JUSTIFY

import os


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




# def gerar_pdf(request):
    if request.method == 'GET':
        # Obtém os dados:
        n_pront = request.GET.get('n_pront')
        
        # Configura o tipo de arquivo como PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="meu_relatorio.pdf"'

        # Cria o canvas para desenhar o PDF
        c = canvas.Canvas(response, pagesize=letter)

        # Define o tamanho da página
        largura, altura = letter
        data = datetime.now().strftime("%d/%m/%Y")
        hora = datetime.now().strftime("%H:%M:%S")  # Formata a hora (horas:minutos:segundos)

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

        # Buscar dados para marca d1agua
        nome_usuario = request.user.codigo_usuario or "Usuário"
        destinatario = request.GET.get('dest')
        print(n_pront)
        

        
        # BUSCA OS OFICIOS RELACIONADOS AOS PRESOS
        oficios = Oficios.objects.filter(
            n_pront_presos__number_doc__exact=n_pront
        )
        print(oficios.count())
        for oficio in oficios:
            print(oficio.n_sei)

        # CONFIGURAÇÃO MARCA DAGUA
        def desenhar_marca_dagua(canvas, largura, altura, nome_usuario):
            canvas.setFont("Helvetica-Bold", 16)
            canvas.setFillColorRGB(0.85, 0.85, 0.85)
            canvas.saveState()
            canvas.rotate(45)
            texto_marca_dagua = f"AC49 {nome_usuario}"
            largura_texto = stringWidth(texto_marca_dagua, "Helvetica-Bold", 16)
            espacamento_x = int(largura_texto) + 20
            espacamento_y = 40
            for x in range(-int(largura), int(largura) * 2, espacamento_x):
                for y in range(-int(altura), int(altura) * 2, espacamento_y):
                    canvas.drawString(x, y, texto_marca_dagua)
            canvas.restoreState()
        desenhar_marca_dagua(c, largura, altura, nome_usuario)

        



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
        c.setFillColorRGB(0, 0, 0)  # Cor cinza claro
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
        c.setFont("Helvetica-Bold", 12)
        c.drawString(int(stringWidth('Prontuário:','Helvetica', 12)) + 170, altura - 130, f'{prontuario}')  # Pode ser dinâmico
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

        

        # Posição inicial para a lista de ofícios
        y_pos = altura - 300  # Ajuste conforme necessário

        # Define a cor do texto
        c.setFillColorRGB(0, 0, 0)

        if oficios.exists():
            for oficio in oficios:
                # Se estiver muito baixo na página, cria uma nova página
                if y_pos < 50:
                    c.showPage()  # Cria nova página
                    desenhar_marca_dagua(c, largura, altura, nome_usuario)
                    y_pos = altura - 50  # Redefine a posição inicial

                # Define a posição X inicial
                x_pos = 40  

                # Campo: "Ofício Nº:"
                c.setFont("Helvetica-Bold", 10)
                c.drawString(x_pos, y_pos, "Ofício Nº:")
                x_pos += stringWidth("Ofício Nº: ", "Helvetica-Bold", 10)

                c.setFont("Helvetica", 10)
                c.drawString(x_pos, y_pos, f"{oficio.n_oficios}")
                x_pos += stringWidth(f"{oficio.n_oficios}  ", "Helvetica", 10)

                # Campo: "Nº SEI:"
                c.setFont("Helvetica-Bold", 10)
                c.drawString(x_pos, y_pos, "Nº SEI:")
                x_pos += stringWidth("Nº SEI: ", "Helvetica-Bold", 10)

                c.setFont("Helvetica", 10)
                c.drawString(x_pos, y_pos, f"{oficio.n_sei}")
                x_pos += stringWidth(f"{oficio.n_sei}  ", "Helvetica", 10)

                # Campo: "Tipo de Prisão:"
                c.setFont("Helvetica-Bold", 10)
                c.drawString(x_pos, y_pos, "Tipo de Prisão:")
                x_pos += stringWidth("Tipo de Prisão: ", "Helvetica-Bold", 10)

                c.setFont("Helvetica", 10)
                c.drawString(x_pos, y_pos, f"{oficio.tipo_prisao}")

                # Move a posição para a descrição, abaixo da linha de dados
                y_pos -= 20  

                # Configurar a descrição para quebrar em múltiplas linhas
                max_width = 500  # Largura máxima do texto na página
                c.setFont("Helvetica", 10)
                
                # Divide o texto em linhas que cabem dentro da largura
                descricao_linhas = simpleSplit(oficio.descricao, "Helvetica", 10, max_width)

                for linha in descricao_linhas:
                    if y_pos < 50:  # Se o texto estiver perto do fim da página, cria uma nova página
                        c.showPage()
                        y_pos = altura - 50
                        c.setFont("Helvetica", 10)  # Precisa redefinir a fonte após `showPage()`

                    c.drawString(40, y_pos, linha)
                    y_pos -= 15  # Move para a próxima linha
                c.line(30,y_pos, largura-30,y_pos)
                # Adiciona espaço entre os ofícios
                y_pos -= 15  

        else:
            c.setFont("Helvetica", 10)
            c.drawString(40, y_pos, "Nenhum ofício encontrado para este preso.")

        # Finaliza o PDF
        c.save()
        return response



def desenhar_marca_dagua(c, largura, altura, nome_usuario):
    c.setFont("Helvetica-Bold", 16)
    c.setFillColorRGB(0.85, 0.85, 0.85)
    c.saveState()
    c.rotate(45)
    texto_marca_dagua = f"AC49 {nome_usuario} "
    largura_texto = stringWidth(texto_marca_dagua, "Helvetica-Bold", 16)
    espacamento_x = int(largura_texto) + 20
    espacamento_y = 40
    for x in range(-int(largura), int(largura) * 2, espacamento_x):
        for y in range(-int(altura), int(altura) * 2, espacamento_y):
            c.drawString(x, y, texto_marca_dagua)
    c.restoreState()

def header_footer(canvas, doc):
    largura, altura = letter  # Garante que as dimensões da página sejam corretas
    data = datetime.now().strftime("%d/%m/%Y")
    hora = datetime.now().strftime("%H:%M:%S")
    nome_usuario = doc.nome_usuario  # Passando dinamicamente
    desenhar_marca_dagua(canvas, largura, altura, nome_usuario)
    # Cabeçalho com "RESERVADO"
    canvas.saveState()
    canvas.setFont("Helvetica-Bold", 14)  # Fonte do texto
    canvas.setFillColorRGB(1, 0, 0)  # Cor vermelha (RGB)
    canvas.drawCentredString(largura / 2.0, altura - 40, "RESERVADO")  # Posição no cabeçalho

    # Nome do dia em que foi criado
    canvas.setFont("Helvetica", 10)  # Fonte do texto
    canvas.setFillColorRGB(0, 0, 0)  # Cor preta (RGB)
    canvas.drawString(40, altura - 50, f"Data: {data} - Hora: {hora}")  # Posição no cabeçalho
    
    # Rodapé com "RESERVADO"
    canvas.setFont("Helvetica-Bold", 14)  # Fonte do texto
    canvas.setFillColorRGB(1, 0, 0)  # Cor vermelha (RGB)
    canvas.drawCentredString(largura / 2.0, 30, "RESERVADO")  # Posição no rodapé
    


def gerar_pdf(request):
    if request.method == 'GET':
        n_pront = request.GET.get('n_pront')
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="relatorio_prisioneiro.pdf"'
        
        largura, altura = letter
        preso = Presos.objects.filter(number_doc=n_pront).first()
        nome_usuario = request.user.codigo_usuario or "Usuário"
        
        doc = SimpleDocTemplate(
            response,
            pagesize=letter,
            leftMargin=inch / 2,
            rightMargin=inch / 2,
            topMargin=inch,
            bottomMargin=inch,
        )
        doc.nome_usuario = nome_usuario  # Adiciona nome_usuario ao documento
        elements = []
        styles = getSampleStyleSheet()

        # Define um frame para a página
        frame = Frame(
            inch / 2, # Diminui margem esquerda
            inch, # Margem inferior
            largura - inch, # margem direita
            altura - 2 * inch, # margem superior
            id='normal'
        )


        # Aplica o template para todas as páginas
        template = PageTemplate(id='marca_dagua', frames=frame, onPage=header_footer)
        doc.addPageTemplates([template])

        styles.add(ParagraphStyle(name='Titulo_rel', parent=styles['Title'], fontSize=24))
        styles.add(ParagraphStyle(
            name='Justifield',
            parent=styles['Normal'],
            alignment=TA_JUSTIFY,
            wordWrap='CJK',
            fontSize=12,
            leading=18
            )
        )
        styles.add(ParagraphStyle(
            name='texto_desc_oficios',
            parent=styles['Normal'],
            alignment=TA_JUSTIFY,
            wordWrap='CJK',
            fontSize=12,
            leading=14
            )
        )
        centered_style2 = ParagraphStyle(
            name='Centered',
            parent=styles["Heading2"],
            alignment=1, # Alinhamento central (0-esq, 1-center, 2-dir)
            textColor="black"
        )
        # Conteúdo do PDF
        elements.append(Paragraph("<b>RELATÓRIO DE PRISIONEIROS</b>", styles["Titulo_rel"]))
        elements.append(Paragraph(f"<b>Gerado por: Sistema de Gestão Prisional</b>", centered_style2))
        
        if preso.photo:  
            caminho_foto = preso.photo.path  
            if os.path.exists(caminho_foto):  
                img = Image(caminho_foto, width=100, height=100)  
                elements.append(Spacer(1, 10))
                elements.append(img)  
                elements.append(Spacer(1, 10))
            else:
                elements.append(Paragraph("Imagem não encontrada.", styles["Normal"]))
        else:
            elements.append(Paragraph("Preso não possui foto.", styles["Normal"]))
        
        dados_preso = [
            ['Dados: ', 'Descrição'],
            ["Prontuário:", preso.number_doc],
            ["Tipo de Prontuário:", preso.type_doc],
            ["Nome:", preso.name_full],
            ["Função:", preso.posto_grad],
            ["Setor:", preso.sector],
            ["Instituição:", preso.institutions],
            ["Estado:", preso.state_origin]
        ]
        
        tabela_preso = Table(dados_preso, colWidths=[150, 380])
        tabela_preso.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('FONTSIZE', (0, 0), (0, -1), 12),
            ('FONTSIZE', (0, 0), (1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
            
        ]))
        elements.append(tabela_preso)
        # Stilo para centralizar
        centered_style = ParagraphStyle(
            name='Centered',
            parent=styles["Heading2"],
            alignment=1, # Alinhamento central (0-esq, 1-center, 2-dir)
            textColor="White"
        )
        
        # elements.append(Paragraph("<b>HISTÓRICO:</b>", centered_style))
        elements.append(Spacer(1,10))
        paragrafo = Paragraph("<b>HISTÓRICO:</b>", centered_style)
        tabela2 = Table([[paragrafo]], colWidths=[530], rowHeights=[20])
        tabela2.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.grey),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))
        elements.append(tabela2)
        elements.append(Spacer(1,10))
        if preso.oficioss.exists():
            for oficio in preso.oficioss.all():
                # descricao_linhas = simpleSplit(oficio.descricao, "Helvetica", 10, 500)
                elements.append(Paragraph(f"<b>Data do ofício:</b> {oficio.date_send.strftime("%d/%m/%Y")} - <b>Ofício Nº</b>: {oficio.n_oficios} - <b>Nº SEI:</b> {oficio.n_sei} - <b>Tipo de Prisão:</b> {oficio.tipo_prisao}", styles["texto_desc_oficios"]))
                elements.append(Spacer(1, 10))
                elements.append(Paragraph(oficio.descricao, styles['Justifield']))
                # for linha in descricao_linhas:
                #     elements.append(Paragraph(linha, styles["Justifield"]))
                elements.append(Spacer(1, 10))
                elements.append(HRFlowable(width="100%", thickness=0.5, color="black"))
                elements.append(Spacer(1, 10))
                elements.append(Spacer(1, 10))
        else:
            elements.append(Paragraph("Nenhum ofício encontrado para este preso.", styles["Normal"]))

        # Gera o PDF
        doc.build(elements, onFirstPage=header_footer, onLaterPages=header_footer)
        return response
