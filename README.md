# 🍽 Local Food Wastage Management System

[![MySQL](https://img.shields.io/badge/MySQL-Database-orange?logo=mysql)](https://www.mysql.com/)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)](https://streamlit.io/)
![Made with VS Code](https://img.shields.io/badge/Made%20with-VS%20Code-blue?logo=visualstudiocode)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

---

## 📑 Table of Contents

- 📌 [Overview](#-overview)
- 📂 [Dataset](#-dataset)
- 🎯 [Objective](#-objective)
- 🛠 [Tools Used](#-tools-used)
- ⚙️ [Steps Implemented](#-steps-implemented)
- 📁 [Repository Contents](#-repository-contents)

---

## 📌 Overview

The **Local Food Wastage Management System** is a Data Analytics & Visualization project that uses **SQL, MySQL, and Streamlit** to analyze food donations, claims, and provider trends.  
It connects to a **MySQL database** and provides an interactive Streamlit dashboard with filters for **city, provider, food type, and meal type**, along with provider contact details for direct coordination.

---

## 📂 Dataset

The project database contains **4 main tables**:

**1. providers**

- `provider_id`: Unique ID of the provider
- `name`: Provider name
- `type`: Provider type (Restaurant, Grocery Store, etc.)
- `contact`: Contact number
- `address`: Address
- `city`: City of operation

**2. receivers**

- `receiver_id`: Unique ID of the receiver
- `name`: Receiver name
- `contact`: Contact number
- `address`: Address
- `city`: City of operation

**3. food_listings**

- `food_id`: Unique food item ID
- `food_name`: Name of the food item
- `quantity`: Quantity available
- `expiry_date`: Expiry date of the item
- `provider_id`: Provider who listed the food
- `provider_type`: Type of provider
- `location`: City/location
- `food_type`: Food category (Vegetarian, Non-Vegetarian, etc.)
- `meal_type`: Meal category (Breakfast, Lunch, Dinner, Snacks)

**4. claims**

- `claim_id`: Unique ID for the claim
- `food_id`: Claimed food item ID
- `receiver_id`: Receiver claiming the food
- `status`: Claim status (Pending, Completed, Cancelled)
- `timestamp`: Date & time of claim

---

## 🎯 Objective

- Analyze and visualize trends in **food donations, claims, and provider activity**.
- Provide **filters** for city, provider, food type, and meal type.
- Display **provider contact information** for easier coordination.
- Generate **insights** from 15 pre-defined SQL queries.

---

## 🛠 Tools Used

- **Python** — Core programming language
- **MySQL** — Relational database for storing and querying data
- **Pandas** — Data analysis and processing
- **Streamlit** — Interactive dashboard development
- **GitHub** — Version control

---

## ⚙️ Steps Implemented

1. Created MySQL database `food_wastage_mgmt_db` and defined **4 tables**.
2. Loaded data from CSV files into MySQL using `LOAD DATA INFILE`.
3. Wrote **15 SQL queries** stored in `Analysis.sql` for different analytical goals.
4. Built a **Streamlit dashboard (`app.py`)** that:
   - Connects to MySQL database
   - Loads queries from GitHub
   - Allows filtering based on city, provider, food type, and meal type
   - Displays query results in tables
5. Deployed the dashboard on **Streamlit Cloud**.

---

## 📁 Repository Contents

| File / Folder Name    | Description                                                                        |
| --------------------- | ---------------------------------------------------------------------------------- |
| 📄 `app.py`           | Streamlit application to run SQL queries and display results with filters          |
| 📄 `Analysis.sql`     | Contains 15 SQL queries for analysis of food providers, receivers, and claims      |
| 📄 `Handle Data.sql`  | SQL scripts for cleaning, updating, and validating database records                |
| 📦 `requirements.txt` | Python dependencies required to run the project                                    |
| 📝 `README.md`        | Project documentation                                                              |
| 📂 `Data/`            | Folder containing CSV datasets for food listings, providers, receivers, and claims |
| 🚫 `.gitignore`       | Specifies files and folders to be ignored by Git                                   |

---

🔗 **Live App:** _[[Streamlit App Link](https://local-foods-wastage-management.streamlit.app/)]_  
📂 **GitHub Repo:** _[[GitHub Repository Link](https://github.com/Neeraj08823/Local-Food-Wastage-Management-System)]_
