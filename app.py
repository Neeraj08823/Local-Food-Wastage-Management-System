import streamlit as st
import pandas as pd
import mysql.connector
import requests

# --- MySQL connection ---
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="computer",  # change
        database="food_wastage_mgmt_db"
    )

# --- Read SQL file from GitHub ---
@st.cache_data
def load_queries():
    url = "https://raw.githubusercontent.com/Neeraj08823/Local-Food-Wastage-Management-System/main/Analysis.sql"
    sql_text = requests.get(url).text
    queries = [q.strip() for q in sql_text.split(";") if q.strip()]
    return queries

# Query titles
query_titles = [
    "Q1 – Providers per City",
    "Q2 – Receivers per City",
    "Q3 – Top Food Provider by Quantity",
    "Q4 – Contact Info of Providers in a City",
    "Q5 – Receivers with Most Claims",
    "Q6 – Total Quantity of Food Available",
    "Q7 – City with Most Listings",
    "Q8 – Listings by Food Type",
    "Q9 – Most Claimed Food Items",
    "Q10 – Provider with Most Completed Claims",
    "Q11 – Claims by Status",
    "Q12 – Average Quantity per Claim by Receiver",
    "Q13 – Claims by Meal Type",
    "Q14 – Providers by Total Donated Quantity",
    "Q15 – Claims Count by City"
]

queries = load_queries()

# --- UI ---
st.title("🍽 Local Food Wastage Management – Analytics Dashboard")
selected_index = st.selectbox("Select Analysis Query", range(len(queries)), format_func=lambda i: query_titles[i])

# Optional dynamic filter example
if "City" in query_titles[selected_index]:
    city_input = st.text_input("Enter City Name", "Bengaluru")
    query = queries[selected_index].replace("'Bengaluru'", f"'{city_input}'")
else:
    query = queries[selected_index]

# Run query
if st.button("Run Query"):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()

    # Show table
    st.subheader("📊 Data Table")
    st.dataframe(df)

    # Optional chart
    if df.shape[1] == 2 and pd.api.types.is_numeric_dtype(df[df.columns[1]]):
        st.subheader("📈 Chart")
        st.bar_chart(df.set_index(df.columns[0]))
