from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from presos.models import Presos, PostGrad, States, Institution
from oficios.models import Oficios
import plotly.express as px


@login_required(login_url='login')
def home(request):
    f_postos = request.GET.get('posto')
    f_estado = request.GET.get('estado')
    f_instituicao = request.GET.get('instituicao')
    f_tipo_prisao = request.GET.get('tipo_prisao')

    presos = Presos.objects.all()
    oficios = Oficios.objects.all()

    if f_postos:
        presos = presos.filter(posto_grad=f_postos)
        # Filtra os Ofícios que contêm algum dos presos filtrados
        oficios = oficios.filter(n_pront_presos__in=presos)

    if f_estado:
        presos = presos.filter(state_origin=f_estado)
        # Filtra os Ofícios que contêm algum dos presos filtrados
        oficios = oficios.filter(n_pront_presos__in=presos)
    if f_instituicao:
        presos = presos.filter(institutions=f_instituicao)
        # Filtra os Ofícios que contêm algum dos presos filtrados
        oficios = oficios.filter(n_pront_presos__in=presos)
    if f_tipo_prisao:
        oficios = oficios.filter(tipo_prisao=f_tipo_prisao)
        # Filtra os Ofícios que contêm algum dos presos filtrados
        presos = presos.filter(oficioss__in=oficios)

    # Retorna pra mim apenas os postos cadastrado na planilha
    # Verifica se existem postos cadastrados
    postos_presentes = list(set(presos.values_list('posto_grad__name', flat=True)))
    if not postos_presentes:
        postos_presentes = ["Nenhum dado"]
    postos_values = [presos.filter(posto_grad__name=posto).count() for posto in postos_presentes]
    if not any(postos_values):
        postos_values = [0]  # Garante que há pelo menos um valor

    # Verifica se existem estados cadastrados
    estado_presentes = list(set(presos.values_list('state_origin__name', flat=True)))
    if not estado_presentes:
        estado_presentes = ["Nenhum dado"]
    estado_values = [presos.filter(state_origin__name=estado).count() for estado in estado_presentes]
    if not any(estado_values):
        estado_values = [0]

    # Verifica se existem instituições cadastradas
    intituicao_presentes = list(set(presos.values_list('institutions__name', flat=True)))
    if not intituicao_presentes:
        intituicao_presentes = ["Nenhum dado"]
    intituicao_values = [presos.filter(institutions__name=intituicao).count() for intituicao in intituicao_presentes]
    if not any(intituicao_values):
        intituicao_values = [0]

    # Verifica se existem tipos de prisão cadastrados
    tipo_prisao_presentes = list(set(oficios.values_list('tipo_prisao', flat=True)))
    if not tipo_prisao_presentes:
        tipo_prisao_presentes = ["Nenhum dado"]
    tipo_prisao_values = [oficios.filter(tipo_prisao=tipo_prisao).count() for tipo_prisao in tipo_prisao_presentes]
    if not any(tipo_prisao_values):
        tipo_prisao_values = [0]
    # criando gráfico de barra comparando presos e oficios
    fig1 = px.bar(
        x=['Presos', 'Oficios'],
        y=[presos.count(), oficios.count()],
        title='Presos x Oficios',
        labels={
            'x': 'Categoria',
            'y': 'Total'
        },
        color=['blue', 'red'],
        template='plotly_dark',
        color_discrete_sequence=px.colors.qualitative.Dark24,
        text_auto=True # adiciona o numero dentro da barra

    )
    fig1.update_layout(
        showlegend=False,  # Remove legenda indesejada
        plot_bgcolor="#212529",  # Cor do fundo do gráfico igual ao Bootstrap Dark
        paper_bgcolor="#212529",  # Cor externa do gráfico igual ao Bootstrap Dark
        font=dict(color="white"),  # Define textos do gráfico como branco para boa visibilidade
        height=400,
        yaxis_range=[0, max([presos.count(), oficios.count()]) * 1.2],
        title_x=0.5  # Centraliza o título do gráfico


        
    )
    fig1.update_traces(textposition='outside', textfont_size=16)

    fig2 = px.pie(
        names=list(postos_presentes),  # Define os rótulos das fatias
        values=postos_values,  # Define os valores absolutos
        title='Distribuição de Presos por Posto / Graduação',
        template='plotly_dark',  # Mantém o tema escuro
        color_discrete_sequence=px.colors.qualitative.Alphabet,  # Aplicando paleta de cores automática
    )

    fig2.update_layout(
        showlegend=True,  # Remove legenda indesejada
        plot_bgcolor="#212529",  # Cor do fundo do gráfico igual ao Bootstrap Dark
        paper_bgcolor="#212529",  # Cor externa do gráfico igual ao Bootstrap Dark
        font=dict(color="white"),  # Define textos do gráfico como branco para boa visibilidade
        height=400,
        title_x=0.5  # Centraliza o título do gráfico

    )
    # Exibir os valores absolutos em vez de porcentagem
    fig2.update_traces(textinfo="value+percent", textfont_size=14)

    # Grafico 3 Estados
    fig3 = px.pie(
        names=list(estado_presentes),  # Define os rótulos das fatias
        values=estado_values,  # Define os valores absolutos
        title='Distribuição de Presos por Estados',
        template='plotly_dark',  # Mantém o tema escuro
        color_discrete_sequence=px.colors.diverging.Spectral,  # Aplicando paleta de cores automática
    )

    fig3.update_layout(
        showlegend=True,  # Remove legenda indesejada
        plot_bgcolor="#212529",  # Cor do fundo do gráfico igual ao Bootstrap Dark
        paper_bgcolor="#212529",  # Cor externa do gráfico igual ao Bootstrap Dark
        font=dict(color="white"),  # Define textos do gráfico como branco para boa visibilidade
        height=400,
        title_x=0.5  # Centraliza o título do gráfico

    )
    # Exibir os valores absolutos em vez de porcentagem
    fig3.update_traces(textinfo="value+percent", textfont_size=14)

    # Figura instituições
    fig4 = px.bar(
        x=list(intituicao_presentes),
        y=intituicao_values,
        title='Distribuição de Presos por Instituições',
        template='plotly_dark',
        labels={
            'x': 'Instituições',
            'y': 'Total'
        },
        color=list(intituicao_presentes),
        color_discrete_sequence=px.colors.qualitative.Set3,
        text_auto=True
    )
    fig4.update_layout(
        showlegend=False,
        plot_bgcolor='#212529',
        paper_bgcolor='#212529',
        font=dict(color='white'),
        height=400,
        yaxis_range=[0, max(intituicao_values) * 1.2],
        title_x=0.5  # Centraliza o título do gráfico

    )
    fig4.update_traces(
        textposition='outside',
        textfont_size=14
    )
    # figura tipo de prisao
    fig5 = px.bar(
        x=list(tipo_prisao_presentes),
        y=tipo_prisao_values,
        title='Distribuição de Ofícios por Tipo de Prisão',
        template='plotly_dark',
        labels={
            'x': 'Tipo de Prisões',
            'y': 'Total'
        },
        color=list(tipo_prisao_presentes),
        color_discrete_sequence=px.colors.qualitative.Pastel1,
        text_auto=True
    )
    fig5.update_layout(
        showlegend=False,
        plot_bgcolor='#212529',
        paper_bgcolor='#212529',
        font=dict(color='white'),
        height=400,
        yaxis_range=[0, max(tipo_prisao_values) * 1.2],
        title_x=0.5  # Centraliza o título do gráfico
    )
    fig5.update_traces(
        textposition='outside',
        textfont_size=14
    )
    # Gerando o HTML do gráfico
    graph_html = fig1.to_html(full_html=False) # Gráfico barra oficio x presos
    graph_html2 = fig2.to_html(full_html=False) # Gráfico posto/grad
    graph_html3 = fig3.to_html(full_html=False) # Gráfico posto/grad
    graph_html4 = fig4.to_html(full_html=False) # Gráfico posto/grad
    graph_html5 = fig5.to_html(full_html=False) # Gráfico posto/grad
    # Contexto para o template
    context = {
        'n_presos': presos.count(),
        'n_oficios': oficios.count(),
        'graph_html': graph_html,
        'graph_html2': graph_html2,
        'graph_html3': graph_html3,
        'graph_html4': graph_html4,
        'graph_html5': graph_html5,
        'postos': PostGrad.objects.all(),
        'estados': States.objects.all(),
        'instituicoes': Institution.objects.all(),

    }
    if request.headers.get("HX-Request"):
        return render(request, "components/_graph_section.html", context)
    
    return render(request, 'home.html', context=context)
