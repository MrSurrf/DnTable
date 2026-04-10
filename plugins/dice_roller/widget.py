"""
Виджет плагина Dice Roller с фигурными кнопками и анимацией броска

- Кнопки имеют форму соответствующую типу кубика (рисуются в paintEvent)
- При броске показывается overlay с анимацией
- Стили в styles.qss
"""

from PySide6.QtWidgets import (
    QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, 
    QScrollArea, QFrame, QSizePolicy, QGridLayout
)
from PySide6.QtCore import Qt, QTimer, QSize, QPoint, QRect, Signal
from PySide6.QtGui import QColor, QPainter, QPolygon, QFont, QMovie
import random
import os
import math


# Цвета для кубиков разного типа (используются в paintEvent и для динамических стилей)
DICE_COLORS = {
    4:  '#FF6B6B',   # Красный (d4)
    6:  '#4ECDC4',   # Бирюзовый (d6)
    8:  '#45B7D1',   # Голубой (d8)
    10: '#96CEB4',   # Зелёный (d10)
    12: '#FFEAA7',   # Жёлтый (d12)
    20: '#DDA0DD',   # Фиолетовый (d20)
    100:'#F8C471',   # Оранжевый (d100)
}


class ShapedDiceButton(QPushButton):
    """Кнопка кубика с фигурной формой (рисуется через paintEvent)"""
    
    def __init__(self, dice_type, parent=None):
        super().__init__(parent)
        self.dice_type = dice_type
        self.color = QColor(DICE_COLORS.get(dice_type, '#888888'))
        self.hovered = False
        self.pressed_state = False
        
        self.setFixedSize(70, 70)
        self.setCursor(Qt.PointingHandCursor)
        
        # Прозрачный фон - фигура рисуется в paintEvent
        self.setStyleSheet("background: transparent; border: none;")
    
    def enterEvent(self, event):
        self.hovered = True
        self.update()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self.hovered = False
        self.update()
        super().leaveEvent(event)
    
    def mousePressEvent(self, event):
        self.pressed_state = True
        self.update()
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        self.pressed_state = False
        self.update()
        super().mouseReleaseEvent(event)
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Определяем цвет
        if self.pressed_state:
            bg_color = self.color.darker(120)
        elif self.hovered:
            bg_color = self.color.lighter(120)
        else:
            bg_color = self.color
        
        # Центр и размер
        center_x = self.width() // 2
        center_y = self.height() // 2
        radius = 28
        
        # Рисуем фигуру в зависимости от типа
        painter.setPen(Qt.white)
        painter.setBrush(bg_color)
        
        if self.dice_type == 4:
            # d4 - треугольник
            polygon = QPolygon([
                QPoint(center_x, center_y - radius),
                QPoint(center_x - int(radius * 0.87), center_y + radius // 2),
                QPoint(center_x + int(radius * 0.87), center_y + radius // 2)
            ])
            painter.drawPolygon(polygon)
        
        elif self.dice_type == 6:
            # d6 - квадрат
            rect = QRect(center_x - radius, center_y - radius, radius * 2, radius * 2)
            painter.drawRect(rect)
            painter.setBrush(bg_color.darker(110))
            inner = QRect(center_x - radius//2, center_y - radius//2, radius, radius)
            painter.drawRect(inner)
        
        elif self.dice_type == 8:
            # d8 - ромб
            polygon = QPolygon([
                QPoint(center_x, center_y - radius),
                QPoint(center_x + radius, center_y),
                QPoint(center_x, center_y + radius),
                QPoint(center_x - radius, center_y)
            ])
            painter.drawPolygon(polygon)
        
        elif self.dice_type == 10:
            # d10 - пятиугольник
            points = []
            for i in range(5):
                angle = math.pi / 2 + (2 * math.pi * i / 5)
                x = center_x + int(radius * math.cos(angle))
                y = center_y - int(radius * math.sin(angle))
                points.append(QPoint(x, y))
            polygon = QPolygon(points)
            painter.drawPolygon(polygon)
        
        elif self.dice_type == 12:
            # d12 - шестиугольник
            points = []
            for i in range(6):
                angle = math.pi / 2 + (2 * math.pi * i / 6)
                x = center_x + int(radius * math.cos(angle))
                y = center_y - int(radius * math.sin(angle))
                points.append(QPoint(x, y))
            polygon = QPolygon(points)
            painter.drawPolygon(polygon)
        
        elif self.dice_type == 20:
            # d20 - круг с треугольником
            painter.drawEllipse(center_x - radius, center_y - radius, radius * 2, radius * 2)
            painter.setBrush(bg_color.lighter(130))
            tri = QPolygon([
                QPoint(center_x, center_y - radius//2),
                QPoint(center_x - radius//2, center_y + radius//3),
                QPoint(center_x + radius//2, center_y + radius//3)
            ])
            painter.drawPolygon(tri)
        
        elif self.dice_type == 100:
            # d100 - круг
            painter.drawEllipse(center_x - radius, center_y - radius, radius * 2, radius * 2)
            painter.setBrush(bg_color.darker(120))
            painter.drawEllipse(center_x - radius//2, center_y - radius//2, radius, radius)
            painter.setBrush(bg_color.lighter(130))
            painter.drawEllipse(center_x - radius//4, center_y - radius//4, radius//2, radius//2)
        
        # Текст
        painter.setPen(Qt.white)
        font = QFont("Arial", 11, QFont.Bold)
        painter.setFont(font)
        text = f"d{self.dice_type}"
        text_rect = painter.boundingRect(self.rect(), Qt.AlignCenter, text)
        painter.drawText(text_rect, Qt.AlignCenter, text)
        
        painter.end()


class DicePoolItem(QFrame):
    """Один кубик в пуле броска"""
    
    def __init__(self, dice_type, parent=None, on_remove=None):
        super().__init__(parent)
        self.dice_type = dice_type
        self.on_remove = on_remove
        self.result = None
        
        self._setup_ui()
    
    def _setup_ui(self):
        color = DICE_COLORS.get(self.dice_type, '#888888')
        
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        # Динамический стиль для рамки (цвет зависит от типа кубика)
        self.setStyleSheet(f"""
            DicePoolItem {{
                background-color: {color}33;
                border: 2px solid {color};
                border-radius: 8px;
            }}
        """)
        self.setFixedSize(60, 60)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(0)
        
        # Тип кубика
        type_label = QLabel(f"d{self.dice_type}")
        type_label.setObjectName("typeLabel")
        type_label.setAlignment(Qt.AlignCenter)
        # Динамический цвет текста
        type_label.setStyleSheet(f"font-size: 10px; color: {color}; font-weight: bold;")
        layout.addWidget(type_label)
        
        # Результат
        self.result_label = QLabel("?")
        self.result_label.setObjectName("resultLabel")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.hide()
        layout.addWidget(self.result_label)
    
    def roll(self):
        """Бросить этот кубик"""
        self.result = random.randint(1, self.dice_type)
        self.result_label.setText(str(self.result))
        self.result_label.show()
        
        # Динамический стиль для результата (цвет зависит от типа кубика)
        color = DICE_COLORS.get(self.dice_type, '#888888')
        self.result_label.setStyleSheet(f"""
            font-size: 20px;
            font-weight: bold;
            color: {color};
            background-color: #1a1a1a;
            border-radius: 4px;
            padding: 2px;
        """)
        
        return self.result
    
    def mouseDoubleClickEvent(self, event):
        if self.on_remove:
            self.on_remove(self)
        self.deleteLater()


class DiceRollOverlay(QFrame):
    """Overlay для анимации броска кубиков"""
    
    finished = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("diceRollOverlay")
        self.setFrameStyle(QFrame.NoFrame)
        
        self.dice_labels = []
        self.movies = []
        self.results = []
        
        self._setup_ui()
        self.hide()
    
    def _setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setSpacing(20)
        
        # Заголовок
        self.title = QLabel("🎲 Бросок!")
        self.title.setObjectName("overlayTitle")
        self.title.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.title)
        
        # Контейнер для анимаций
        self.dice_container = QWidget()
        self.dice_layout = QHBoxLayout(self.dice_container)
        self.dice_layout.setAlignment(Qt.AlignCenter)
        self.dice_layout.setSpacing(15)
        self.main_layout.addWidget(self.dice_container)
        
        # Результат
        self.result_label = QLabel("")
        self.result_label.setObjectName("overlayResult")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.result_label)
        
        # Подсказка
        self.click_hint = QLabel("(кликните чтобы закрыть)")
        self.click_hint.setObjectName("overlayHint")
        self.click_hint.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.click_hint)
    
    def show_roll(self, dice_types):
        """Показать анимацию броска"""
        self._clear_dice()
        
        if self.parent():
            self.setGeometry(self.parent().rect())
        
        self.result_label.setText("")
        self.results = []
        
        anim_dir = os.path.join(os.path.dirname(__file__), 'animations')
        
        for dice_type in dice_types:
            dice_widget = QWidget()
            dice_widget.setFixedSize(100, 100)
            dice_layout = QVBoxLayout(dice_widget)
            dice_layout.setContentsMargins(0, 0, 0, 0)
            
            # GIF анимация
            anim_label = QLabel()
            anim_label.setAlignment(Qt.AlignCenter)
            anim_label.setFixedSize(80, 80)
            
            gif_path = os.path.join(anim_dir, f'd{dice_type}.gif')
            if os.path.exists(gif_path):
                movie = QMovie(gif_path)
                movie.setScaledSize(QSize(80, 80))
                anim_label.setMovie(movie)
                movie.start()
                self.movies.append(movie)
            else:
                # Fallback
                color = DICE_COLORS.get(dice_type, '#888888')
                anim_label.setStyleSheet(f"""
                    background-color: {color};
                    border-radius: 40px;
                    font-size: 24px;
                    font-weight: bold;
                    color: white;
                """)
                anim_label.setText(f"d{dice_type}")
            
            # Результат
            result_label = QLabel("?")
            result_label.setAlignment(Qt.AlignCenter)
            result_label.setFixedSize(80, 80)
            result_label.hide()
            result_label.setStyleSheet(f"""
                background-color: {DICE_COLORS.get(dice_type, '#888888')};
                border-radius: 40px;
                font-size: 32px;
                font-weight: bold;
                color: white;
            """)
            
            dice_layout.addWidget(anim_label)
            dice_layout.addWidget(result_label)
            
            self.dice_labels.append({
                'widget': dice_widget,
                'anim': anim_label,
                'result': result_label,
                'type': dice_type
            })
            self.dice_layout.addWidget(dice_widget)
        
        self.show()
        self.raise_()
        
        QTimer.singleShot(1500, self._show_results)
    
    def _show_results(self):
        total = 0
        
        for dice_info in self.dice_labels:
            result = random.randint(1, dice_info['type'])
            total += result
            
            dice_info['anim'].hide()
            dice_info['result'].setText(str(result))
            dice_info['result'].show()
        
        for movie in self.movies:
            movie.stop()
        
        self.result_label.setText(f"Всего: {total}")
        self.title.setText("✓ Результат!")
    
    def _clear_dice(self):
        for movie in self.movies:
            movie.stop()
            movie.deleteLater()
        self.movies.clear()
        
        for dice_info in self.dice_labels:
            dice_info['widget'].deleteLater()
        self.dice_labels.clear()
    
    def mousePressEvent(self, event):
        if self.result_label.text():
            self.hide()
            self._clear_dice()
            self.finished.emit()


class PluginWidget(QWidget):
    """Главный виджет плагина Dice Roller"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dice_pool = []
        self.is_rolling = False
        
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        
        # Заголовок
        header = QLabel("🎲 Бросок кубиков")
        header.setObjectName("header")
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)
        
        # Кнопки кубиков
        dice_buttons_frame = QFrame()
        dice_buttons_frame.setObjectName("diceButtonsFrame")
        
        dice_grid = QGridLayout(dice_buttons_frame)
        dice_grid.setSpacing(8)
        dice_grid.setContentsMargins(8, 8, 8, 8)
        
        dice_types = [4, 6, 8, 10, 12, 20, 100]
        positions = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2)]
        
        for dice_type, (row, col) in zip(dice_types, positions):
            btn = ShapedDiceButton(dice_type)
            btn.clicked.connect(lambda checked, d=dice_type: self._add_dice(d))
            dice_grid.addWidget(btn, row, col, Qt.AlignCenter)
        
        # Кнопка очистки
        clear_pool_btn = QPushButton("🗑️")
        clear_pool_btn.setObjectName("clearPoolBtn")
        clear_pool_btn.setFixedSize(70, 70)
        clear_pool_btn.setToolTip("Очистить пул")
        clear_pool_btn.clicked.connect(self._clear_pool)
        dice_grid.addWidget(clear_pool_btn, 1, 3, Qt.AlignCenter)
        
        layout.addWidget(dice_buttons_frame)
        
        # Инфо о пуле
        self.pool_info = QLabel("Пул пуст (кликни на кубик)")
        self.pool_info.setObjectName("poolInfo")
        self.pool_info.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.pool_info)
        
        # Область пула
        pool_scroll = QScrollArea()
        pool_scroll.setObjectName("poolScroll")
        pool_scroll.setWidgetResizable(True)
        pool_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        pool_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        pool_scroll.setFixedHeight(90)
        
        self.pool_container = QWidget()
        self.pool_layout = QHBoxLayout(self.pool_container)
        self.pool_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.pool_layout.setSpacing(8)
        self.pool_layout.setContentsMargins(8, 8, 8, 8)
        
        pool_scroll.setWidget(self.pool_container)
        layout.addWidget(pool_scroll)
        
        # Подсказка
        hint = QLabel("💡 Двойной клик на кубике — удалить")
        hint.setObjectName("hint")
        hint.setAlignment(Qt.AlignCenter)
        layout.addWidget(hint)
        
        # Результат
        self.total_label = QLabel("Всего: —")
        self.total_label.setObjectName("totalLabel")
        self.total_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.total_label)
        
        # Кнопка броска
        self.roll_btn = QPushButton("🎲 БРОСИТЬ!")
        self.roll_btn.setObjectName("rollBtn")
        self.roll_btn.setMinimumHeight(50)
        self.roll_btn.setEnabled(False)
        self.roll_btn.clicked.connect(self._roll_all)
        layout.addWidget(self.roll_btn)
        
        # Overlay
        self.overlay = DiceRollOverlay(self)
        self.overlay.finished.connect(self._on_roll_finished)
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.overlay:
            self.overlay.setGeometry(self.rect())
    
    def _add_dice(self, dice_type):
        if len(self.dice_pool) >= 20:
            self.pool_info.setText("❌ Максимум 20 кубиков!")
            return
        
        dice = DicePoolItem(dice_type, on_remove=self._remove_dice)
        self.pool_layout.addWidget(dice)
        self.dice_pool.append(dice)
        
        self._update_pool_info()
        self.roll_btn.setEnabled(True)
    
    def _remove_dice(self, dice):
        if dice in self.dice_pool:
            self.dice_pool.remove(dice)
        
        self._update_pool_info()
        
        if not self.dice_pool:
            self.roll_btn.setEnabled(False)
    
    def _clear_pool(self):
        for dice in list(self.dice_pool):
            dice.deleteLater()
        
        self.dice_pool.clear()
        self._update_pool_info()
        self.roll_btn.setEnabled(False)
        self.total_label.setText("Всего: —")
    
    def _update_pool_info(self):
        if not self.dice_pool:
            self.pool_info.setText("Пул пуст (кликни на кубик)")
            self.pool_info.setProperty("hasItems", "false")
        else:
            count = len(self.dice_pool)
            type_counts = {}
            for dice in self.dice_pool:
                type_counts[dice.dice_type] = type_counts.get(dice.dice_type, 0) + 1
            
            parts = [f"{count}d{t}" if c == 1 else f"{c}d{t}" for t, c in sorted(type_counts.items())]
            self.pool_info.setText(f"В пуле: {', '.join(parts)}")
            self.pool_info.setProperty("hasItems", "true")
        
        # Обновляем стиль (для применения QSS по свойству)
        self.pool_info.style().unpolish(self.pool_info)
        self.pool_info.style().polish(self.pool_info)
    
    def _roll_all(self):
        if not self.dice_pool or self.is_rolling:
            return
        
        self.is_rolling = True
        self.roll_btn.setEnabled(False)
        
        dice_types = [dice.dice_type for dice in self.dice_pool]
        self.overlay.show_roll(dice_types)
    
    def _on_roll_finished(self):
        total = 0
        
        for dice in self.dice_pool:
            if dice.result_label.text() and dice.result_label.text() != "?":
                dice.result_label.show()
                total += int(dice.result_label.text())
        
        self.total_label.setText(f"Всего: {total}")
        
        self.is_rolling = False
        self.roll_btn.setEnabled(True)
        self.roll_btn.setText("🎲 БРОСИТЬ ЕЩЁ!")
