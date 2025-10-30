# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Power BI-like dashboard built with Streamlit for analyzing Excel requirements data. The application provides interactive filtering, KPIs, visualizations, and data export capabilities.

**Stack:** Python, Streamlit, pandas, openpyxl, plotly

## Development Setup

1. **Activate virtual environment:**
   ```bash
   # Windows
   venv\Scripts\activate

   # Unix/MacOS
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

## Architecture

### Entry Point
- `app.py` - Main Streamlit application containing the full dashboard UI and logic

### Core Components
- `utils.py` - Utility functions for data validation and filtering
  - `validate_excel_file()`: Validates uploaded Excel files against required 17-column schema
  - `get_filter_options()`: Extracts unique values for filter dropdowns

### Data Model
The application expects Excel files with exactly **17 required columns:**
1. RBS-ID (ON)
2. RBS-ID (OG)
3. Eis naam
4. Eistekst
5. Contractuele Toelichting
6. Brondocument/Referentie
7. Verwijzing naar brondocument en/of bijlage
8. Bijlage
9. In scope
10. Eis Definitie
11. Opmerking bij eisdefinitie
12. Discipline
13. Reviewed
14. Opmerking validatie OG
15. Fase
16. Object-ID
17. Toegewezen aan object

**Sheet Name:** Any name is acceptable as long as the required columns are present (e.g., "Proceseisen", "Systeemeisen"). The first sheet is used by default.

### Key Features
1. **File Upload & Validation** - Validates Excel structure and displays detailed error messages for missing columns
2. **Dynamic Filtering** - Sidebar filters for Discipline, Fase, Reviewed status, and In scope status
3. **KPI Metrics** - Total requirements, reviewed count, in-scope count, review progress percentage
4. **Visualizations** - Bar charts showing distribution by Discipline and Fase
5. **Data Table** - Filtered requirements displayed in an interactive table
6. **Export** - Download filtered data as Excel file

## Application Flow

1. User uploads Excel file via file uploader
2. `validate_excel_file()` checks structure and returns (is_valid, error_message, dataframe)
3. If invalid, error message displayed with missing columns and available columns
4. If valid, dashboard renders with:
   - Sidebar filters (Discipline, Fase, Reviewed, In scope)
   - Four KPI metrics in columns
   - Two charts side-by-side showing distributions
   - Full data table with key columns
   - Excel export button with filtered data

## Important Notes

- `main.py` is a boilerplate PyCharm file and is not used in the application
- All boolean columns ('Reviewed', 'In scope') are expected to be proper boolean values in the Excel file
- The app uses `openpyxl` engine for reading Excel files
- Streamlit's layout is set to "wide" mode for better dashboard viewing
- Filter selections are cumulative (multiple filters applied simultaneously)
