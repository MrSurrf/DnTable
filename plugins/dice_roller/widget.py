"""
Виджет плагина Dice Roller с фигурными кнопками и анимацией броска

- Кнопки имеют форму соответствующую типу кубика
- При броске показывается overlay с анимацией
"""

from PySide6.QtWidgets import (
    QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, 
    QScrollArea, QFrame, QSizePolicy, QGridLayout, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QTimer, QSize, QPoint, QRect, Signal
from PySide6.QtGui import QColor, QPainter, QPolygon, QFont, QMovie, QCursor
import random
import os
import math


# Цвета для кубиков разного типа
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
    """Кнопка кубика с фигурной формой"""
    
    def __init__(self, dice_type, parent=None):
        super().__init__(parent)
        self.dice_type = dice_type
        self.color = QColor(DICE_COLORS.get(dice_type, '#888888'))
        self.hovered = False
        self.pressed_state = False
        
        self.setFixedSize(70, 70)
        self.setCursor(Qt.PointingHandCursor)
        
        # Убираем стандартный стиль
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
            # d4 - треугольник (тетраэдр)
            polygon = QPolygon([
                QPoint(center_x, center_y - radius),
                QPoint(center_x - int(radius * 0.87), center_y + radius // 2),
                QPoint(center_x + int(radius * 0.87), center_y + radius // 2)
            ])
            painter.drawPolygon(polygon)
        
        elif self.dice_type == 6:
            # d6 - квадрат (куб)
            rect = QRect(center_x - radius, center_y - radius, radius * 2, radius * 2)
            painter.drawRect(rect)
            # Внутренний квадрат для объёма
            painter.setBrush(bg_color.darker(110))
            inner = QRect(center_x - radius//2, center_y - radius//2, radius, radius)
            painter.drawRect(inner)
        
        elif self.dice_type == 8:
            # d8 - ромб (октаэдр)
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
            # d20 - круг с треугольником внутри
            painter.drawEllipse(center_x - radius, center_y - radius, radius * 2, radius * 2)
            # Треугольник внутри
            painter.setBrush(bg_color.lighter(130))
            tri = QPolygon([
                QPoint(center_x, center_y - radius//2),
                QPoint(center_x - radius//2, center_y + radius//3),
                QPoint(center_x + radius//2, center_y + radius//3)
            ])
            painter.drawPolygon(tri)
        
        elif self.dice_type == 100:
            # d100 - круг (процентильный)
            painter.drawEllipse(center_x - radius, center_y - radius, radius * 2, radius * 2)
            # Внутренний круг
            painter.setBrush(bg_color.darker(120))
            painter.drawEllipse(center_x - radius//2, center_y - radius//2, radius, radius)
            # Самый маленький круг
            painter.setBrush(bg_color.lighter(130))
            painter.drawEllipse(center_x - radius//4, center_y - radius//4, radius//2, radius//2)
        
        # Рисуем текст (dX)
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
        type_label.setAlignment(Qt.AlignCenter)
        type_label.setStyleSheet(f"font-size: 10px; color: {color}; font-weight: bold;")
        layout.addWidget(type_label)
        
        # Результат (скрыт до броска)
        self.result_label = QLabel("?")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #eee;
            background-color: #1a1a1a;
            border-radius: 4px;
        """)
        self.result_label.hide()
        layout.addWidget(self.result_label)
    
    def roll(self):
        """Бросить этот кубик"""
        self.result = random.randint(1, self.dice_type)
        self.result_label.setText(str(self.result))
        self.result_label.show()
        
        # Подсветка результата
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
        """Двойной клик удаляет кубик из пула"""
        if self.on_remove:
            self.on_remove(self)
        self.deleteLater()


class DiceRollOverlay(QFrame):
    """Overlay для анимации броска кубиков"""
    
    finished = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 180);")
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
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #64FF64;
            background: transparent;
        """)
        self.main_layout.addWidget(self.title)
        
        # Контейнер для анимаций кубиков
        self.dice_container = QWidget()
        self.dice_layout = QHBoxLayout(self.dice_container)
        self.dice_layout.setAlignment(Qt.AlignCenter)
        self.dice_layout.setSpacing(15)
        self.main_layout.addWidget(self.dice_container)
        
        # Результат
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("""
            font-size: 36px;
            font-weight: bold;
            color: #FFFF64;
            background: transparent;
        """)
        self.main_layout.addWidget(self.result_label)
        
        # Клик для закрытия
        self.click_hint = QLabel("(кликните чтобы закрыть)")
        self.click_hint.setAlignment(Qt.AlignCenter)
        self.click_hint.setStyleSheet("color: #888; font-size: 10px; background: transparent;")
        self.main_layout.addWidget(self.click_hint)
    
    def show_roll(self, dice_types):
        """Показать анимацию броска для списка кубиков"""
        # Очищаем предыдущее
        self._clear_dice()
        
        # Получаем размер родителя
        if self.parent():
            self.setGeometry(self.parent().rect())
        
        self.result_label.setText("")
        self.results = []
        
        # Создаём виджеты для каждого кубика
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
                # Fallback - цветной круг
                color = DICE_COLORS.get(dice_type, '#888888')
                anim_label.setStyleSheet(f"""
                    background-color: {color};
                    border-radius: 40px;
                    font-size: 24px;
                    font-weight: bold;
                    color: white;
                """)
                anim_label.setText(f"d{dice_type}")
            
            # Результат кубика (скрыт сначала)
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
        
        # Через 1.5 секунды показываем результаты
        QTimer.singleShot(1500, self._show_results)
    
    def _show_results(self):
        """Показать результаты броска"""
        total = 0
        
        for dice_info in self.dice_labels:
            # Бросаем кубик
            result = random.randint(1, dice_info['type'])
            total += result
            
            # Прячем анимацию, показываем результат
            dice_info['anim'].hide()
            dice_info['result'].setText(str(result))
            dice_info['result'].show()
        
        # Останавливаем GIF
        for movie in self.movies:
            movie.stop()
        
        self.result_label.setText(f"Всего: {total}")
        self.title.setText("✓ Результат!")
    
    def _clear_dice(self):
        """Очистить кубики"""
        for movie in self.movies:
            movie.stop()
            movie.deleteLater()
        self.movies.clear()
        
        for dice_info in self.dice_labels:
            dice_info['widget'].deleteLater()
        self.dice_labels.clear()
    
    def mousePressEvent(self, event):
        """Закрыть по клику"""
        if self.result_label.text():  # Только если результаты показаны
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
        """Настройка интерфейса"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)
        
        # === ЗАГОЛОВОК ===
        header = QLabel("🎲 Бросок кубиков")
        header.setAlignment(Qt.AlignCenter)
        header.setStyleSheet("font-weight: bold; color: #eee; font-size: 14px;")
        layout.addWidget(header)
        
        # === КНОПКИ ДОБАВЛЕНИЯ КУБИКОВ (фигурные) ===
        dice_buttons_frame = QFrame()
        dice_buttons_frame.setStyleSheet("""
            QFrame {
                background-color: #252525;
                border-radius: 8px;
                padding: 4px;
            }
        """)
        
        dice_grid = QGridLayout(dice_buttons_frame)
        dice_grid.setSpacing(8)
        dice_grid.setContentsMargins(8, 8, 8, 8)
        
        # Создаём фигурные кнопки для каждого типа кубика
        dice_types = [4, 6, 8, 10, 12, 20, 100]
        positions = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2)]
        
        for dice_type, (row, col) in zip(dice_types, positions):
            btn = ShapedDiceButton(dice_type)
            btn.clicked.connect(lambda checked, d=dice_type: self._add_dice(d))
            dice_grid.addWidget(btn, row, col, Qt.AlignCenter)
        
        # Кнопка очистки пула
        clear_pool_btn = QPushButton("🗑️")
        clear_pool_btn.setFixedSize(70, 70)
        clear_pool_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF646433;
                color: #FF6464;
                border: 2px solid #FF6464;
                border-radius: 35px;
                font-size: 24px;
            }
            QPushButton:hover {
                background-color: #FF646466;
            }
        """)
        clear_pool_btn.setToolTip("Очистить пул")
        clear_pool_btn.clicked.connect(self._clear_pool)
        dice_grid.addWidget(clear_pool_btn, 1, 3, Qt.AlignCenter)
        
        layout.addWidget(dice_buttons_frame)
        
        # === ИНФОРМАЦИЯ О ПУЛЕ ===
        self.pool_info = QLabel("Пул пуст (кликни на кубик)")
        self.pool_info.setAlignment(Qt.AlignCenter)
        self.pool_info.setStyleSheet("color: #888; font-size: 11px;")
        layout.addWidget(self.pool_info)
        
        # === ОБЛАСТЬ ПУЛА КУБИКОВ ===
        pool_scroll = QScrollArea()
        pool_scroll.setWidgetResizable(True)
        pool_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        pool_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        pool_scroll.setFixedHeight(90)
        pool_scroll.setStyleSheet("""
            QScrollArea {
                background-color: #1a1a1a;
                border: 2px dashed #444;
                border-radius: 8px;
            }
            QScrollBar:horizontal {
                background-color: #2d2d2d;
                height: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:horizontal {
                background-color: #555;
                border-radius: 4px;
            }
        """)
        
        self.pool_container = QWidget()
        self.pool_layout = QHBoxLayout(self.pool_container)
        self.pool_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.pool_layout.setSpacing(8)
        self.pool_layout.setContentsMargins(8, 8, 8, 8)
        
        pool_scroll.setWidget(self.pool_container)
        layout.addWidget(pool_scroll)
        
        # Подсказка
        hint = QLabel("💡 Двойной клик на кубике — удалить")
        hint.setAlignment(Qt.AlignCenter)
        hint.setStyleSheet("color: #666; font-size: 9px;")
        layout.addWidget(hint)
        
        # === РЕЗУЛЬТАТ ===
        self.total_label = QLabel("Всего: —")
        self.total_label.setAlignment(Qt.AlignCenter)
        self.total_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #64FF64;
            background-color: #1a2f1a;
            border-radius: 8px;
            padding: 8px;
        """)
        layout.addWidget(self.total_label)
        
        # === КНОПКА БРОСИТЬ ===
        self.roll_btn = QPushButton("🎲 БРОСИТЬ!")
        self.roll_btn.setMinimumHeight(50)
        self.roll_btn.setEnabled(False)
        self.roll_btn.setStyleSheet("""
            QPushButton {
                background-color: #3d3d3d;
                color: #666;
                border: none;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:enabled {
                background-color: #6496FF;
                color: white;
            }
            QPushButton:enabled:hover {
                background-color: #7aa6ff;
            }
        """)
        self.roll_btn.clicked.connect(self._roll_all)
        layout.addWidget(self.roll_btn)
        
        # === OVERLAY ===
        self.overlay = DiceRollOverlay(self)
        self.overlay.finished.connect(self._on_roll_finished)
    
    def resizeEvent(self, event):
        """Обновляем размер overlay при изменении размера"""
        super().resizeEvent(event)
        if self.overlay:
            self.overlay.setGeometry(self.rect())
    
    def _add_dice(self, dice_type):
        """Добавить кубик в пул"""
        if len(self.dice_pool) >= 20:
            self.pool_info.setText("❌ Максимум 20 кубиков!")
            return
        
        dice = DicePoolItem(dice_type, on_remove=self._remove_dice)
        self.pool_layout.addWidget(dice)
        self.dice_pool.append(dice)
        
        self._update_pool_info()
        self.roll_btn.setEnabled(True)
    
    def _remove_dice(self, dice):
        """Удалить кубик из пула"""
        if dice in self.dice_pool:
            self.dice_pool.remove(dice)
        
        self._update_pool_info()
        
        if not self.dice_pool:
            self.roll_btn.setEnabled(False)
    
    def _clear_pool(self):
        """Очистить весь пул"""
        for dice in list(self.dice_pool):
            dice.deleteLater()
        
        self.dice_pool.clear()
        self._update_pool_info()
        self.roll_btn.setEnabled(False)
        self.total_label.setText("Всего: —")
    
    def _update_pool_info(self):
        """Обновить информацию о пуле"""
        if not self.dice_pool:
            self.pool_info.setText("Пул пуст (кликни на кубик)")
            self.pool_info.setStyleSheet("color: #888; font-size: 11px;")
        else:
            count = len(self.dice_pool)
            type_counts = {}
            for dice in self.dice_pool:
                type_counts[dice.dice_type] = type_counts.get(dice.dice_type, 0) + 1
            
            parts = [f"{count}d{t}" if c == 1 else f"{c}d{t}" for t, c in sorted(type_counts.items())]
            self.pool_info.setText(f"В пуле: {', '.join(parts)}")
            self.pool_info.setStyleSheet("color: #6496FF; font-size: 11px; font-weight: bold;")
    
    def _roll_all(self):
        """Бросить все кубики с анимацией overlay"""
        if not self.dice_pool or self.is_rolling:
            return
        
        self.is_rolling = True
        self.roll_btn.setEnabled(False)
        
        # Собираем типы кубиков для анимации
        dice_types = [dice.dice_type for dice in self.dice_pool]
        
        # Показываем overlay с анимацией
        self.overlay.show_roll(dice_types)
    
    def _on_roll_finished(self):
        """Анимация закончена"""
        # Обновляем результаты в пуле
        total = 0
        
        for dice in self.dice_pool:
            if dice.result_label.text() and dice.result_label.text() != "?":
                dice.result_label.show()
                total += int(dice.result_label.text())
        
        self.total_label.setText(f"Всего: {total}")
        
        self.is_rolling = False
        self.roll_btn.setEnabled(True)
        self.roll_btn.setText("🎲 БРОСИТЬ ЕЩЁ!")
