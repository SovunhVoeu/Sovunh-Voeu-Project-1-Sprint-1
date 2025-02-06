"""
Author: Sovunh Voeu
Date: 2/6/2025
"""

import sqlite3
import json

# Creates a list for JSON objects
data_list = []

# Open and reads the JSON file
with open('rapidResults.json', 'r') as file:
    for line in file:
        data = json.loads(line.strip())
        data_list.append(data)

# Connects to the SQLite db
conn = sqlite3.connect('jobs.db')
cursor = conn.cursor()

# Creates the table if it does not already exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    site TEXT,
    job_url TEXT,
    job_url_direct TEXT,
    title TEXT,
    company TEXT,
    location TEXT,
    job_type TEXT,
    date_posted DATE,
    salary_source TEXT,
    interval TEXT,
    min_amount DECIMAL(100000, 1),
    max_amount DECIMAL(100000, 2),
    currency TEXT, 
    is_remote BOOLEAN, 
    job_level TEXT,
    job_function TEXT,
    company_industry TEXT,
    listing_type TEXT,
    emails TEXT,
    description TEXT,
    company_url TEXT,
    company_url_direct TEXT,
    company_addresses TEXT,
    company_num_employees INTEGER,
    company_revenue TEXT,
    company_description TEXT,
    logo_photo_url TEXT,
    banner_photo_url TEXT,
    ceo_name TEXT,
    ceo_photo_url TEXT
)
''')


# Commits the data
conn.commit()

# Insert data into the table
for data in data_list:
    cursor.execute('''
        INSERT INTO users (id, site, job_url, job_url_direct, title, company, location, job_type, date_posted,
        salary_source, interval, min_amount, max_amount, currency, is_remote, job_level, job_function, company_industry,
        listing_type, emails, description, company_url, company_url_direct, company_addresses, company_num_employees,
        company_revenue, company_description, logo_photo_url, banner_photo_url, ceo_name, ceo_photo_url) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
        data['id'], data['site'], data['job_url'], data['job_url_direct'], data['title'], data['company'],
        data['location'], data['job_type'], data['date_posted'], data['salary_source'], data['interval'],
        data['min_amount'], data['max_amount'], data['currency'], data['is_remote'], data['job_level'],
        data['job_function'], data['company_industry'], data['listing_type'], data['emails'], data['description'],
        data['company_url'], data['company_url_direct'], data['company_addresses'], data['company_num_employees'],
        data['company_revenue'], data['company_description'], data['logo_photo_url'], data['banner_photo_url'],
        data['ceo_name'], data['ceo_photo_url']
    ))

# Commits the data
conn.commit()

# Closes the connection
conn.close()