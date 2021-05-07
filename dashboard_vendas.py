# Fazendo IMport das Bibliotecas Necessárias
import pandas as pd
import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbgit inic

# lendo os arquivos
df = pd.read_csv("sales_data_sample.csv" , encoding = "latin-1")

# fazendo uma cópia do dataframe
global_df = df.copy()

# editando as colunas de datas
global_df['Data_Pedido'] = pd.to_datetime(global_df['ORDERDATE'])
global_df['Ano'] = global_df['Data_Pedido'].dt.year
global_df['Mes'] = global_df['Data_Pedido'].dt.month_name()

# retirando colunas que não serão úteis pr hora
drop_cols  = ['ADDRESSLINE1', 'ADDRESSLINE2', 'POSTALCODE', 'TERRITORY', 'PHONE', 'CONTACTFIRSTNAME', 'CONTACTLASTNAME', 'CUSTOMERNAME', 'ORDERNUMBER']
global_df = global_df.drop(drop_cols, axis = 1)

# agrupandos os dados por país , ano e status da compra
global_pais_ano_status_df = global_df.groupby(['COUNTRY','Ano','STATUS'])[['SALES']].mean()
global_pais_ano_status_df.reset_index(inplace=True)

# agrupandos os dados por país , ano , status da compra e linha de produção
global_pais_ano_status_PRODUCTLINE_df = global_df.groupby(['COUNTRY','Ano','STATUS', 'PRODUCTLINE', 'DEALSIZE'])[['SALES']].mean()
global_pais_ano_status_PRODUCTLINE_df.reset_index(inplace=True)

# agrupandos os dados pelas vendas
sales_data_df = global_df.groupby(['COUNTRY','Data_Pedido', 'DEALSIZE'])[['SALES']].mean()
sales_data_df.reset_index(inplace=True)


# Configurando as cores a serem usadas na Dashboard
colors_ = {
    'background': '#EFF2FB',
    'text': '#6449C8'
}

# Criando o app da dashboard setando um tema do Bootstrap
app = dash.Dash(__name__, external_stylesheets = [dbc.themes.FLATLY],
                                        # Responsivilidade para mobile layout
                                        meta_tags=[ {'name': 'viewport',
                                                    'content': 'width=device-width, initial-scale=1.0'}  ] )

# criando o layout
app.layout = dbc.Container([

    # criando uma Linha qua agrupe tudo do "cabeçalho"
    dbc.Row([
        dbc.Col([
            # título principal
            html.H1("Dashboard de Vendas" ,
                    className = "text-center text-primary, display-2 shadow") ,
            # descrição abaixo do título
            html.P("Esta Dashboard foi feita no Módulo 7 do curso 'Data Science do Zero' do Blog Minerando Dados!" ,
                    className = "text-sm-center text-secondary display-3 shadow" ,
                    style = {"font-size":26})
                ] , width=10) ,

        # criando uma coluna dentro da linha que agrupe outros itens
        dbc.Col([
            dbc.Card([
                # logo Minerando Dados
                dbc.CardImg(
                    src = "assets/Robô-Minerador_metade-final_fundo-preto.jpg" , top=True , bottom=False
                ),

                # Descrição abaixo da Imagem
                dbc.CardBody(
                    [html.H2("Minerando Dados" , style = {"font-size":16}) , html.P("Feito por Luís Miguel!" , style = {"font-size":14})],
                    className="card text-center bg-primary text-white"
                ) ,

                # links para páginas externas
                dbc.CardLink("Minerando Dados web page" , href="https://minerandodados.com.br/" ,
                             target = "_blank" , className="text-center") ,

                dbc.CardLink("Onde me encontrar ?" , href="https://linktr.ee/iNukss" ,
                             target = "_blank" , className="text-center")
            ] , style = {'width':'15rem'})



        ] , width={'size':2 , 'order':2})
    ]) ,

    # Linha que plota os 3 primeiros gráficos:
    dbc.Row([

        # Primeiro gráfico
        dbc.Col([
            html.P("Selecione o tipo de veículo:") ,

            dcc.Dropdown(id="dropdown-1" ,
                         multi = False ,
                         value = "Classic Cars",
                         options = [
                             {'label': x, 'value': x} for x in df["PRODUCTLINE"].unique()
                         ]) ,

            dcc.Graph(id="bar-fig" , figure ={})
        ] ,  width = {'size' : 4 , 'order':1} ) ,


        # Segundo gráfico
                dbc.Col([
                    html.P("Selecione o País:") ,

                    dcc.Dropdown(id="dropdown-2" ,
                                 multi = True ,
                                 value = "USA",
                                 options = [
                                     {'label': x, 'value': x}
                                     for x in sales_data_df["COUNTRY"].unique()
                                 ]) ,

                    dcc.Graph(id="line-fig-2" , figure ={})
                ] ,  width = {'size' : 4 , 'order':2} ) ,

        # Terceiro gráfico
                dbc.Col([
                    html.P("Selecione a label:") ,

                    dcc.Dropdown(id="pie_dropdown",
                                 multi = False,
                                 value = "Ano",
                                 options= [
                                     {'label': x , 'value':x}
                                     for x in ["STATUS","COUNTRY","DEALSIZE","Ano"]
                                 ],
                                 style ={"width":"90%"} , className="text-left") ,

                    dcc.Graph(id = "pie_chart" , figure = {})
                ] ,  width = {'size' : 4 , 'order':3} )


    ]) ,

    html.Br() ,

    # Terceira Linha que plota os últimos 3 gráficos:
    dbc.Row([

        # Coluna do gráfico do tipo "Histograma"
        dbc.Col([
            html.P("Selecione o Tamanho do produto:") ,

            dcc.Checklist(id="minha_checklist" ,
                          value = ["Small"],
                          options= [
                              {"label":x , "value":x}
                              for x in sales_data_df["DEALSIZE"].unique()
                          ],
                          labelClassName = "mr-3 text-secundary"),

            dcc.Graph(id="histograma" , figure = {})
        ] , width = {'size':6 , 'order':1}) ,


        # Coluna do gráfico com o Mapa:
        dbc.Col([
            html.P("Selecione o Ano:"),

            dcc.Dropdown(id="ano_selecionado",
                         options= [
                             {"label":x , "value":x}
                             for x in range(2003,2006)
                         ] ,
                         multi=False,
                         value=2003,
                         style= {"width":"60%"}) ,

            dcc.Graph(id="mapa" , figure= {})

        ] , width = {'size':6 , 'order':2})

    ] , align="center")

] , fluid = True)



# Callbacks:
#----------------------------------------------------------------------------------------------------------------------#
## Callback Figura 1:
@app.callback(
    Output('bar-fig', 'figure'),
    Input('dropdown-1', 'value')
)
## Função que plota o gráfico da figura 1
def update_bar_chart_1(produto_selecionado):
    df_temp = df[df['PRODUCTLINE'] == produto_selecionado]
    fig = px.bar(df_temp, x='SALES', y='COUNTRY',
                 orientation='h',
                 color_discrete_sequence=['#194ca3'])

    fig.update_xaxes(showgrid=False , title_text = "Vendas")
    fig.update_yaxes(showgrid=False , title_text = "País")

    fig.update_layout(
        plot_bgcolor=colors_['background'],
        paper_bgcolor=colors_['background'],
        font_color=colors_['text']
    )
    return fig

## Callback da figura 2 (Linechart):
@app.callback(
    Output('line-fig-2','figure') ,
    Input('dropdown-2','value')
)
## Função que plota o gráfico da figura 2:
def update_line_chart_2(paises_selecionados):
    if len(paises_selecionados) == 0:
        paises_selecionados = "USA"

    paises_selecionados = paises_selecionados

    def_temp = sales_data_df.query('COUNTRY == @paises_selecionados')

    fig = px.line(def_temp , y="SALES" , x="Data_Pedido" , color = "COUNTRY",
                    )

    fig.update_xaxes(showgrid=False , title_text = "Data")
    fig.update_yaxes(gridcolor= "#08298A" , title_text = "Vendas")

    fig.update_layout(
        plot_bgcolor=colors_['background'],
        paper_bgcolor=colors_['background'],
        font_color=colors_['text']
    )
    return fig

## Callback da figura 3 (pie chart):
@app.callback(
    Output("pie_chart" , "figure"),
    Input("pie_dropdown" , "value")
)
## Função que Plota o gráfico de torta (pie chart):
def update_pie_chart(label_selecionada):
    if label_selecionada == None:
        label_selecionada = "Ano"

    pie_chart = px.pie(global_df, names=label_selecionada, hole=.4)

    pie_chart.update_xaxes(showgrid=False)
    pie_chart.update_yaxes(showgrid=False)

    pie_chart.update_layout(
        plot_bgcolor=colors_['background'],
        paper_bgcolor=colors_['background'],
        font_color=colors_['text']
    )
    return pie_chart


## Callback do Histograma:
@app.callback(
    Output("histograma" , "figure"),
    Input("minha_checklist","value")
)
## Função que Plota o Histograma:
def update_hist(tamanho):
    df_temp = global_df.query("DEALSIZE == @tamanho")

    fig = px.histogram(df_temp , x="COUNTRY" , y = "SALES" , color_discrete_sequence=["#819FF7"])

    fig.update_xaxes(showgrid=False , title_text = "País")
    fig.update_yaxes(gridcolor= "#819FF7" , title_text = "Quantidade")

    fig.update_layout(
        plot_bgcolor=colors_['background'],
        paper_bgcolor=colors_['background'],
        font_color=colors_['text'] ,
        title_text='Quantidade de Vendas por País',
        bargap=0.2
    )
    return fig

## Callback do Mapa dos Estados Unidos
@app.callback(
    Output(component_id='mapa', component_property='figure'),
    Input(component_id='ano_selecionado', component_property='value')
)
## Plotando o Mapa
def update_mapa(ano_selecionado):
    title = "Mapa de Vendas nos EUA no ano de {}".format(ano_selecionado)

    df_ = global_df.copy()
    #df_ = df_[df_['COUNTRY'] == 'USA']
    df_ = df_[df_["Ano"] == ano_selecionado]
    df_ = df_[df_["STATUS"] == "Shipped"]

    fig = px.choropleth(
        data_frame=df_,
        locationmode='USA-states',
        locations='STATE',
        scope="usa",
        color='SALES',
        hover_data=['STATE', 'SALES'],
        color_continuous_scale=px.colors.sequential.YlOrRd
    )

    fig.update_layout(
        plot_bgcolor=colors_['background'],
        paper_bgcolor=colors_['background'],
        font_color=colors_['text'],
        title_text = title
    )

    return fig

# Instanciando a aplicação:
if __name__ == '__main__':
    app.run_server(debug=True , port=8000)