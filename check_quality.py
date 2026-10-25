import pandas as pd
import re

df = pd.read_csv("bank_customers.csv")
issues = []

for index, row in df.iterrows():
    row_number = index + 2

    if pd.isna(row["email"]) or str(row["email"]).strip() == "":
        issues.append({
            "row": row_number,
            "customer_id": row["customer_id"],
            "dimension": "Completeness",
            "field": "email",
            "problem": "Email fehlt"
        })
    elif not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", str(row["email"])):
        issues.append({
            "row": row_number,
            "customer_id": row["customer_id"],
            "dimension": "Validity",
            "field": "email",
            "problem": "Ungültiges E-Mail-Format"
        })

    if row["age"] < 18 or row["age"] > 120:
        issues.append({
            "row": row_number,
            "customer_id": row["customer_id"],
            "dimension": "Validity",
            "field": "age",
            "problem": f"Unplausibles Alter: {row['age']}"
        })

    if row["balance"] < 0:
        issues.append({
            "row": row_number,
            "customer_id": row["customer_id"],
            "dimension": "Validity",
            "field": "balance",
            "problem": f"Negativer Kontostand: {row['balance']}"
        })

duplicates = df[df.duplicated(subset=["customer_id"], keep=False)]

for _, row in duplicates.iterrows():
    issues.append({
        "row": None,
        "customer_id": row["customer_id"],
        "dimension": "Uniqueness",
        "field": "customer_id",
        "problem": "Customer ID ist nicht eindeutig"
    })

print("\n=== DATA QUALITY REPORT ===")
print(f"Geprüfte Datensätze: {len(df)}")
print(f"Gefundene Probleme: {len(issues)}")

for issue in issues:
    print(
        f"[{issue['dimension']}] "
        f"Customer {issue['customer_id']} | "
        f"Feld: {issue['field']} | "
        f"{issue['problem']}"
    )

pd.DataFrame(issues).to_csv("data_quality_report.csv", index=False)
print("\nBericht gespeichert: data_quality_report.csv")
