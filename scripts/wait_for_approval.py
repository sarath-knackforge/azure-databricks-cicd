import time
import pandas as pd
import sys
from pyspark.sql import SparkSession
from pyspark.dbutils import DBUtils

spark = SparkSession.builder.getOrCreate()
dbutils = DBUtils(spark)

# ---- Read arguments from workflow ----
args = sys.argv

model_name = args[args.index("--model_name") + 1]
model_version = args[args.index("--model_version") + 1]
run_id = args[args.index("--run_id") + 1]

# Your Google Sheet CSV URL
GOOGLE_SHEET_CSV = (
    "https://docs.google.com/spreadsheets/d/e/2PACX-1vTa_8A_mZwDsAkkQeU2RSBLhQZ-lDsHj1uE_tv2QPvBigC40AogVhQOGsKcG_dm5WfQB9RAqi_j8vFM/pub?gid=0&single=true&output=csv"
)

def fetch_sheet():
    try:
        return pd.read_csv(GOOGLE_SHEET_CSV)
    except Exception as e:
        print("⚠️ Could not read sheet:", e)
        return pd.DataFrame()

print(f"🔍 Waiting for approval: run_id={run_id}")

while True:
    df = fetch_sheet()

    if df.empty:
        print("📭 Sheet empty... waiting...")
        time.sleep(15)
        continue

    # REQUIRE COLUMNS: run_id, approved_flag
    expected_cols = {"run_id", "approved_flag"}
    if not expected_cols.issubset(df.columns):
        print("⚠️ Sheet missing required columns: run_id, approved_flag")
        print("Found columns:", df.columns)
        time.sleep(10)
        continue

    # Match run_id row
    rows = df[df["run_id"].astype(str) == str(run_id)]
    flag = str(rows.iloc[-1]["approved_flag"]).strip().upper() 

    if rows.empty:
        print(f"⏳ run_id {run_id} not found yet... waiting...")
        time.sleep(15)
        continue

    print(f"🔎 Found approval flag for {run_id}: {flag}")

    if flag == "TRUE":
        print("✅ Model APPROVED — moving forward...")
        dbutils.jobs.taskValues.set(key="approval", value="APPROVED")
        break

    if flag == "FALSE":
        print("❌ Model REJECTED — stopping workflow...")
        dbutils.jobs.taskValues.set(key="approval", value="REJECTED")
        break

    print("⏳ Waiting for approval flag to become TRUE/FALSE...")
    time.sleep(30)

print("🏁 Approval check finished.")


# import time
# import pandas as pd
# import sys
# from pyspark.sql import SparkSession
# from pyspark.dbutils import DBUtils

# spark = SparkSession.builder.getOrCreate()
# dbutils = DBUtils(spark)

# # ---- Read arguments from workflow ----
# args = sys.argv

# model_name = args[args.index("--model_name") + 1]
# model_version = args[args.index("--model_version") + 1]
# run_id = args[args.index("--run_id") + 1]

# # Google Sheet Public CSV URL
# GOOGLE_SHEET_CSV = (
#     "https://docs.google.com/spreadsheets/d/e/2PACX-1vTa_8A_mZwDsAkkQeU2RSBLhQZ-lDsHj1uE_tv2QPvBigC40AogVhQOGsKcG_dm5WfQB9RAqi_j8vFM/pub?gid=0&single=true&output=csv"
# )

# def fetch_sheet():
#     try:
#         return pd.read_csv(GOOGLE_SHEET_CSV)
#     except Exception as e:
#         print("⚠️ Could not load sheet:", e)
#         return pd.DataFrame()

# # ------------------------------
# # CONFIGURATION
# # ------------------------------
# MAX_WAIT_MINUTES = 20            # 🔥 Timeout after 20 minutes
# initial_delay = 10               # start with 10 sec
# max_delay = 120                  # max wait = 2 minutes

# start_time = time.time()
# delay = initial_delay

# print(f"🔍 Waiting for approval for run_id={run_id}")

# while True:

#     # Timeout logic
#     elapsed_minutes = (time.time() - start_time) / 60.0
#     if elapsed_minutes > MAX_WAIT_MINUTES:
#         print(f"⛔ TIMEOUT: No approval received in {MAX_WAIT_MINUTES} minutes.")
#         dbutils.jobs.taskValues.set(key="approval", value="TIMEOUT")
#         break

#     df = fetch_sheet()

#     if df.empty:
#         print("📭 Empty sheet... retrying...")
#         time.sleep(delay)
#         delay = min(delay * 2, max_delay)  # Exponential backoff
#         continue

#     # Required columns
#     if not {"run_id", "approved_flag"}.issubset(df.columns):
#         print("⚠️ Sheet missing columns (run_id, approved_flag)")
#         time.sleep(delay)
#         delay = min(delay * 2, max_delay)
#         continue

#     # Match run_id
#     rows = df[df["run_id"].astype(str) == str(run_id)]

#     if rows.empty:
#         print(f"⏳ No approval row found for run_id={run_id}. Waiting...")
#         time.sleep(delay)
#         delay = min(delay * 2, max_delay)
#         continue

#     flag_raw = rows.iloc[-1]["approved_flag"]

#     # Null/Blank case
#     if pd.isna(flag_raw) or str(flag_raw).strip() == "":
#         print("⏳ Approval flag is blank... waiting...")
#         time.sleep(delay)
#         delay = min(delay * 2, max_delay)
#         continue

#     # Normalize
#     flag = str(flag_raw).strip().upper()
#     print(f"🔎 Approval flag = {flag}")

#     if flag == "TRUE":
#         print("✅ Model APPROVED")
#         dbutils.jobs.taskValues.set(key="approval", value="APPROVED")
#         break

#     if flag == "FALSE":
#         print("❌ Model REJECTED")
#         dbutils.jobs.taskValues.set(key="approval", value="REJECTED")
#         break

#     # If flag is something else (e.g., "PENDING")
#     print(f"⏳ Waiting… flag={flag}")
#     time.sleep(delay)
#     delay = min(delay * 2, max_delay)

# print("🏁 Approval check finished.")
