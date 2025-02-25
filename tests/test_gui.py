"""
Author: Sovunh Voeu
Date: 2/22/2025
"""
import os
# os.environ["QT_QPA_PLATFORM"] = "offscreen"
import sys
import pytest
from gui import MainWindow, SecondWindow
from PyQt6.QtWidgets import QApplication
# from PyQt6.QtSql import QSqlQuery
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt

os.environ["QT_QPA_PLATFORM"] = "offscreen"


@pytest.fixture(scope="session")
def app():
    return QApplication(sys.argv)


@pytest.fixture
def second_window(app):
    db = 'jobs.db'
    window = SecondWindow(db)
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
