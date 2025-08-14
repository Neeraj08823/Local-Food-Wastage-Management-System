import streamlit as st
import pandas as pd
import mysql.connector
import requests


# Get secrets
db_config = st.secrets["mysql"]


# --- MySQL connection using secrets ---
def get_connection():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"]
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
    "Q16 – Most Common Food Items & Quantities"
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

def add_filter_condition(query, column_name, filter_value):
    if not filter_value:
        return query  # no filter

    # Find if GROUP BY exists
    group_pos = query.upper().find("GROUP BY")
    if group_pos != -1:
        before_group = query[:group_pos].strip()
        after_group = query[group_pos:]
        if "WHERE" in before_group.upper():
            before_group += f" AND {column_name} LIKE '%{filter_value}%'"
        else:
            before_group += f" WHERE {column_name} LIKE '%{filter_value}%'"
        return before_group + "\n" + after_group
    else:
        if "WHERE" in query.upper():
            return query + f" AND {column_name} LIKE '%{filter_value}%'"
        else:
            return query + f" WHERE {column_name} LIKE '%{filter_value}%'"


# Apply filters dynamically — no hardcoded food_type in SQL
query = add_filter_condition(query, "city", city_filter)
query = add_filter_condition(query, "name", provider_filter)
query = add_filter_condition(query, "food_type", food_type_filter)
query = add_filter_condition(query, "meal_type", meal_type_filter)


# ---------- Run Query ----------
if st.button("Run Query"):
    conn = get_connection()
    try:
        df = pd.read_sql(query, conn)

        if "contact" in df.columns:
            st.subheader("📞 Provider Contact Information")
            st.dataframe(df[["name", "contact", "address"]])
        else:
            st.subheader("📊 Query Output")
            st.dataframe(df)

    except Exception as e:
        st.error(f"Error running query: {e}")
    finally:
        conn.close()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center;'>Food Wastage Analytics Dashboard - by Neeraj Kumar</div>",
    unsafe_allow_html=True
)
