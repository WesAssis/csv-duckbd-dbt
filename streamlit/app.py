import streamlit as st
import duckdb
import pandas as pd
import os
import subprocess
import csv
import sys # Importar sys para encontrar o executável python correto

# --- Configuração da Página ---
st.set_page_config(page_title="Pipeline de Dados ELT", layout="wide")

st.title("📊 Pipeline ELT: CSV para Análise com dbt e DuckDB")
st.markdown("""
Esta aplicação demonstra um pipeline de dados completo:
1.  **Extract & Load (EL):** Você envia um arquivo CSV, que é carregado em uma tabela `raw_cars` no DuckDB.
2.  **Transform (T):** O `dbt` é executado para transformar os dados brutos, aplicando as regras da arquitetura Medalhão (Bronze -> Silver -> Gold).
3.  **Analysis:** Os modelos de negócio da camada **Gold** são exibidos, prontos para análise.
""")

# --- Upload do Arquivo ---
uploaded_file = st.file_uploader("📁 Escolha um arquivo CSV para iniciar o pipeline", type="csv")

if uploaded_file:
    # --- Etapa de Leitura e Validação ---
    with st.spinner("Lendo e validando o CSV..."):
        try:
            # Detectar separador automaticamente para maior flexibilidade
            uploaded_file.seek(0)
            sample = uploaded_file.read(1024).decode("utf-8")
            uploaded_file.seek(0)
            dialect = csv.Sniffer().sniff(sample, delimiters=[',', ';', '\t'])
            df = pd.read_csv(uploaded_file, sep=dialect.delimiter)
        except (csv.Error, pd.errors.ParserError) as e:
            st.error(f"❌ Não foi possível ler ou detectar o separador do CSV. Verifique o formato do arquivo. Erro: {e}")
            st.stop()
        except Exception as e:
            st.error(f"❌ Erro inesperado ao ler o arquivo: {e}")
            st.stop()

    st.success("✅ Arquivo CSV lido com sucesso!")
    st.write("#### Pré-visualização dos Dados Brutos:")
    st.dataframe(df.head())

    # --- Etapa de Load (Carregamento no DuckDB) ---
    with st.spinner("Carregando dados na camada Bronze do DuckDB..."):
        # Garantir que os diretórios existam
        os.makedirs("data", exist_ok=True)
        os.makedirs("duckdb", exist_ok=True)
        
        # Salvar CSV localmente para ingestão pelo DuckDB
        csv_path = "data/input.csv"
        df.to_csv(csv_path, index=False, sep=dialect.delimiter)
        
        db_path = "duckdb/database.duckdb"
        try:
            con = duckdb.connect(db_path)
            # Na arquitetura Medalhão, a primeira tabela é a 'raw'
            con.execute("CREATE SCHEMA IF NOT EXISTS bronze;")
            con.execute(f"CREATE OR REPLACE TABLE bronze.raw_cars AS SELECT * FROM read_csv_auto('{csv_path}')")
            con.close()
            st.success("🦆 Dados carregados na tabela `bronze.raw_cars` do DuckDB!")
        except Exception as e:
            st.error(f"❌ Erro ao carregar dados no DuckDB: {e}")
            st.stop()

    # --- Etapa de Transformação (dbt) ---
    st.write("---")
    st.write("#### ⚙️ Etapa de Transformação com dbt")
    
    # Função para executar comandos dbt de forma robusta
    def run_dbt_command(command):
        # Usar sys.executable garante que estamos usando o python do ambiente correto (ex: Poetry)
        # Isso evita problemas de 'dbt: command not found'
        full_command = [sys.executable, "-m", "dbt.cli.main"] + command
        
        try:
            result = subprocess.run(
                full_command,
                cwd="dbt_project", # Rodar a partir da pasta do projeto dbt
                capture_output=True,
                text=True,
                check=True
            )
            return True, result.stdout
        except subprocess.CalledProcessError as e:
            error_message = f"stdout:\n{e.stdout}\nstderr:\n{e.stderr}"
            return False, error_message
        except Exception as e:
            return False, str(e)

    # 1. Executar dbt run
    with st.spinner("Executando `dbt run`... Isso pode levar um momento."):
        success, output = run_dbt_command(["run"])
        if success:
            st.success("✅ `dbt run` concluído!")
            with st.expander("Ver logs de `dbt run`"):
                st.code(output, language="log")
        else:
            st.error("❌ Erro ao executar `dbt run`:")
            st.code(output, language="log")
            st.stop()

    # 2. Executar dbt test
    with st.spinner("Executando `dbt test` para garantir a qualidade dos dados..."):
        success, output = run_dbt_command(["test"])
        if success:
            st.success("✅ `dbt test` concluído! A qualidade dos dados está garantida.")
            with st.expander("Ver logs de `dbt test`"):
                st.code(output, language="log")
        else:
            st.error("❌ Erro nos testes de qualidade de dados (`dbt test`):")
            st.code(output, language="log")
            st.stop()

    # --- Etapa de Análise (Camada Gold) ---
    st.write("---")
    st.write("#### 🏅 Camada Gold: Modelos de Negócio Prontos para Análise")
    
    try:
        with duckdb.connect(db_path, read_only=True) as con:
            # CORREÇÃO: Consultar os nomes corretos dos modelos da camada Gold
            df_avg_price = con.execute("SELECT * FROM avg_price_by_manufacturer_year").df()
            df_mileage_segments = con.execute("SELECT * FROM car_mileage_segments").df()

            tab1, tab2 = st.tabs([
                "📈 Preço Médio por Fabricante e Ano", 
                "🚗 Segmentação por Quilometragem"
            ])

            with tab1:
                st.write("##### Análise de Tendência de Preços")
                st.dataframe(df_avg_price)
                
                # Gráfico de linhas para visualizar a tendência de preço
                st.write("Visualização de Preços ao Longo dos Anos (Fabricantes Selecionados)")
                manufacturers = st.multiselect(
                    'Selecione os fabricantes:',
                    options=df_avg_price['manufacturer'].unique(),
                    default=list(df_avg_price['manufacturer'].unique()[:3]) # Seleciona os 3 primeiros por padrão
                )
                
                if manufacturers:
                    chart_data = df_avg_price[df_avg_price['manufacturer'].isin(manufacturers)]
                    st.line_chart(
                        chart_data, 
                        x='year_of_manufacture', 
                        y='average_price_eur', 
                        color='manufacturer'
                    )

            with tab2:
                st.write("##### Perfil dos Carros por Segmento de KM")
                st.dataframe(df_mileage_segments)

                # Gráfico de barras para contagem de carros por segmento
                st.write("Contagem de Veículos por Segmento")
                segment_counts = df_mileage_segments['mileage_segment'].value_counts()
                st.bar_chart(segment_counts)

    except Exception as e:
        st.error(f"⚠️ Erro ao consultar ou visualizar os dados da camada Gold: {e}")

