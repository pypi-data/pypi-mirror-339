"""Style processing for captions."""

import os
from pathlib import Path
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class FontManager:
    """Manages font availability and paths."""
    
    def __init__(self):
        """Initialize font manager."""
        self.font_dir = Path(__file__).parent.parent / "fonts"
        if not self.font_dir.exists():
            alt_paths = [
                Path(__file__).parent / "fonts",
                Path.cwd() / "fonts"
            ]
            for path in alt_paths:
                if path.exists():
                    self.font_dir = path
                    break
        self.font_map = self._load_fonts()
        
    def _load_fonts(self) -> Dict[str, str]:
        """Load available fonts and their paths."""
        fonts = {}
        for font_file in self.font_dir.glob("*.ttf"):
            stem = font_file.stem
            fonts[stem] = str(font_file)
            fonts[stem.lower()] = str(font_file)
        return fonts
        
    def get_font_path(self, font_name: str) -> Optional[str]:
        """Get path to font file.
        
        Args:
            font_name: Name of font (with or without extension)
            
        Returns:
            Path to font file or None if not found
        """
        if font_name in self.font_map:
            return self.font_map[font_name]
        if font_name.lower() in self.font_map:
            return self.font_map[font_name.lower()]
            
        base_name = Path(font_name).stem
        if base_name in self.font_map:
            return self.font_map[base_name]
            
        if not font_name.endswith('.ttf'):
            return self.get_font_path(f"{font_name}.ttf")
            
        return None
        
    def get_font_path(self, font_name: str) -> Optional[str]:
        """Get path to font file.
        
        Args:
            font_name: Display name of font
            
        Returns:
            Path to font file or None if not found
        """
        return self.font_map.get(font_name)
        
    def list_fonts(self) -> list[str]:
        """List available font display names.
        
        Returns:
            List of available font names
        """
        return list(self.font_map.keys())

class StyleManager:
    """Manages caption styling."""
    
    def __init__(self):
        """Initialize style manager."""
        self.font_manager = FontManager()
        
    def _validate_color(self, color: str, default: str = "&HFFFFFF&") -> str:
        """Validate ASS color format."""
        if not (color.startswith("&H") and color.endswith("&") and len(color) == 10):
            logger.warning(f"Invalid color format '{color}', using default")
            return default
        return color
        
 