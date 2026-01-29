# Data Analyzer
Site do código: <a href='https://data-analyzer-joaov0015.streamlit.app/'>
Ferramenta simples feita em Python e Streamlit para visualizar e comparar datasets de forma rápida.

### 🛠️ Funcionalidades

* **Upload de arquivos**: Suporta formatos `.csv`, `.txt` e `.xlsx`.
* **Cabeçalhos customizados**: Permite definir nomes para as colunas se o arquivo não tiver header.
* **Limpeza automática**: Remove aspas e espaços extras nos nomes das colunas.
* **Análise Visual**: Gera gráficos de correlação (Heatmap) e distribuição automaticamente.
* **Comparação**: Aba dedicada para comparar arquivos de Treino e Teste, mostrando diferenças de colunas e valores.

### 🚀 Como usar localmente

1. **Instale as dependências**:
```bash
pip install streamlit pandas seaborn matplotlib openpyxl

```


2. **Execute o projeto**:
```bash
streamlit run csv_analyzer.py

```


