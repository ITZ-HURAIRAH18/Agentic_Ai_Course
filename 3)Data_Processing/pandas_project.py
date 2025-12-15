# Project 1: IMDb Movie Data Analysis

# Objective:
# Analyze IMDb movie data to find top-rated movies, most popular genres, and trends over the years.

# import pandas as pd
# import matplotlib.pyplot as plt

# Load dataset

# df = pd.read_csv("imdb-top-1000.csv")

# # Display first few rows
# print(df.head())

# # Convert 'Released_Year' column to numeric
# df['Released_Year'] = pd.to_numeric(df['Released_Year'], errors='coerce')

# # Top 10 highest-rated movies
# top_movies = df[['Series_Title', 'IMDB_Rating']].sort_values(by='IMDB_Rating', ascending=False).head(10)
# print("\nTop 10 Highest-Rated Movies:\n", top_movies)

# # Count movies by genre
# df['Genre'] = df['Genre'].apply(lambda x: x.split(',')[0])  # Take first genre if multiple
# genre_counts = df['Genre'].value_counts()

# # Plot genres
# plt.figure(figsize=(10,5))
# genre_counts.head(10).plot(kind='bar', color='skyblue')
# plt.title("Top 10 Movie Genres in IMDb Dataset")
# plt.xlabel("Genre")
# plt.ylabel("Number of Movies")
# plt.xticks(rotation=45)
# plt.show()

# # Trend of movies released over years
# df.groupby('Released_Year').size().plot(kind='line', figsize=(10,5), color='red', marker='o')
# plt.title("Movies Released Over the Years")
# plt.xlabel("Year")
# plt.ylabel("Number of Movies")
# plt.grid()
# plt.show()



#  Project 2: Stock Market Data Analysis
# Objective:
# Analyze stock price data, calculate moving averages, and visualize stock trends.


# import pandas as pd
# import matplotlib.pyplot as plt

# df = pd.read_csv('stock.csv')

# # Strip spaces from column names
# df.columns = df.columns.str.strip()

# # Convert 'Date' column to datetime
# df['Date'] = pd.to_datetime(df['Date'])

# # Convert numerical columns (remove '$' and ',' before converting to float)
# numeric_cols = ['Close', 'Open', 'High', 'Low']
# for col in numeric_cols:
#     df[col] = df[col].replace({r'\$': '', ',': ''}, regex=True).astype(float)

# # Set Date as index
# df.set_index('Date', inplace=True)

# # Plot closing price over time
# plt.figure(figsize=(10,5))
# plt.plot(df.index, df['Close'], label="Closing Price", color='blue')
# plt.title("Apple Stock Prices")
# plt.xlabel("Date")
# plt.ylabel("Price (USD)")
# plt.legend()
# plt.grid()
# plt.show()

# # Calculate moving average (50-day and 200-day)
# df['50-day MA'] = df['Close'].rolling(window=50).mean()
# df['200-day MA'] = df['Close'].rolling(window=200).mean()

# # Plot Moving Averages
# plt.figure(figsize=(10,5))
# plt.plot(df.index, df['Close'], label="Closing Price", color='blue', alpha=0.5)
# plt.plot(df.index, df['50-day MA'], label="50-Day Moving Average", color='red')
# plt.plot(df.index, df['200-day MA'], label="200-Day Moving Average", color='green')
# plt.title("Apple Stock Price with Moving Averages")
# plt.xlabel("Date")
# plt.ylabel("Price (USD)")
# plt.legend()
# plt.grid()
# plt.show()




#  Project 3: COVID-19 Data Analysis
# Objective:
# Analyze COVID-19 cases, deaths, and trends across different countries.

import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("COVID.csv")

# Strip spaces from column names
df.columns = df.columns.str.strip()

# Display first few rows and columns
print("Columns in dataset:", df.columns.tolist())
print("\nFirst few rows:\n", df.head())

# Top 10 countries by confirmed cases
top_countries = df.nlargest(10, 'Confirmed')[['Country/Region', 'Confirmed', 'Deaths']]
print("\nTop 10 Countries by Confirmed Cases:\n", top_countries)

# Plot top 10 countries by confirmed cases
plt.figure(figsize=(12,6))
plt.barh(top_countries['Country/Region'], top_countries['Confirmed'], color='orange')
plt.xlabel('Confirmed Cases')
plt.title('Top 10 Countries by COVID-19 Confirmed Cases')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# Calculate and plot death rate
df['Death Rate (%)'] = (df['Deaths'] / df['Confirmed']) * 100
top_death_rate = df.nlargest(10, 'Death Rate (%)')[['Country/Region', 'Death Rate (%)']]

plt.figure(figsize=(12,6))
plt.barh(top_death_rate['Country/Region'], top_death_rate['Death Rate (%)'], color='red')
plt.xlabel('Death Rate (%)')
plt.title('Top 10 Countries by COVID-19 Death Rate')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()