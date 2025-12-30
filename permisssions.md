<!-- 
-- -- Create main catalog if not exists (only if you don’t already have one)
-- CREATE CATALOG IF NOT EXISTS mlops_dev;

-- sheama creation
  -- CREATE SCHEMA IF NOT EXISTS mlops_dev.model_test

-- 1. Select catalog & schema

-- USE CATALOG mlops_dev;
-- select current_catalog();

-- USE SCHEMA model_test;

-- -- 2. Create table
-- CREATE TABLE IF NOT EXISTS model_approvals (
--     run_id STRING COMMENT 'MLflow run ID',
--     model_name STRING COMMENT 'Registered model name',
--     model_version STRING COMMENT 'Model version',
--     status STRING COMMENT 'Approval status (PENDING, APPROVED, REJECTED)',
--     requested_on TIMESTAMP COMMENT 'Approval request timestamp'
-- )
-- COMMENT 'Tracks model approval lifecycle and governance status'
-- TBLPROPERTIES (
--     'delta.autoOptimize.optimizeWrite' = 'true',
--     'delta.autoOptimize.autoCompact' = 'true'
-- );


-- USE CATALOG mlops_dev;
-- USE SCHEMA model_test;

-- CREATE TABLE IF NOT EXISTS model_approvals (
--     run_id STRING,
--     model_name STRING,
--     model_version STRING,
--     status STRING,
--     requested_on TIMESTAMP
-- )
-- COMMENT 'Tracks model approval lifecycle and governance status';

-- USE CATALOG mlops_dev;
-- USE SCHEMA model_test;

-- CREATE TABLE IF NOT EXISTS training_control (
--     allow_training BOOLEAN COMMENT 'Whether model training is allowed',
--     updated_on TIMESTAMP COMMENT 'Last update timestamp'
-- )
-- COMMENT 'Global control flag to enable or disable model training';

-- GRANT ALL PRIVILEGES ON SCHEMA mlops_dev.model_test
-- TO `yours@gmail.com`;

-- GRANT ALL PRIVILEGES
-- ON CATALOG mlops_dev
-- TO `yours@gmail.com`;


-- CREATE TABLE IF NOT EXISTS mlops_prod.platform.customers_master (
--   customer_id        STRING NOT NULL,
--   customer_name      STRING,
--   schema_name        STRING,
--   cloud_provider     STRING,
--   data_path          STRING,
--   is_active          BOOLEAN,
--   onboarding_status STRING,
--   last_pipeline_run TIMESTAMP,
--   created_by         STRING,
--   created_at         TIMESTAMP,
--   updated_at         TIMESTAMP
-- )
-- USING DELTA;

-- ALTER TABLE mlops_prod.platform.customers_master
-- ADD CONSTRAINT customers_master_pk PRIMARY KEY (customer_id);



-- INSERT INTO mlops_prod.platform.customers_master VALUES
-- (
--   'cust_0001',
--   'Acme Corporation',
--   'cust_0001',
--   'aws',
--   's3://ml-data/acme/',
--   true,
--   'ACTIVE',
--   NULL,
--   'system',
--   current_timestamp(),
--   current_timestamp()
-- ),
-- (
--   'cust_0002',
--   'Beta Analytics',
--   'cust_0002',
--   'azure',
--   'abfss://raw@datalake.dfs.core.windows.net/beta/',
--   true,
--   'ACTIVE',
--   NULL,
--   'system',
--   current_timestamp(),
--   current_timestamp()
-- ); -->





databrick auth login --host https://dbc-1208c84c-e3b6.cloud.databricks.com/

databricks secrets create-scope mlops
databricks secrets put-secret mlops email_user
databricks secrets put-secret mlops email_password

sarathkumar-r@Sarathkumar:~$ databricks secrets put-acl mlops a1d40de5-02df-4307-b264-2ad65c8b51de READ  **once give permission to catalog and then we need to give all previlage access for the service principal id**
sarathkumar-r@Sarathkumar:~$ databricks secrets list-acls mlops
[
  {
    "permission": "READ",
    "principal": "a1d40de5-02df-4307-b264-2ad65c8b51de"
  },
  {
    "permission": "READ",
    "principal": "sreekrishwin.s@honeywell.com"
  }
]

# Catalog permission for GITHUB-CICD

Datarbicks -> Catalog -> permission -> Grant -> give permission ( ALL previlage to all users, OR  All Previalate to specifc User)

# Serving Engpoint permission for GITHUB-CICD

Databricks -> Serving -> Permission -> Grant -> add permission ( Add permssion to serving endpoint user)

# Github secret and host 

Add Databrick service principle Client_ID, Client_Secrets, Databricks Host in github env vairablts. 

# Add profile in datrabircks

Add profile in .databrickscfg