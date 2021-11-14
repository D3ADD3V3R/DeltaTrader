from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout


class ApplicationDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(1000)
        self.setFixedWidth(1000)
        layout = QVBoxLayout()
        layout.addWidget(QPushButton('Top'))
        layout.addWidget(QPushButton('Bottom'))
        self.setLayout(layout)
