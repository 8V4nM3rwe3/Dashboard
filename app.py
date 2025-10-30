"""
Project Dashboard - Streamlit Application
Upload and analyze Excel files with requirements data.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from utils import validate_excel_file, get_filter_options

# Page configuration
st.set_page_config(
    page_title="Project Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Project Dashboard")
st.markdown("Upload your Excel file to analyze requirements data")

# File uploader
uploaded_file = st.file_uploader(
    "Choose an Excel file",
    type=['xlsx', 'xls'],
    help="Upload an Excel file with required columns"
)

if uploaded_file is not None:
    # Validate and load data
    with st.spinner("Loading and validating file..."):
        is_valid, error_message, df = validate_excel_file(uploaded_file)

    if not is_valid:
        # Show error message
        st.error(error_message)
    else:
        # File is valid - clean the data
        # Convert boolean columns to proper boolean type
        if 'Reviewed' in df.columns:
            df['Reviewed'] = df['Reviewed'].map(lambda x: bool(x) if pd.notna(x) and x != '' and str(x).lower() not in ['false', 'no', '0', 'nee'] else False)

        if 'In scope' in df.columns:
            df['In scope'] = df['In scope'].map(lambda x: bool(x) if pd.notna(x) and x != '' and str(x).lower() not in ['false', 'no', '0', 'nee'] else False)

        # Detect duplicates
        duplicate_mask = df.duplicated(subset=['RBS-ID (ON)'], keep='first')
        duplicate_count = duplicate_mask.sum()

        if duplicate_count > 0:
            st.success(f"✅ File loaded successfully! {len(df)} requirements found.")
            st.warning(f"⚠️ Found {duplicate_count} duplicate entries based on RBS-ID (ON)")
        else:
            st.success(f"✅ File loaded successfully! {len(df)} requirements found. No duplicates detected.")

        # Sidebar filters
        st.sidebar.header("🔍 Filters")

        # Discipline filter
        disciplines = get_filter_options(df, 'Discipline')
        selected_discipline = st.sidebar.selectbox(
            "Discipline",
            ['All'] + disciplines
        )

        # Fase filter
        fases = get_filter_options(df, 'Fase')
        selected_fase = st.sidebar.selectbox(
            "Fase",
            ['All'] + fases
        )

        # Reviewed filter
        show_reviewed_only = st.sidebar.checkbox("Show only reviewed")

        # In scope filter
        show_in_scope_only = st.sidebar.checkbox("Show only in scope")

        # Duplicate filter
        st.sidebar.markdown("---")
        hide_duplicates = st.sidebar.checkbox(
            "Hide duplicate RBS-IDs",
            value=False,
            help=f"Remove {duplicate_count} duplicate entries (keeps first occurrence)"
        )

        # Apply filters
        filtered_df = df.copy()

        # Remove duplicates if requested
        if hide_duplicates:
            filtered_df = filtered_df[~filtered_df.duplicated(subset=['RBS-ID (ON)'], keep='first')]

        if selected_discipline != 'All':
            filtered_df = filtered_df[filtered_df['Discipline'] == selected_discipline]

        if selected_fase != 'All':
            filtered_df = filtered_df[filtered_df['Fase'] == selected_fase]

        if show_reviewed_only:
            filtered_df = filtered_df[filtered_df['Reviewed'] == True]

        if show_in_scope_only:
            filtered_df = filtered_df[filtered_df['In scope'] == True]

        # KPI Section
        st.header("📈 Key Metrics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                label="Total Requirements",
                value=len(filtered_df)
            )

        with col2:
            reviewed_count = filtered_df['Reviewed'].sum() if 'Reviewed' in filtered_df else 0
            st.metric(
                label="Reviewed",
                value=int(reviewed_count)
            )

        with col3:
            in_scope_count = filtered_df['In scope'].sum() if 'In scope' in filtered_df else 0
            st.metric(
                label="In Scope",
                value=int(in_scope_count)
            )

        with col4:
            if len(filtered_df) > 0:
                review_percentage = (reviewed_count / len(filtered_df)) * 100
            else:
                review_percentage = 0
            st.metric(
                label="Review Progress",
                value=f"{review_percentage:.1f}%"
            )

        # Data Completeness Section
        st.header("📋 Data Completeness Analysis")
        st.markdown("Track how well requirements data is being filled out in the system")

        comp_col1, comp_col2, comp_col3, comp_col4, comp_col5 = st.columns(5)

        total_reqs = len(filtered_df)

        with comp_col1:
            in_scope_complete = filtered_df['In scope'].sum() if 'In scope' in filtered_df.columns else 0
            in_scope_pct = (in_scope_complete / total_reqs * 100) if total_reqs > 0 else 0
            st.metric(
                label="In Scope",
                value=f"{int(in_scope_complete)}/{total_reqs}",
                delta=f"{in_scope_pct:.1f}%"
            )

        with comp_col2:
            has_discipline = filtered_df['Discipline'].notna().sum() if 'Discipline' in filtered_df.columns else 0
            discipline_pct = (has_discipline / total_reqs * 100) if total_reqs > 0 else 0
            st.metric(
                label="Has Discipline",
                value=f"{int(has_discipline)}/{total_reqs}",
                delta=f"{discipline_pct:.1f}%"
            )

        with comp_col3:
            has_fase = filtered_df['Fase'].notna().sum() if 'Fase' in filtered_df.columns else 0
            fase_pct = (has_fase / total_reqs * 100) if total_reqs > 0 else 0
            st.metric(
                label="Has Fase",
                value=f"{int(has_fase)}/{total_reqs}",
                delta=f"{fase_pct:.1f}%"
            )

        with comp_col4:
            has_object = filtered_df['Toegewezen aan object'].notna().sum() if 'Toegewezen aan object' in filtered_df.columns else 0
            object_pct = (has_object / total_reqs * 100) if total_reqs > 0 else 0
            st.metric(
                label="Has Object Assignment",
                value=f"{int(has_object)}/{total_reqs}",
                delta=f"{object_pct:.1f}%"
            )

        with comp_col5:
            has_definitie = filtered_df['Eis Definitie'].notna().sum() if 'Eis Definitie' in filtered_df.columns else 0
            definitie_pct = (has_definitie / total_reqs * 100) if total_reqs > 0 else 0
            st.metric(
                label="Has Eis Definitie",
                value=f"{int(has_definitie)}/{total_reqs}",
                delta=f"{definitie_pct:.1f}%"
            )

        # Charts Section
        st.header("📊 Visualizations")

        chart_col1, chart_col2 = st.columns(2)

        with chart_col1:
            st.subheader("Requirements by Discipline")
            if len(filtered_df) > 0:
                discipline_counts = filtered_df['Discipline'].value_counts().reset_index()
                discipline_counts.columns = ['Discipline', 'Count']
                fig1 = px.bar(discipline_counts, x='Discipline', y='Count',
                             color='Count', color_continuous_scale='Blues')
                fig1.update_layout(showlegend=False, height=400)
                st.plotly_chart(fig1, use_container_width=True)
            else:
                st.info("No data to display")

        with chart_col2:
            st.subheader("Requirements by Fase")
            if len(filtered_df) > 0:
                fase_counts = filtered_df['Fase'].value_counts().reset_index()
                fase_counts.columns = ['Fase', 'Count']
                fig2 = px.bar(fase_counts, x='Fase', y='Count',
                             color='Count', color_continuous_scale='Greens')
                fig2.update_layout(showlegend=False, height=400)
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.info("No data to display")

        # Data Table Section
        st.header("📋 Requirements Data")

        # Select columns to display
        display_columns = [
            'RBS-ID (ON)',
            'Eis naam',
            'Discipline',
            'Fase',
            'Reviewed',
            'In scope'
        ]

        # Filter to only columns that exist in the dataframe
        available_display_columns = [col for col in display_columns if col in filtered_df.columns]

        if len(filtered_df) > 0:
            st.dataframe(
                filtered_df[available_display_columns],
                use_container_width=True,
                height=400
            )
        else:
            st.info("No requirements match the selected filters")

        # Download Section
        st.header("⬇️ Export Data")

        # Convert dataframe to Excel
        from io import BytesIO

        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            filtered_df.to_excel(writer, index=False, sheet_name='Filtered_Data')

        excel_data = output.getvalue()

        st.download_button(
            label="📥 Download Filtered Data as Excel",
            data=excel_data,
            file_name="filtered_requirements.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

else:
    # Show instructions when no file is uploaded
    st.info("👆 Please upload an Excel file to get started")

    with st.expander("ℹ️ File Requirements"):
        st.markdown("""
        Your Excel file should have these **17 required columns:**

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

        **Note:** The sheet name can be anything (e.g., "Proceseisen", "Systeemeisen"), 
        as long as the required columns are present.
        """)