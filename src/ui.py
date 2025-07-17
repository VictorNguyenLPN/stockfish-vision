# ui.py
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stockfish Vision v1.0.0")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        self.upload_button = QPushButton("Analyze Image")
        layout.addWidget(self.upload_button)

        self.result_label = QLabel("Best move will be shown here")
        self.result_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #3498db;")
        layout.addWidget(self.result_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)