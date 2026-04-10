"""Виджет плагина Заметки"""

from PySide6.QtWidgets import QTextEdit, QVBoxLayout, QLabel, QWidget
from PySide6.QtCore import Qt


class PluginWidget(QWidget):
    """Виджет заметок"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # Заголовок
        header = QLabel("📝 Заметки")
        header.setStyleSheet("font-weight: bold; color: #eee;")
        layout.addWidget(header)
        
        # Текстовое поле
        self.text = QTextEdit()
        self.text.setPlaceholderText("Введите заметки здесь...")
        self.text.setStyleSheet("""
            QTextEdit {
                background-color: #252525;
                border: 1px solid #444;
                border-radius: 6px;
                color: #eee;
                padding: 8px;
                font-family: Segoe UI;
                font-size: 11px;
            }
        """)
        layout.addWidget(self.text, 1)
        
        # Счётчик символов
        self.counter = QLabel("0 / 5000")
        self.counter.setAlignment(Qt.AlignRight)
        self.counter.setStyleSheet("color: #666; font-size: 10px;")
        layout.addWidget(self.counter)
        
        self.text.textChanged.connect(self._update_counter)
    
    def _update_counter(self):
        length = len(self.text.toPlainText())
        self.counter.setText(f"{length} / 5000")
        if length > 4500:
            self.counter.setStyleSheet("color: #FF6464; font-size: 10px;")
        else:
            self.counter.setStyleSheet("color: #666; font-size: 10px;")
    
    def get_text(self) -> str:
        return self.text.toPlainText()
    
    def set_text(self, text: str):
        self.text.setPlainText(text)
