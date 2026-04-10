"""Виджет плагина Кости"""

from PySide6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QComboBox
from PySide6.QtCore import Qt
import random


class PluginWidget(QWidget):
    """Виджет броска костей"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dice_type = 20
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # Результат
        self.result = QLabel("🎲")
        self.result.setAlignment(Qt.AlignCenter)
        self.result.setStyleSheet("font-size: 48px;")
        layout.addWidget(self.result)
        
        # Тип кости
        self.dice_selector = QComboBox()
        self.dice_selector.addItems([f"d{sides}" for sides in [4, 6, 8, 10, 12, 20, 100]])
        self.dice_selector.setCurrentIndex(5)  # d20
        self.dice_selector.currentTextChanged.connect(self._on_dice_changed)
        layout.addWidget(self.dice_selector)
        
        # Кнопка броска
        self.roll_btn = QPushButton("Бросить")
        self.roll_btn.setStyleSheet("""
            QPushButton {
                background-color: #6496FF;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: #7aa6ff; }
            QPushButton:pressed { background-color: #4d85ff; }
        """)
        self.roll_btn.clicked.connect(self._roll)
        layout.addWidget(self.roll_btn)
        
        # История
        self.history = QLabel("История: -")
        self.history.setAlignment(Qt.AlignCenter)
        self.history.setStyleSheet("color: #888; font-size: 10px;")
        layout.addWidget(self.history)
        
        self.rolls = []
    
    def _on_dice_changed(self, text):
        self.dice_type = int(text[1:])
    
    def _roll(self):
        result = random.randint(1, self.dice_type)
        self.result.setText(str(result))
        
        self.rolls.append(f"d{self.dice_type}:{result}")
        if len(self.rolls) > 5:
            self.rolls.pop(0)
        
        history_text = " ".join(self.rolls)
        self.history.setText(f"История: {history_text}")
