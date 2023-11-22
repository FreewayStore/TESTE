#----------------------------------------------------------------------------------------
#Dashboard Finanças Pessoais

import streamlit as st
import pandas as pd
import openpyxl as xl

#----------------------------------------------------------------------------------------
#exibição de dados

st.set_page_config(layout="wide",page_title="Adicionar Movimentação")
st.title("➕ Adicionar Movimentação",anchor=False)


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
   
entrada_data = st.date_input("DATA","today",format= "DD/MM/YYYY")

entrada_descrição = st.text_input("FORNECEDOR")

entrada_valor = st.number_input("VALOR")

entrada_status = st.selectbox("STATUS",["EM ABERTO","PAGO"])

#----------------------------------------------------------------------------------------
#Adicionar a nova linha

if st.button("ADICIONAR"):
    # Abrir o arquivo do Excel
    planilha = xl.load_workbook("Movimentação.xlsx")
    planilha = planilha.active

    # Criar uma nova linha com os dados inseridos
    nova_linha = [entrada_data, entrada_descrição,entrada_status, entrada_valor]
    
    # Adicionar a nova linha à planilha
    planilha.append(nova_linha)

    # Salvar as alterações de volta no arquivo Excel
    planilha.parent.save("Movimentação.xlsx")
   
    st.success("Movimentação salva!")


