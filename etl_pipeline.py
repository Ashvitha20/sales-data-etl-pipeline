import pandas as pd
from datetime import datetime
df= pd.read_csv("order.csv")
print("heading\n", df.head())
print(df.info())
order_null= df["order_id"].isnull().sum()
print(order_null)
print(df[df["order_id"].isnull()])
amt_null= df["amount"].isnull().sum()
print(amt_null)
print(df[df["amount"].isnull()])
df["date"] = pd.to_datetime(df["date"], errors="coerce")
print(df[df["date"].isnull()])
print(len(df))
print(df[df.duplicated()])
dcount=len(df[df.duplicated()])
print("the duplicate rows count:",dcount )
df["amount"] = df["amount"].str.strip().str.replace("$","",regex=False)
df["amount"]=pd.to_numeric(df["amount"], errors="coerce")
print(df["amount"])
flag_ano=df[df["amount"]<0]
#flag_ano.to_csv("negative.csv",index=False)
df= df[df["amount"]>0]
invalid_orders = df[
    ~df["order_id"].str.match(r"^ORD\d+$", na=False)
]
df = df[
    df["order_id"].str.match(r"^ORD\d+$", na=False)
]
print(invalid_orders)
df=df.drop_duplicates()
df.to_csv("clean_sales.csv", index=False)
print("Null order IDs:", order_null)
print("Null amount rows:", amt_null)
print("Duplicate rows:", dcount)
print("Negative amount rows:", len(flag_ano))
print("Invalid order IDs:", len(invalid_orders))
print("Final clean rows:", len(df))

# Create report dictionary
report = {
    "null_order_ids": order_null,
    "null_amounts": amt_null,
    "duplicate_rows": dcount,
    "negative_rows": len(flag_ano),
    "invalid_order_ids": len(invalid_orders),
    "final_clean_rows": len(df)
}

# Convert report to dataframe
report_df = pd.DataFrame([report])

# Export report CSV
report_df.to_csv("data_quality_report.csv", index=False)

print("Data quality report created successfully!")
