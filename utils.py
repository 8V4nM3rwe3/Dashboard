"""
Utility functions for the Dashboard project.
"""

import pandas as pd


def validate_excel_file(uploaded_file, sheet_name=None):
    """
    Validates that the uploaded Excel file has the correct structure.
    Works with ANY sheet name as long as required columns are present.

    Args:
        uploaded_file: File-like object from Streamlit's file_uploader
        sheet_name: (Optional) Specific sheet name to read.
                    If None, uses the first sheet in the file.

    Returns:
        tuple: (is_valid: bool, error_message: str or None, dataframe: pd.DataFrame or None)

    Example:
        # Auto-detect first sheet
        valid, error, df = validate_excel_file(uploaded_file)

        # Or specify a sheet
        valid, error, df = validate_excel_file(uploaded_file, sheet_name="Proceseisen")
    """

    # Required columns - these MUST be present
    REQUIRED_COLUMNS = [
        "RBS-ID (ON)",
        "RBS-ID (OG)",
        "Eis naam",
        "Eistekst",
        "Contractuele Toelichting",
        "Brondocument/Referentie",
        "Verwijzing naar brondocument en/of bijlage",
        "Bijlage",
        "In scope",
        "Eis Definitie",
        "Opmerking bij eisdefinitie",
        "Discipline",
        "Reviewed",
        "Opmerking validatie OG",
        "Fase",
        "Object-ID",
        "Toegewezen aan object"
    ]

    try:
        # Read the Excel file to get available sheets
        excel_file = pd.ExcelFile(uploaded_file, engine='openpyxl')

        # Determine which sheet to use
        if sheet_name is None:
            # No sheet specified - use the first sheet
            sheet_to_read = excel_file.sheet_names[0]
            info_message = f"ℹ️ Using first sheet: '{sheet_to_read}'"
        else:
            # Specific sheet requested - check if it exists
            if sheet_name not in excel_file.sheet_names:
                available_sheets = ", ".join(excel_file.sheet_names)
                return (
                    False,
                    f"❌ Sheet '{sheet_name}' not found. Available sheets: {available_sheets}",
                    None
                )
            sheet_to_read = sheet_name
            info_message = f"ℹ️ Reading sheet: '{sheet_to_read}'"

        # Read the sheet
        df = pd.read_excel(
            uploaded_file,
            sheet_name=sheet_to_read,
            engine='openpyxl'
        )

        # Check if dataframe is empty
        if df.empty:
            return (
                False,
                f"❌ Sheet '{sheet_to_read}' is empty. Please upload a file with data.",
                None
            )

        # Check for required columns
        missing_columns = []
        for col in REQUIRED_COLUMNS:
            if col not in df.columns:
                missing_columns.append(col)

        if missing_columns:
            # Show all available columns (since there might be many)
            available_cols = ", ".join(df.columns.tolist())
            missing_cols_str = "\n  • ".join(missing_columns)

            return (
                False,
                f"❌ Missing {len(missing_columns)} required column(s):\n  • {missing_cols_str}\n\n"
                f"📋 Available columns in file ({len(df.columns)} total):\n{available_cols}\n\n"
                f"📄 Sheet read: '{sheet_to_read}'",
                None
            )

        # All checks passed!
        print(info_message)  # Log which sheet was used
        print(f"✅ Validation passed: {len(df)} rows, {len(df.columns)} columns")
        return (True, None, df)

    except Exception as e:
        return (
            False,
            f"❌ Error reading Excel file: {str(e)}",
            None
        )


def get_filter_options(df, column_name):
    """
    Get unique values from a column for filter dropdown.

    Args:
        df: pandas DataFrame
        column_name: Name of the column

    Returns:
        list: Sorted list of unique values (excluding NaN)
    """
    # Check if column exists in dataframe
    if column_name not in df.columns:
        return []

    unique_values = df[column_name].dropna().unique().tolist()
    return sorted(unique_values)