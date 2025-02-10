from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, current_date
import logging
import json

# Configuração do logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("data_transformation.log")
    ]
)
logger = logging.getLogger()

# Carregando as tabelas a partir do JSON
json_path = "../config/tables_to_transform.json"
try:
    with open(json_path, "r") as f:
        tables = json.load(f)["tables"]
    logger.info(f"Tabelas carregadas do JSON: {tables}")
except Exception as e:
    logger.error(f"Erro ao carregar JSON: {str(e)}")
    tables = []

# Inicializa a sessão do Spark
spark = SparkSession.builder.appName("Transform RAW to STG").getOrCreate()

# Criando o schema STG se não existir
spark.sql("CREATE SCHEMA IF NOT EXISTS gabriel_augusto_santana_pereira_stg.sales")

# Função para aplicar transformações genéricas
def transform_table(df, table_name):
    try:
        # Renomeia todas as colunas para lowercase
        df = df.select([col(c).alias(c.lower()) for c in df.columns])

        # Renomeia a coluna 'modifieddate' para 'ModifiedDate' (se necessário)
        if "modifieddate" in df.columns:
            df = df.withColumnRenamed("modifieddate", "ModifiedDate")

        # Substitui valores nulos por 0
        df = df.na.fill(0)

        # Remove linhas duplicadas
        df = df.dropDuplicates()

        # Limpeza de espaços no início e final de cada valor de coluna
        df = df.select([trim(col(c)).alias(c) for c in df.columns])

        # Adicionando a coluna com a data da transformação
        df = df.withColumn("transformation_date", current_date())

        return df
    except Exception as e:
        logger.error(f"Erro ao transformar a tabela {table_name}: {str(e)}")
        raise

# Loop para processar todas as tabelas da lista
for table_name in tables:
    try:
        logger.info(f"Começando a transformação dos dados da tabela: {table_name}...")

        # Lendo a tabela do catálogo RAW
        raw_table = spark.read.table(f"gabriel_augusto_santana_pereira_raw.sales.{table_name}")

        # Aplicando transformações
        transformed_table = transform_table(raw_table, table_name)

        # Mostra o schema e algumas linhas da tabela transformada
        transformed_table.printSchema()
        transformed_table.show(5)

        # Salvando a tabela transformada no catálogo STG
        transformed_table.write \
            .mode("overwrite") \
            .option("overwriteSchema", "true") \
            .saveAsTable(f"gabriel_augusto_santana_pereira_stg.sales.{table_name}")

        logger.info(f"Tabela {table_name} transformada e salva no catálogo STG.")

    except Exception as e:
        logger.error(f"Erro ao processar a tabela {table_name}: {str(e)}")

print("Transformação concluída para todas as tabelas.")