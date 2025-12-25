databrick auth login --host https://dbc-1208c84c-e3b6.cloud.databricks.com/

databricks secrets create-scope mlops
databricks secrets put-secret mlops email_user
databricks secrets put-secret mlops email_password

sarathkumar-r@Sarathkumar:~$ databricks secrets put-acl mlops a1d40de5-02df-4307-b264-2ad65c8b51de READ
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