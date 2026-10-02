import pandas as pd

df = pd.read_csv("ecommerce_sales.csv")

print("Rows =", df.shape[0])
print("Columns =", df.shape[1])
df.info()
print("------------------------------------------------------------------")
print("Average number of items purchased by a single customer =",round(df["Quantity"].mean(), 2))

print("Total items sold =", df["Quantity"].sum())

print("Duplicate rows:")
print(df[df.duplicated(keep=False)].to_string())

print("Total null values in each column:")
print(df.isnull().sum())

print("Total null values in each row:")
print(df.isnull().sum(axis=1))

print("Rows containing null values:")
print(df[df.isnull().any(axis=1)])

print("Columns containing null values:")
print(df.columns[df.isnull().any()])

# DATA CLEANING
print("======================================================================")
# Remove duplicates
df.drop_duplicates(inplace=True)
df.reset_index(drop=True, inplace=True)

print("New no. of rows =", df.shape[0])
print("New no. of columns =", df.shape[1])

# Convert Date to datetime
df["Date"]=pd.to_datetime(df["Date"], errors="coerce")

# Remove invalid values
df=df[df["Unit_Price"]>0]
df=df[df["Quantity"]>0]

# Clean text
df["Product"]=df["Product"].str.strip().str.capitalize()
df["Category"]=df["Category"].str.strip().str.capitalize()
df["City"]=df["City"].str.strip().str.capitalize()
df["Payment_Method"]=df["Payment_Method"].str.strip().str.capitalize()

# Remove rows with invalid dates
df=df.dropna(subset=["Date"])

# Create Revenue column
df["Revenue"]=df["Quantity"] * df["Unit_Price"]

# TOTAL REVENUE
print("======================================================================")
total_revenue=df["Revenue"].sum()
print("Total revenue =", total_revenue)
print("Total items sold =", df["Quantity"].sum())

# TOP 10 PRODUCTS BY QUANTITY
product_quantity=(df.groupby("Product")["Quantity"].sum().sort_values(ascending=False).head(10))

print("Top 10 products by quantity sold:")
print(product_quantity)

# TOP 10 PRODUCTS BY REVENUE
product_revenue=(df.groupby("Product")["Revenue"].sum().sort_values(ascending=False).head(10))
print("Top 10 products by revenue:")
print(product_revenue)

# CATEGORY-WISE REVENUE
category_revenue=(df.groupby("Category")["Revenue"].sum().sort_values(ascending=False))

print("Category-wise revenue:")
print(category_revenue)

# AVERAGE ORDER VALUE
average_order_value=df["Revenue"].mean()
print("Average order value =", round(average_order_value, 2))

# CITY-WISE REVENUE
city_data=df.dropna(subset=["City"])
city_revenue=(city_data.groupby("City")["Revenue"].sum().sort_values(ascending=False))

print("City-wise revenue:")
print(city_revenue)
print("City generating the highest revenue:",city_revenue.index[0],"(",city_revenue.iloc[0],")")

# TOP 10 CUSTOMERS BY SPENDING
customer_data=df.dropna(subset=["Customer"])

customer_revenue =(customer_data.groupby("Customer")["Revenue"].sum().sort_values(ascending=False))

print("Top 10 customers based on spending:")
print(customer_revenue.head(10))

print("Top customer:", customer_revenue.index[0])
print("Revenue from this customer:", customer_revenue.iloc[0])

# MONTHLY REVENUE
df["Month"]=df["Date"].dt.strftime("%Y-%m")

monthly_revenue=(df.groupby("Month")["Revenue"].sum().sort_index())

print("Monthly sales:")
print(monthly_revenue)
if not monthly_revenue.empty:
    print("Month with highest sales:", monthly_revenue.idxmax())
    print("Revenue:", monthly_revenue.max())
    print("Month with lowest sales:", monthly_revenue.idxmin())
    print("Revenue:", monthly_revenue.min())
else:
    print("No valid monthly sales data available.")

# PAYMENT METHOD
payment_method =df["Payment_Method"].value_counts()

print("Payment method usage:")
print(payment_method)
if not payment_method.empty:
    print("Most common way of payment:", payment_method.index[0])

# CATEGORY-WISE QUANTITY
category_quantity =(df.groupby("Category")["Quantity"].sum().sort_values(ascending=False))

print("Category-wise quantity:")
print(category_quantity)

# CATEGORY-WISE QUANTITY + REVENUE
category_analysis=pd.DataFrame({
    "Revenue": category_revenue,
    "Quantity": category_quantity})
print("Category-wise quantity and revenue:")
print(category_analysis)

# AVERAGE ORDER VALUE BY CATEGORY
category_average_order=(df.groupby("Category")["Revenue"].mean().sort_values(ascending=False))

print("Average order value by category:")
print(category_average_order)

# CITY WITH HIGHEST AVERAGE ORDER VALUE
city_average_order=(city_data.groupby("City")["Revenue"].mean().sort_values(ascending=False))

print("City with highest average order value:")
if not city_average_order.empty:
    print(city_average_order.index[0])
    print("Average order value:",round(city_average_order.iloc[0], 2))

# CUSTOMERS WITH MORE THAN 5 ORDERS
customer_orders=(customer_data.groupby("Customer")["Order_ID"].count())
customers_more_than_5=customer_orders[customer_orders > 5]

print("Customers with more than 5 orders:")
print(customers_more_than_5)

# PRODUCTS ABOVE AVERAGE REVENUE
all_product_revenue=(df.groupby("Product")["Revenue"].sum())
average_product_revenue=all_product_revenue.mean()

products_above_average =all_product_revenue[all_product_revenue >average_product_revenue].sort_values(ascending=False)

print("Products above average product revenue:")
print(products_above_average)
print("======================================================================")
print("Project completed successfully!")
print("======================================================================")