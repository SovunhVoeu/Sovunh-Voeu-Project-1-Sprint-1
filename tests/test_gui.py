"""
Author: Sovunh Voeu
Date: 2/22/2025
"""
import sys
import pytest
from gui import MainWindow, SecondWindow
from PyQt6.QtWidgets import QApplication
from PyQt6.QtSql import QSqlQuery, QSqlDatabase
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt


@pytest.fixture(scope="session")
def app():
    return QApplication(sys.argv)


@pytest.fixture
def second_window(app):
    window = SecondWindow("jobs.db")
    window.show()
    return window


@pytest.fixture
def main_window(app):
    window = MainWindow()
    window.show()
    return window


def test_job_select_return(main_window):
    job_list_view = main_window.table_view1

    assert job_list_view.model().rowCount() > 0, "There are no jobs available for selection"

    index = job_list_view.model().index(0, 0)
    QTest.mouseClick(job_list_view.viewport(), Qt.MouseButton.LeftButton, pos=job_list_view.visualRect(index).center())

    main_window.display_details1(index)

    displayed_text = main_window.details_text.toPlainText()
    assert "title:" in displayed_text, "Job title is missing"
    assert "site:" in displayed_text, "site is missing"
    assert len(displayed_text) > 10, "Displayed details is short"


def test_job_select_return2(main_window):
    job_list_view = main_window.table_view2

    assert job_list_view.model().rowCount() > 0, "There are no jobs available for selection"

    index = job_list_view.model().index(0, 0)
    QTest.mouseClick(job_list_view.viewport(), Qt.MouseButton.LeftButton, pos=job_list_view.visualRect(index).center())

    main_window.display_details2(index)

    displayed_text = main_window.details_text.toPlainText()
    assert "title:" in displayed_text, "Job title is missing"
    assert "jobProviders:" in displayed_text, "jobProviders is missing"
    assert len(displayed_text) > 10, "Displayed details is short"


""" Got from Copilot since my previous function kept giving me errors """


def test_user_data_entry(second_window):
    """Test to ensure user-entered data is properly stored in the database."""
    # Simulate user input
    QTest.keyClicks(second_window.name_input, "John Doe")
    QTest.keyClicks(second_window.email_input, "johndoe@example.com")
    QTest.keyClicks(second_window.phone_input, "123-456-7890")
    QTest.keyClicks(second_window.github_input, "github.com/johndoe")
    QTest.keyClicks(second_window.linkedin_input, "linkedin.com/in/johndoe")
    QTest.keyClicks(second_window.projects_input, "Project A, Project B")
    QTest.keyClicks(second_window.classes_input, "Class 101, Class 102")
    QTest.keyClicks(second_window.other_input, "Additional details")

    # Click the save button
    QTest.mouseClick(second_window.save_button, Qt.MouseButton.LeftButton)

    # Query the database to verify insertion
    query = QSqlQuery(second_window.db)
    query.prepare(
        "SELECT name, email, phone, github, linkedin, projects, classes, other FROM user_data WHERE email = ?")
    query.addBindValue("johndoe@example.com")
    query.exec()

    assert query.next(), "No data found in database"
    assert query.value(0) == "John Doe"
    assert query.value(1) == "johndoe@example.com"
    assert query.value(2) == "123-456-7890"
    assert query.value(3) == "github.com/johndoe"
    assert query.value(4) == "linkedin.com/in/johndoe"
    assert query.value(5) == "Project A, Project B"
    assert query.value(6) == "Class 101, Class 102"
    assert query.value(7) == "Additional details"
