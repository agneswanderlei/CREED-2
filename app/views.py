from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from presos.models import Presos
from oficios.models import Oficios
import plotly.express as px


@login_required(login_url='login')
def home(request):
    presos = Presos.objects.all()
    oficios = Oficios.objects.all()

    # Retorna pra mim apenas os postos cadastrado na planilha
    postos_presentes = presos.values_list('posto_grad__name', flat=True).distinct()
    postos_values = [presos.filter(posto_grad__name=posto).count() for posto in postos_presentes]
    estado_presentes = presos.values_list('state_origin__name', flat=True).distinct()
    estado_values = [presos.filter(state_origin__name=estado).count() for estado in estado_presentes]
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
        
    )
    fig1.update_traces(textposition='inside', textfont_size=16)

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
        height=400
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
        height=400
    )
    # Exibir os valores absolutos em vez de porcentagem
    fig3.update_traces(textinfo="value+percent", textfont_size=14)

    # Gerando o HTML do gráfico
    graph_html = fig1.to_html(full_html=False) # Gráfico barra oficio x presos
    graph_html2 = fig2.to_html(full_html=False) # Gráfico posto/grad
    graph_html3 = fig3.to_html(full_html=False) # Gráfico posto/grad
    # Contexto para o template
    context = {
        'n_presos': presos.count(),
        'n_oficios': oficios.count(),
        'graph_html': graph_html,
        'graph_html2': graph_html2,
        'graph_html3': graph_html3
    }

    return render(request, 'home.html', context=context)
