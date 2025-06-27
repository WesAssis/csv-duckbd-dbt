instalar:
	poetry install

dbt_run:
	poetry run dbt run

dbt_test:
	poetry run dbt test

limpar:
	rm -rf dbt_modules target
