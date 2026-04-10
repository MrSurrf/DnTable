"""
Plugin System for Tile Dashboard
Автоматическая загрузка плагинов из подпапок
"""

import os
import importlib
import importlib.util
from typing import Dict, Type, Optional
from dataclasses import dataclass


@dataclass
class PluginInfo:
    """Информация о плагине"""
    name: str                    # Уникальное имя (id)
    title: str                   # Отображаемое название
    cols: int                    # Ширина в ячейках
    rows: int                    # Высота в ячейках
    icon: str                    # Эмодзи иконка
    category: str                # Категория для меню
    widget_class: Type           # Класс виджета
    styles: Optional[str] = None # QSS стили плагина


class PluginManager:
    """Менеджер загрузки и управления плагинами"""
    
    def __init__(self, plugins_dir: str = None):
        if plugins_dir is None:
            # Определяем папку plugins относительно этого файла
            self.plugins_dir = os.path.dirname(os.path.abspath(__file__))
        else:
            self.plugins_dir = plugins_dir
        
        self.plugins: Dict[str, PluginInfo] = {}
        self._load_all_plugins()
    
    def _load_all_plugins(self):
        """Автоматически загрузить все плагины из подпапок"""
        # Получаем все подпапки в plugins/
        plugin_names = [
            name for name in os.listdir(self.plugins_dir)
            if os.path.isdir(os.path.join(self.plugins_dir, name))
            and not name.startswith('__')
            and not name.startswith('.')
        ]
        
        for plugin_name in sorted(plugin_names):
            try:
                self._load_plugin(plugin_name)
            except Exception as e:
                print(f"[PluginManager] Ошибка загрузки плагина '{plugin_name}': {e}")
    
    def _load_plugin(self, plugin_name: str):
        """Загрузить один плагин из папки"""
        plugin_path = os.path.join(self.plugins_dir, plugin_name)
        
        # Проверяем наличие необходимых файлов
        config_path = os.path.join(plugin_path, 'config.py')
        widget_path = os.path.join(plugin_path, 'widget.py')
        
        if not os.path.exists(config_path):
            print(f"[PluginManager] Пропуск {plugin_name}: нет config.py")
            return
        
        if not os.path.exists(widget_path):
            print(f"[PluginManager] Пропуск {plugin_name}: нет widget.py")
            return
        
        # Загружаем config.py
        spec = importlib.util.spec_from_file_location(
            f"plugins.{plugin_name}.config", config_path
        )
        config_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config_module)
        
        # Загружаем widget.py
        spec = importlib.util.spec_from_file_location(
            f"plugins.{plugin_name}.widget", widget_path
        )
        widget_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(widget_module)
        
        # Получаем класс виджета
        widget_class = getattr(widget_module, 'PluginWidget', None)
        if widget_class is None:
            raise ImportError(f"В {plugin_name}/widget.py не найден класс PluginWidget")
        
        # Проверяем, включен ли плагин
        enabled = getattr(config_module, 'ENABLED', True)
        if not enabled:
            print(f"[PluginManager] Плагин '{plugin_name}' отключен (ENABLED=False)")
            return
        
        # Читаем конфигурацию
        plugin_info = PluginInfo(
            name=getattr(config_module, 'PLUGIN_NAME', plugin_name),
            title=getattr(config_module, 'PLUGIN_TITLE', plugin_name.capitalize()),
            cols=getattr(config_module, 'PLUGIN_COLS', 2),
            rows=getattr(config_module, 'PLUGIN_ROWS', 2),
            icon=getattr(config_module, 'PLUGIN_ICON', '📦'),
            category=getattr(config_module, 'PLUGIN_CATEGORY', 'Общее'),
            widget_class=widget_class,
            styles=self._load_styles(plugin_path)
        )
        
        self.plugins[plugin_info.name] = plugin_info
        print(f"[PluginManager] Загружен плагин: {plugin_info.title}")
    
    def _load_styles(self, plugin_path: str) -> Optional[str]:
        """Загрузить QSS стили плагина если есть"""
        styles_path = os.path.join(plugin_path, 'styles.qss')
        if os.path.exists(styles_path):
            with open(styles_path, 'r', encoding='utf-8') as f:
                return f.read()
        return None
    
    def get_plugin(self, name: str) -> Optional[PluginInfo]:
        """Получить информацию о плагине по имени"""
        return self.plugins.get(name)
    
    def get_all_plugins(self) -> Dict[str, PluginInfo]:
        """Получить все загруженные плагины"""
        return self.plugins.copy()
    
    def get_menu_items(self) -> list:
        """Получить список пунктов меню из плагинов"""
        items = []
        
        # Группируем по категориям
        categories = {}
        for plugin in self.plugins.values():
            cat = plugin.category
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(plugin)
        
        # Формируем меню
        for category in sorted(categories.keys()):
            plugins_in_cat = sorted(categories[category], key=lambda p: p.title)
            
            # Добавляем заголовок категории (если нужно)
            if len(categories) > 1:
                items.append(('header', category))
            
            for plugin in plugins_in_cat:
                items.append(('plugin', plugin.name, plugin.title))
            
            items.append(('separator',))
        
        # Добавляем системные пункты
        items.append(('action', 'save', 'Сохранить layout'))
        items.append(('action', 'clear', 'Очистить все'))
        
        return items
    
    def get_all_styles(self) -> str:
        """Получить все QSS стили от плагинов"""
        styles = []
        for plugin in self.plugins.values():
            if plugin.styles:
                styles.append(f"/* Styles for {plugin.name} */")
                styles.append(plugin.styles)
                styles.append("")
        return "\n".join(styles)


# Глобальный экземпляр менеджера
_plugin_manager = None

def get_plugin_manager() -> PluginManager:
    """Получить глобальный экземпляр PluginManager"""
    global _plugin_manager
    if _plugin_manager is None:
        _plugin_manager = PluginManager()
    return _plugin_manager
