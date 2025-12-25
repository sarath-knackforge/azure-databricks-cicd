
#############################################################################
# This is for customer onboard and schema creation and permission
#############################################################################

# Create main catalog if not exists (only if you don’t already have one)
CREATE CATALOG IF NOT EXISTS mlops_dev;

# Create a platform schema to store control tables
CREATE SCHEMA IF NOT EXISTS mlops_dev.platform;

# Create customer db table to enroll new customer uisng [ DELTA TABLE ]
CREATE TABLE IF NOT EXISTS mlops_dev.platform.customers_master (

  customer_id        STRING NOT NULL COMMENT 'Unique customer ID like cust_0001',
  customer_name      STRING  COMMENT 'Display name of customer',
  schema_name        STRING  COMMENT 'Databricks schema name',
  cloud_provider     STRING  COMMENT 'aws | azure | gcp',
  data_path          STRING  COMMENT 's3:// | abfss:// | gs://',
  is_active          BOOLEAN COMMENT 'If false, pipelines skip this customer',
  onboarding_status STRING  COMMENT 'PENDING | ACTIVE | SUSPENDED',
  last_pipeline_run TIMESTAMP COMMENT 'Last successful pipeline run time',

  created_by         STRING,
  created_at         TIMESTAMP,
  updated_at         TIMESTAMP

)
USING DELTA;

# Alter table add primary key
ALTER TABLE mlops_prod.platform.customers_master
ADD CONSTRAINT customers_master_pk PRIMARY KEY (customer_id);

# Check the cusomter master table to see records
SELECT * FROM mlops_prod.platform.customers_master;

# Proivde instruction to Databrciks to default to use this catalog
USE CATALOG mlops_dev;

# Command to use current catalog to Databricks
SELECT current_catalog();

# IF BELOW CODE IS NOT WOKRING TRY TO USE NEXT CODE ( this is to grand permission to create catalog and schema to user):

GRANT USAGE ON CATALOG mlops_prod TO `sarathrkrishna96@gmail.com`;
GRANT CREATE SCHEMA ON CATALOG mlops_prod TO `sarathrkrishna96@gmail.com`;

GRANT ALL PRIVILEGES ON SCHEMA mlops_prod.platform
TO `sarathrkrishna96@gmail.com`;

GRANT ALL PRIVILEGES
ON CATALOG mlops_prod
TO `sarathrkrishna96@gmail`;

GRANT CREATE MODEL ON SCHEMA workspace.default TO `sarathrkrishna96@gmail.com`;

# Create a exampel customer in cusomer_master table to test 

INSERT INTO mlops_prod.platform.customers_master VALUES
(
  'cust_0001',
  'Acme Corporation',
  'cust_0001',
  'aws',
  's3://ml-data/acme/',
  true,
  'ACTIVE',
  NULL,
  'system',
  current_timestamp(),
  current_timestamp()
),
(
  'cust_0002',
  'Beta Analytics',
  'cust_0002',
  'azure',
  'abfss://raw@datalake.dfs.core.windows.net/beta/',
  true,
  'ACTIVE',
  NULL,
  'system',
  current_timestamp(),
  current_timestamp()
);

# to see curretn admin or current user in databricks
SELECT current_user();

# It show current metastore ( unity catalog location ( aws, gcp, azure, etc..), )
SELECT current_metastore(), current_catalog(), current_schema();

# Show list of data inside model test
SHOW TABLES IN mlops_dev.model_test;




