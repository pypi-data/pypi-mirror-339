import streamlit as st
from datetime import datetime
from lds_pipelines.core.api_processor import get_starting_df, get_latest_df, check_alarm, login
from lds_pipelines.visualization.plotly_charts import Plotter
from streamlit_autorefresh import st_autorefresh
from datetime import datetime, timedelta
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def show_api_page():
    st.title("🌐 Real-Time Leak Analysis")

    if 'api_running' not in st.session_state:
        st.session_state.api_running = False
        st.session_state.api_df = None
        st.session_state.api_interval = 5  # seconds
        st.session_state.leak_detected= False
        st.session_state.leak_time= None

    if not st.session_state.api_running:
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Select start date")
            start_time = st.time_input("Select start time")
        st.markdown("""---""")
        col3, col4, col5= st.columns(3)
        with col3:
            api_url= st.text_input("Enter OSI-PI API URL (optional)")
        with col4:
            api_username= st.text_input("Enter login ID (optional)")
        with col5:    
            api_password= st.text_input("Enter login password (optional)", type="password")
        st.markdown("""---""")
            
        with col2:
            pass
        start_dt = datetime.combine(start_date, start_time)
        start_iso = start_dt.isoformat()

        st.session_state.button_clicked = False

        if st.button("🚀 Start Analysis", disabled=st.session_state.button_clicked):
            if not st.session_state.api_running:
                login(api_url, api_username, api_password)
            st.session_state.button_clicked = True
            st.session_state.api_df = get_starting_df(start_iso)
            df=st.session_state.api_df
            st.session_state.api_running = True
            st.rerun()

    else:
        st_autorefresh(interval=int(st.session_state.api_interval * 1000), key="api_refresh")

        st.session_state.api_df = get_latest_df(st.session_state.api_df)
        df = st.session_state.api_df

        if st.session_state.leak_detected==False:            
            if check_alarm(df):
                leak_time= check_alarm(df)
                timestamp= leak_time- timedelta(hours=1)
                st.session_state.leak_time= timestamp
                st.session_state.leak_detected= True
                st.session_state.api_interval= 2
            
        else:
            st.warning(f'Leak has been detected at {st.session_state.leak_time}', icon="⚠️")

        plotter = Plotter()

        st.subheader("📈 Leak Likelihood")
        fig1 = plotter.create_plot(df, y1_column='min_zn')
        fig1.update_layout(uirevision="min_zn")
        st.plotly_chart(fig1, use_container_width=True)

        st.subheader("📈 Volume Fluctuations")
        fig2 = plotter.create_plot(df, y1_column='inlet_volume', y2_column='outlet_volume')
        fig2.update_layout(uirevision="volume_plot") 
        st.plotly_chart(fig2, use_container_width=True)

        st.subheader("📈 Pressure Fluctuations")
        fig3 = plotter.create_plot(df, y1_column='inlet_pressure', y2_column='outlet_pressure')
        fig3.update_layout(uirevision="pressure_plot")
        st.plotly_chart(fig3, use_container_width=True)

        if st.button("🛑 Stop"):
            st.session_state.api_running = False
            st.session_state.api_df = None
            st.rerun()


if __name__ == "__main__":
    pass
