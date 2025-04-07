"""
CSV/Excel analysis page for the Z_n analyzer dashboard.
"""

import streamlit as st
import pandas as pd
import tempfile
import os
from lds_pipelines.visualization.plotly_charts import Plotter
from lds_pipelines.core.csv_processor import calculate_zn_values
from lds_pipelines.core.api_processor import check_alarm
from datetime import datetime, timedelta

def show_csv_page():
    st.title("📁 CSV/Excel Data Analysis")

    st.markdown("""
    Upload a CSV or Excel file containing your static data to analyze time-based metrics.

    The file should have the following columns:
    - `timestamps`: Date and time of the measurement is ISO format
    - `inlet_volume`, `inlet_pressure`, `outlet_volume`, `outlet_pressure`.
    """)

    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xls", "xlsx"])

    if uploaded_file is not None:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[-1]) as temp_file:
                temp_file.write(uploaded_file.getvalue())
                temp_path = temp_file.name

            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(temp_path)
            else:
                df = pd.read_excel(temp_path)

            os.unlink(temp_path)

            df['timestamps'] = pd.to_datetime(df['timestamps'])
            df = df.sort_values('timestamps').reset_index(drop=True)
            df= calculate_zn_values(df)

            leak_time= check_alarm(df)
            if check_alarm(df):
                if len(df)>300:
                    timestamp= leak_time- timedelta(hours=1)
                else:
                    timestamp= leak_time- timedelta(minutes=10)
                st.warning(f'Leak has been detected in the data at: {str(timestamp)}', icon="⚠️")


            y_column= "min_zn"

            plotter = Plotter()
            fig = plotter.create_plot(df, y_column)

            st.subheader("📈 Leak Likelihood")
            st.plotly_chart(fig, use_container_width=True)

            plotter = Plotter()
            fig = plotter.create_plot(df, "inlet_volume", "outlet_volume")

            st.subheader(f"📈 Volume Fluctuations")
            st.plotly_chart(fig, use_container_width=True)

            plotter = Plotter()
            fig = plotter.create_plot(df, "inlet_pressure", "outlet_pressure")

            st.subheader(f"📈 Pressure Fluctuations")
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"❌ Please check your input data/ date: {e}")

    else:
        st.info("📤 Please upload a CSV or Excel file to begin analysis.")


if __name__ == "__main__":
    show_csv_page()
