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

# Query Titles (Match exactly with file order)
query_titles = [
    "Q1 – Providers per City",
    "Q2 – Receivers per City",
    "Q3 – Top Food Provider by Quantity",
    "Q4 – Contact Info of Providers by City",
    "Q5 – Receivers with Most Claims",
    "Q6 – Total Quantity of Food Available",
    "Q7 – City with Most Listings",
    "Q8 – Listings by Food Type",
    "Q9 – Claims per Food Item",
    "Q10 – Provider with Most Completed Claims",
    "Q11 – Claims by Status (%)",
    "Q12 – Avg Quantity per Claim by Receiver",
    "Q13 – Claims per Meal Type",
    "Q14 – Providers by Total Donated Quantity",
    "Q15 – Claims Count by City",
    "Q16 – Pending Claims Older than 2 Days",
    "Q17 – Most Common Food Items & Quantities"
]

queries = load_queries()

# ---------- Streamlit UI ----------
st.set_page_config(page_title="Food Wastage Analytics", layout="wide")
st.title("🍽♻️ Local Food Wastage Management System")
st.markdown("---")
selected_index = st.selectbox("Select Analysis Query", range(len(queries)), format_func=lambda i: query_titles[i])
query = queries[selected_index]

# ---------- Sidebar Filters ----------
st.sidebar.header("🔍 Filters")
city_filter = st.sidebar.text_input("City")
provider_filter = st.sidebar.text_input("Provider Name")
food_type_filter = st.sidebar.text_input("Food Type")
meal_type_filter = st.sidebar.text_input("Meal Type")

# ---------- Apply Filters ----------
def add_filter_condition(query, column, value):
    if not value or column.lower() not in query.lower():
        return query
    if "group by" in query.lower():
        # If already has HAVING, add AND, else start HAVING
        if "having" in query.lower():
            query += f" AND {column} LIKE '%{value}%'"
        else:
            query += f" HAVING {column} LIKE '%{value}%'"
    else:
        if "where" in query.lower():
            query += f" AND {column} LIKE '%{value}%'"
        else:
            query += f" WHERE {column} LIKE '%{value}%'"
    return query

# Apply filters
query = add_filter_condition(query, "city", city_filter)
query = add_filter_condition(query, "name", provider_filter)
query = add_filter_condition(query, "food_type", food_type_filter)
query = add_filter_condition(query, "meal_type", meal_type_filter)



# ---------- Run Query ----------
if st.button("Run Query"):
    conn = get_connection()
    try:
        df = pd.read_sql(query, conn)

        # Show provider contact info if present
        if "contact" in df.columns:
            st.subheader("📞 Provider Contact Information")
            st.dataframe(df[["name", "contact", "address"]])
            st.markdown("---")

        st.subheader("📊 Query Output")
        st.dataframe(df)

    except Exception as e:
        st.error(f"Error running query: {e}")
    finally:
        conn.close()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center;'>Food Wastage Analytics Dashboard --- by Neeraj Kumar</div>",
    unsafe_allow_html=True
)

