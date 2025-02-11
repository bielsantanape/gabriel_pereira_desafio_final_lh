# Desafio Final Lighthouse

Este repositório contém o projeto do desafio final do Lighthouse, com o desenvolvimento de um pipeline de dados utilizando o Databricks e Terraform. O objetivo é realizar a extração, transformação e carregamento (ETL) de dados do banco de dados Adventure Works (ADW) para uma estrutura organizada em camadas (raw e stg), pronta para ser consumida por ferramentas como o DBT.

A documentação está dividida em duas partes:

1. **Guia de Uso** – Explicação passo a passo sobre como configurar e executar o projeto localmente.
2. **O que foi feito** – Resumo das etapas implementadas no projeto.

---

## 1. Guia de Uso

Siga as instruções abaixo para configurar e executar o projeto em um ambiente local.

### 1.1 Clonar o Repositório

Primeiro, clone este repositório e navegue até o diretório do projeto:

    git clone https://github.com/bielsantanape/gabriel_pereira_desafio_final_lh.git
    cd gabriel_pereira_desafio_final_lh

**1.2 Criar um Ambiente Virtual**

Recomenda-se a criação de um ambiente virtual Python para isolar as dependências do projeto e evitar conflitos entre bibliotecas.

Para criar e ativar o ambiente virtual, utilize os comandos abaixo:


    python3 -m venv .venv
    source .venv/bin/activate

**1.3 Instalar as Dependências**

Com o ambiente virtual ativado, instale todas as dependências do projeto através do pip:

    pip install -r requirements.txt

Esse comando instalará todas as bibliotecas necessárias para a execução do projeto.

**1.4 Configurar Autenticação no Databricks**

O acesso ao Databricks foi configurado utilizando o Databricks CLI, que permite a interação com a plataforma diretamente do terminal.
Instalar o Databricks CLI

Se ainda não tiver o Databricks CLI instalado, execute o seguinte comando:

    pip install databricks-cli

Configurar o CLI com o Token

Configure o CLI com o token gerado no Databricks:

    databricks configure --token

Quando solicitado, insira:

    Host: A URL do seu workspace do Databricks (ex: https://<workspace-url>.cloud.databricks.com).

    Token: O token de autenticação gerado na UI do Databricks.

Essa configuração permitirá a execução de comandos no Databricks diretamente do terminal.

**1.5 Configurar o Terraform**

O Terraform foi utilizado para criar e configurar os catalogs no Databricks. Siga os passos abaixo para configurar o Terraform.
Instalar o Terraform CLI

Se ainda não tiver o Terraform instalado, siga as instruções oficiais: Instalar Terraform.
Autenticar o Terraform no Databricks

Para autenticar o Terraform no Databricks, utilize o mesmo token configurado no Databricks CLI. Certifique-se de que o token esteja definido na variável de ambiente DATABRICKS_TOKEN:

    export DATABRICKS_TOKEN="<seu-token>"

Aplicar a Configuração do Terraform

Navegue até a pasta do Terraform e aplique a configuração:

    cd terraform/
    terraform init
    terraform apply

Isso criará os catalogs gabriel_pereira_raw e gabriel_pereira_stg no Databricks.

**1.6 Configurar o Databricks Asset Bundle**

O Databricks Asset Bundle foi utilizado para organizar e automatizar a execução do pipeline de dados.
Navegar até a Pasta do Bundle

Navegue até a pasta do bundle:

    cd bundles/

Configurar o Bundle

Edite o arquivo bundle.yml para ajustar as configurações conforme necessário (ex: nome do job, agendamento, etc.).
Implantar o Bundle

Implante o bundle no Databricks (esse comando só funciona se estiver no diretório onde o bundle foi instalado):

    databricks bundle deploy

Isso criará os jobs e notebooks no Databricks conforme definido no bundle.

**1.7 Executar o Pipeline**

Após configurar o Terraform e o bundle, você pode executar o pipeline de dados.
Executar o Job de Extração

O job de extração é responsável por carregar os dados do banco de dados Adventure Works para a camada raw. Execute o job manualmente através do Databricks UI ou usando o CLI:

    databricks jobs run-now --job-id <job-id>

Executar o Job de Transformação

O job de transformação migra os dados da camada raw para a camada stg, aplicando as transformações necessárias. Execute o job manualmente:

    databricks jobs run-now --job-id <job-id>

**1.8 Adicionando Extração/Transformação de Novas Tabelas**

O bundle.yml é o arquivo principal do Databricks Asset Bundle. Ele define os jobs, tasks, clusters e outras configurações necessárias para executar o pipeline de dados. Cada job pode conter várias tasks, que são executadas em sequência.

No bundle.yml, adicione uma nova task ao job extract_adw_to_raw:
yaml

    - task_key: <nome_da_task>
      existing_cluster_id: <id_do_cluster>
      spark_python_task:
        python_file: ../scripts/extract_to_raw.py # manter o script que realiza as extrações 
        parameters:
          - --table_name= <nome_tabela>

O arquivo tables_to_transform.json contém uma lista de tabelas que devem ser transformadas. Ao adicionar o nome de uma nova tabela a essa lista, o job de transformação automaticamente processará essa tabela.

No arquivo tables_to_transform.json, adicione o nome da nova tabela:
    json


    {
        "tables": [
          "CountryRegionCurrency",
          "CreditCard",
          "Currency",
          "<nome_tabela>"
        ]
    }

Rode o comando databricks bundle deploy para as alterações surtirem efeito.

## 2. O que foi feito

Este projeto foi estruturado para realizar a extração, transformação e carregamento de dados utilizando o Databricks e o Terraform. Abaixo estão as principais etapas concluídas.
**2.1 Configuração da Infraestrutura**

O projeto Terraform foi iniciado com a criação do diretório e dos arquivos necessários. Foi gerado um token na UI do Databricks e autenticado através do Terraform CLI.

Foram criados dois catalogs no Databricks via Terraform:

    gabriel_augusto_santana_pereira_raw: Camada onde os dados extraídos são armazenados sem transformações.

    gabriel_augusto_santana_pereira_stg: Camada intermediária onde os dados passam por transformações antes de serem consumidos.

**2.2 Implementação do Databricks Asset Bundle**

O Databricks Asset Bundle foi criado para gerenciar e implantar ativos no Databricks de forma estruturada. A autenticação foi feita com o token gerado na UI do Databricks, garantindo acesso seguro à plataforma. Utilizamos a Databricks CLI para configurar e gerenciar o bundle, facilitando a automação e a orquestração dos recursos dentro do ambiente Databricks.

**2.3 Pipeline de Extração e Transformação de Dados**

As tabelas pertencentes ao departamento de sales foram extraídas através do job extract_adw_to_raw, no qual foram criadas tasks manualmente para a extração de cada uma das tabelas. Foi realizada essa separação de tasks para garantir modularidade, facilitar manutenção, não afetar a extração de outras em caso de falha, permitindo a reexecução independente de cada extração.

Essas tasks usam o script extract_to_raw.py para extrair as tabelas do banco de dados. Esse arquivo Python configura um logger para registrar os eventos, recebe o nome da tabela como parâmetro através da biblioteca argparse, inicia sessão Spark, realiza a conexão com o banco de dados e usa uma query simples de SELECT * FROM Sales.<nome_tabela> para extrair os dados, que são carregados em um DataFrame do Spark e posteriormente salvos no schema sales dentro de gabriel_augusto_santana_pereira_raw através do overwrite, que substitui todos os dados, mantendo somente os mais atualizados, como se fosse um full refresh.

As transformações foram realizadas com Spark através do job transform_adw_raw_to_stg, que usa o script transform_to_stg.py. Esse arquivo Python configura um logger para registro de eventos, carrega uma lista de tabelas a serem transformadas do arquivo tables_to_transform.json. Esse JSON foi criado para que o processo de transformação seja flexível e escalável, já que novas tabelas podem ser adicionadas ao JSON sem precisar alterar o código. Então, o script inicia sessão Spark, cria o schema stg (se não existir no Databricks), aplica transformações nos dados, incluindo padronização e renomeação de colunas, substituição de nulos, remoção de duplicatas, limpeza de espaços e adição de uma coluna transformation_date com a data atual. Após as transformações, as tabelas são salvas no catalog gabriel_augusto_santana_pereira_stg.sales, também com o overwrite.

**2.4 Pontos Importantes**

Execução Paralela das Tasks de Extração:

Quando criei as tasks de extração, todas elas executavam ao mesmo tempo, o que poderia sobrecarregar o cluster. Nesse caso, o pipeline é pequeno, então não faria tanta diferença, mas em produção isso poderia ser um problema. A solução ideal seria colocar algum limitador, como as pools da UI do Databricks, mas eu não consegui aparentemente por não ter permissão. Então, a solução temporária que encontrei foi colocar dependências entre as tasks de extração, fazendo com que rodassem em sequência. Porém, o ideal mesmo nesse caso seria setar uma pool. Então, se esse código fosse para produção, a primeira coisa que deve ser feita é remover as dependências das tasks e setar pools, até para uma melhor escalabilidade, caso novas tasks de extração sejam adicionadas.

Configuração dos Jobs de Extração e Transformação:

Ao ler o enunciado, entendi que seria necessário criar jobs distintos: um para a extração e outro para a transformação, com o job de transformação dependendo da conclusão do de extração para iniciar. Seguindo essa lógica, criei os dois jobs, mas encontrei dificuldades para configurar o trigger pela UI, provavelmente devido à falta de permissões. Testei os jobs separadamente e ambos funcionaram, mas, para garantir que o código funcionasse corretamente (sem precisar acionar o job de transformação manualmente), coloquei uma task de transformação dentro do job de extração. 
Essa task foi configurada para depender de todas as tasks de extração, garantindo que fosse executada por último, finalizando o pipeline de uma vez só. Fiquei um pouco confuso sobre o que manter no código: se era para ter os dois jobs, mesmo sem serem triggered, ou deixar somente a task de extração. Então, deixei ambos, mas comentei a task de transformação no job de extração, acreditando que deveria haver dois jobs distintos. No entanto, ainda é necessário configurar o trigger na UI do Databricks para que tudo funcione conforme o esperado.