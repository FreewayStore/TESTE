#----------------------------------------------------------------------------------------
#Dashboard Finanças Pessoais

import streamlit as st
import pandas as pd
import plotly.express as px


#----------------------------------------------------------------------------------------
#exibição de dados

st.set_page_config(layout="wide",initial_sidebar_state="collapsed")

#----------------------------------------------------------------------------------------
#Layout em duas colunas
col1,col2,col3,col4,col5,col6 = st.columns([3,2,2,2,1,1])
col7,col8 = st.columns(2)
col9,col10 = st.columns([100,1])

#----------------------------------------------------------------------------------------
#Dados

df = pd.read_excel("Movimentação.xlsx")
pd.to_datetime(df["DATA"])
df["Ano"] = df["DATA"].dt.year
df["Mês"] = df["DATA"].dt.month
df.sort_values("DATA")
df["Ano"].astype(int)
df["Mês"].astype(int)
df['VALOR'].astype(float)

def determinar_mês(valor):
    meses = {
        1: "Jan",
        2: "Fev",
        3: "Mar",
        4: "Abr",
        5: "Mai",
        6: "Jun",
        7: "Jul",
        8: "Ago",
        9: "Set",
        10: "Out",
        11: "Nov",
        12: "Dez"
    }
    return meses.get(valor)


df["Mês"] = df["Mês"].apply(determinar_mês)
df = df.drop(columns=["DATA"])

#----------------------------------------------------------------------------------------
#Filtros/Layout

with col1:
    st.image('Logo2.png',width=300)
   
with col5:
    filtro_ano = st.selectbox("Ano", df["Ano"].unique(),placeholder="2023")
    
    
with col6:
     filtro_mes = st.selectbox("Mês", df["Mês"].unique()) 

#----------------------------------------------------------------------------------------
#Dataframes filtrados

df_filtrado1 = df.loc[(df["Ano"] == filtro_ano) & (df["Mês"] == filtro_mes)]

df_em_aberto = df.loc[(df["Ano"] == filtro_ano) & (df["STATUS"] == 'EM ABERTO') & (df["Mês"] == filtro_mes)]

df_filtrado2 = df.loc[(df["Ano"] == filtro_ano) & (df["Mês"] == filtro_mes)]
df_filtrado2 = df_filtrado2.groupby(['CATEGORIA','Mês'])['VALOR'].sum().reset_index()
df_filtrado2 = df_filtrado2.sort_values('VALOR')


classificar_meses = {'Jan':1, 'Fev': 2, 'Mar': 3, 'Abr': 4, 'Mai':5, 'Jun': 6, 'Jul': 7, 'Ago': 8, 'Set':9, 'Out': 10, 'Nov': 11, 'Dez': 12}

df_filtrado3 = df.loc[(df["Ano"] == filtro_ano)]

df_filtrado3 = df_filtrado3.groupby(["TIPO","Mês"])["VALOR"].sum().reset_index()
df_filtrado3['Ordem_Mês'] = df_filtrado3['Mês'].map(classificar_meses)
df_filtrado3 = df_filtrado3.sort_values(by='Ordem_Mês',ascending = True).drop(columns=['Ordem_Mês'])


df_filtrado4 = df.loc[(df["Ano"] == filtro_ano) & (df["STATUS"] == "PAGO") & (df["Mês"] == filtro_mes)]
#----------------------------------------------------------------------------------------
#Gráficos

grafico_Rosca = px.pie(df_filtrado1,names="STATUS",values="VALOR",color_discrete_sequence=["#06d6a0","#941b0c"],title='DISPERSÃO POR STATUS')
grafico_Rosca.update_traces(showlegend=False)


grafico_barras = px.bar(df_filtrado2,x="VALOR",y='CATEGORIA',orientation='h',title="VALOR POR CATEGORIA")

grafico_colunas = px.bar(df_filtrado3,x="Mês",y=["VALOR"],title='Entrada e Saída',barmode='group')
grafico_colunas.update_yaxes(showgrid=False)
grafico_colunas.update_traces(showlegend=False)


#----------------------------------------------------------------------------------------
# Layout gráficos
with col2:
    st.metric("PAGO",f'R$ {round(df_filtrado4["VALOR"].sum(),2):.2f}')
with col3:
    st.metric("EM ABERTO",f'R$ {round(df_em_aberto["VALOR"].sum(),2):.2f}')
with col7:
    st.markdown('----------------------')
    st.plotly_chart(grafico_barras,use_container_width=True) 
with col8:
    st.markdown('----------------------')
    st.plotly_chart(grafico_Rosca,use_container_width=True) 
with col9:
    st.markdown('----------------------')
    st.plotly_chart(grafico_colunas,use_container_width=True)
    st.markdown('----------------------')


st.write("Movimentações do Mês")

df_filtrado1["VALOR"] = df_filtrado1["VALOR"].apply(lambda x: f'R$ {x:.2f}')

st.table(df_filtrado1)

#----------------------------------------------------------------------------------------