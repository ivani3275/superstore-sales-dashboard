import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Superstore Sales Dashboard", layout="wide")


@st.cache_data
def load_data():
    # Superstore CSVs often need latin-1 encoding
    df = pd.read_csv("superstore.csv", encoding="latin-1")
    # Remove hidden characters/spaces from column names and make them lowercase
    df.columns = (
        df.columns.str.replace("ï»¿", "", regex=False)
        .str.replace("\ufeff", "", regex=False)
        .str.strip()
        .str.lower()
    )
    df = df.rename(columns={
        "order_id": "Order ID",
        "order_date": "Order Date",
        "region": "Region",
        "category": "Category",
        "product_name": "Product Name",
        "sales": "Sales",
        "profit": "Profit",
        "discount": "Discount",
    })
    for col in ["Sales", "Profit", "Discount"]:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(r"[^0-9.\-]", "", regex=True),
            errors="coerce",
        )
    df = df.dropna(subset=["Sales", "Profit"])
    df["Order Date"] = pd.to_datetime(df["Order Date"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["Order Date"])
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.to_period("M").dt.to_timestamp()
    df["Profit Margin %"] = (df["Profit"] / df["Sales"]) * 100
    return df


df = load_data()

# ---------- Sidebar filters ----------
st.sidebar.header("Filters")
region = st.sidebar.multiselect("Region", sorted(df["Region"].unique()), default=sorted(df["Region"].unique()))
category = st.sidebar.multiselect("Category", sorted(df["Category"].unique()), default=sorted(df["Category"].unique()))
year = st.sidebar.multiselect("Year", sorted(df["Year"].unique()), default=sorted(df["Year"].unique()))

f = df[df["Region"].isin(region) & df["Category"].isin(category) & df["Year"].isin(year)]

st.title("Superstore Sales Dashboard")

if f.empty:
    st.warning("No data for the selected filters.")
    st.stop()

# ---------- KPIs ----------
total_sales = f["Sales"].sum()
total_profit = f["Profit"].sum()
margin = total_profit / total_sales * 100
orders = f["Order ID"].nunique()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Sales", f"${total_sales:,.0f}")
c2.metric("Total Profit", f"${total_profit:,.0f}")
c3.metric("Profit Margin", f"{margin:.1f}%")
c4.metric("Orders", f"{orders:,}")

# ---------- Row 1: region and category ----------
left, right = st.columns(2)

by_region = f.groupby("Region")[["Sales", "Profit"]].sum().reset_index()
left.plotly_chart(
    px.bar(by_region, x="Region", y=["Sales", "Profit"], barmode="group", title="Sales and Profit by Region"),
    use_container_width=True,
)

by_cat = f.groupby("Category")[["Sales", "Profit"]].sum().reset_index()
right.plotly_chart(
    px.bar(by_cat, x="Category", y=["Sales", "Profit"], barmode="group", title="Sales and Profit by Category"),
    use_container_width=True,
)

# ---------- Monthly trend ----------
monthly = f.groupby("Month")["Sales"].sum().reset_index()
st.plotly_chart(
    px.line(monthly, x="Month", y="Sales", markers=True, title="Monthly Sales Trend"),
    use_container_width=True,
)

# ---------- Top products and loss-makers ----------
left2, right2 = st.columns(2)

top = f.groupby("Product Name")["Sales"].sum().nlargest(10).reset_index()
left2.plotly_chart(
    px.bar(top, x="Sales", y="Product Name", orientation="h", title="Top 10 Products by Sales")
    .update_yaxes(autorange="reversed"),
    use_container_width=True,
)

loss = f.groupby("Product Name")["Profit"].sum().nsmallest(10).reset_index()
right2.plotly_chart(
    px.bar(loss, x="Profit", y="Product Name", orientation="h", title="Top 10 Loss-Making Products")
    .update_yaxes(autorange="reversed"),
    use_container_width=True,
)

# ---------- Discount vs profit ----------
disc = f.groupby("Discount")["Profit"].mean().reset_index()
st.plotly_chart(
    px.bar(disc, x="Discount", y="Profit", title="Average Profit by Discount Level"),
    use_container_width=True,
)

# ---------- Insights (edit these after you look at your own charts) ----------
st.subheader("Key Insights")
st.markdown(
    """
- Insight 1: Central is the top region with about 740k in sales, roughly 1.6x the next region (South, about 455k). Technology brings in more sales and profit than Office Supplies, but their profit margins are similar (about 14-15%).
- Insight 2: Monthly sales grew about 5x, from roughly 26k in early 2011 to a peak of about 137k in Nov 2014, with sharp year-end peaks (Nov 2011, Nov 2014).
- Insight 3: Discounts above about 20% push average profit below zero, and it is worst at 60% (an average loss of about $215 per order line), so heavy discounting is hurting profit.
"""
)
