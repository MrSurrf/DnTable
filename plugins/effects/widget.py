"""
Виджет плагина Эффекты с предпросмотром и списком
Поддержка GIF-анимаций из папок fx/
"""

from PySide6.QtWidgets import (
    QLabel, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QWidget, QFrame, QSizePolicy
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QMovie
import os
import sys

# Добавляем путь к корню проекта для импорта fx
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from fx import get_effects_manager, EffectInfo


class EffectPreviewWidget(QFrame):
    """Виджет предпросмотра эффекта с поддержкой GIF"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_effect = None
        self.movie = None
        
        self._setup_ui()
    
    def _setup_ui(self):
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.setStyleSheet("""
            EffectPreviewWidget {
                background-color: #1a1a1a;
                border: 2px solid #444;
                border-radius: 8px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        
        # Заголовок
        self.title_label = QLabel("Выберите эффект")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-weight: bold; color: #eee; font-size: 12px;")
        layout.addWidget(self.title_label)
        
        # Область предпросмотра
        self.preview_container = QFrame()
        self.preview_container.setMinimumSize(120, 120)
        self.preview_container.setStyleSheet("""
            QFrame {
                background-color: #252525;
                border-radius: 8px;
                border: 1px dashed #555;
            }
        """)
        
        preview_layout = QVBoxLayout(self.preview_container)
        preview_layout.setContentsMargins(4, 4, 4, 4)
        
        # QLabel для GIF-анимации (или иконки)
        self.preview_label = QLabel("✨")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setStyleSheet("font-size: 48px; background: transparent;")
        self.preview_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        preview_layout.addWidget(self.preview_label)
        
        layout.addWidget(self.preview_container, 1)
        
        # Описание
        self.desc_label = QLabel("")
        self.desc_label.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self.desc_label.setWordWrap(True)
        self.desc_label.setStyleSheet("color: #888; font-size: 10px;")
        layout.addWidget(self.desc_label)
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        
        self.play_btn = QPushButton("▶ Воспроизвести")
        self.play_btn.setEnabled(False)
        self.play_btn.setStyleSheet("""
            QPushButton {
                background-color: #3d3d3d;
                color: #eee;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 6px;
                font-size: 11px;
            }
            QPushButton:enabled {
                background-color: #6496FF;
            }
            QPushButton:enabled:hover {
                background-color: #7aa6ff;
            }
        """)
        self.play_btn.clicked.connect(self._toggle_animation)
        buttons_layout.addWidget(self.play_btn)
        
        layout.addLayout(buttons_layout)
    
    def _stop_movie(self):
        """Остановить текущую анимацию"""
        if self.movie:
            self.movie.stop()
            self.movie.deleteLater()
            self.movie = None
    
    def set_effect(self, effect: EffectInfo):
        """Установить эффект для предпросмотра"""
        self.current_effect = effect
        
        # Останавливаем предыдущую анимацию
        self._stop_movie()
        
        # Обновляем заголовок
        self.title_label.setText(f"{effect.icon} {effect.title}")
        
        # Пытаемся загрузить GIF
        effects_manager = get_effects_manager()
        gif_path = effects_manager.get_animation_path(effect.name)
        
        if gif_path and os.path.exists(gif_path):
            # Загружаем GIF
            self.movie = QMovie(gif_path)
            self.movie.setScaledSize(QSize(100, 100))
            self.preview_label.setMovie(self.movie)
            self.preview_label.setText("")
            self.movie.start()
            self.play_btn.setText("⏸ Остановить")
        else:
            # Показываем иконку если GIF нет
            self.preview_label.setText(effect.icon)
            self.preview_label.setStyleSheet(f"font-size: 48px; color: {effect.color}; background: transparent;")
            self.play_btn.setText("▶ Воспроизвести")
        
        # Описание
        self.desc_label.setText(effect.description)
        
        # Включаем кнопку
        self.play_btn.setEnabled(True)
    
    def _toggle_animation(self):
        """Воспроизвести/остановить анимацию"""
        if not self.current_effect:
            return
        
        if self.movie and self.movie.state() == QMovie.Running:
            self.movie.stop()
            self.play_btn.setText("▶ Воспроизвести")
        elif self.movie:
            self.movie.start()
            self.play_btn.setText("⏸ Остановить")
    
    def cleanup(self):
        """Очистка ресурсов при удалении"""
        self._stop_movie()


class PluginWidget(QWidget):
    """Главный виджет плагина Эффекты"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.effects_manager = get_effects_manager()
        self._setup_ui()
        self._load_effects_list()
    
    def _setup_ui(self):
        """Настройка интерфейса"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)
        
        # === ЛЕВАЯ ЧАСТЬ: Предпросмотр ===
        left_layout = QVBoxLayout()
        
        # Заголовок
        header = QLabel("Предпросмотр")
        header.setStyleSheet("font-weight: bold; color: #6496FF; font-size: 11px;")
        left_layout.addWidget(header)
        
        # Виджет предпросмотра
        self.preview = EffectPreviewWidget()
        left_layout.addWidget(self.preview, 1)
        
        # Кнопки применения
        apply_btn = QPushButton("✓ Применить к карте")
        apply_btn.setStyleSheet("""
            QPushButton {
                background-color: #64FF64;
                color: #1a1a1a;
                border: none;
                border-radius: 6px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7aff7a;
            }
        """)
        apply_btn.clicked.connect(self._apply_effect)
        left_layout.addWidget(apply_btn)
        
        clear_btn = QPushButton("✗ Очистить")
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF6464;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px;
            }
        """)
        clear_btn.clicked.connect(self._clear_effect)
        left_layout.addWidget(clear_btn)
        
        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        left_widget.setMinimumWidth(130)
        layout.addWidget(left_widget, 3)
        
        # === ПРАВАЯ ЧАСТЬ: Список эффектов ===
        right_layout = QVBoxLayout()
        
        # Заголовок
        list_header = QLabel("Эффекты")
        list_header.setStyleSheet("font-weight: bold; color: #6496FF; font-size: 11px;")
        right_layout.addWidget(list_header)
        
        # Список эффектов с прокруткой
        self.effects_list = QListWidget()
        self.effects_list.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.effects_list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.effects_list.setSpacing(4)
        
        # Стиль списка
        self.effects_list.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                border: none;
                outline: none;
            }
            QListWidget::item {
                background-color: #2d2d2d;
                border: 1px solid #444;
                border-radius: 6px;
                padding: 6px 8px;
                margin: 2px 2px;
                min-height: 36px;
            }
            QListWidget::item:selected {
                background-color: #3d3d3d;
                border: 2px solid #6496FF;
            }
            QListWidget::item:hover {
                background-color: #353535;
                border-color: #555;
            }
            QScrollBar:vertical {
                background-color: #2d2d2d;
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background-color: #555;
                border-radius: 4px;
                min-height: 30px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #666;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        self.effects_list.currentItemChanged.connect(self._on_effect_selected)
        right_layout.addWidget(self.effects_list, 1)
        
        right_widget = QWidget()
        right_widget.setLayout(right_layout)
        right_widget.setMinimumWidth(140)
        layout.addWidget(right_widget, 2)
    
    def _load_effects_list(self):
        """Загрузить список эффектов"""
        effects = self.effects_manager.get_all_effects()
        
        for effect in effects:
            # Используем title (который уже содержит иконку)
            item = QListWidgetItem(effect.title)
            item.setData(Qt.UserRole, effect.name)
            item.setSizeHint(QSize(0, 40))
            item.setTextAlignment(Qt.AlignVCenter)
            self.effects_list.addItem(item)
    
    def _on_effect_selected(self, current, previous):
        """Выбран эффект из списка"""
        if not current:
            return
        
        effect_name = current.data(Qt.UserRole)
        effect = self.effects_manager.get_effect(effect_name)
        
        if effect:
            self.preview.set_effect(effect)
    
    def _apply_effect(self):
        """Применить выбранный эффект к карте"""
        if not self.preview.current_effect:
            return
        
        effect_name = self.preview.current_effect.name
        print(f"[Effects] Применяю эффект: {effect_name}")
        
        # TODO: Отправить сигнал на основную карту для применения эффекта
        # Например, через events или callback
    
    def _clear_effect(self):
        """Очистить эффекты с карты"""
        print("[Effects] Очищаю все эффекты")
        
        # TODO: Отправить сигнал на очистку эффектов
