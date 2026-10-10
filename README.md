# Lead Qualification System

## Project Overview

The Lead Qualification System is a rule-based text classification application built with Python and Streamlit.

It automatically classifies customer enquiries into three categories:

- 🔥 Hot Lead
- 🟠 Warm Lead
- ❄️ Cold Lead

The classification is based on predefined keywords, text preprocessing, scoring rules, and deterministic tie-handling logic.

## Features

- Single lead qualification
- Hot, Warm, and Cold classification
- Keyword-based scoring
- Text cleaning and normalization
- CSV and Excel file upload
- Bulk lead qualification
- Lead distribution dashboard
- Download processed results
- Manual validation results
- Accuracy calculation
- Error analysis

## Validation Results

The system was tested using 30 customer enquiries.

- Total Leads Validated: 30
- Correct Predictions: 27
- Incorrect Predictions: 3
- Validation Accuracy: 90%

The main classification errors occurred because simple keyword matching does not fully understand:

- Negation
- Conflicting customer intent
- Future buying intent
- Context around urgency keywords

## Technologies Used

- Python
- Pandas
- Streamlit
- OpenPyXL
- CSV / Excel
- Git
- GitHub

## Project Structure

```text
Lead_Qualification_System/
│
├── app.py
├── classifier.py
├── requirements.txt
├── .gitignore
└── README.md