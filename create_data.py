
import random
import pandas as pd

random.seed(42)

N = 500

first_names = [
    "Anna", "Max", "Lisa", "Tom", "Eva",
    "Paul", "Laura", "Leon", "Julia", "Felix",
    "Marie", "Lukas", "Sarah", "Jonas", "Lena",
    "Tim", "Sophie", "David", "Mia", "Ben"
]

last_names = [
    "Muller", "Schmidt", "Weber", "Fischer", "Meyer",
    "Wagner", "Becker", "Schulz", "Hoffmann", "Schneider",
    "Koch", "Bauer", "Richter", "Klein", "Wolf",
    "Schroder", "Neumann", "Schwarz", "Zimmermann", "Braun"
]

# Generate 500 baseline customer records
customers = []

for i in range(N):
    customer_id = 1001 + i

    customers.append({
        "customer_id": customer_id,
        "name": f"{random.choice(first_names)} "
                f"{random.choice(last_names)}",
        "email": f"customer{customer_id}@example.de",
        "age": random.randint(18, 85),
        "balance": round(random.uniform(100, 25000), 2)
    })

df = pd.DataFrame(customers)

# Inject controlled data quality problems.
# All row positions below are zero-based.

# 20 missing email addresses
for i in range(20, 40):
    df.loc[i, "email"] = None

# 15 invalid email addresses
for i in range(40, 55):
    df.loc[i, "email"] = f"customer{i}@invalid-email"

# 10 ages outside the configured range 18–120
invalid_ages = [16, 17, 15, 121, 130, 150, 14, 125, 12, 140]

for i, age in zip(range(60, 70), invalid_ages):
    df.loc[i, "age"] = age

# 12 negative account balances
for i in range(70, 82):
    df.loc[i, "balance"] = -round(
        random.uniform(10, 2000), 2
    )

# 8 duplicate customer IDs
# Rows 100–107 receive IDs from rows 0–7.
for target, source in zip(range(100, 108), range(0, 8)):
    df.loc[target, "customer_id"] = df.loc[source, "customer_id"]

# Save the dataset
df.to_csv("bank_customers.csv", index=False)

print("Synthetic banking dataset created.")
print(f"Total records: {len(df)}")
print("Injected issues:")
print("- Missing emails: 20")
print("- Invalid emails: 15")
print("- Ages outside 18–120: 10")
print("- Negative balances: 12")
print("- Duplicate customer IDs: 8 duplicate pairs")
print("File: bank_customers.csv")
