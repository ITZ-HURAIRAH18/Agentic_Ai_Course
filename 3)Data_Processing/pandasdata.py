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