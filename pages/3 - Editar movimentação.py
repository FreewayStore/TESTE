import streamlit as st
import pandas as pd
import openpyxl as xl

st.set_page_config(layout='wide')
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
#Filtros
st.title("📝 Editar Status",anchor=False)
filtro_ano = st.selectbox('Ano',df["Ano"].unique())
filtro_mês = st.selectbox('Mês',df["Mês"].unique())
filtro_despesas = st.selectbox('Movimentação',df['CATEGORIA'].unique())
editar_status = st.selectbox('Editar',["A Receber","Recebido","A pagar","Pago"])
#----------------------------------------------------------------------------------------
#Dataframe filtrado

df = df.query('Ano == @filtro_ano & Mês == @filtro_mês & CATEGORIA == @filtro_despesas')


#----------------------------------------------------------------------------------------
#Indice da linha a ser editada

linha = df.index.max() + 2

coluna = 4

#----------------------------------------------------------------------------------------
#Editar

if st.button("SALVAR EDIÇÃO"):
    planilha = xl.load_workbook("Movimentação.xlsx")
    sheet = planilha["Despesas"]
    
    editar = sheet.cell(row=linha,column=coluna)
    editar.value = editar_status
    novo_valor = editar
    
    planilha.save("Movimentação.xlsx")
    
    st.success("Edição salva!")

df["VALOR"] = df["VALOR"].apply(lambda x: f'R$ {x:.2f}')
st.table(df)