import pandas as pd
import ollama

report = pd.read_csv("data_quality_report.csv")

print("=== DATA QUALITY METRICS ===")
print(f"Geprüfte Datensätze: 6")
print(f"Gefundene Regelverletzungen: {len(report)}")
print("\nVerletzungen nach Dimension:")
print(report.groupby("dimension").size().to_string())

problem_types = (
    report[["dimension", "field", "problem"]]
    .drop_duplicates()
    .to_string(index=False)
)

prompt = f"""
Du bist ein Data-Quality-Analyst in einer Bank.

Die folgenden Problemtypen wurden durch Python-Regeln erkannt:

{problem_types}

Erkläre auf Deutsch:
1. Welche Bedeutung haben diese Problemtypen?
2. Welche möglichen Risiken entstehen für Datenmanagement und Reporting?
3. Welche konkreten Maßnahmen sind sinnvoll?

Wichtige Regeln:
- Erfinde keine Zahlen, Kunden, IDs oder zusätzliche Fehler.
- Wiederhole keine Anzahl von Fehlern.
- Unterscheide technische Fehler von fachlichen Auffälligkeiten.
- Ein negativer Kontostand ist nicht automatisch falsch.
- Schlage vor, Fehlerursachen zu untersuchen, statt Daten blind zu verändern.
- Halte die Antwort kurz und strukturiert.
"""

response = ollama.chat(
    model="gemma3:1b",
    messages=[{"role": "user", "content": prompt}]
)

print("\n=== AI INTERPRETATION ===\n")
print(response["message"]["content"])
