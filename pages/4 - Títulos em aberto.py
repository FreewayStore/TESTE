
import streamlit as st
import pandas as pd

#----------------------------------------------------------------------------------------
#exibição de dados

st.set_page_config(layout="wide",page_title="Título em Aberto")

#----------------------------------------------------------------------------------------
#Layout em duas colunas
col1 = st.columns(1)

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
#Dados
st.title("🔍 Títulos em aberto",anchor=False)

filtro_em_aberto = "EM ABERTO"

df_filtrado1 = df.query('STATUS == @filtro_em_aberto')
df_filtrado1 = df_filtrado1.drop(columns=["CATEGORIA","STATUS"])
df_filtrado1["VALOR"] = df_filtrado1["VALOR"].apply(lambda x: f'R$ {x:.2f}')
st.table(df_filtrado1)
