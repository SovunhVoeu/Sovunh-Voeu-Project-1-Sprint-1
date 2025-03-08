"""
Author: Sovunh Voeu
Date: 3/4/2025
"""
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QTableView,
    QPushButton,
    QMessageBox,
    QLabel,
    QTextEdit,
    )
from PyQt6.QtSql import QSqlQuery, QSqlDatabase, QSqlQueryModel
from secondWindow import SecondWindow
from PyQt6.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Database Viewer")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        self.details_label = QLabel("Select a job title from either two of the lists to view the full details. "
                                    "There may be two jobs with the same title but they are from different companies.\n"
                                    "You can expand the title to see the full job by dragging the right side of the "
                                    "title box or by double clicking the right side of the title box .\n"
                                    "Use the scroll bar or scroll wheel to navigate through the list. "
                                    "Full screen the window for the best view of the data. \n"
                                    "To save information about yourself click the Open User Input Data button.")
        layout.addWidget(self.details_label)

        if QSqlDatabase.contains("qt_sql_default_connection"):
            self.db = QSqlDatabase.database("qt_sql_default_connection")
        else:
            self.db = QSqlDatabase.addDatabase('QSQLITE')
            self.db.setDatabaseName('jobs.db')

        if not self.db.open():
            QMessageBox.critical(self, "Database Error", "Unable to open database")
            return

        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        layout.addWidget(self.details_text)
        self.create_user_data_table()

        self.table_rapid_results_view = QTableView()
        self.rapid_results_model = QSqlQueryModel()

        self.table_rapid_jobs_view = QTableView()
        self.rapid_jobs_model = QSqlQueryModel()

        self.table_rapid_results_view.clicked.connect(self.display_rapid_results)
        layout.addWidget(self.table_rapid_results_view)

        self.table_rapid_jobs_view.clicked.connect(self.display_rapid_jobs)
        layout.addWidget(self.table_rapid_jobs_view)

        self.user_data_button = QPushButton("Open User Input Data")
        self.user_data_button.clicked.connect(self.open_second_window)
        layout.addWidget(self.user_data_button)

        self.table_rapid_results()
        self.table_rapid_jobs()

    def table_rapid_results(self):
        self.rapid_results_model.setQuery("SELECT * FROM rapidResults", self.db)
        self.table_rapid_results_view.setModel(self.rapid_results_model)
        for col in range(self.rapid_results_model.columnCount()):
            if col != 4:
                self.table_rapid_results_view.setColumnHidden(col, True)

    def display_rapid_results(self, index):
        row = index.row()
        job_details = []
        for col in range(self.rapid_results_model.columnCount()):
            column_name = self.rapid_results_model.headerData(col, Qt.Orientation.Horizontal)
            column_value = self.rapid_results_model.data(self.rapid_results_model.index(row, col))
            job_details.append(f"{column_name}: {column_value}")
        self.details_text.setText("\n".join(job_details))

    def table_rapid_jobs(self):
        self.rapid_jobs_model.setQuery("SELECT * FROM rapid_jobs2", self.db)
        self.table_rapid_jobs_view.setModel(self.rapid_jobs_model)
        for col in range(self.rapid_jobs_model.columnCount()):
            if col != 1:
                self.table_rapid_jobs_view.setColumnHidden(col, True)

    def display_rapid_jobs(self, index):
        row = index.row()
        job_details = []
        for col in range(self.rapid_jobs_model.columnCount()):
            column_name = self.rapid_jobs_model.headerData(col, Qt.Orientation.Horizontal)
            column_value = self.rapid_jobs_model.data(self.rapid_jobs_model.index(row, col))
            job_details.append(f"{column_name}: {column_value}")
        self.details_text.setText("\n".join(job_details))

    def create_user_data_table(self):
        query = QSqlQuery(self.db)
        query.exec("""
           CREATE TABLE IF NOT EXISTS user_data (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           name VARCHAR(255),
           email VARCHAR(255),
           phone VARCHAR(255),
           github VARCHAR(255),
           linkedin VARCHAR(255),
           projects TEXT,
           classes TEXT,
           other TEXT
           )
           """)

    def open_second_window(self):
        self.user_data_window = SecondWindow(self.db)
        self.user_data_window.show()

    def quit(self):
        QApplication.instance().quit()
