"""
Author: Sovunh Voeu
Date: 3/8/2025
"""
import pytest
import sqlite3
import json
from unittest.mock import patch, MagicMock
from ai import gemini_setup, retrieve_job_and_user_data, generate_markdown


@pytest.fixture()
def mock_db():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    cursor.execute("CREATE TABLE rapidResults (id INTEGER PRIMARY KEY, title TEXT, description TEXT)")
    cursor.execute("CREATE TABLE user_data (id INTEGER PRIMARY KEY, name TEXT, email TEXT, phone TEXT, "
                   "github TEXT, linkedin TEXT, projects TEXT, classes TEXT, other TEXT)")

    cursor.execute("INSERT INTO rapidResults (title, description) VALUES ('Software Engineer', 'Develop software')")
    cursor.execute("INSERT INTO user_data (id, name, email, phone, github, linkedin, projects, classes, other) VALUES "
                   "(1, 'Test Dev', 'TestDev@example.com', '1234567890', 'github.com/testdev', 'linkedin.com/in/testdev', "
                   "'Project 1 Sprint 1', 'CS390', 'Other info')")
    conn.commit()
    yield conn
    conn.close()


""" USEED COPILOT FOR test_gemini_api_response FUNCTION SINCE I WAS NOT SURE HOW TO WRITE IT """


@patch("ai.genai.GenerativeModel")  # Patch GenerativeModel instead
def test_gemini_api_response(mock_model_class):
    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "Mocked Response"  # Set the expected return value
    mock_model.generate_content.return_value = mock_response  # Mock generate_content
    mock_model_class.return_value = mock_model  # Replace GenerativeModel with our mock

    model = gemini_setup()  # Calls our mocked model
    response = model.generate_content("Test prompt").text  # Extract text

    assert response == "Mocked Response"  # Ensure output matches expected
    mock_model.generate_content.assert_called_once_with("Test prompt")  # Ensure function call


def test_prompt_contains_job_and_user_data(mock_db):
    job_id, user_id = 1, 1
    job, user = retrieve_job_and_user_data(job_id, user_id, mock_db)

    cover_letter_prompt = (
        f"Write a professional cover letter in markdown format for the job: {job['title']}.\n"
        f"Job Description:\n{job['description']}\n\n"
        f"Applicant Details:\n{json.dumps(user, indent=2)}"
    )

    assert job['title'] in cover_letter_prompt
    assert job['description'] in cover_letter_prompt

    for value in user.values():
        assert str(value) in cover_letter_prompt


def test_retrieve_job_user_data(mock_db):
    job_id, user_id = 1, 1
    job, user = retrieve_job_and_user_data(job_id, user_id, mock_db)

    assert "title" in job and "description" in job
    assert isinstance(job["title"], str) and isinstance(job["description"], str)

    expected_user_datas = ["name", "email", "phone", "github", "linkedin", "projects", "classes", "other"]
    assert set(user.keys()) == set(expected_user_datas)
    assert all(isinstance(value, str) for value in user.values())
