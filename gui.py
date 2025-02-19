"""
Author: Sovunh Voeu
Date: 2/18/2025
"""
import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QTableView, QPushButton,
                             QLineEdit, QFormLayout, QHBoxLayout, QMessageBox, QLabel)
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQueryModel


class SecondWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setWindowTitle("User Input Window")
        self.setGeometry(1000, 100, 800, 600)

        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.search_input = QLineEdit()
        form_layout.addRow("Search:", self.search_input)

        add_button = QPushButton("Search in rapidResults")
        add_button.clicked.connect(self.search_table1)

        input_layout = QHBoxLayout()
        input_layout.addLayout(form_layout)
        input_layout.addWidget(add_button)

        layout.addLayout(input_layout)

        self.setLayout(layout)


    def search_table1(self):
        search_term = self.search_input.text()
        if search_term:
            self.main_window.search_table1(search_term)
        else:
            QMessageBox.warning(self, "Input Error", "Search term cannot be left empty.")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Database Viewer Test")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('jobs.db')
        if not self.db.open():
            print("Unable to open database")
            return

        self.table_view1 = QTableView()
        self.model1 = QSqlTableModel()
        self.model1.setTable('rapidResults')
        self.model1.select()
        self.table_view1.setModel(self.model1)
        self.table_view1.clicked.connect(self.display_details)
        layout.addWidget(self.table_view1)

        self.details_label = QLabel("Select a Job so that you may see the full details.")
        layout.addWidget(self.details_label)

        self.table_view2 = QTableView()
        self.model2 = QSqlTableModel()
        self.model2.setTable('rapid_jobs2')
        self.model2.select()
        self.table_view2.setModel(self.model2)
        layout.addWidget(self.table_view2)

        button = QPushButton("Open Search Window")
        button.clicked.connect(self.open_second_window)
        layout.addWidget(button)

        self.second_window = None

    def open_second_window(self):
        if self.second_window is None:
            self.second_window = SecondWindow(self)
        self.second_window.show()

    def search_table1(self, search_term):
        query = f"site LIKE '%{search_term}%'"
        self.model1.setFilter(query)
        self.model1.select()

    def display_details(self, index):
        row = index.row()
        job_id = self.model1.data(self.model1.index(row, 0))
        job_name = self.model1.data(self.model1.index(row, 4))
        job_details = f"ID: {job_id}\nTitle: {job_name}"
        self.details_label.setText(job_details)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())