terraform {
  required_providers {
    databricks = {
      source  = "databricks/databricks"
      version = "1.12.0"
    }
  }
}

provider "databricks" {}

resource "databricks_catalog" "raw" {
  name    = "gabriel_augusto_santana_pereira_raw"
  comment = "RAW data catalog"
}

resource "databricks_catalog" "stg" {
  name    = "gabriel_augusto_santana_pereira_stg"
  comment = "STG data catalog"
}
