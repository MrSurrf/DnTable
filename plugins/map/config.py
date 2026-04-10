"""
Конфигурация плагина "Карта"
"""

# Включить/выключить плагин
ENABLED = True

# Уникальное имя плагина (используется как id)
PLUGIN_NAME = 'map'

# Отображаемое название в меню
PLUGIN_TITLE = 'Карта'

# Размер виджета в ячейках сетки
PLUGIN_COLS = 3   # ширина
PLUGIN_ROWS = 3   # высота

# Иконка для виджета
PLUGIN_ICON = '🗺️'

# Категория в меню
PLUGIN_CATEGORY = 'Игра'

# Дополнительные настройки плагина
MAP_SETTINGS = {
    'default_image': None,           # Путь к дефолтному изображению
    'supported_formats': ['.png', '.jpg', '.jpeg', '.bmp'],
    'zoom_enabled': True,
    'pan_enabled': True,
}

# Цвета специфичные для этого плагина (опционально)
PLUGIN_COLORS = {
    'border': '#444444',
    'active': '#6496FF',
}
