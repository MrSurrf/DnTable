"""
Виджет плагина - ПРИМЕР для сторонних разработчиков

Этот файл должен содержать класс PluginWidget - это обязательное имя!
Система автоматически найдет и загрузит этот класс.
"""

from PySide6.QtWidgets import (
    QLabel, QVBoxLayout, QHBoxLayout, QPushButton, 
    QWidget, QFrame
)
from PySide6.QtCore import Qt

# Импортируем свои настройки из config.py
# (опционально, если нужны специфичные настройки)
# from .config import EXAMPLE_SETTING, MAX_ITEMS


class PluginWidget(QWidget):
    """
    Главный виджет плагина.
    
    ЭТО ОБЯЗАТЕЛЬНОЕ ИМЯ КЛАССА!
    Система ищет именно класс с названием PluginWidget.
    
    Размер виджета определяется в config.py:
    - PLUGIN_COLS = ширина в ячейках сетки
    - PLUGIN_ROWS = высота в ячейках сетки
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        """Настройка интерфейса виджета"""
        # Главный layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        
        # === ЗАГОЛОВОК ===
        header = QLabel('Карта с Эффектами ')
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet('font-weight: bold; color: #eee; font-size: 14px;')
        layout.addWidget(header)
        
        # === КОНТЕНТ ===
        # Здесь размещайте свой функционал
        
        # Пример: информационная панель
        info_frame = QFrame()
        info_frame.setStyleSheet('''
            QFrame {
                background-color: #252525;
                border-radius: 8px;
                padding: 8px;
            }
        ''')
        info_layout = QVBoxLayout(info_frame)
        
        info_text = QLabel(
            'Это пример плагина.\n\n'
            'Здесь может быть:\n'
            '• Ваш функционал\n'
            '• Кнопки, поля ввода\n'
            '• Изображения, анимации\n'
            '• Любые Qt виджеты'
        )
        info_text.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        info_text.setStyleSheet('color: #aaa; font-size: 11px;')
        info_text.setWordWrap(True)
        info_layout.addWidget(info_text)
        
        layout.addWidget(info_frame)
        
        # === КНОПКИ ===
        buttons = QHBoxLayout()
        
        btn1 = QPushButton('Кнопка 1')
        btn1.setStyleSheet('''
            QPushButton {
                background-color: #3d3d3d;
                color: #eee;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #4d4d4d;
            }
        ''')
        btn1.clicked.connect(self._on_button1_click)
        buttons.addWidget(btn1)
        
        btn2 = QPushButton('Кнопка 2')
        btn2.setStyleSheet('''
            QPushButton {
                background-color: #6496FF;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #7aa6ff;
            }
        ''')
        btn2.clicked.connect(self._on_button2_click)
        buttons.addWidget(btn2)
        
        layout.addLayout(buttons)
        
        # Растягивающийся spacer (чтобы контент был сверху)
        layout.addStretch()
    
    def _on_button1_click(self):
        """Обработчик клика по кнопке 1"""
        print('[ExamplePlugin] Нажата кнопка 1')
    
    def _on_button2_click(self):
        """Обработчик клика по кнопке 2"""
        print('[ExamplePlugin] Нажата кнопка 2')


# =============================================================================
# ДОПОЛНИТЕЛЬНЫЕ СОВЕТЫ:
# =============================================================================
#
# 1. Стили можно задавать:
#    - Программно (как в примере выше через setStyleSheet)
#    - В отдельном файле styles.qss в папке плагина
#
# 2. Для сохранения данных плагина между запусками:
#    - Используйте стандартный модуль json или QSettings
#    - Сохраняйте в папку плагина или в ~/.config/DnTable/
#
# 3. Для коммуникации между плагинами:
#    - Используйте сигналы/слоты Qt
#    - Или создайте общий event bus
#
# 4. Документация PySide6:
#    https://doc.qt.io/qtforpython-6/
#
# 5. Примеры других плагинов смотрите в папках:
#    - plugins/timer/      - простой таймер
#    - plugins/notes/      - текстовые заметки
#    - plugins/dice_roller/ - сложный плагин с анимацией
# =============================================================================
