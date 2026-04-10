"""Виджет плагина Таймер"""

from PySide6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QWidget
from PySide6.QtCore import Qt, QTimer


class PluginWidget(QWidget):
    """Виджет таймера"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.seconds = 0
        self.running = False
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        
        # Дисплей
        self.display = QLabel("00:00:00")
        self.display.setAlignment(Qt.AlignCenter)
        self.display.setStyleSheet("""
            font-family: Consolas;
            font-size: 28px;
            color: #64FF64;
            background-color: #0d1f0d;
            border-radius: 6px;
            padding: 4px;
        """)
        layout.addWidget(self.display)
        
        # Кнопки
        buttons = QHBoxLayout()
        
        self.start_btn = QPushButton("▶")
        self.start_btn.setFixedSize(40, 28)
        self.start_btn.clicked.connect(self._toggle)
        buttons.addWidget(self.start_btn)
        
        self.reset_btn = QPushButton("↺")
        self.reset_btn.setFixedSize(40, 28)
        self.reset_btn.clicked.connect(self._reset)
        buttons.addWidget(self.reset_btn)
        
        layout.addLayout(buttons)
        
        # Таймер
        self.timer = QTimer()
        self.timer.timeout.connect(self._tick)
        self.timer.setInterval(1000)
    
    def _toggle(self):
        if self.running:
            self.timer.stop()
            self.start_btn.setText("▶")
            self.display.setStyleSheet("""
                font-family: Consolas;
                font-size: 28px;
                color: #64FF64;
                background-color: #0d1f0d;
                border-radius: 6px;
                padding: 4px;
            """)
        else:
            self.timer.start()
            self.start_btn.setText("⏸")
            self.display.setStyleSheet("""
                font-family: Consolas;
                font-size: 28px;
                color: #64FF64;
                background-color: #1a3d1a;
                border-radius: 6px;
                padding: 4px;
            """)
        self.running = not self.running
    
    def _reset(self):
        self.timer.stop()
        self.running = False
        self.seconds = 0
        self.start_btn.setText("▶")
        self._update_display()
    
    def _tick(self):
        self.seconds += 1
        self._update_display()
    
    def _update_display(self):
        hours = self.seconds // 3600
        minutes = (self.seconds % 3600) // 60
        secs = self.seconds % 60
        self.display.setText(f"{hours:02d}:{minutes:02d}:{secs:02d}")
