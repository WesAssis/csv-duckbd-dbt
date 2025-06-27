import streamlit as st
import duckdb
import pandas as pd
import os
import subprocess
import csv

st.set_page_config(page_title="Pipeline CSV com dbt + DuckDB", layout="wide")
st.title("📊 Upload de CSV e transformação com dbt + DuckDB")

uploaded_file = st.file_uploader("📁 Escolha um arquivo CSV", type="csv")

if uploaded_file:
    # Detectar separador automaticamente
    uploaded_file.seek(0)
    sample = uploaded_file.read(1024).decode("utf-8")
    uploaded_file.seek(0)
    try:
        dialect = csv.Sniffer().sniff(sample)
    except csv.Error:
        st.error("❌ Não foi possível detectar o separador do CSV.")
        st.stop()

    # Ler CSV com separador detectado
    try:
        df = pd.read_csv(uploaded_file, sep=dialect.delimiter)
    except Exception as e:
        st.error(f"❌ Erro ao ler o CSV: {e}")
        st.stop()

    st.write("✅ Pré-visualização do CSV enviado:")
    st.dataframe(df)

    # Salvar CSV localmente para ingestão pelo DuckDB
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/input.csv", index=False, sep=dialect.delimiter)

    # Criar ou substituir tabela no DuckDB
    con = duckdb.connect("duckdb/database.duckdb")
    con.execute("CREATE OR REPLACE TABLE input AS SELECT * FROM read_csv_auto('data/input.csv')")
    con.close()  # fechar para liberar o arquivo para o dbt
    st.success("🦆 Tabela `input` criada no DuckDB!")

    # Executar dbt run
    st.write("⚙️ Executando `dbt run`...")
    try:
        result = subprocess.run(
            ["dbt", "run", "--profiles-dir", "."],
            cwd="dbt_project",
            capture_output=True,
            text=True,
            check=True
        )
        st.success("✅ `dbt run` concluído com sucesso!")
        st.code(result.stdout)
    except subprocess.CalledProcessError as e:
        st.error("❌ Erro ao executar `dbt run`:")
        st.write("stdout:")
        st.code(e.stdout or "<vazio>")
        st.write("stderr:")
        st.code(e.stderr or "<vazio>")
        st.stop()
    except Exception as e:
        st.error(f"⚠️ Erro inesperado ao executar `dbt run`: {e}")
        st.stop()

    # Consultar resultado da transformação
    try:
        with duckdb.connect("duckdb/database.duckdb") as con:
            df_result = con.execute("SELECT * FROM transform").df()
            st.write("📄 Resultado da tabela `transform`:")
            st.dataframe(df_result)
    except Exception as e:
        st.error(f"⚠️ Erro ao ler a tabela `transform`: {e}")
