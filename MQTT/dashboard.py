import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="IoT Temperature Dashboard",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ IoT Temperature & Humidity Monitoring Dashboard")
st.markdown("### MQTT + Arduino UNO + HiveMQ + SQLite")

# Refresh every 2 seconds
st_autorefresh(interval=2000, key="refresh")

# Database
conn = sqlite3.connect("sensor_data.db")

query = """
SELECT *
FROM sensor_data
ORDER BY id DESC
LIMIT 100
"""

df = pd.read_sql_query(query, conn)

if len(df)==0:
    st.warning("No Sensor Data Available")
    st.stop()

df = df.iloc[::-1]

latest = df.iloc[-1]

temp = latest["temperature"]
hum = latest["humidity"]
heat = latest["heat_index"]
time = latest["timestamp"]

###################################################

col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "🌡 Temperature",
    f"{temp:.2f} °C"
)

col2.metric(
    "💧 Humidity",
    f"{hum:.2f} %"
)

col3.metric(
    "🔥 Heat Index",
    f"{heat:.2f} °C"
)

col4.metric(
    "🕒 Last Update",
    str(time)[11:]
)

###################################################

c1,c2 = st.columns(2)

fig1 = px.line(
    df,
    x="timestamp",
    y="temperature",
    markers=True,
    title="Temperature Trend"
)

c1.plotly_chart(
    fig1,
    use_container_width=True
)

fig2 = px.line(
    df,
    x="timestamp",
    y="humidity",
    markers=True,
    title="Humidity Trend"
)

c2.plotly_chart(
    fig2,
    use_container_width=True
)

###################################################

fig3 = px.line(
    df,
    x="timestamp",
    y="heat_index",
    markers=True,
    title="Heat Index Trend"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

###################################################

st.subheader("Latest Sensor Readings")

st.dataframe(
    df.sort_values("id",ascending=False),
    use_container_width=True,
    height=350
)

###################################################

st.subheader("Statistics")

s1,s2,s3 = st.columns(3)

s1.info(
    f"""
Maximum Temperature

{df.temperature.max():.2f} °C
"""
)

s2.info(
    f"""
Maximum Humidity

{df.humidity.max():.2f} %
"""
)

s3.info(
    f"""
Maximum Heat Index

{df.heat_index.max():.2f} °C
"""
)