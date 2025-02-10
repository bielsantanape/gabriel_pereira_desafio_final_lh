output "raw_catalog_id" {
  value = databricks_catalog.raw.id
}

output "stg_catalog_id" {
  value = databricks_catalog.stg.id
}