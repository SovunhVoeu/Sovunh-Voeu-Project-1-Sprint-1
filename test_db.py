"""
Author: Sovunh Voeu
Date: 2/6/2025
"""

import sqlite3
import json


def test_read_rapidResults(file_path):
    data = []
    with open('rapidResults.json', 'r') as file:
        for line in file:
            data_strip = json.loads(line.strip())
            data.append(data_strip)
    return data


def connect_db_rapidResults(db_path='jobs.db'):
    conn = sqlite3.connect('jobs.db')
    return conn


def create_table_rapidResults(cursor):
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


def insert_data_rapidResults(conn, data):
    cursor = conn.cursor()
    for data in data:
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


def test_read_json_rapid_jobs2(file_path):
    data = []
    with open('rapid_jobs2.json', 'r') as file:
        for line in file:
            data.extend(json.loads(line))
    return data


def connect_db_rapid_jobs2(db_path='jobs.db'):
    conn = sqlite3.connect(db_path)
    return conn


def create_table_rapid_jobs2(cursor):
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


def insert_data_rapid_jobs2(conn, data):
    cursor = conn.cursor()
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


def main():
    json_file = "rapidResults.json"
    json_file_2 = "rapid_jobs2.json"
    db_path = "jobs.db"

    data = test_read_rapidResults(json_file)
    conn = connect_db_rapidResults(db_path)
    create_table_rapidResults(conn)
    insert_data_rapidResults(conn, data)

    data2 = test_read_json_rapid_jobs2(json_file_2)
    conn2 = connect_db_rapid_jobs2(db_path)
    create_table_rapid_jobs2(conn2)
    insert_data_rapid_jobs2(conn2, data2)

    conn.close()
    conn2.close()

if __name__ == '__main__':
    main()
