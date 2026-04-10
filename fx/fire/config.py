"""Эффект Огонь"""

EFFECT_NAME = 'fire'
EFFECT_TITLE = '🔥 Огонь'
EFFECT_ICON = '🔥'
EFFECT_COLOR = '#FF4444'

# Настройки анимации (будут использоваться при реализации)
ANIMATION_SETTINGS = {
    'frames_count': 12,        # Количество кадров
    'frame_rate': 15,          # FPS
    'loop': True,              # Зацикливать
    'duration': 2000,          # Длительность в мс (если не зациклено)
}

# Пути к файлам (относительно папки effects/fire/)
ASSETS = {
    'preview': 'preview.png',           # Статичное превью
    'animation': 'animation.gif',       # Анимация (или mp4/webm)
    'frames': 'frames/',                # Папка с кадрами
    'icon': 'icon.png',                 # Иконка эффекта
}

# Описание для подсказки
DESCRIPTION = 'Эффект огня с пламенем и искрами'
