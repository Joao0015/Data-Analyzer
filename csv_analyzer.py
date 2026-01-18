import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import csv 
import os

st.set_page_config(layout="wide")

#Carrega o dataframe com cache para nao ficar demorando para rodar toda vez
@st.cache_data
def carregar_dados(arquivo, tem_header, lista_nomes=None):
    #  Ajusta o cabeçalho: 0 se tiver nomes na primeira linha, None se não tiver
    config_header = 0 if tem_header else None
    
    # Identifica qual "ferramenta" usar baseada na extensão do arquivo
    if arquivo.name.endswith((".csv", ".txt")):
        metodo_leitura = pd.read_csv
    elif arquivo.name.endswith(".xlsx"):
        metodo_leitura = pd.read_excel
    else:
        st.error("Formato de arquivo não suportado!")
        return None

    # Faz a leitura final. O Pandas ignora o 'names' se ele for None.
    return metodo_leitura(arquivo, header=config_header, names=lista_nomes)

def exibir_info(df, nome_df):
    
    st.write(f"### Visualizando: {nome_df}")

    # --- MOSTRAR DADOS ---
    st.success("Dados carregados com sucesso!")

    st.write("### 📄 Pré-visualização do DF")
    st.dataframe(df, use_container_width=True) # Mostra todo o df

    st.divider()

    col1,col2, col3 = st.columns([4,2,1])

    with col1:
        with st.container(height=500):
            st.write("### ⚡ Resumo colunas numericas")
            st.write(df.describe())

    with col2:
        with st.container(height=500):
            st.write("### 👁️ Tipos das colunas")
            st.dataframe(df.dtypes) # Mostra as primeiras 10 linhas

    with col3:
        with st.container(height=500):
            st.write("### Shape do DF")
            st.write(df.shape)

            st.write("### Qtd de cada dtype")
            contagem_tipo = df.dtypes.value_counts()
            st.write(contagem_tipo)

    st.divider()

    st.write("Ver se tem valores vazios")
    st.write(df.isnull().sum())

    st.divider()
# ---- SIDEBAR ----
st.sidebar.header("Configurações")

possui_header = st.sidebar.checkbox("O arquivo possui cabeçalho?", value=True)

custom_columns = None

# Só abre a caixa de texto se o usuário desmarcar o "Tem cabeçalho"
if not possui_header:
    st.sidebar.info("Cole os nomes das colunas separados por vírgula.")
    texto_colunas = st.sidebar.text_area("Nomes das colunas:")
    
    if texto_colunas:
        # Limpeza dupla para tirar espaços e aspas 
        custom_columns = [c.strip().strip("'\"") for c in texto_colunas.split(',')]

arquivo1 = st.sidebar.file_uploader("Fazer uplodad do arquivo que deseja visualizar: ", type=["xlsx", "csv", "txt"])

if arquivo1 is not None:
    
    df1 = carregar_dados(arquivo1, possui_header, custom_columns)

    arquivo2 = st.sidebar.file_uploader("Fazer upload do segundo arquivo se desejar: ", type=["xlsx", "csv", "txt"])

    if arquivo2 is not None:
        #Criamos três abas 
        aba1, aba2, aba3 = st.tabs(["Arquivo 1", "Arquivo 2", "📊 Comparação"])
        
        df2 = carregar_dados(arquivo2, possui_header, custom_columns)

        with aba1:
            exibir_info(df1, arquivo1.name)
        
        with aba2:
            exibir_info(df2, arquivo2.name)
            
        with aba3:
            st.header("🔍 Comparação entre Datasets")
            
            # --- PARTE 1: COLUNAS ---
            st.subheader("1. Consistência das Colunas")
            colunas1 = set(df1.columns)
            colunas2 = set(df2.columns)
            
            if colunas1 == colunas2:
                st.success("✅ Ambos os arquivos possuem as mesmas colunas.")
            else:
                st.warning("⚠️ Atenção: As colunas não são idênticas!")
                col_so_no_1 = colunas1 - colunas2
                col_so_no_2 = colunas2 - colunas1
                if col_so_no_1: st.write(f"Apenas no Arquivo 1: `{list(col_so_no_1)}`")
                if col_so_no_2: st.write(f"Apenas no Arquivo 2: `{list(col_so_no_2)}`")

            st.divider()

            # --- PARTE 2: COLUNA ALVO ---
            st.subheader("2. Comparação da Coluna Alvo (Target)")
            
            colunas_comuns = list(colunas1.intersection(colunas2))
            
            if colunas_comuns:
                coluna_alvo = st.selectbox(
                    "Selecione a coluna alvo para comparar:", 
                    colunas_comuns, 
                    key="target_comparison"
                )
                
                # Lógica para encontrar as diferenças de valores (Target unique)
                u1 = set(df1[coluna_alvo].unique())
                u2 = set(df2[coluna_alvo].unique())
                
                c1, c2 = st.columns(2)
                
                with c1:
                    st.write(f"**Distribuição no Arquivo 1**")
                    st.write(df1[coluna_alvo].value_counts())
                    st.write(f"Valores únicos: {df1[coluna_alvo].unique()}")
                    
                    # Identifica o que só tem no Treino
                    diff1 = u1 - u2
                    if diff1: st.warning(f"Apenas no Arquivo 1: `{list(diff1)}`")
                
                with c2:
                    st.write(f"**Distribuição no Arquivo 2**")
                    st.write(df2[coluna_alvo].value_counts())
                    st.write(f"Valores únicos: {df2[coluna_alvo].unique()}")
                    
                    # Identifica o que só tem no Teste
                    diff2 = u2 - u1
                    if diff2: st.error(f"Apenas no Arquivo 2: `{list(diff2)}`")

                # Gráfico comparativo de proporção
                st.write("#### Proporção das Classes")
                p1 = df1[coluna_alvo].value_counts(normalize=True).rename("Treino")
                p2 = df2[coluna_alvo].value_counts(normalize=True).rename("Teste")
                comparativo = pd.concat([p1, p2], axis=1).fillna(0)
                st.bar_chart(comparativo)
            else:
                st.error("Não foram encontradas colunas comuns para comparar.")
    else:
        exibir_info(df1,arquivo1.name)
        

else:
    st.info("Selecione um arquivo válido para começar")
