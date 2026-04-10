"""Виджет плагина Музыка"""

from PySide6.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QWidget
from PySide6.QtCore import Qt


class PluginWidget(QWidget):
    """Виджет управления музыкой"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.playing = False
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        
        # Текущий трек
        self.track_label = QLabel("🎵 Нет трека")
        self.track_label.setAlignment(Qt.AlignCenter)
        self.track_label.setStyleSheet("color: #eee; font-size: 12px;")
        self.track_label.setWordWrap(True)
        layout.addWidget(self.track_label)
        
        # Полоса прогресса
        self.progress = QSlider(Qt.Horizontal)
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setStyleSheet("""
            QSlider::groove:horizontal {
                height: 4px;
                background: #444;
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                width: 12px;
                margin: -4px 0;
                background: #6496FF;
                border-radius: 6px;
            }
            QSlider::sub-page:horizontal {
                background: #6496FF;
                border-radius: 2px;
            }
        """)
        layout.addWidget(self.progress)
        
        # Кнопки управления
        buttons = QHBoxLayout()
        
        self.prev_btn = QPushButton("⏮")
        self.prev_btn.setFixedSize(36, 32)
        buttons.addWidget(self.prev_btn)
        
        self.play_btn = QPushButton("▶")
        self.play_btn.setFixedSize(48, 32)
        self.play_btn.setStyleSheet("""
            QPushButton {
                background-color: #6496FF;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover { background-color: #7aa6ff; }
        """)
        self.play_btn.clicked.connect(self._toggle_play)
        buttons.addWidget(self.play_btn)
        
        self.next_btn = QPushButton("⏭")
        self.next_btn.setFixedSize(36, 32)
        buttons.addWidget(self.next_btn)
        
        layout.addLayout(buttons)
    
    def _toggle_play(self):
        self.playing = not self.playing
        self.play_btn.setText("⏸" if self.playing else "▶")
        self.track_label.setText("🎵 Играет..." if self.playing else "🎵 Пауза")
