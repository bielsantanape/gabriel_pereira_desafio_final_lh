import argparse
import logging
from pyspark.sql import SparkSession

# Configuração do logger para exibir apenas no console
logging.basicConfig(
    level=logging.INFO,  # Para registrar todos os níveis (INFO, ERROR, etc.)
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]  # Apenas exibe no console
)
logger = logging.getLogger()

# Configura o parser de argumentos
parser = argparse.ArgumentParser(description="Extrair dados de uma tabela do banco de dados.")
parser.add_argument("--table_name", required=True, help="Nome da tabela a ser extraída.")
args = parser.parse_args()

# Inicializa a sessão do Spark
spark = SparkSession.builder.appName("Extract Data").getOrCreate()

# Conectando ao banco de dados
jdbc_hostname = dbutils.secrets.get("gabriel_pereira_adw", "adw_db_host")
jdbc_port = dbutils.secrets.get("gabriel_pereira_adw", "adw_db_port")
jdbc_database = dbutils.secrets.get("gabriel_pereira_adw", "adw_db_database")
user_adw = dbutils.secrets.get("gabriel_pereira_adw", "adw_db_user")
passsword_adw = dbutils.secrets.get("gabriel_pereira_adw", "adw_db_password")

jdbc_url = f"jdbc:sqlserver://{jdbc_hostname}:{jdbc_port};databaseName={jdbc_database};encrypt=false"

connection_properties = {
    "user": user_adw,
    "password": passsword_adw,
    "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
}

# Nome da tabela passado como argumento
table_name = args.table_name

# Log de início da extração
logger.info(f"Iniciando a extração de dados da tabela: {table_name}...")

try:
    # Query para extrair os dados da tabela
    query_data = f"SELECT * FROM Sales.{table_name}"

    # Lê os dados da tabela do banco de dados
    table_df = spark.read \
        .format("jdbc") \
        .option("url", jdbc_url) \
        .option("query", query_data) \
        .option("user", connection_properties["user"]) \
        .option("password", connection_properties["password"]) \
        .option("driver", connection_properties["driver"]) \
        .load()

    # Log de sucesso na extração
    logger.info(f"Dados da tabela {table_name} extraídos com sucesso.")

    # Salva os dados no catalog raw no Databricks
    table_df.write.mode("overwrite").saveAsTable(f"gabriel_augusto_santana_pereira_raw.sales.{table_name}")

    # Log de sucesso ao salvar os dados
    logger.info(f"A tabela {table_name} foi salva no catálogo raw no Databricks (_raw.sales).")
    logger.info(f"Extração realizada com sucesso.")

except Exception as e:
    # Log de erro
    logger.error(f"Erro ao extrair ou salvar a tabela {table_name}: {str(e)}")