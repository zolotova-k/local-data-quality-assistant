import pandas as pd

df = pd.read_csv("bank_customers.csv")

checks = {
    "Email completeness": df["email"].notna() & df["email"].astype(str).str.strip().ne(""),
    "Email validity": df["email"].astype(str).str.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", na=False),
    "Age validity": df["age"].between(18, 120),
    "Balance rule": df["balance"] >= 0,
}

print("=== DATA QUALITY SCORECARD ===")

all_passed = 0
all_checks = 0

for name, passed in checks.items():
    passed_count = int(passed.sum())
    total = len(df)
    score = passed_count / total * 100

    all_passed += passed_count
    all_checks += total

    print(f"{name}: {score:.1f}% ({passed_count}/{total} Datensätze bestanden)")

overall_score = all_passed / all_checks * 100
duplicate_rows = int(df.duplicated(subset=["customer_id"], keep=False).sum())

print(f"\nOverall field-level score: {overall_score:.1f}%")
print(f"Datensätze mit doppelter Customer ID: {duplicate_rows} von {len(df)}")
