import sys
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QPushButton, QWidget, QTableWidget, QTableWidgetItem, QLineEdit, QLabel, QMessageBox, QHBoxLayout, QHeaderView
from PyQt5.QtCore import Qt

from database import fetch_all_books, update_db

class CSVViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Book Viewer")
        self.setGeometry(100, 100, 1200, 800)

        self.layout = QVBoxLayout()

        self.load_button = QPushButton("Load Books")
        self.load_button.clicked.connect(self.load_books)
        self.layout.addWidget(self.load_button)

        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)

        self.filter_label = QLabel("Filter Value:")
        self.layout.addWidget(self.filter_label)

        self.filter_input = QLineEdit()
        self.layout.addWidget(self.filter_input)

        self.filter_button = QPushButton("Apply Filter")
        self.filter_button.clicked.connect(self.apply_filter)
        self.layout.addWidget(self.filter_button)

        self.add_entry_label = QLabel("Add New Entry:")
        self.layout.addWidget(self.add_entry_label)

        self.entry_layout = QHBoxLayout()
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Title")
        self.entry_layout.addWidget(self.title_input)

        self.authors_input = QLineEdit()
        self.authors_input.setPlaceholderText("Authors")
        self.entry_layout.addWidget(self.authors_input)

        self.pages_input = QLineEdit()
        self.pages_input.setPlaceholderText("Number of Pages")
        self.entry_layout.addWidget(self.pages_input)

        self.pages_read_input = QLineEdit()
        self.pages_read_input.setPlaceholderText("Pages Read")
        self.entry_layout.addWidget(self.pages_read_input)

        self.category_input = QLineEdit()
        self.category_input.setPlaceholderText("Category")
        self.entry_layout.addWidget(self.category_input)

        self.format_input = QLineEdit()
        self.format_input.setPlaceholderText("Format")
        self.entry_layout.addWidget(self.format_input)

        self.layout.addLayout(self.entry_layout)

        self.add_button = QPushButton("Add Entry")
        self.add_button.clicked.connect(self.add_entry)
        self.layout.addWidget(self.add_button)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.df = None

    def load_books(self):
        self.df = fetch_all_books()
        self.display_dataframe(self.df)

    def display_dataframe(self, df):
        if df is not None:
            self.table_widget.setRowCount(df.shape[0] + 1)  # Add an extra row for the sum
            self.table_widget.setColumnCount(df.shape[1] + 1)  # Add an extra column for the delete button
            self.table_widget.setHorizontalHeaderLabels(list(df.columns) + ["Actions"])

            for i in range(df.shape[0]):
                for j in range(df.shape[1]):
                    self.table_widget.setItem(i, j, QTableWidgetItem(str(df.iat[i, j])))

                # Add delete button to the last column
                delete_button = QPushButton("Delete")
                delete_button.clicked.connect(lambda _, row=i: self.delete_entry(row))
                self.table_widget.setCellWidget(i, df.shape[1], delete_button)

            # Calculate the sum of the number_of_pages column
            total_pages = df['number_of_pages'].sum()

            # Add the sum to the last row
            self.table_widget.setItem(df.shape[0], df.columns.get_loc('number_of_pages'), QTableWidgetItem(f"Total Pages: {total_pages}"))

            # Set default column widths
            if 'title' in df.columns:
                self.table_widget.setColumnWidth(df.columns.get_loc('title'), 300)  # Set width for 'Title' column
            if 'authors' in df.columns:
                self.table_widget.setColumnWidth(df.columns.get_loc('authors'), 200)  # Set width for 'Authors' column

            # Resize the last column to fit the content
            self.table_widget.horizontalHeader().setSectionResizeMode(df.shape[1], QHeaderView.ResizeToContents)

    def apply_filter(self):
        filter_value = self.filter_input.text()
        if self.df is not None and filter_value:
            filtered_df = self.df[self.df.apply(lambda row: row.astype(str).str.contains(filter_value).any(), axis=1)]
            self.display_dataframe(filtered_df)
        else:
            QMessageBox.warning(self, "Input Error", "Please load books and enter a filter value.")

    def add_entry(self):
        title = self.title_input.text()
        authors = self.authors_input.text()
        number_of_pages = self.pages_input.text()
        pages_read = self.pages_read_input.text()
        category = self.category_input.text()
        format_ = self.format_input.text()

        if title and authors and number_of_pages and pages_read and category and format_:
            new_entry = pd.DataFrame({
                'title': [title],
                'authors': [authors],
                'number_of_pages': [number_of_pages],
                'pages_read': [pages_read],
                'category': [category],
                'format': [format_]
            })
            update_db(new_entry)
            self.load_books()
            QMessageBox.information(self, "Success", "New entry added successfully.")
        else:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields to add a new entry.")

    def delete_entry(self, row):
        if self.df is not None:
            try:
                self.df = self.df.drop(self.df.index[row])
                self.df.to_sql('books', sqlite3.connect(config.DB_PATH), if_exists='replace', index=False)
                self.load_books()
                QMessageBox.information(self, "Success", "Entry deleted successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete entry. Error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = CSVViewer()
    viewer.show()
    sys.exit(app.exec_())