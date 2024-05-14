import os

import pandas as pd
import numpy as np

# get current working directory. Convert to text and store in cwd variable
cwd = str(os.getcwd())

# read the data files
orders = pd.read_csv(cwd + "\orders.csv")
products = pd.read_csv(cwd + '\products.csv')
orderProductsTrain = pd.read_csv(cwd + '\order_products__train.csv')
orderProductsPrior = pd.read_csv(cwd + '\order_products__prior.csv')
dept = pd.read_csv(cwd + '\departments.csv')

# Browse dataframes
orders.info()
products.info()
orderProductsTrain.info()
orderProductsPrior.info()

# create a dataframe for ordered products
orderedProducts = pd.concat(
    [orderProductsPrior, orderProductsTrain])  # Append orderProductsTrain dataframe to orderProductsPrior dataframe.
orderedProducts = pd.merge(orderedProducts, products[["product_name", "product_id", "department_id"]], on="product_id",
                           how="left")  # Add the product description in orderedProducts dataframe
orderedProducts = pd.merge(orderedProducts, dept[["department_id", "department"]], on="department_id",
                           how="left")  # Add the product department in orderedProducts dataframe

orderedProducts=orderedProducts.groupby(["product_id","product_name","department_id","department"]) # group ordered products
orderedProducts=orderedProducts["order_id"].count() # count the number of products in each group
orderedProducts=orderedProducts.reset_index()
orderedProducts.rename(columns={"order_id":"product_count"}, inplace=True)
orderedProducts=orderedProducts[["product_id","product_name","department_id","department","product_count"]]

# Create a dataframe for customer shopping pattern (by time and day)
groupedOrders = orders.groupby(["order_dow", "order_hour_of_day"])  # group orders dataframe by day week and time of day
# groupedOrdersCount = groupedOrders["order_id"].count()  # count the number of orders in each group
groupedOrders = groupedOrders[
    "order_id"].count()  # find number of orders in each group
groupedOrders = groupedOrders.reset_index()  # convert series object to a dataframe
groupedOrders.rename(columns={"order_id": "OrderCount"},
                          inplace=True)  # rename "order_id" column as "OrderCount"


# Create a dataframe to show distribution of shopping intervals
orderFreq = orders[["order_id", "days_since_prior_order"]][
    orders.days_since_prior_order > 0]  # remove initial order since there is no preceeding order
orderFreq = orderFreq.groupby("days_since_prior_order")
orderFreq = orderFreq["order_id"].count()
orderFreq = orderFreq.reset_index()
orderFreq.rename(columns={"order_id": "frequency"}, inplace=True)  # rename "order_id" column as "frequency"
orderFreq["days_since_prior_order"] = orderFreq["days_since_prior_order"].astype(int)  # convert from float to integer


# Create a dataframe to capture order, products and customer statistics
statsOrders=orders.order_id.nunique()
statsProducts=products.product_id.nunique()
statsCustomers=orders.user_id.nunique()
stats=pd.DataFrame({"Orders":statsOrders, "Products":statsProducts, "Customers":statsCustomers}, index=[0])


# Export dataframes to csv file
orderedProducts.to_csv(cwd + '\orderedProducts.csv', index=False, encoding='utf-8')
groupedOrders.to_csv(cwd + '\groupedOrders.csv', index=False, encoding='utf-8')
orderFreq.to_csv(cwd + '\orderFreq.csv', index=False, encoding='utf-8')
stats.to_csv(cwd + '\stats.csv', index=False, encoding='utf-8')
