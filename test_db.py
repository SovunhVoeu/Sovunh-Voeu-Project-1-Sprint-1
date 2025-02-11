"""
Author: Sovunh Voeu
Date: 2/6/2025
"""

import sqlite3
import json


def test_rapid_results():
    data_list = []

    with open('rapidResults.json', 'r') as file:
        for line in file:
            data = json.loads(line.strip())
            data_list.append(data)

    conn = sqlite3.connect('jobs.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rapidResults (
        id VARCHAR(32) PRIMARY KEY,
        site VARCHAR(255) NOT NULL,
        job_url VARCHAR(255),
        job_url_direct VARCHAR(255),
        title VARCHAR(255),
        company VARCHAR(255),
        location VARCHAR(255),
        job_type VARCHAR(255),
        date_posted DATE,
        salary_source VARCHAR(255),
        interval VARCHAR(255),
        min_amount DECIMAL(100000, 1),
        max_amount DECIMAL(100000, 2),
        currency VARCHAR(255),
        is_remote BOOLEAN,
        job_level VARCHAR(255),
        job_function VARCHAR(255),
        company_industry VARCHAR(255),
        listing_type VARCHAR(255),
        emails VARCHAR(255),
        description TEXT,
        company_url TEXT,
        company_url_direct TEXT,
        company_addresses TEXT,
        company_num_employees INTEGER,
        company_revenue DECIMAL(100000, 2),
        company_description TEXT,
        logo_photo_url TEXT NOT NULL,
        banner_photo_url TEXT NOT NULL,
        ceo_name VARCHAR(255),
        ceo_photo_url TEXT
    )
    ''')

    for data in data_list:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO rapidResults (id, site, job_url, job_url_direct, title, company, location,
                job_type, date_posted,
                salary_source, interval, min_amount, max_amount, currency, is_remote, job_level, job_function,
                company_industry,
                listing_type, emails, description, company_url, company_url_direct, company_addresses,
                company_num_employees,
                company_revenue, company_description, logo_photo_url, banner_photo_url, ceo_name, ceo_photo_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                data['id'], data['site'], data['job_url'], data['job_url_direct'], data['title'], data['company'],
                data['location'], data['job_type'], data['date_posted'], data['salary_source'], data['interval'],
                data['min_amount'], data['max_amount'], data['currency'], data['is_remote'], data['job_level'],
                data['job_function'], data['company_industry'], data['listing_type'],
                data['emails'], data['description'],
                data['company_url'], data['company_url_direct'], data['company_addresses'],
                data['company_num_employees'],
                data['company_revenue'], data['company_description'], data['logo_photo_url'],
                data['banner_photo_url'], data['ceo_name'], data['ceo_photo_url']
            ))
        except KeyError as e:
            print(f"Missing key: {e}")

    conn.commit()
    conn.close()


def test_rapid_jobs2():
    data = []
    with open('rapid_jobs2.json', 'r') as file:
        for line in file:
            data.extend(json.loads(line))

    conn = sqlite3.connect('jobs.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rapid_jobs2 (
        id VARCHAR(32) PRIMARY KEY,
        title VARCHAR(255),
        jobProviders VARCHAR(255),
        company VARCHAR(255),
        image VARCHAR(255),
        location VARCHAR(255),
        datePosted DATE,
        salaryRange VARCHAR(255),
        description TEXT,
        employmentType TEXT
    )
    ''')

    for item in data:
        cursor.execute('''
            INSERT OR IGNORE INTO rapid_jobs2 (id, title, jobProviders, company, image,
            location, datePosted, salaryRange, description, employmentType)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
            item['id'],
            item['title'],
            ", ".join(provider["jobProvider"] for provider in item.get('jobProviders', [])),
            item['company'],
            item['image'],
            item['location'],
            item['datePosted'],
            item['salaryRange'],
            item['description'],
            item['employmentType']

        ))

    conn.commit()
    conn.close()


if __name__ == '__main__':
    test_rapid_results()
    test_rapid_jobs2()
