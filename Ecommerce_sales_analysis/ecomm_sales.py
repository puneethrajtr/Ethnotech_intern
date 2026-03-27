import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("Sales_analysis.csv")

# Convert date column
df['OrderDate'] = pd.to_datetime(df['OrderDate'])

# Create Revenue column
df['Revenue'] = df['Price'] * df['Quantity']

# =========================
# 1. Monthly Revenue Trend
# =========================
df['Month'] = df['OrderDate'].dt.to_period('M')

monthly_revenue = df.groupby('Month')['Revenue'].sum()

plt.figure()
monthly_revenue.plot(kind='line', marker='o')
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# =========================
# 2. Top Selling Products
# =========================
product_sales = df.groupby('Product')['Quantity'].sum()

plt.figure()
product_sales.plot(kind='bar')
plt.title("Top Selling Products")
plt.xlabel("Product")
plt.ylabel("Quantity Sold")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# =========================
# 3. Revenue by Category
# =========================
category_revenue = df.groupby('Category')['Revenue'].sum()

plt.figure()
category_revenue.plot(kind='pie', autopct='%1.1f%%')
plt.title("Revenue by Category")
plt.ylabel("")
plt.tight_layout()
plt.show()

# =========================
# 4. City-wise Revenue
# =========================
city_revenue = df.groupby('City')['Revenue'].sum()

plt.figure()
city_revenue.plot(kind='bar')
plt.title("Revenue by City")
plt.xlabel("City")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# =========================
# 5. Top Customers
# =========================
customer_spending = df.groupby('CustomerID')['Revenue'].sum().sort_values(ascending=False)

plt.figure()
customer_spending.head(5).plot(kind='bar')
plt.title("Top 5 Customers by Spending")
plt.xlabel("Customer ID")
plt.ylabel("Revenue")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

# =========================
# 6. Order Count per Customer
# =========================
order_count = df.groupby('CustomerID')['OrderID'].count()

plt.figure()
order_count.plot(kind='hist')
plt.title("Order Frequency Distribution")
plt.xlabel("Number of Orders")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

print("Dashboard Generated Successfully!")