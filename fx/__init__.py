"""
Система управления эффектами
"""

import os
import importlib.util
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class EffectInfo:
    """Информация об эффекте"""
    name: str
    title: str
    icon: str
    color: str
    description: str
    folder_path: str
    animation_settings: dict
    assets: dict


class EffectsManager:
    """Менеджер загрузки эффектов из папки fx/"""
    
    def __init__(self, effects_dir: str = None):
        if effects_dir is None:
            # Папка fx относительно корня проекта
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.effects_dir = os.path.join(base_dir, 'fx')
        else:
            self.effects_dir = effects_dir
        
        self.effects: Dict[str, EffectInfo] = {}
        self._load_all_effects()
    
    def _load_all_effects(self):
        """Загрузить все эффекты из папок"""
        if not os.path.exists(self.effects_dir):
            print(f"[EffectsManager] Папка fx не найдена: {self.effects_dir}")
            return
        
        effect_names = [
            name for name in os.listdir(self.effects_dir)
            if os.path.isdir(os.path.join(self.effects_dir, name))
            and not name.startswith('__')
            and not name.startswith('.')
        ]
        
        for effect_name in sorted(effect_names):
            try:
                self._load_effect(effect_name)
            except Exception as e:
                print(f"[EffectsManager] Ошибка загрузки эффекта '{effect_name}': {e}")
    
    def _load_effect(self, effect_name: str):
        """Загрузить один эффект"""
        effect_path = os.path.join(self.effects_dir, effect_name)
        config_path = os.path.join(effect_path, 'config.py')
        
        if not os.path.exists(config_path):
            return
        
        # Загружаем config.py
        spec = importlib.util.spec_from_file_location(
            f"effects.{effect_name}.config", config_path
        )
        config_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(config_module)
        
        effect_info = EffectInfo(
            name=getattr(config_module, 'EFFECT_NAME', effect_name),
            title=getattr(config_module, 'EFFECT_TITLE', effect_name.capitalize()),
            icon=getattr(config_module, 'EFFECT_ICON', '✨'),
            color=getattr(config_module, 'EFFECT_COLOR', '#888888'),
            description=getattr(config_module, 'DESCRIPTION', ''),
            folder_path=effect_path,
            animation_settings=getattr(config_module, 'ANIMATION_SETTINGS', {}),
            assets=getattr(config_module, 'ASSETS', {})
        )
        
        self.effects[effect_info.name] = effect_info
        print(f"[EffectsManager] Загружен эффект: {effect_info.title}")
    
    def get_effect(self, name: str) -> Optional[EffectInfo]:
        """Получить эффект по имени"""
        return self.effects.get(name)
    
    def get_all_effects(self) -> List[EffectInfo]:
        """Получить список всех эффектов"""
        return list(self.effects.values())
    
    def get_preview_path(self, effect_name: str) -> Optional[str]:
        """Получить путь к превью эффекта"""
        effect = self.get_effect(effect_name)
        if not effect:
            return None
        
        preview_file = effect.assets.get('preview', 'preview.png')
        preview_path = os.path.join(effect.folder_path, preview_file)
        
        if os.path.exists(preview_path):
            return preview_path
        return None
    
    def get_animation_path(self, effect_name: str) -> Optional[str]:
        """Получить путь к анимации эффекта"""
        effect = self.get_effect(effect_name)
        if not effect:
            return None
        
        anim_file = effect.assets.get('animation', 'animation.gif')
        anim_path = os.path.join(effect.folder_path, anim_file)
        
        if os.path.exists(anim_path):
            return anim_path
        return None


# Глобальный экземпляр
_effects_manager = None

def get_effects_manager() -> EffectsManager:
    """Получить глобальный экземпляр EffectsManager"""
    global _effects_manager
    if _effects_manager is None:
        _effects_manager = EffectsManager()
    return _effects_manager
