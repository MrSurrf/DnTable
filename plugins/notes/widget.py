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
        header.setObjectName("header")
        layout.addWidget(header)
        
        # Текстовое поле
        self.text = QTextEdit()
        self.text.setObjectName("textEdit")
        self.text.setPlaceholderText("Введите заметки здесь...")
        layout.addWidget(self.text, 1)
        
        # Счётчик символов
        self.counter = QLabel("0 / 5000")
        self.counter.setObjectName("counter")
        self.counter.setAlignment(Qt.AlignRight)
        layout.addWidget(self.counter)
        
        self.text.textChanged.connect(self._update_counter)
    
    def _update_counter(self):
        length = len(self.text.toPlainText())
        self.counter.setText(f"{length} / 5000")
        
        # Используем свойство для изменения цвета через QSS
        if length > 4500:
            self.counter.setProperty("almostFull", "true")
        else:
            self.counter.setProperty("almostFull", "false")
        
        # Обновляем стиль
        self.counter.style().unpolish(self.counter)
        self.counter.style().polish(self.counter)
    
    def get_text(self) -> str:
        return self.text.toPlainText()
    
    def set_text(self, text: str):
        self.text.setPlainText(text)
