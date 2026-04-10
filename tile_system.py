"""
Tile-based widget system for Raspberry Pi 5
Модульная система с автозагрузкой плагинов
"""

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFrame, QLabel,
    QVBoxLayout, QHBoxLayout, QMenu, QSizePolicy,
    QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, QPoint, QRect, Signal
from PySide6.QtGui import QAction, QColor
import json
import os
import sys

# Добавляем папку плагинов в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Импорт конфигурации
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT,
    GRID_COLS, GRID_ROWS, GRID_GAP, GRID_MARGIN,
    COLORS
)

# Импорт плагин-системы
from plugins import get_plugin_manager, PluginInfo


# ==================== TILE WIDGET ====================

class TileWidget(QFrame):
    """
    Контейнер для плагина с drag-and-drop.
    Содержит заголовок и область для контента плагина.
    """
    drag_started = Signal(object, QPoint)  # self, global_pos
    closed = Signal(object)  # self - сигнал при закрытии виджета
    
    def __init__(self, plugin_info: PluginInfo, parent=None):
        super().__init__(parent)
        
        self.plugin_info = plugin_info
        self.title = plugin_info.title
        self.size_cols = plugin_info.cols
        self.size_rows = plugin_info.rows
        self.widget_id = f"{plugin_info.name}_{id(self)}"
        
        self.drag_start_pos = None
        self._is_dragging = False
        
        self._setup_ui()
        self._setup_content()
    
    def _setup_ui(self):
        """Настройка UI контейнера"""
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        self.setLineWidth(2)
        
        # Главный layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(4, 4, 4, 4)
        self.main_layout.setSpacing(2)
        
        # Заголовок (draggable area)
        self.header = QFrame(self)
        self.header.setFixedHeight(28)
        self.header.setCursor(Qt.OpenHandCursor)
        self.header.setObjectName("header")
        
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(8, 2, 8, 2)
        header_layout.setSpacing(4)
        
        # Иконка + название
        title_text = f"{self.plugin_info.icon} {self.title}"
        self.title_label = QLabel(title_text)
        self.title_label.setObjectName("titleLabel")
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        
        # Кнопка закрыть
        self.close_btn = QLabel("×")
        self.close_btn.setObjectName("closeBtn")
        self.close_btn.setCursor(Qt.PointingHandCursor)
        header_layout.addWidget(self.close_btn)
        
        self.main_layout.addWidget(self.header)
        
        # Контейнер для контента плагина
        self.content_container = QWidget(self)
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        
        self.main_layout.addWidget(self.content_container, 1)
        
        # Тень
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(2, 2)
        self.setGraphicsEffect(shadow)
    
    def _setup_content(self):
        """Установить контент из плагина"""
        # Создаём экземпляр виджета плагина
        self.plugin_widget = self.plugin_info.widget_class(self.content_container)
        self.content_layout.addWidget(self.plugin_widget)
    
    def mousePressEvent(self, event):
        """Начало перетаскивания"""
        if event.button() == Qt.LeftButton:
            # Клик по кнопке закрыть (проверяем первым!)
            child = self.childAt(event.pos())
            if child == self.close_btn:
                self.close_clicked()
                event.accept()
                return
            
            # Клик по заголовку для перетаскивания
            if self.header.geometry().contains(event.pos()):
                self.drag_start_pos = event.pos()
                self._is_dragging = True
                self.setCursor(Qt.ClosedHandCursor)
                event.accept()
                return
        
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """Обработка перемещения мыши"""
        if not (event.buttons() & Qt.LeftButton):
            return
        
        if not self._is_dragging or self.drag_start_pos is None:
            super().mouseMoveEvent(event)
            return
        
        if (event.pos() - self.drag_start_pos).manhattanLength() < 10:
            return
        
        self.drag_started.emit(self, self.mapToGlobal(event.pos()))
        self._is_dragging = False
        self.setCursor(Qt.OpenHandCursor)
    
    def mouseReleaseEvent(self, event):
        """Конец перетаскивания"""
        self._is_dragging = False
        self.setCursor(Qt.ArrowCursor)
        if self.header.geometry().contains(event.pos()):
            self.setCursor(Qt.OpenHandCursor)
        super().mouseReleaseEvent(event)
    
    def enterEvent(self, event):
        if self.header.geometry().contains(self.mapFromGlobal(self.cursor().pos())):
            self.setCursor(Qt.OpenHandCursor)
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        self.setCursor(Qt.ArrowCursor)
        super().leaveEvent(event)
    
    def close_clicked(self):
        """Закрыть виджет"""
        self.closed.emit(self)
        self.hide()
        self.deleteLater()
    
    def to_dict(self):
        """Сериализация для сохранения"""
        return {
            'id': self.widget_id,
            'type': self.plugin_info.name,
            'title': self.title,
            'size_cols': self.size_cols,
            'size_rows': self.size_rows
        }


# ==================== TILE GRID ====================

class TileGrid(QWidget):
    """Сетка для размещения tile-виджетов с drag-and-drop"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.cols = GRID_COLS
        self.rows = GRID_ROWS
        self.gap = GRID_GAP
        self.margin = GRID_MARGIN
        
        self.cell_width = 0
        self.cell_height = 0
        
        # Сетка: ключ = (col, row), значение = widget
        self.grid_positions = {}
        # Список всех виджетов
        self.widgets = []
        
        # Drag & drop состояние
        self.drag_widget = None
        self.drag_start_col = None
        self.drag_start_row = None
        
        self._setup_ui()
        self._calculate_cell_size()
    
    def _setup_ui(self):
        self.setMinimumSize(400, 300)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._calculate_cell_size()
        self._reposition_widgets()
    
    def _calculate_cell_size(self):
        available_width = self.width() - 2 * self.margin - (self.cols - 1) * self.gap
        available_height = self.height() - 2 * self.margin - (self.rows - 1) * self.gap
        self.cell_width = available_width // self.cols
        self.cell_height = available_height // self.rows
    
    def _get_rect_for_position(self, col, row, cols_span, rows_span):
        """Получить QRect для позиции в сетке"""
        x = self.margin + col * (self.cell_width + self.gap)
        y = self.margin + row * (self.cell_height + self.gap)
        width = cols_span * self.cell_width + (cols_span - 1) * self.gap
        height = rows_span * self.cell_height + (rows_span - 1) * self.gap
        return QRect(x, y, width, height)
    
    def _get_position_at_point(self, point):
        """Получить (col, row) для точки на экране"""
        x = point.x() - self.margin
        y = point.y() - self.margin
        col = int(x / (self.cell_width + self.gap))
        row = int(y / (self.cell_height + self.gap))
        return col, row
    
    def _clamp_to_grid(self, col, row, cols_span, rows_span):
        """Ограничить позицию границами сетки"""
        max_col = self.cols - cols_span
        max_row = self.rows - rows_span
        return max(0, min(col, max_col)), max(0, min(row, max_row))
    
    def _is_valid_position(self, col, row, cols_span, rows_span):
        """Проверить что позиция валидна (внутри сетки)"""
        if col < 0 or row < 0:
            return False
        if col + cols_span > self.cols or row + rows_span > self.rows:
            return False
        return True
    
    def _get_occupant(self, col, row, cols_span, rows_span, exclude=None):
        """Получить виджет, занимающий эту область (кроме exclude)"""
        for c in range(col, col + cols_span):
            for r in range(row, row + rows_span):
                pos = (c, r)
                if pos in self.grid_positions:
                    w = self.grid_positions[pos]
                    if w != exclude:
                        return w
        return None
    
    def _place_widget(self, widget, col, row):
        """Разместить виджет в сетке (обновить grid_positions и геометрию)"""
        # Удаляем старые позиции этого виджета
        self._remove_from_grid(widget)
        
        # Добавляем новые позиции
        for c in range(col, col + widget.size_cols):
            for r in range(row, row + widget.size_rows):
                self.grid_positions[(c, r)] = widget
        
        # Обновляем геометрию
        rect = self._get_rect_for_position(col, row, widget.size_cols, widget.size_rows)
        widget.setParent(self)
        widget.setGeometry(rect)
        widget.show()
    
    def _remove_from_grid(self, widget):
        """Удалить виджет из grid_positions"""
        positions_to_remove = [pos for pos, w in self.grid_positions.items() if w == widget]
        for pos in positions_to_remove:
            del self.grid_positions[pos]
    
    def _get_widget_position(self, widget):
        """Получить позицию виджета в сетке"""
        for (col, row), w in self.grid_positions.items():
            if w == widget:
                return col, row
        return None, None
    
    def _reposition_widgets(self):
        """Обновить геометрию всех виджетов"""
        for widget in self.widgets:
            pos = self._get_widget_position(widget)
            if pos:
                col, row = pos
                rect = self._get_rect_for_position(col, row, widget.size_cols, widget.size_rows)
                widget.setGeometry(rect)
    
    def add_widget(self, widget, col=None, row=None):
        """Добавить виджет в сетку"""
        if widget in self.widgets:
            return False
        
        # Если позиция не указана - ищем свободное место
        if col is None or row is None:
            for r in range(self.rows - widget.size_rows + 1):
                for c in range(self.cols - widget.size_cols + 1):
                    occupant = self._get_occupant(c, r, widget.size_cols, widget.size_rows)
                    if occupant is None:
                        col, row = c, r
                        break
                if col is not None:
                    break
        
        if col is None:
            return False  # Нет места
        
        # Проверяем валидность
        col, row = self._clamp_to_grid(col, row, widget.size_cols, widget.size_rows)
        
        # Если место занято - ищем другое
        if self._get_occupant(col, row, widget.size_cols, widget.size_rows):
            for r in range(self.rows - widget.size_rows + 1):
                for c in range(self.cols - widget.size_cols + 1):
                    if self._get_occupant(c, r, widget.size_cols, widget.size_rows) is None:
                        col, row = c, r
                        break
                else:
                    continue
                break
            else:
                return False  # Нет свободного места
        
        # Размещаем
        self._place_widget(widget, col, row)
        self.widgets.append(widget)
        widget.drag_started.connect(self._on_drag_started)
        widget.closed.connect(self._on_widget_closed)
        
        return True
    
    def remove_widget(self, widget):
        """Удалить виджет из сетки"""
        if widget not in self.widgets:
            return
        self._remove_from_grid(widget)
        self.widgets.remove(widget)
        widget.hide()
        widget.setParent(None)
    
    def _on_widget_closed(self, widget):
        """Обработчик закрытия виджета"""
        self.remove_widget(widget)
    
    def _on_drag_started(self, widget, global_pos):
        """Начало перетаскивания"""
        self.drag_widget = widget
        pos = self._get_widget_position(widget)
        if pos:
            self.drag_start_col, self.drag_start_row = pos
        widget.raise_()
    
    def mouseMoveEvent(self, event):
        """Перемещение виджета за курсором"""
        if self.drag_widget:
            local_pos = event.pos()
            
            # Двигаем виджет за курсором
            new_pos = QPoint(
                local_pos.x() - self.drag_widget.width() // 2,
                local_pos.y() - self.drag_widget.height() // 2
            )
            self.drag_widget.move(new_pos)
    
    def mouseReleaseEvent(self, event):
        """Окончание перетаскивания"""
        if not self.drag_widget:
            return
        
        # Определяем целевую позицию
        local_pos = event.pos()
        col, row = self._get_position_at_point(local_pos)
        
        # Ограничиваем границами сетки
        col, row = self._clamp_to_grid(col, row, self.drag_widget.size_cols, self.drag_widget.size_rows)
        
        # Проверяем валидность
        if not self._is_valid_position(col, row, self.drag_widget.size_cols, self.drag_widget.size_rows):
            # Возвращаем на исходную позицию
            self._reposition_widgets()
            self.drag_widget = None
            return
        
        # Проверяем занятость
        occupant = self._get_occupant(col, row, self.drag_widget.size_cols, self.drag_widget.size_rows, self.drag_widget)
        
        if occupant is None:
            # Свободно - размещаем
            self._place_widget(self.drag_widget, col, row)
        else:
            # Занято - пробуем поменяться местами
            success = self._try_swap(self.drag_widget, occupant, col, row)
            if not success:
                # Не получилось - возвращаем на место
                self._reposition_widgets()
        
        self.drag_widget = None
    
    def _try_swap(self, drag_widget, target_widget, target_col, target_row):
        """Попробовать поменять виджеты местами"""
        drag_col, drag_row = self.drag_start_col, self.drag_start_row
        
        if drag_col is None or drag_row is None:
            return False
        
        # Получаем позицию target_widget
        occ_col, occ_row = self._get_widget_position(target_widget)
        if occ_col is None:
            return False
        
        # Проверяем влезет ли drag_widget на позицию target_widget
        if not self._is_valid_position(occ_col, occ_row, drag_widget.size_cols, drag_widget.size_rows):
            return False
        
        # Проверяем не занята ли позиция target_widget другими виджетами (кроме самого target_widget)
        occupant_at_target_pos = self._get_occupant(occ_col, occ_row, drag_widget.size_cols, drag_widget.size_rows, target_widget)
        if occupant_at_target_pos is not None and occupant_at_target_pos != drag_widget:
            return False
        
        # Одинаковые размеры - просто меняем местами
        if (drag_widget.size_cols == target_widget.size_cols and 
            drag_widget.size_rows == target_widget.size_rows):
            self._place_widget(drag_widget, occ_col, occ_row)
            self._place_widget(target_widget, drag_col, drag_row)
            return True
        
        # Разные размеры - ищем место для target_widget
        # Сначала пробуем позицию drag_widget
        if self._can_place_at(drag_col, drag_row, target_widget.size_cols, target_widget.size_rows, drag_widget):
            self._place_widget(target_widget, drag_col, drag_row)
            self._place_widget(drag_widget, occ_col, occ_row)
            return True
        
        # Ищем любое свободное место для target_widget
        for r in range(self.rows - target_widget.size_rows + 1):
            for c in range(self.cols - target_widget.size_cols + 1):
                if self._can_place_at(c, r, target_widget.size_cols, target_widget.size_rows, target_widget):
                    self._place_widget(target_widget, c, r)
                    self._place_widget(drag_widget, occ_col, occ_row)
                    return True
        
        return False
    
    def _can_place_at(self, col, row, cols_span, rows_span, exclude=None):
        """Проверить можно ли разместить виджет в позиции"""
        if not self._is_valid_position(col, row, cols_span, rows_span):
            return False
        return self._get_occupant(col, row, cols_span, rows_span, exclude) is None


# ==================== MAIN WINDOW ====================

class MainWindow(QMainWindow):
    """Главное окно приложения"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tile Dashboard")
        self.resize(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.setFixedSize(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Загружаем плагины
        self.plugin_manager = get_plugin_manager()
        
        # UI
        self.central = QWidget()
        self.setCentralWidget(self.central)
        
        layout = QVBoxLayout(self.central)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.tile_grid = TileGrid()
        layout.addWidget(self.tile_grid)
        
        # Меню
        self._setup_menu()
        
        # Стили
        self._load_styles()
        
        # Загрузить layout
        self._load_layout()
    
    def _setup_menu(self):
        """Настройка меню автоматически из plugins/ (с учетом ENABLED)"""
        menubar = self.menuBar()
        widgets_menu = menubar.addMenu("Виджеты")
        
        menu_items = self.plugin_manager.get_menu_items()
        
        for item in menu_items:
            item_type = item[0]
            
            if item_type == 'separator':
                widgets_menu.addSeparator()
            
            elif item_type == 'header':
                # Заголовок категории
                header = QAction(f"━━ {item[1]} ━━", self)
                header.setEnabled(False)
                widgets_menu.addAction(header)
            
            elif item_type == 'plugin':
                _, plugin_name, title = item
                action = QAction(title, self)
                action.triggered.connect(lambda checked, n=plugin_name: self._add_widget(n))
                widgets_menu.addAction(action)
            
            elif item_type == 'action':
                _, action_name, title = item
                action = QAction(title, self)
                if action_name == 'save':
                    action.triggered.connect(self._save_layout)
                elif action_name == 'clear':
                    action.triggered.connect(self._clear_all)
                widgets_menu.addAction(action)
    
    def _load_styles(self):
        """Загрузить все QSS стили"""
        styles = []
        
        # Общие стили
        if os.path.exists('styles.qss'):
            with open('styles.qss', 'r', encoding='utf-8') as f:
                styles.append(f.read())
        
        # Стили плагинов
        styles.append(self.plugin_manager.get_all_styles())
        
        self.setStyleSheet("\n".join(styles))
    
    def _add_widget(self, plugin_name: str):
        """Добавить виджет плагина"""
        plugin_info = self.plugin_manager.get_plugin(plugin_name)
        if not plugin_info:
            print(f"Плагин '{plugin_name}' не найден")
            return
        
        widget = TileWidget(plugin_info)
        
        if not self.tile_grid.add_widget(widget):
            print(f"Нет места для виджета {plugin_info.title}")
            widget.deleteLater()
    
    def _save_layout(self):
        """Сохранить layout"""
        layout_data = []
        for widget in self.tile_grid.widgets:
            for (col, row), w in self.tile_grid.grid_positions.items():
                if w == widget:
                    data = widget.to_dict()
                    data['col'] = col
                    data['row'] = row
                    layout_data.append(data)
                    break
        
        try:
            with open('layout.json', 'w', encoding='utf-8') as f:
                json.dump(layout_data, f, ensure_ascii=False, indent=2)
            print("Layout сохранён")
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
    
    def _load_layout(self):
        """Загрузить layout"""
        if not os.path.exists('layout.json'):
            return
        
        try:
            with open('layout.json', 'r', encoding='utf-8') as f:
                layout_data = json.load(f)
            
            for item in layout_data:
                plugin_type = item.get('type')
                if self.plugin_manager.get_plugin(plugin_type):
                    self._add_widget(plugin_type)
            
            print("Layout загружен")
        except Exception as e:
            print(f"Ошибка загрузки: {e}")
    
    def _clear_all(self):
        """Удалить все виджеты"""
        for widget in list(self.tile_grid.widgets):
            self.tile_grid.remove_widget(widget)
            widget.deleteLater()
    
    def closeEvent(self, event):
        self._save_layout()
        event.accept()


def main():
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
