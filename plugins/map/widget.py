"""
Виджет плагина "Карта" - просмотр карт D&D
Слева превью карты, справа список карт с навигацией
"""

from PySide6.QtWidgets import (
    QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, 
    QFrame, QComboBox, QSizePolicy
)
from PySide6.QtCore import Qt, QSize
from PySide6 import QtCore
from PySide6.QtGui import QPixmap
import os


class MapPreviewWidget(QFrame):
    """Виджет предпросмотра карты"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_map_path = None
        
        self._setup_ui()
    
    def _setup_ui(self):
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)
        self.setStyleSheet("""
            MapPreviewWidget {
                background-color: #1a1a1a;
                border: 2px solid #444;
                border-radius: 8px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)
        
        # Заголовок с названием карты
        self.title_label = QLabel("🗺️ Выберите карту")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-weight: bold; color: #eee; font-size: 12px;")
        layout.addWidget(self.title_label)
        
        # Область отображения карты
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("""
            background-color: #252525;
            border: 2px dashed #555;
            border-radius: 8px;
            color: #666;
        """)
        self.image_label.setMinimumSize(180, 180)
        self.image_label.setText("🗺️\nНет карты")
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.image_label, 1)
        
        # Инфо о размере
        self.info_label = QLabel("")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("color: #888; font-size: 10px;")
        layout.addWidget(self.info_label)
    
    def set_map(self, map_path: str, map_name: str):
        """Установить карту для отображения"""
        self.current_map_path = map_path
        
        if not map_path or not os.path.exists(map_path):
            self.image_label.setText("🗺️\nКарта не найдена")
            self.title_label.setText("🗺️ Карта")
            self.info_label.setText("")
            return
        
        # Загружаем изображение
        pixmap = QPixmap(map_path)
        if pixmap.isNull():
            self.image_label.setText("❌\nОшибка загрузки")
            return
        
        # Масштабируем под размер виджета
        available_size = self.image_label.size() - QSize(20, 20)
        scaled = pixmap.scaled(
            available_size,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        
        self.image_label.setPixmap(scaled)
        self.image_label.setStyleSheet("background-color: #1a1a1a; border-radius: 8px;")
        self.title_label.setText(f"🗺️ {map_name}")
        
        # Инфо о размере файла
        size_kb = os.path.getsize(map_path) / 1024
        self.info_label.setText(f"{pixmap.width()}x{pixmap.height()} | {size_kb:.0f} KB")
    
    def resizeEvent(self, event):
        """При изменении размера пересчитываем масштаб"""
        super().resizeEvent(event)
        if self.current_map_path and os.path.exists(self.current_map_path):
            # Перезагружаем текущую карту с новым размером
            pixmap = QPixmap(self.current_map_path)
            if not pixmap.isNull():
                available_size = self.image_label.size() - QtCore.QSize(20, 20)
                scaled = pixmap.scaled(
                    available_size,
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                )
                self.image_label.setPixmap(scaled)


class PluginWidget(QWidget):
    """Главный виджет плагина Карта"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.maps_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'maps')
        self.map_files = []
        self.current_index = -1
        
        self._setup_ui()
        self._load_maps_list()
    
    def _setup_ui(self):
        """Настройка интерфейса"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)
        
        # === ЛЕВАЯ ЧАСТЬ: Предпросмотр карты ===
        left_layout = QVBoxLayout()
        
        # Панель навигации (стрелки)
        nav_layout = QHBoxLayout()
        
        self.prev_btn = QPushButton("◀")
        self.prev_btn.setFixedSize(32, 32)
        self.prev_btn.setToolTip("Предыдущая карта")
        self.prev_btn.setStyleSheet("""
            QPushButton {
                background-color: #3d3d3d;
                color: #eee;
                border: 1px solid #555;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6496FF;
            }
            QPushButton:disabled {
                background-color: #2d2d2d;
                color: #555;
            }
        """)
        self.prev_btn.clicked.connect(self._prev_map)
        nav_layout.addWidget(self.prev_btn)
        
        nav_layout.addStretch()
        
        self.next_btn = QPushButton("▶")
        self.next_btn.setFixedSize(32, 32)
        self.next_btn.setToolTip("Следующая карта")
        self.next_btn.setStyleSheet("""
            QPushButton {
                background-color: #3d3d3d;
                color: #eee;
                border: 1px solid #555;
                border-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6496FF;
            }
            QPushButton:disabled {
                background-color: #2d2d2d;
                color: #555;
            }
        """)
        self.next_btn.clicked.connect(self._next_map)
        nav_layout.addWidget(self.next_btn)
        
        left_layout.addLayout(nav_layout)
        
        # Виджет предпросмотра
        self.preview = MapPreviewWidget()
        left_layout.addWidget(self.preview, 1)
        
        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        left_widget.setMinimumWidth(180)
        layout.addWidget(left_widget, 3)
        
        # === ПРАВАЯ ЧАСТЬ: Список карт ===
        right_layout = QVBoxLayout()
        
        # Заголовок
        list_header = QLabel("📂 Карты")
        list_header.setStyleSheet("font-weight: bold; color: #6496FF; font-size: 11px;")
        right_layout.addWidget(list_header)
        
        # Комбобокс для выбора карты
        self.map_combo = QComboBox()
        self.map_combo.setStyleSheet("""
            QComboBox {
                background-color: #2d2d2d;
                color: #eee;
                border: 1px solid #444;
                border-radius: 6px;
                padding: 6px;
                font-size: 11px;
            }
            QComboBox:hover {
                border-color: #555;
            }
            QComboBox::drop-down {
                border: none;
                width: 24px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #eee;
                margin-right: 8px;
            }
            QComboBox QAbstractItemView {
                background-color: #2d2d2d;
                color: #eee;
                border: 1px solid #444;
                selection-background-color: #6496FF;
                selection-color: white;
            }
        """)
        self.map_combo.currentIndexChanged.connect(self._on_map_selected)
        right_layout.addWidget(self.map_combo)
        
        # Список карт (дополнительно)
        self.maps_list_label = QLabel("Доступные карты:")
        self.maps_list_label.setStyleSheet("color: #888; font-size: 10px; margin-top: 8px;")
        right_layout.addWidget(self.maps_list_label)
        
        # Текстовый список карт
        self.maps_list = QLabel("Загрузка...")
        self.maps_list.setStyleSheet("""
            color: #aaa;
            font-size: 10px;
            background-color: #252525;
            border-radius: 6px;
            padding: 8px;
        """)
        self.maps_list.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.maps_list.setWordWrap(True)
        self.maps_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_layout.addWidget(self.maps_list, 1)
        
        # Инфо о папке
        folder_info = QLabel(f"📁 Папка: maps/")
        folder_info.setStyleSheet("color: #666; font-size: 9px;")
        folder_info.setWordWrap(True)
        right_layout.addWidget(folder_info)
        
        right_widget = QWidget()
        right_widget.setLayout(right_layout)
        right_widget.setMinimumWidth(130)
        layout.addWidget(right_widget, 2)
    
    def _load_maps_list(self):
        """Загрузить список карт из папки"""
        self.map_files = []
        
        if os.path.exists(self.maps_dir):
            supported_exts = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']
            files = sorted(os.listdir(self.maps_dir))
            
            for filename in files:
                ext = os.path.splitext(filename)[1].lower()
                if ext in supported_exts:
                    self.map_files.append(filename)
        
        # Заполняем комбобокс
        self.map_combo.clear()
        
        if self.map_files:
            for filename in self.map_files:
                # Имя без расширения для отображения
                display_name = os.path.splitext(filename)[0]
                self.map_combo.addItem(f"🗺️ {display_name}", filename)
            
            # Обновляем текстовый список
            maps_text = "\n".join([f"• {os.path.splitext(f)[0]}" for f in self.map_files])
            self.maps_list.setText(maps_text)
            
            # Выбираем первую карту
            self.current_index = 0
            self._update_navigation()
        else:
            self.map_combo.addItem("Нет карт")
            self.maps_list.setText("Папка пуста")
            self.prev_btn.setEnabled(False)
            self.next_btn.setEnabled(False)
    
    def _on_map_selected(self, index):
        """Выбрана карта из списка"""
        if index < 0 or index >= len(self.map_files):
            return
        
        self.current_index = index
        filename = self.map_files[index]
        map_path = os.path.join(self.maps_dir, filename)
        display_name = os.path.splitext(filename)[0]
        
        self.preview.set_map(map_path, display_name)
        self._update_navigation()
    
    def _prev_map(self):
        """Предыдущая карта"""
        if self.current_index > 0:
            self.current_index -= 1
            self.map_combo.setCurrentIndex(self.current_index)
    
    def _next_map(self):
        """Следующая карта"""
        if self.current_index < len(self.map_files) - 1:
            self.current_index += 1
            self.map_combo.setCurrentIndex(self.current_index)
    
    def _update_navigation(self):
        """Обновить состояние кнопок навигации"""
        self.prev_btn.setEnabled(self.current_index > 0)
        self.next_btn.setEnabled(self.current_index < len(self.map_files) - 1)


