# 🛠️ Leak Detection Analysis Dashboard

## 👋 Welcome to the Leak Detection Analysis Dashboard

This dashboard helps you analyze **likelihood values of leakage** from your data — whether it's **static (CSV/Excel)** or **real-time (from OSI-PI server)**.

---

### 🚀 Key Features

- **📁 CSV/Excel Analysis**: Upload historical data for static analysis using interactive charts.
- **🌐 Real-time Analysis**: Connect live to an OSI-PI server and analyze streaming sensor data in real time.

---

### 🛠️ How to Use

1. **Select the desired analysis mode** from the **sidebar**.
   
2. **For static analysis**:
   - Upload a **CSV** or **Excel** file containing your sensor data.
   - View the interactive visualizations and **Zn** statistics.

3. **For real-time analysis**:
   - Choose a **start date and time**.
   - The dashboard will begin streaming and visualizing the live **Zn** values.

---

## ℹ️ About Likelihood Values (Zn)

The **Zn score** represents the system’s confidence in detecting disturbances or leaks.

- **Zn** is computed using a modified **SPRT (Sequential Probability Ratio Test)** technique — designed for early and reliable detection.
- When **Zn crosses the upper threshold**, the system is confident that a leak or disturbance **has likely occurred**.
- If **Zn stays below the lower threshold**, the system is confident that **no disturbance has occurred so far**.

---

### 📝 Sample Data Files

Three sample CSV files have been included in the **core module** of this project. You can use these files for a quick **static analysis** demo. These files are based on real-time data collected from the actual field. Please note:
- **Pressure values were missing**, so we used **volume values** as pressure values since they don't affect the analysis.

Feel free to experiment with these sample files to get a feel for the application.

---

### 🖥️ Mock API and Configuration

Since many users may not have access to an **API key** for connecting to a real-time OSI-PI database, I've created a **mock API** within the main logic. This mock API will simulate a sample run of the software using mock data.

#### If you have your own API key:
- You will need to **uncomment** the relevant sections in the `api_processor.py` file located in the **core module**.
- The logic for connecting to the OSI-PI server is already in place. You only need to provide a few details such as:
  - Web ID tags of the sensors
  - Duration for updating data

These parameters can be found and configured within the `api_processor.py` file.

---

### 🚀 Running the Program Locally

To run the program locally, use the following command in your terminal:

```bash
dashboard
```

To stop the execution use Ctrl+C in the terminal. 

