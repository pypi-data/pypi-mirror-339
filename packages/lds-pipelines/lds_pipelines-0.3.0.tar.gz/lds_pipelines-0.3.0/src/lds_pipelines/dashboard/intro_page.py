"""
Introduction page for the Z_n analyzer dashboard.
"""
import streamlit as st
import pkg_resources


def show_intro_page():
    """Display the introduction page."""
    st.title("Leak Detection Analysis Dashboard")

    st.image(pkg_resources.resource_filename('lds_pipelines.dashboard', 'static_pipeline.jpg') , use_container_width=True)

    st.markdown("""
    ## 👋 Welcome to the Leak Detection Analysis Dashboard

    This dashboard helps you analyze **likelihood values of leakage** from your data — whether it's **static (CSV/Excel)** or **real-time (from OSI-PI server)**.

    ---

    ### 🚀 Key Features

    - **📁 CSV/Excel Analysis**: Upload historical data for static analysis using interactive charts.
    - **🌐 Real-time Analysis**: Connect live to an OSI-PI server and analyze streaming sensor data in real time.

    ---

    ### 🛠️ How to Use

    1. Select the desired analysis mode from the **sidebar**.
    2. For **static analysis**:
    - Upload a CSV or Excel file containing your sensor data.
    - View the interactive visualizations and Zn statistics.
    3. For **real-time analysis**:
    - Choose a **start date and time**.
    - The dashboard will begin streaming and visualizing the live Zn values.

    ---

    ## ℹ️ About Likelihood Values (Zn)

    The **Zn score** represents the system’s confidence in detecting disturbances or leaks.

    - Zn is computed using a modified **SPRT (Sequential Probability Ratio Test)** technique — designed for early and reliable detection.
    - When **Zn crosses the upper threshold**, the system is confident that a leak or disturbance **has likely occurred**.
    - If Zn stays **below the lower threshold**, the system is confident that **no disturbance has occurred so far**.

    ---
    
    """)
    


if __name__ == "__main__":
    show_intro_page()