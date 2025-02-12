"""
Author: Sovunh Voeu
Date: 2/6/2025
"""
import sqlite3
import json


def read_rapidResults(json_file):
    data = []
    with open(json_file, 'r') as file:
        for line in file:
            data_strip = json.loads(line.strip())
            data.append(data_strip)
    return data


def connect_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return conn


def create_table_rapidResults(cursor):
    #cursor = conn.cursor()
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
    sql_insert_data = '''
        INSERT OR IGNORE INTO rapidResults (id, site, job_url, job_url_direct, title, company, location,
        job_type, date_posted,
        salary_source, interval, min_amount, max_amount, currency, is_remote, job_level, job_function,
        company_industry,
        listing_type, emails, description, company_url, company_url_direct, company_addresses,
        company_num_employees,
        company_revenue, company_description, logo_photo_url, banner_photo_url, ceo_name, ceo_photo_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''
    for item in data:
        cursor.execute(sql_insert_data, (
            item['id'], item['site'], item['job_url'], item['job_url_direct'], item['title'], item['company'],
            item['location'], item['job_type'], item['date_posted'], item['salary_source'], item['interval'],
            item['min_amount'], item['max_amount'], item['currency'], item['is_remote'], item['job_level'],
            item['job_function'], item['company_industry'], item['listing_type'],
            item['emails'], item['description'],
            item['company_url'], item['company_url_direct'], item['company_addresses'],
            item['company_num_employees'],
            item['company_revenue'], item['company_description'], item.get('logo_photo_url', ''),
            item.get('banner_photo_url', ''), item.get('ceo_name', ''), item.get('ceo_photo_url', '')
        ))
    conn.commit()


def read_rapidJobs(json_file_2):
    data = []
    with open(json_file_2, 'r') as file:
        for line in file:
            data.extend(json.loads(line))
    return data


def create_table_rapidJobs(cursor):
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


def insert_data_rapidJobs(conn, data):
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
    json_file = 'rapidResults.json'
    json_file_2 = 'rapid_jobs2.json'
    db_path = 'jobs.db'

    data = read_rapidResults(json_file)
    conn = connect_db(db_path)
    create_table_rapidResults(conn)
    insert_data_rapidResults(conn, data)

    data2 = read_rapidJobs(json_file_2)
    conn2 = connect_db(db_path)
    create_table_rapidJobs(conn)
    insert_data_rapidJobs(conn, data2)

    conn.close()
    conn2.close()


if __name__ == '__main__':
    main()
