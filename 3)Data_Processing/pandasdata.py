import pandas as pd

data = [10, 20, 30, 40]
series = pd.Series(data, index=['a', 'b', 'c', 'd'])
print(series)

# DataFrame (2D Data)
# A two-dimensional labeled data structure, similar to a table or spreadsheet.

# Creating a DataFrame:
data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "Salary": [50000, 60000, 70000]
}
df = pd.DataFrame(data)
print(df)

# Loading Data:

# df = pd.read_csv("data.csv")  # Load CSV file
# df = pd.read_excel("data.xlsx")  # Load Excel file
# df = pd.read_json("data.json")  # Load JSON file
# Saving Data:
df.to_csv("output.csv", index=False)
# df.to_excel("output.xlsx", index=False)
# df.to_json("output.json")


# 3. DataFrame Operations

df.head()       # First 5 rows
df.tail()       # Last 5 rows
df.info()       # Summary of the DataFrame
df.describe()   # Statistical summary
df.shape        # Rows and columns count
df.columns      # List of column names
df.dtypes       # Data types of columns


# b. Selecting Data
# Column Selection

df["Name"]       # Single column as Series
df[["Name", "Age"]]  # Multiple columns as DataFrame


# ow Selection

df.iloc[0]       # First row (Index-based)
df.loc[1]        # Row by label/index
df.loc[df["Age"] > 30]  # Filtering rows


# 4. Data Manipulation
# a. Adding and Removing Columns
df["Bonus"] = df["Salary"] * 0.10  # Add new column
df.drop("Bonus", axis=1, inplace=True)  # Remove column
# b. Adding and Removing Rows
df.loc[3] = ["David", 40, 80000]  # Add new row
df.drop(3, axis=0, inplace=True)  # Remove row

# c. Sorting Data
df.sort_values("Age", ascending=False, inplace=True)  # Sort by Age descending
df.sort_values(["Salary", "Age"], ascending=[True, False])  # Sort by multiple columns



# 5. Handling Missing Data
# a. Checking for Missing Data
df.isnull().sum()  # Count of missing values in each column
# b. Filling Missing Values
df.fillna(0, inplace=True)  # Replace NaN with 0
df.fillna(df.mean(), inplace=True)  # Replace NaN with column mean
# c. Dropping Missing Values
df.dropna(inplace=True)  # Drop rows with NaN values
df.dropna(axis=1, inplace=True)  # Drop columns with NaN values



# 6. Grouping and Aggregation
# a. Grouping Data
df.groupby("Age").mean()  # Group by Age and compute mean
df.groupby("Age")["Salary"].sum()  # Sum Salary by Age
# b. Aggregation Functions
df.agg({"Age": "max", "Salary": "sum"})  # Aggregate multiple functions
df.groupby("Age").agg({"Salary": ["mean", "sum"]})  # Multiple aggregations

# 7. Merging and Joining Data
# a. Concatenation
df1 = pd.DataFrame({"ID": [1, 2, 3], "Name": ["A", "B", "C"]})
df2 = pd.DataFrame({"ID": [4, 5, 6], "Name": ["D", "E", "F"]})

result = pd.concat([df1, df2], ignore_index=True)
# b. Merging DataFrames
df1 = pd.DataFrame({"ID": [1, 2, 3], "Salary": [1000, 2000, 3000]})
df2 = pd.DataFrame({"ID": [1, 2, 4], "Bonus": [100, 200, 400]})

merged_df = df1.merge(df2, on="ID", how="inner")  # Inner join
merged_df = df1.merge(df2, on="ID", how="outer")  # Outer join

# 8. Pivot Tables & Reshaping
# a. Creating Pivot Tables
df.pivot_table(index="Name", columns="Age", values="Salary", aggfunc="sum")
# b. Melting DataFrames
df.melt(id_vars=["Name"], value_vars=["Age", "Salary"], var_name="Metric", value_name="Value")

# 10. Visualization with Pandas
import matplotlib.pyplot as plt

df["Salary"].plot(kind="bar")  # Bar chart
df.plot(x="Age", y="Salary", kind="line")  # Line chart
plt.show()