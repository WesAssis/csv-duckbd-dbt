# csv-duckbd-dbt

Este projeto demonstra uma arquitetura de dados moderna utilizando DuckDB para processamento de dados CSV e dbt (data build tool) para transformação e modelagem de dados. Ele inclui também uma interface Streamlit para visualização e interação com os dados transformados.



## Funcionalidades

- **Ingestão de Dados CSV**: Processa arquivos CSV de forma eficiente.
- **Transformação de Dados com dbt**: Utiliza dbt para criar camadas de dados (Bronze, Silver, Gold).
- **Armazenamento com DuckDB**: Armazena e consulta dados localmente com DuckDB.
- **Visualização com Streamlit**: Interface interativa para explorar os dados transformados.
- **Orquestração**: Automatiza o fluxo de trabalho de dados.



## Estrutura do Projeto

O projeto está organizado da seguinte forma:

- `data/`: Contém os arquivos CSV de entrada.
- `dbt_project/`: Contém os modelos dbt para transformação de dados.
  - `models/`: Modelos SQL que definem as camadas Bronze, Silver e Gold.
- `duckdb/`: Configurações e scripts relacionados ao DuckDB.
- `ingestao/`: Scripts para ingestão de dados CSV para o DuckDB.
- `streamlit/`: Aplicação Streamlit para visualização de dados.
- `logs/`: Logs de execução do projeto.
- `Makefile`: Contém comandos para automatizar tarefas como instalação de dependências, execução de pipelines e inicialização da aplicação Streamlit.
- `pyproject.toml`: Define as dependências do projeto e metadados.



## Instalação

Para configurar e executar este projeto localmente, siga os passos abaixo:

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/wesassis/csv-duckbd-dbt.git
    cd csv-duckbd-dbt
    ```

2.  **Instale as dependências:**

    Este projeto utiliza [Poetry](https://python-poetry.org/) para gerenciamento de dependências. Se você não o tem instalado, siga as instruções em sua documentação.

    ```bash
    poetry install
    ```

3.  **Ative o ambiente virtual:**

    ```bash
    poetry shell
    ```

4.  **Configuração do DuckDB e dbt:**

    As configurações para DuckDB e dbt estão incluídas no projeto. Não é necessária nenhuma configuração manual adicional, pois o dbt será configurado para usar o DuckDB automaticamente.



## Uso

Para executar o pipeline de dados e a aplicação Streamlit, utilize os comandos definidos no `Makefile`:

1.  **Executar o pipeline de dados (ingestão e dbt):**

    ```bash
    make run-pipeline
    ```

    Este comando irá:
    - Ingerir os dados CSV para o DuckDB.
    - Executar os modelos dbt para criar as camadas Bronze, Silver e Gold.

2.  **Iniciar a aplicação Streamlit:**

    ```bash
    make run-streamlit
    ```

    Após a execução, a aplicação Streamlit estará disponível no seu navegador (geralmente em `http://localhost:8501`).

