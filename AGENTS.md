# DnTable - AI Agent Guide

## Project Overview

DnTable is a **tile-based dashboard application** for tabletop role-playing games (Dungeons & Dragons), designed primarily for **Raspberry Pi 5** with a vertical touchscreen display. The application provides a modular, customizable interface with draggable widgets for managing game sessions.

### Key Features
- **Grid-based Layout**: 4×6 tile grid optimized for 720×1280 vertical screen
- **Drag-and-Drop**: Widgets can be rearranged by dragging their headers
- **Plugin System**: Automatic discovery and loading of plugins from `plugins/` directory
- **Effects System**: Visual effects (fire, ice, lightning, etc.) managed through `fx/` directory
- **Layout Persistence**: Widget positions are saved to `layout.json` and restored on startup
- **Dark Theme**: Optimized for tabletop gaming environment

## Technology Stack

- **Language**: Python 3.10+
- **GUI Framework**: PySide6 6.11.0 (Qt6 bindings)
- **UI Design**: Programmatic widget construction (legacy Qt Designer files present but not primary)
- **Target Platform**: Raspberry Pi 5 (Linux), cross-platform compatible

## Project Structure

```
c:\ProjectM\DnTable
├── tile_system.py          # Main application entry point (RUN THIS)
├── config.py               # Global configuration (screen size, grid, colors, fonts)
├── styles.qss              # Global QSS stylesheet
├── layout.json             # Saved widget positions (auto-generated)
├── README.md               # Project description (minimal)
├── .gitignore              # Ignores venv/, __pycache__/
├── 
├── plugins/                # Plugin system directory
│   ├── __init__.py         # PluginManager implementation
│   ├── map/                # Map display plugin
│   ├── dice/               # Simple dice roller (DISABLED)
│   ├── dice_roller/        # Advanced dice roller with pool system
│   ├── effects/            # Visual effects manager
│   ├── timer/              # Count-up timer
│   ├── notes/              # Text notes widget
│   └── music/              # Music player controls (placeholder)
│
├── fx/                     # Visual effects definitions
│   ├── __init__.py         # EffectsManager implementation
│   ├── fire/               # Fire effect configuration
│   ├── ice/                # Ice effect configuration
│   ├── lightning/          # Lightning effect configuration
│   ├── fog/                # Fog effect configuration
│   ├── light/              # Light effect configuration
│   └── darkness/           # Darkness effect configuration
│
├── venv/                   # Python virtual environment (Python 3.10)
└── __pycache__/            # Python bytecode cache

# Legacy files (not currently used):
├── main_UI.py              # Old dock-based implementation
├── design.py               # Auto-generated from design.ui
└── design.ui               # Qt Designer file (legacy)
```

## Entry Points

### Main Application
```bash
# Activate virtual environment
venv\Scripts\activate

# Run the tile-based dashboard (primary entry point)
python tile_system.py
```

### Legacy Application (Dock-based)
```bash
# Old implementation with dock widgets - not recommended
python main_UI.py
```

## Plugin System Architecture

### Philosophy
**Каждый плагин — это отдельный модуль.** Все настройки плагина содержатся ТОЛЬКО в его собственной папке. Сторонний разработчик может создать плагин, не изменяя ни одного системного файла.

### Plugin Structure
Each plugin is a subdirectory in `plugins/` with exactly two required files:

```
plugins/{plugin_name}/
├── config.py       # ВСЕ настройки плагина (обязательно)
├── widget.py       # Класс PluginWidget (обязательно)
└── styles.qss      # Стили плагина (опционально)
```

**plugins/{plugin_name}/config.py** — ЕДИНСТВЕННЫЙ файл, который нужно редактировать:
```python
# =============================================================================
# ОБЯЗАТЕЛЬНЫЕ ПАРАМЕТРЫ (система не загрузит плагин без них)
# =============================================================================

ENABLED = True                    # Включить/выключить плагин
PLUGIN_NAME = 'my_plugin'         # Уникальное имя (латиница, цифры, _)
PLUGIN_TITLE = 'Мой плагин'       # Название в меню
PLUGIN_COLS = 2                   # Ширина в ячейках сетки (1-6)
PLUGIN_ROWS = 2                   # Высота в ячейках сетки (1-4)
PLUGIN_ICON = '📦'                # Иконка (эмодзи)
PLUGIN_CATEGORY = 'Инструменты'   # Категория в меню

# =============================================================================
# ОПЦИОНАЛЬНЫЕ ПАРАМЕТРЫ (специфичные для вашего плагина)
# =============================================================================

MY_SETTING = 'value'              # Любые ваши настройки
MAX_ITEMS = 10                    # Используйте в widget.py через импорт

PLUGIN_COLORS = {                 # Цвета специфичные для плагина
    'primary': '#6496FF',
}
```

**ВАЖНО:** НЕ редактируйте глобальный `config.py`! Все настройки вашего плагина — только в `plugins/{plugin_name}/config.py`.

# Категория в меню
PLUGIN_CATEGORY = 'Игра'  # или 'Инструменты'
```

**plugins/{plugin_name}/widget.py**:
```python
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt

class PluginWidget(QWidget):
    """
    Главный виджет плагина - ОБЯЗАТЕЛЬНОЕ ИМЯ КЛАССА!
    Система ищет именно класс с названием PluginWidget.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        # Размер виджета определяется в config.py через PLUGIN_COLS и PLUGIN_ROWS
        layout = QVBoxLayout(self)
        
        label = QLabel('Привет из моего плагина!')
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
```

### Creating a New Plugin (Step-by-Step)

Самый быстрый способ — скопировать пример:

```bash
# 1. Скопируйте папку-пример
cp -r plugins/example_plugin/ plugins/my_awesome_plugin/

# 2. Измените настройки в config.py
# 3. Реализуйте логику в widget.py
# 4. Готово! Перезапустите приложение.
```

**Или создайте вручную:**

1. Create folder `plugins/{your_plugin}/`
2. Create `config.py` with required constants (see example above)
3. Create `widget.py` with `PluginWidget` class
4. (Optional) Create `styles.qss` for custom styling
5. Restart application - plugin loads automatically

### Plugin Template

Смотрите полный рабочий пример в `plugins/example_plugin/`:
- `config.py` — документированный шаблон конфигурации
- `widget.py` — пример структуры виджета с комментариями
- `styles.qss` — пример стилей

### Disabling a Plugin

Set `ENABLED = False` in the plugin's `config.py`.

## Effects System Architecture

### Effect Structure
Effects are defined in `fx/` directory with a similar pattern:

**fx/{effect_name}/config.py**:
```python
EFFECT_NAME = 'fire'
EFFECT_TITLE = '🔥 Огонь'
EFFECT_ICON = '🔥'
EFFECT_COLOR = '#FF4444'
DESCRIPTION = 'Эффект огня с пламенем и искрами'

ANIMATION_SETTINGS = {
    'frames_count': 12,
    'frame_rate': 15,
    'loop': True,
    'duration': 2000,
}

ASSETS = {
    'preview': 'preview.png',
    'animation': 'animation.gif',
    'frames': 'frames/',
}
```

## Configuration Reference

### Global Config (config.py)

**Screen Settings**:
```python
SCREEN_WIDTH = 720    # Window width (fixed)
SCREEN_HEIGHT = 1280  # Window height (fixed)
```

**Grid Settings**:
```python
GRID_COLS = 4         # Columns (horizontal cells)
GRID_ROWS = 6         # Rows (vertical cells)
GRID_GAP = 8          # Gap between widgets (pixels)
GRID_MARGIN = 8       # Screen edge margin (pixels)
```

**Colors** (QSS-compatible format):
```python
COLORS = {
    'background':        '#1a1a1a',  # Window background
    'surface':           '#2d2d2d',  # Widget background
    'surface_light':     '#3d3d3d',  # Header background
    'text_primary':      '#eeeeee',  # Main text
    'text_secondary':    '#aaaaaa',  # Secondary text
    'accent_blue':       '#6496FF',  # Blue accent
    'accent_green':      '#64FF64',  # Green accent
    'accent_red':        '#FF6464',  # Red accent
    'drag_valid':        '#64FF64',  # Valid drop position
    'drag_invalid':      '#FF6464',  # Invalid drop position
}
```

## Available Plugins

| Plugin | Status | Size | Description |
|--------|--------|------|-------------|
| map | ✅ Enabled | 3×3 | Map display with image loading |
| dice | ❌ Disabled | 2×2 | Simple dice roller (replaced by dice_roller) |
| dice_roller | ✅ Enabled | 3×3 | Advanced dice pool roller with animation |
| effects | ✅ Enabled | 2×2 | Visual effects manager with preview |
| timer | ✅ Enabled | 2×1 | Count-up timer (HH:MM:SS) |
| notes | ✅ Enabled | 2×2 | Text notes with character counter |
| music | ✅ Enabled | 2×1 | Music player controls (placeholder) |

## Build Process

### No Build Required
This is a pure Python application with no build step. Simply run `tile_system.py`.

### Virtual Environment Setup
```bash
# Create venv (if needed)
python -m venv venv

# Activate
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install PySide6
```

### Qt Designer (Legacy)
If modifying `design.ui` (legacy file):
```bash
pyside6-uic design.ui -o design.py
```

## Development Conventions

### Code Style
- **Language**: Russian for UI text, comments, and documentation
- **Class Names**: `PascalCase` (e.g., `PluginWidget`, `TileGrid`)
- **Function/Variable Names**: `snake_case` (e.g., `_setup_ui`, `plugin_manager`)
- **Constants**: `UPPER_CASE` (e.g., `PLUGIN_NAME`, `SCREEN_WIDTH`)

### File Organization
- Each plugin is self-contained in its own directory
- Plugin configuration in `config.py`
- Plugin implementation in `widget.py`
- Optional plugin-specific styles in `styles.qss`

### UI Guidelines
- Use emoji icons for visual recognition
- Dark theme with `#1a1a1a` background
- Accent colors: blue (`#6496FF`) for primary actions
- Green (`#64FF64`) for success/running states
- Red (`#FF6464`) for danger/stop actions

### Widget Sizing
Widget sizes are defined in grid cells:
- Small widgets: 2×1 (timer, music)
- Medium widgets: 2×2 (effects, notes, dice)
- Large widgets: 3×3 (map, dice_roller)

## Layout System

### Grid-Based Positioning
The screen is divided into a 4×6 grid. Each widget occupies one or more cells.

### Layout Persistence
- Layout is saved to `layout.json` on application exit
- Layout is loaded on application startup
- Manual save: Menu → Виджеты → Сохранить layout
- Clear all: Menu → Виджеты → Очистить все

### Drag and Drop
1. Grab widget by its header (cursor changes to open hand)
2. Drag to new position
3. Release - widget snaps to grid
4. Other widgets auto-rearrange to make space

## Testing

No automated test suite is currently configured. Testing is manual:

1. Run `python tile_system.py`
2. Add widgets via menu (Виджеты)
3. Drag to rearrange
4. Verify layout saves on exit
5. Verify layout restores on restart

## Dependencies

Main dependencies (installed in venv):
- `PySide6` (6.11.0) - Qt6 Python bindings
- `shiboken6` (6.11.0) - Python binding generator

No `requirements.txt` or `pyproject.toml` exists.

## Deployment

### Target Platform
- **Primary**: Raspberry Pi 5 with 720×1280 touchscreen
- **OS**: Raspberry Pi OS (Linux)
- **Screen**: Vertical orientation

### Running on Raspberry Pi
```bash
# Enable venv
source venv/bin/activate

# Run
python tile_system.py
```

### Cross-Platform
The application runs on any platform supporting PySide6:
- Windows
- macOS
- Linux (including Raspberry Pi)

## Notes for AI Agents

1. **Main Entry Point**: Use `tile_system.py`, not `main_UI.py`
2. **Plugin Development**: Follow the `config.py` + `widget.py` pattern
3. **Language**: Keep UI text and comments in Russian
4. **Colors**: Use constants from `config.COLORS` rather than hardcoding
5. **Grid Sizes**: Respect `GRID_COLS=4` and `GRID_ROWS=6` limits
6. **Legacy Files**: `design.ui` and `design.py` are not actively used
7. **Effects**: New effects go in `fx/{name}/config.py` following existing patterns
8. **Auto-loading**: Both plugins and effects are discovered automatically at startup
