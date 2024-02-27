#!/usr/bin/env python
# coding: utf-8

# <p style="text-align:center">
#     <a href="https://skills.network/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkPY0220ENSkillsNetwork900-2022-01-01" target="_blank">
#     <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/assets/logos/SN_web_lightmode.png" width="200" alt="Skills Network Logo">
#     </a>
# </p>
# 

# <h1>Extracting and Visualizing Stock Data</h1>
# <h2>Description</h2>
# 

# Extracting essential data from a dataset and displaying it is a necessary part of data science; therefore individuals can make correct decisions based on the data. In this assignment, you will extract some stock data, you will then display this data in a graph.
# 

# <h2>Table of Contents</h2>
# <div class="alert alert-block alert-info" style="margin-top: 20px">
#     <ul>
#         <li>Define a Function that Makes a Graph</li>
#         <li>Question 1: Use yfinance to Extract Stock Data</li>
#         <li>Question 2: Use Webscraping to Extract Tesla Revenue Data</li>
#         <li>Question 3: Use yfinance to Extract Stock Data</li>
#         <li>Question 4: Use Webscraping to Extract GME Revenue Data</li>
#         <li>Question 5: Plot Tesla Stock Graph</li>
#         <li>Question 6: Plot GameStop Stock Graph</li>
#     </ul>
# <p>
#     Estimated Time Needed: <strong>30 min</strong></p>
# </div>
# 
# <hr>
# 

# ***Note***:- If you are working in IBM Cloud Watson Studio, please replace the command for installing nbformat from `!pip install nbformat==4.2.0` to simply `!pip install nbformat`
# 

# In[1]:


get_ipython().system('pip install yfinance==0.1.67')
get_ipython().system('mamba install bs4==4.10.0 -y')
get_ipython().system('pip install nbformat==4.2.0')


# In[2]:


import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# In Python, you can ignore warnings using the warnings module. You can use the filterwarnings function to filter or ignore specific warning messages or categories.
# 

# In[3]:


import warnings
# Ignore all warnings
warnings.filterwarnings("ignore", category=FutureWarning)


# ## Define Graphing Function
# 

# In this section, we define the function `make_graph`. You don't have to know how the function works, you should only care about the inputs. It takes a dataframe with stock data (dataframe must contain Date and Close columns), a dataframe with revenue data (dataframe must contain Date and Revenue columns), and the name of the stock.
# 

# In[4]:


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


# ## Question 1: Use yfinance to Extract Stock Data
# 

# Using the `Ticker` function enter the ticker symbol of the stock we want to extract data on to create a ticker object. The stock is Tesla and its ticker symbol is `TSLA`.
# 

# In[6]:


import yfinance as yf

# Create a ticker object for Tesla (TSLA)
ticker_symbol = "TSLA"
tesla_stock = yf.Ticker(ticker_symbol)

# Get historical stock data
historical_data = tesla_stock.history(period="1d", interval="1m")  # Adjust the period and interval as needed

# Display the historical data
print(historical_data)


# Using the ticker object and the function `history` extract stock information and save it in a dataframe named `tesla_data`. Set the `period` parameter to `max` so we get information for the maximum amount of time.
# 

# In[7]:


import yfinance as yf
import pandas as pd

# Get historical stock data for the maximum period
tesla_data = tesla_stock.history(period="max")

# Display the DataFrame
print(tesla_data)

# If you want to save the data to a CSV file
tesla_data.to_csv('tesla_stock_data.csv')


# **Reset the index** using the `reset_index(inplace=True)` function on the tesla_data DataFrame and display the first five rows of the `tesla_data` dataframe using the `head` function. Take a screenshot of the results and code from the beginning of Question 1 to the results below.
# 

# In[7]:


# Get historical stock data for the maximum period
tesla_data = tesla_stock.history(period="max")

# Reset the index inplace
tesla_data.reset_index(inplace=True)

# Display the first five rows of the DataFrame
print(tesla_data.head())


# ## Question 2: Use Webscraping to Extract Tesla Revenue Data
# 

# Use the `requests` library to download the webpage https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm Save the text of the response as a variable named `html_data`.
# 

# In[8]:


import requests

# URL of the webpage
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Save the HTML content as a variable named html_data
    html_data = response.text
    print("HTML data successfully retrieved.")
else:
    print("Failed to retrieve data. Status code:", response.status_code)


# Parse the html data using `beautiful_soup`.
# 

# In[9]:


from bs4 import BeautifulSoup

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_data, 'html.parser')


# Using `BeautifulSoup` or the `read_html` function extract the table with `Tesla Revenue` and store it into a dataframe named `tesla_revenue`. The dataframe should have columns `Date` and `Revenue`.
# 

# <details><summary>Click here if you need help locating the table</summary>
# 
# ```
#     
# Below is the code to isolate the table, you will now need to loop through the rows and columns like in the previous lab
#     
# soup.find_all("tbody")[1]
#     
# If you want to use the read_html function the table is located at index 1
# 
# 
# ```
# 
# </details>
# 

# In[10]:


import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the webpage
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table with Tesla Revenue
    table = soup.find('table')

    # Extract data from the table and create a DataFrame
    tesla_revenue = pd.read_html(str(table))[0]

    # Rename columns as needed
    tesla_revenue.columns = ["Date", "Revenue"]

    # Display the DataFrame
    print(tesla_revenue.head())
else:
    print("Failed to retrieve data. Status code:", response.status_code)


# Execute the following line to remove the comma and dollar sign from the `Revenue` column. 
# 

# In[11]:


tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"")


# Execute the following lines to remove an null or empty strings in the Revenue column.
# 

# In[12]:


tesla_revenue.dropna(inplace=True)

tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]


# Display the last 5 row of the `tesla_revenue` dataframe using the `tail` function. Take a screenshot of the results.
# 

# In[13]:


print(tesla_revenue.tail())


# ## Question 3: Use yfinance to Extract Stock Data
# 

# Using the `Ticker` function enter the ticker symbol of the stock we want to extract data on to create a ticker object. The stock is GameStop and its ticker symbol is `GME`.
# 

# In[16]:


import yfinance as yf

# Create a ticker object for Gamestop 
ticker_symbol = "GME"
GME_stock = yf.Ticker(ticker_symbol)

# Get historical stock data
historical_data = GME_stock.history(period="1d", interval="1m")  # Adjust the period and interval as needed

# Display the historical data
print(historical_data)


# Using the ticker object and the function `history` extract stock information and save it in a dataframe named `gme_data`. Set the `period` parameter to `max` so we get information for the maximum amount of time.
# 

# In[20]:


ticker_symbol = "GME"

# Create a Ticker object
gme_ticker = yf.Ticker(ticker_symbol)

# Extract historical stock data with the period parameter set to max
gme_data = gme_ticker.history(period="max")

# Display the dataframe
print(gme_data.head())


# **Reset the index** using the `reset_index(inplace=True)` function on the gme_data DataFrame and display the first five rows of the `gme_data` dataframe using the `head` function. Take a screenshot of the results and code from the beginning of Question 3 to the results below.
# 

# In[21]:


# Reset the index of the gme_data DataFrame
gme_data.reset_index(inplace=True)

# Display the first five rows of the gme_data dataframe using the head function
print(gme_data.head())


# ## Question 4: Use Webscraping to Extract GME Revenue Data
# 

# Use the `requests` library to download the webpage https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html. Save the text of the response as a variable named `html_data`.
# 

# In[22]:


# URL of the webpage
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"

# Send a GET request to the URL
response = requests.get(url)


# Parse the html data using `beautiful_soup`.
# 

# In[23]:


# Parse HTML data using BeautifulSoup
soup = BeautifulSoup(html_data, 'html.parser')

# Print the parsed HTML (optional)
print(soup.prettify())


# Using `BeautifulSoup` or the `read_html` function extract the table with `GameStop Revenue` and store it into a dataframe named `gme_revenue`. The dataframe should have columns `Date` and `Revenue`. Make sure the comma and dollar sign is removed from the `Revenue` column using a method similar to what you did in Question 2.
# 

# <details><summary>Click here if you need help locating the table</summary>
# 
# ```
#     
# Below is the code to isolate the table, you will now need to loop through the rows and columns like in the previous lab
#     
# soup.find_all("tbody")[1]
#     
# If you want to use the read_html function the table is located at index 1
# 
# 
# ```
# 
# </details>
# 

# In[27]:


# Read HTML tables from the URL
tables = pd.read_html(url)

# Assuming the GameStop revenue table is the first table on the page
gme_revenue = tables[0]

# Display the DataFrame
print(gme_revenue.head())


# Display the last five rows of the `gme_revenue` dataframe using the `tail` function. Take a screenshot of the results.
# 

# In[28]:


# Display the last five rows of the gme_revenue dataframe using the tail function
print(gme_revenue.tail())


# ## Question 5: Plot Tesla Stock Graph
# 

# Use the `make_graph` function to graph the Tesla Stock Data, also provide a title for the graph. The structure to call the `make_graph` function is `make_graph(tesla_data, tesla_revenue, 'Tesla')`. Note the graph will only show data upto June 2021.
# 

# In[31]:


import yfinance as yf
import matplotlib.pyplot as plt

# Download Tesla stock data (replace period and interval as needed)
tesla = yf.Ticker("TSLA")
tesla_data = tesla.history(period="max", interval="1d")

# Extract desired data: close prices
close_prices = tesla_data["Close"]

# Create the graph
plt.figure(figsize=(12, 6))  # Adjust figure size as desired
plt.plot(close_prices.index, close_prices, label="TSLA Closing Price")
plt.title("Tesla Stock Closing Prices (Past Max Period)")
plt.xlabel("Date")
plt.ylabel("Closing Price")
plt.legend()
plt.grid(True)  # Add gridlines for better readability
plt.xticks(rotation=45)  # Rotate x-axis labels for readability

# Optional customizations:
# - Add annotations for significant events
# - Modify line color and style
# - Display additional data (e.g., moving averages)

plt.show()





# ## Question 6: Plot GameStop Stock Graph
# import yfinance as yf
# import matplotlib.pyplot as plt
# 
# # Download Tesla stock data (replace period and interval as needed)
# GameStop = yf.Ticker("TSLA")
# tesla_data = tesla.history(period="max", interval="1d")
# 
# # Extract desired data: close prices
# close_prices = tesla_data["Close"]
# 
# # Create the graph
# plt.figure(figsize=(12, 6))  # Adjust figure size as desired
# plt.plot(close_prices.index, close_prices, label="TSLA Closing Price")
# plt.title("Tesla Stock Closing Prices (Past Max Period)")
# plt.xlabel("Date")
# plt.ylabel("Closing Price")
# plt.legend()
# plt.grid(True)  # Add gridlines for better readability
# plt.xticks(rotation=45)  # Rotate x-axis labels for readability
# 
# # Optional customizations:
# # - Add annotations for significant events
# # - Modify line color and style
# # - Display additional data (e.g., moving averages)
# 
# plt.show()
# 
# 

# Use the `make_graph` function to graph the GameStop Stock Data, also provide a title for the graph. The structure to call the `make_graph` function is `make_graph(gme_data, gme_revenue, 'GameStop')`. Note the graph will only show data upto June 2021.
# 

# In[32]:


import yfinance as yf
import matplotlib.pyplot as plt

# Download GameStop stock data (up to June 2021)
gme = yf.Ticker("GME")
gme_data = gme.history(end="2021-06-30")  # Modify end date as needed

# Extract desired data: close prices
close_prices = gme_data["Close"]

# Create the graph
plt.figure(figsize=(12, 6))  # Adjust figure size as desired
plt.plot(close_prices.index, close_prices, label="GME Closing Price")
plt.title("GameStop Stock Closing Prices (Up to June 2021)")
plt.xlabel("Date")
plt.ylabel("Closing Price")
plt.legend()
plt.grid(True)  # Add gridlines for better readability
plt.xticks(rotation=45)  # Rotate x-axis labels for readability

# Optional customizations:
# - Add annotations for significant events
# - Modify line color and style
# - Display additional data (e.g., moving averages)

plt.show()


# <h2>About the Authors:</h2> 
# 
# <a href="https://www.linkedin.com/in/joseph-s-50398b136/">Joseph Santarcangelo</a> has a PhD in Electrical Engineering, his research focused on using machine learning, signal processing, and computer vision to determine how videos impact human cognition. Joseph has been working for IBM since he completed his PhD.
# 
# Azim Hirjani
# 

# ## Change Log
# 
# | Date (YYYY-MM-DD) | Version | Changed By    | Change Description        |
# | ----------------- | ------- | ------------- | ------------------------- |
# | 2022-02-28        | 1.2     | Lakshmi Holla | Changed the URL of GameStop |
# | 2020-11-10        | 1.1     | Malika Singla | Deleted the Optional part |
# | 2020-08-27        | 1.0     | Malika Singla | Added lab to GitLab       |
# 
# <hr>
# 
# ## <h3 align="center"> © IBM Corporation 2020. All rights reserved. <h3/>
# 
# <p>
# 
