# main.py
import sys
from PyQt6.QtWidgets import QApplication
from src.ui import MainWindow
import src.image_processing as image_processing
import src.engine as engine

class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.view = MainWindow()
        self._connect_signals()

    def run(self):
        self.view.show()
        sys.exit(self.app.exec())

    def _connect_signals(self):
        self.view.upload_button.clicked.connect(self.handle_upload)

    def handle_upload(self):
        self.view.result_label.setText("Image processing...")
        fen = image_processing.process_image_from_path("images/screenshot.png")
        self._analyze_and_show_result(fen)

    def _analyze_and_show_result(self, fen):
        if fen:
            self.view.result_label.setText(f"Analyzing FEN: {fen[:20]}...")
            best_move = engine.get_best_move(fen)
            self.view.result_label.setText(f"Best move: {best_move}")
        else:
            self.view.result_label.setText("Image processing fail")

if __name__ == "__main__":
    controller = AppController()
    controller.run()