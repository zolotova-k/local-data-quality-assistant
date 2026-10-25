
import subprocess
import sys
from pathlib import Path

import pandas as pd
import ollama

BASE_DIR = Path(__file__).parent
PYTHON = sys.executable
MODEL = "gemma3:1b"


def run_tool(script_name):
    """Run a Python tool and return its output."""
    result = subprocess.run(
        [PYTHON, str(BASE_DIR / script_name)],
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    if result.returncode != 0:
        raise RuntimeError(result.stderr or f"Tool failed: {script_name}")

    return result.stdout.strip()


def select_key_issues():
    """Select predefined issue categories from actual validation results."""
    report_path = BASE_DIR / "data_quality_report.csv"
    report = pd.read_csv(report_path)

    priorities = [
        ("Uniqueness", "customer_id", "Doppelte Kunden-IDs"),
        ("Validity", "age", "Alter außerhalb des Regelbereichs"),
        ("Validity", "balance", "Negativer Kontostand"),
    ]

    selected = []

    for dimension, field, title in priorities:
        rows = report[
            (report["dimension"] == dimension)
            & (report["field"] == field)
        ]

        if rows.empty:
            continue

        details = rows[
            ["customer_id", "problem"]
        ].drop_duplicates()

        selected.append(
            f"{title} ({len(details)} unterschiedliche Befunde):\n"
            + "\n".join(
                f"- Customer {row.customer_id}: {row.problem}"
                for row in details.itertuples(index=False)
            )
        )

    return "\n\n".join(selected)



def main():
    print("=== Local Data Quality Agent ===")
    user_request = input("\nDeine Anfrage: ").strip()

    if not user_request:
        print("Bitte gib eine Anfrage ein.")
        return

    print("\n[Agent] Analysiere die Anfrage ...")

    print("[Agent] Tool ausgewählt: check_quality.py")
    run_tool("check_quality.py")

    print("[Agent] Tool ausgewählt: scorecard.py")
    scorecard_results = run_tool("scorecard.py")

    print("[Agent] Python wählt die priorisierten Befunde aus ...")
    selected_issues = select_key_issues()

    skill_path = BASE_DIR / "skills" / "data-quality" / "SKILL.md"
    skill_instructions = skill_path.read_text(encoding="utf-8-sig")

    context = f"""
Nutzeranfrage:
{user_request}

Skill-Anweisungen:
{skill_instructions}

Von Python ausgewählte Befunde:
{selected_issues}

Kennzahlen aus Python:
{scorecard_results}
"""

    print("[Agent] Gemma erstellt Erklärungen ...\n")

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Du bist ein Assistent für Datenqualität. "
                    "Antworte ausschließlich auf Deutsch. "
                    "Python hat die relevanten Probleme bereits ausgewählt. "
                    "Deine Aufgabe ist nur, diese Probleme zu erklären. "
                    "Erfinde keine zusätzlichen Befunde, IDs, Zahlen oder Ursachen. "
                    "Wiederhole keine konkreten Kunden-IDs, Alterswerte oder Salden. "
                    "Erkläre nicht erneut die Kennzahlen oder die Scorecard. "
                    "Vermische niemals unterschiedliche Prüfregeln. "
                    "Behaupte nicht, dass eine Regelverletzung automatisch "
                    "einen tatsächlichen Datenfehler beweist. "
                    "Nenne keine vermuteten Ursachen als gesicherte Tatsachen. "
                    "Gib für jede vorgegebene Problemkategorie genau zwei Punkte aus: "
                    "'Bedeutung:' mit einer kurzen allgemeinen Erklärung und "
                    "'Maßnahme:' mit einem konkreten Vorschlag. "
                    "Füge keine Einleitung, Zusammenfassung oder weitere Probleme hinzu."
                ),
            },
            {"role": "user", "content": context},
        ],
    )

    print("=== AI-Erklärungen ===\n")
    print(response.message.content)

    print("\n=== Verifizierte Befunde aus Python ===\n")
    print(selected_issues)

    print("\n=== Kennzahlen aus Python ===\n")
    print(scorecard_results)


if __name__ == "__main__":
    main()
