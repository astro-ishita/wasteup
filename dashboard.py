
import streamlit as st
import pandas as pd
import plotly.express as px

# PAGE CONFIGURATION
@st.cache_data #to catch data so it doesn't reload every time
def load_data():
    df = pd.read_csv("factory_waste_data.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    # Ensure anomaly is a real boolean (CSV may load it as string)
    if df['anomaly'].dtype == object:
        df['anomaly'] = df['anomaly'].astype(str).str.lower().map({'true': True, 'false': False})
    return df

df = load_data()

#SIDEBAR FILTERS
st.sidebar.image("https://via.placeholder.com/200x60/0D9E76/FFFFFF?text=WasteUp", width=200)
st.sidebar.markdown("## Filter Data")

machines = st.sidebar.multiselect(
    "Machines",
    options=df['Machine'].unique(),
    default=df['Machine'].unique()
)

shifts = st.sidebar.multiselect(
    "Shifts",
    options=df['Shift'].unique(),
    default=df['Shift'].unique()
)

show_anomalies = st.sidebar.checkbox("Show Anomalies Only", value=False)


#FILTER DATA
filtered = df[df['Machine'].isin(machines) & df["Shift"].isin(shifts)]
if show_anomalies:
    filtered = filtered[filtered['anomaly'] == True]

#HEADER
st.title("Waste Intelligence Dashboard")
st.markdown(f"**Factory:** {df['factory'].iloc[0]} | **Period:** {df['Date'].min().date()} - {df['Date'].max().date()}")
st.divider()

#KPI Cards
col1, col2, col3, col4 = st.columns(4)

total_waste = filtered["Waste (kg)"].sum()
avg_daily = filtered.groupby("Date")["Waste (kg)"].sum().mean()
anomaly_count = int(filtered["anomaly"].sum())
top_machine = filtered.groupby("Machine")["Waste (kg)"].sum().idxmax() if not filtered.empty else "N/A"

col1.metric("Total Waste (KG)", f"{total_waste:.1f}")
col2.metric("Avg Daily Waste (KG)", f"{avg_daily:.1f}")
col3.metric("Anomalies Detected", f"{anomaly_count}")
col4.metric("Highest Waste Machine", top_machine)

st.divider()

#CHARTS
left, right = st.columns(2)

#WASTE BY MACHINE (BAR CHART)
with left:
    st.subheader("Waste by Machine (KG)")
    machine_df = filtered.groupby("Machine")["Waste (kg)"].sum().reset_index()
    fig1 = px.bar(machine_df, x="Machine", y="Waste (kg)", color="Waste (kg)",
                  color_continuous_scale="Teal",
                  labels={"Waste (kg)": "Total Waste (kg)", "Machine": ""})
    fig1.update_layout(showlegend=False, coloraxis_showscale=False)
    st.plotly_chart(fig1, use_container_width=True)


#WASTE BY SHIFT (PIE CHART)
with right:
    st.subheader("Waste By Shift")
    shift_df = filtered.groupby("Shift")["Waste (kg)"].sum().reset_index()
    fig2 = px.pie(shift_df, names="Shift", values="Waste (kg)",
                  color_discrete_sequence=["#0D9E76", "#5DCAA5", "#0A7A5A"])
    st.plotly_chart(fig2, use_container_width=True)

#DAILY WASTE TREND (LINE CHART)
st.subheader("Daily Waste Trend (KG)")
daily_df = filtered.groupby("Date")["Waste (kg)"].sum().reset_index()
fig3 = px.line(daily_df, x="Date", y="Waste (kg)", markers=True,
               labels={"Waste (kg)": "Total Waste (KG)", "Date": ""},
               color_discrete_sequence=["#0D9E76"])
fig3.update_traces(line_width=2.5)
st.plotly_chart(fig3, use_container_width=True)

#ANOMALIES OVER TIME (SCATTER PLOT)
st.subheader("Anomaly Events")
anomalies = filtered[filtered["anomaly"] == True].sort_values("Waste (kg)", ascending=False)
if len(anomalies) > 0:
    st.dataframe(anomalies[["Date", "Machine", "Shift", "Waste Type", "Waste (kg)"]],
                 use_container_width=True)
else:
    st.info("No anomalies detected for the selected filters.")

#FOOTER
st.divider()
st.caption("© 2026 WasteUp. All rights reserved. | Data last updated: 07.05.2026")
