"""
Author: Sovunh Voeu
Date: 2/10/2025
"""
# conftest.py
import pytest
import json
import sqlite3
from db import read_rapidResults, create_table_rapidResults, insert_data_rapidResults


@pytest.fixture
def test_json_file():
    test_file = 'test_data.json'
    test_data = [{"id": "f97b4a007d08a432", "site": "indeed",
                  "job_url": "https://www.indeed.com/viewjob?jk=f97b4a007d08a432",
                  "job_url_direct": "http://www.indeed.com/job/information"
                                    "-security-analystsr-information-security-analyst-f97b4a007d08a432"},
                 {"id": "9d51f80c2334c33f", "site": "indeed",
                  "job_url": "https://www.indeed.com/viewjob?jk=9d51f80c2334c33f",
                  "job_url_direct": "http://www.indeed.com/job/help-desk-production-support-9d51f80c2334c33f"},
                 {"id": "cee95e7fa46f8677", "site": "indeed",
                  "job_url": "https://www.indeed.com/viewjob?jk=cee95e7fa46f8677",
                  "job_url_direct": "https://careersatricoh.com/FO/P6IFK026203F3VBQB688NF6WN/"
                                    "components/details.html?jobId=16277&jobTitle=Customer%20Support%20Technician"}]
    with open(test_file, "w") as file:
        for item in test_data:
            file.write(json.dumps(item) + '\n')
    yield test_file
    # if os.path.exists(test_file):
    #     os.remove(test_file)


def test_read_rapidResults(test_json_file):
    data = read_rapidResults(test_json_file)

    assert len(data) == 3, "Number of data items"
    assert data[0] == {"id": "f97b4a007d08a432", "site": "indeed",
                       "job_url": "https://www.indeed.com/viewjob?jk=f97b4a007d08a432",
                       "job_url_direct": "http://www.indeed.com/job/information"
                                         "-security-analystsr-information-security-analyst-f97b4a007d08a432"}
    assert data[1] == {"id": "9d51f80c2334c33f", "site": "indeed",
                       "job_url": "https://www.indeed.com/viewjob?jk=9d51f80c2334c33f",
                       "job_url_direct": "http://www.indeed.com/job/help-desk-production-support-9d51f80c2334c33f"}
    assert data[2] == {"id": "cee95e7fa46f8677", "site": "indeed",
                       "job_url": "https://www.indeed.com/viewjob?jk=cee95e7fa46f8677",
                       "job_url_direct": "https://careersatricoh.com/FO/P6IFK026203F3VBQB688NF6WN/components/"
                                         "details.html?jobId=16277&jobTitle=Customer%20Support%20Technician"}


@pytest.fixture
def test_db():
    test_db = 'test_db.db'
    conn = sqlite3.connect(test_db)
    cursor = conn.cursor()
    yield conn, cursor
    conn.close()
    # if os.path.exists(test_db):
    #     os.remove(test_db)


""" Used Copilot to solve the assert issue, it kept having an error w/ dicts and lists and str errors """
def test_create_table_rapidResults(test_db):


    conn, cursor = test_db
    create_table_rapidResults(cursor)

    json_file = 'rapidResults.json'
    test_data = read_rapidResults(json_file)

    insert_data_rapidResults(conn, test_data)

    cursor.execute("SELECT * FROM rapidResults WHERE title = 'PS Engineer'")
    result = cursor.fetchone()

    assert result is not None
    for item in test_data:
        if item["title"] == "PS Engineer":
            assert result[0] == test_data[9]["id"]
            assert result[1] == test_data[9]["site"]
            assert result[2] == test_data[9]["job_url"]
            assert result[3] == test_data[9]["job_url_direct"]
            assert result[4] == test_data[9]["title"]
            break
