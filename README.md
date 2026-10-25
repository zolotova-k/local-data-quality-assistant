# Local Data Quality Assistant

A local AI-assisted prototype for detecting and explaining data quality issues in synthetic banking customer data.

## Project Overview

The project combines deterministic Python-based data validation with a locally running Large Language Model (LLM). Python detects data quality violations and calculates metrics, while the LLM generates explanations and suggests possible next steps.

The goal is to explore how local LLMs, Python tools and instruction-based Skills can work together in a data quality workflow.

## Architecture

1. **Data generation:** `create_data.py` creates a reproducible dataset of 500 synthetic banking customers with deliberately introduced data quality issues.
2. **Data validation:** `check_quality.py` checks the dataset against predefined validation rules.
3. **Quality metrics:** `scorecard.py` calculates completeness, validity and overall field-level quality metrics.
4. **Issue selection:** `agent.py` uses Python to select prioritized findings from the validation report.
5. **Skill instructions:** `skills/data-quality/SKILL.md` provides domain-specific instructions for the LLM.
6. **AI explanations:** A locally running Gemma 3 1B model, accessed through Ollama, explains the selected findings.
7. **Verified output:** Python findings and quality metrics are displayed separately from the LLM-generated explanations.

## Data Quality Checks

The synthetic dataset includes deliberately introduced issues such as:

- Missing and invalid email addresses
- Duplicate customer IDs
- Ages outside the configured range of 18–120
- Negative account balances

These violations are used to demonstrate data validation and reporting.

## Example Results

The 500-record dataset produces the following metrics:

| Metric | Result |
|---|---:|
| Email completeness | 96.0% |
| Email validity | 93.0% |
| Age validity | 98.0% |
| Balance rule | 97.6% |
| Overall field-level score | 96.2% |

The validation also identifies 16 records involved in duplicate customer IDs, corresponding to eight deliberately introduced duplicate pairs.

## Technology Stack

- Python
- pandas
- Ollama
- Gemma 3 1B
- CSV
- Markdown-based Skill instructions

## Running the Project

Prerequisites: Python, the required Python packages, Ollama and the locally available `gemma3:1b` model.

Generate the dataset:

```powershell
python create_data.py
```

Run the assistant:

```powershell
python agent.py
```

When prompted, enter a request such as:

```text
Analysiere die Datenqualität und erkläre die wichtigsten Probleme.
```

## Limitations

This is an experimental prototype, not a production-ready data quality platform.

- The small local LLM may omit findings, misinterpret validation rules or generate unsupported explanations.
- Tool execution and issue selection are controlled by Python; the model does not autonomously select and execute tools.
- The Python validation results and metrics are presented separately so that they remain distinguishable from AI-generated text.
- The dataset is synthetic and does not contain real customer information.
- MCP integration is not implemented in this version.

## Key Learning

The project demonstrates a practical approach to combining deterministic data validation with local LLM-based explanations. It also illustrates why AI-generated interpretations should be distinguished from verified computational results.
