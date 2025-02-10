#Desafio Final Lighthouse

Este repositório contém o projeto do desafio final do Lighthouse, com o desenvolvimento do pipeline de dados utilizando o Databricks e Terraform.

A documentação está dividida em duas partes:

- Guia de Uso – Explicação passo a passo sobre como configurar e executar o projeto localmente.
- O que foi feito – Resumo das etapas implementadas no projeto.

1. Guia de Uso
Passos Iniciais

Para executar o projeto corretamente em um ambiente local, siga as instruções abaixo:
1.1 Clonar o Repositório

Execute os comandos a seguir para clonar este repositório e navegar até o diretório do projeto:

    git clone https://github.com/bielsantanape/gabriel_pereira_desafio_final_lh.git
    cd gabriel_pereira_desafio_final_lh

1.2 Criar um Ambiente Virtual

Recomenda-se a criação de um ambiente virtual Python para isolar as dependências do projeto e evitar conflitos entre bibliotecas.

Para criar e ativar o ambiente virtual, utilize os comandos abaixo:

    python3 -m venv .venv
    source .venv/bin/activate  

1.3 Instalar as Dependências

Com o ambiente virtual ativado, instale todas as dependências do projeto através do pip:

    pip install requirements.txt

Esse comando instalará todas as bibliotecas necessárias para a execução do projeto.
1.4 Configurar Autenticação no Databricks

O acesso ao Databricks foi configurado utilizando o Databricks CLI, o que permite a interação com a plataforma diretamente do terminal.

Caso ainda não tenha configurado o CLI, siga os passos abaixo:

Instale o Databricks CLI:

    pip install databricks-cli

Configure o CLI com o token gerado no Databricks:

    databricks configure --token

Insira a URL do workspace e o token de autenticação quando solicitado.

Essa configuração permitirá a execução de comandos no Databricks diretamente do terminal.
2. O que foi feito

Este projeto foi estruturado para realizar a extração, transformação e carregamento de dados utilizando o Databricks e Terraform. Abaixo estão as principais etapas concluídas:
2.1 Configuração da Infraestrutura

Foram criados dois catalogs no Databricks aravés do terraform:
- <nome_completo>_raw: Camada onde os dados extraídos são armazenados sem transformações.
- <nome_completo>_stg: Camada intermediária onde os dados passam por transformações antes de serem consumidos.

2.2 Implementação do Databricks Asset Bundle

O Databricks Asset Bundle foi configurado para organizar e automatizar a execução do pipeline de dados.
A estrutura do bundle inclui notebooks, jobs e configurações necessárias para executar o pipeline no Databricks.

2.3 Pipeline de Extração e Transformação de Dados

Os dados do banco de dados Adventure Works (ADW) foram extraídos para a camada raw utilizando jobs do Databricks.
Foram extraídas todas as tabelas pertencentes ao departamento de sales.
As transformações foram realizadas no Apache Spark, migrando os dados da camada raw para a camada stg.

2.4 Agendamento de Execução

O job de processamento dos dados foi configurado para ser executado diariamente às 6h da manhã (UTC).
Esse agendamento foi definido utilizando crontab no Databricks Bundle.

2.5 Documentação e Organização do Código

O código foi estruturado em um repositório organizado, contendo:
Uma pasta para os arquivos do Terraform.
Uma pasta para os bundles do Databricks.
Além disso, foi adicionada uma descrição detalhada sobre a execução do projeto.
