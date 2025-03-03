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
    app = QApplication(sys.argv)
    yield app
    app.quit()


@pytest.fixture
def second_window(app):
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("jobs.db")
    assert db.open(), "Database failed to open"

    window = SecondWindow("jobs.db")
    window.show()
    yield window
    window.db.close()


@pytest.fixture
def main_window(app):
    window = MainWindow()
    yield window
    window.close()


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


def test_user_data_entry_save(second_window):
    db = second_window.db

    second_window = SecondWindow(db)

    test_data = {
        "name": "Program Tester",
        "email": "ProgramTester@example.com",
        "phone": "123-456-7890",
        "github": "github.com/tester",
        "linkedin": "linkedin.com/in/tester",
        "projects": "Project 1 Sprint 1, Project 2 Sprint 2",
        "classes": "COMP 490-003 Senior Design & Development S25",
        "other": "Interned as an IT at Bridgewater State University"
    }

    second_window.name_input.setText(test_data["name"])
    second_window.email_input.setText(test_data["email"])
    second_window.phone_input.setText(test_data["phone"])
    second_window.github_input.setText(test_data["github"])
    second_window.linkedin_input.setText(test_data["linkedin"])
    second_window.projects_input.setPlainText(test_data["projects"])
    second_window.classes_input.setPlainText(test_data["classes"])
    second_window.other_input.setPlainText(test_data["other"])

    QTest.mouseClick(second_window.save_button, Qt.MouseButton.LeftButton)
    QApplication.processEvents()

    query = QSqlQuery(db)
    query.prepare("SELECT name, email, phone, github, linkedin, projects, classes, other FROM user_data WHERE name = ?")
    query.addBindValue(test_data["name"])

    assert query.exec(), f"Query execution failed: {query.lastError().text()}"
    assert query.next(), "No data was found in the database"

    saved_data = (
        query.value(0), query.value(1), query.value(2), query.value(3),
        query.value(4), query.value(5), query.value(6), query.value(7)
    )

    expected_data = (
        test_data["name"], test_data["email"], test_data["phone"], test_data["github"],
        test_data["linkedin"], test_data["projects"], test_data["classes"], test_data["other"]
    )

    assert saved_data == expected_data, f"Saved data does not match: {saved_data} != {expected_data}"

    db.close()
    QSqlDatabase.removeDatabase("qt_sql_default_connection")
