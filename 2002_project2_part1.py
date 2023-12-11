import requests
from bs4 import BeautifulSoup
import time
import mysql.connector
import json

# Specify the URL you want to scrape
html = 'https://4feaquhyai.execute-api.us-east-1.amazonaws.com/api/pi'

conn = mysql.connector.connect(
    host='localhost',
    user='ds2002',
    password='Uva!1819',
    database='classicmodels'
)
cursor = conn.cursor()


# Create a table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS scraped_data (
        factor INT,
        pi DOUBLE,
        time VARCHAR(50)
    )
''')
conn.commit()

# Set the duration for scraping in seconds (1 hour = 60 minutes * 60 seconds)
scraping_duration = 60 * 60

# Set the interval for refreshing the website in seconds (1 minute)
refresh_interval = 60

# Get the current time to calculate the end time
start_time = time.time()
end_time = start_time + scraping_duration

while time.time() < end_time:
    start_iteration_time = time.time()
    response = requests.get(html)

    soup = BeautifulSoup(response.text, 'html')
    body = soup.find('body')

    if body:
        data_dict = json.loads(body.text)

        cursor.execute('''
                INSERT INTO scraped_data (factor, pi, time)
                VALUES (%s, %s, %s)
            ''', (data_dict['factor'], data_dict['pi'], data_dict['time']))
        conn.commit()
        print(body.text)
    
    else:
        print("didn't find body")
    
    iteration_time = time.time() - start_iteration_time
    sleep_time = max(0, 60 - iteration_time)
    time.sleep(sleep_time)


print("Scraping duration reached. Exiting the program.")

# Close the database connection
cursor.close()
conn.close()
