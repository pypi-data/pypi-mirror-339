from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton

class EasyWindow:
    """Easy creating windows."""
    
    def __init__(self, title="EasyPython Window", size=(400, 300)):
        self.app = QApplication([])
        self.window = QWidget()
        self.window.setWindowTitle(title)
        self.window.setFixedSize(*size)
        self.layout = QVBoxLayout()
        self.window.setLayout(self.layout)
        
    def add_label(self, text: str):
        label = QLabel(text)
        self.layout.addWidget(label)
        return label
        
    def add_button(self, text: str, callback):
        button = QPushButton(text)
        button.clicked.connect(callback)
        self.layout.addWidget(button)
        return button
        
    def run(self):
        self.window.show()
        self.app.exec()