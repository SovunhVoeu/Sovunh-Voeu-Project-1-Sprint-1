"""
Author: Sovunh Voeu
Date: 2/22/2025
"""
import pytest
from gui import MainWindow
from PyQt6.QtWidgets import QApplication
from PyQt6.QtSql import QSqlQuery
from PyQt6.QtTest import QTest
from PyQt6.QtCore import Qt


@pytest.fixture(scope="session")
def app():
    return QApplication([])


@pytest.fixture
def main_window(app):
    window = MainWindow()
    window.show()
    return window


def test_job_select_return(main_window):
    job_list_view = main_window.table_view1

    assert job_list_view.model().rowCount() > 0, "There are no jobs available for selection"

    index =  job_list_view.model().index(0,0)
    QTest.mouseClick(job_list_view.viewport(),Qt.MouseButton.LeftButton,pos = job_list_view.visualRect(index).center())

    main_window.display_details1(index)

    displayed_text = main_window.details_text.toPlainText()
    assert "id:" in displayed_text, "Job ID is missing"
    assert "site:" in displayed_text, "site is missing"
    assert len(displayed_text) > 10, "Displayed details is short"