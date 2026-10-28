# Superstore Sales Dashboard

An interactive sales analytics dashboard built with Python and Streamlit. It helps explore sales and profit by region, category, and year, and finds where the business makes or loses money.

**Live demo:** [paste your Streamlit link here after deploying]

## Dataset
Global Superstore retail sales data (2011-2014) from Kaggle, with orders across multiple regions and product categories.

## Features
- Sidebar filters for Region, Category, and Year
- KPI cards: Total Sales, Total Profit, Profit Margin, Orders
- Sales and profit by region and category
- Monthly sales trend
- Top 10 products by sales and top 10 loss-making products
- Average profit by discount level

## Key Insights
- Central is the top region with about 740k in sales, roughly 1.6x the next region (South, about 455k).
- Monthly sales grew about 5x, from roughly 26k in early 2011 to a peak of about 137k in Nov 2014, with strong year-end peaks.
- Discounts above about 20% push average profit below zero, and it is worst at 60% discount.
- Best-sellers are not always profitable: the Samsung Smart Phone (Cordless) is #2 by sales but also among the biggest loss-makers.

## Tools Used
Python, Pandas, Plotly, Streamlit

## Run Locally
1. Install the libraries: `pip install streamlit pandas plotly`
2. Run: `python -m streamlit run app.py`
