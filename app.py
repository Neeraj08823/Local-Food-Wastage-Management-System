import streamlit as st
import pandas as pd
import mysql.connector
import requests

# ---------- Page Config ----------
st.set_page_config(page_title="Food Wastage Dashboard", layout="wide")

# ---------- Title ----------
st.markdown(
    "<h1 style='text-align: center; font-size: 42px;'>🍜🍛♻️ Local Food Wastage Management System</h1>",
    unsafe_allow_html=True
)

# ---------- Custom CSS ----------
st.markdown("""
    <style>
    /* Make the selectbox bigger */
    div[data-baseweb="select"] {
        font-size: 20px !important;
    }
    div[data-baseweb="select"] > div {
        min-height: 55px;
    }
    /* Center column content */
    .center-col {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- MySQL Connection ----------
def get_connection():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"]
    )

# ---------- Load Queries from GitHub ----------
@st.cache_data
def load_queries():
    url = "https://raw.githubusercontent.com/Neeraj08823/Local-Food-Wastage-Management-System/main/Analysis.sql"
    sql_text = requests.get(url).text
    queries = [q.strip() for q in sql_text.split(";") if q.strip()]
    return queries

queries = load_queries()

# ---------- Query Titles ----------
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

# ---------- Filter Function ----------
def add_filter_condition(query, column_name, filter_value):
    if not filter_value:
        return query
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

# ---------- Layout ----------
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown('<div class="center-col">', unsafe_allow_html=True)

    st.markdown("<h3 style='font-weight: bold; font-size: 22px;'>📊 Select Analysis Query</h3>", unsafe_allow_html=True)
    query_choice = st.selectbox("", query_titles, label_visibility="collapsed")

    # Default filters
    city_filter, provider_filter, food_type_filter, meal_type_filter = None, None, None, None

    # Apply filters conditionally
    if query_choice == "Q3 – Top Food Provider by Quantity":
        provider_filter = st.text_input("🏪 Provider Name")

    elif query_choice == "Q4 – Contact Info of Providers by City":
        city_filter = st.text_input("🏙 City Filter")
        provider_filter = st.text_input("🏪 Provider Name")

    elif query_choice == "Q8 – Listings by Food Type":
        food_type_filter = st.text_input("🥗 Food Type")

    elif query_choice == "Q13 – Claims per Meal Type":
        meal_type_filter = st.text_input("🍽 Meal Type")

    run_query = st.button("🚀 Execute")

    st.markdown('</div>', unsafe_allow_html=True)


with col2:
    if run_query:
        query_index = query_titles.index(query_choice)
        query = queries[query_index]

        # Apply filters
        query = add_filter_condition(query, "city", city_filter)
        query = add_filter_condition(query, "name", provider_filter)
        query = add_filter_condition(query, "food_type", food_type_filter)
        query = add_filter_condition(query, "meal_type", meal_type_filter)

        st.subheader("📝 SQL Query")
        st.code(query, language="sql")

        try:
            conn = get_connection()
            df = pd.read_sql(query, conn)
            conn.close()
            st.subheader("📊 Result")
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Error running query: {e}")

# ---------- Footer ----------
st.markdown("---")
st.markdown(
    "<div style='text-align: center;'>Food Wastage Analytics Dashboard - by Neeraj Kumar</div>",
    unsafe_allow_html=True
)
